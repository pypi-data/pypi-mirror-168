"""
Block Neural Autoregressive bijection implementation.
"""

from typing import Callable
import equinox as eqx
import jax
import jax.numpy as jnp
from flowjax.bijections.abc import Bijection
from jax import random
from jax.random import KeyArray
from jax.nn.initializers import glorot_uniform
import jax.numpy as jnp
from flowjax.utils import Array


def b_diag_mask(block_shape: tuple, n_blocks: int):
    "Block diagonal mask."
    return jax.scipy.linalg.block_diag(
        *[jnp.ones(block_shape, jnp.int32) for _ in range(n_blocks)]
    )


def b_tril_mask(block_shape: tuple, n_blocks: int):
    "Upper triangular block mask, excluding diagonal blocks."
    mask = jnp.zeros((block_shape[0] * n_blocks, block_shape[1] * n_blocks), jnp.int32)

    for i in range(n_blocks):
        mask = mask.at[
            (i + 1) * block_shape[0] :, i * block_shape[1] : (i + 1) * block_shape[1]
        ].set(1)
    return mask


class BlockAutoregressiveLinear(eqx.Module):
    n_blocks: int
    block_shape: tuple
    cond_dim: int
    W: Array
    bias: Array
    W_log_scale: Array
    in_features: int
    out_features: int
    b_diag_mask: Array
    b_diag_mask_idxs: Array
    b_tril_mask: Array

    def __init__(
        self,
        key: KeyArray,
        n_blocks: int,
        block_shape: tuple,
        cond_dim: int = 0,
        init: Callable = glorot_uniform(),
    ):
        """Block autoregressive neural network layer (https://arxiv.org/abs/1904.04676).
        Conditioning variables are incorporated by appending columns (one for each
        conditioning variable) to the left of the block diagonal weight matrix.

        Args:
            key KeyArray: Random key
            n_blocks (int): Number of diagonal blocks (dimension of original input).
            block_shape (tuple): The shape of the (unconstrained) blocks.
            cond_dim (int): Number of additional conditioning variables. Defaults to 0.
            init (Callable, optional): Default initialisation method for the weight matrix. Defaults to glorot_uniform().
        """
        cond_size = (block_shape[0] * n_blocks, cond_dim)

        self.b_diag_mask = jnp.column_stack(
            (jnp.zeros(cond_size, jnp.int32), b_diag_mask(block_shape, n_blocks))
        )

        self.b_tril_mask = jnp.column_stack(
            (jnp.ones(cond_size, jnp.int32), b_tril_mask(block_shape, n_blocks))
        )
        self.b_diag_mask_idxs = jnp.where(self.b_diag_mask)

        in_features, out_features = (
            block_shape[1] * n_blocks + cond_dim,
            block_shape[0] * n_blocks,
        )

        *w_key, bias_key, scale_key = random.split(key, n_blocks + 2)

        self.W = init(w_key[0], (out_features, in_features)) * (
            self.b_tril_mask + self.b_diag_mask
        )
        self.bias = (random.uniform(bias_key, (out_features,)) - 0.5) * (
            2 / jnp.sqrt(out_features)
        )

        self.n_blocks = n_blocks
        self.block_shape = block_shape
        self.cond_dim = cond_dim
        self.W_log_scale = jnp.log(random.uniform(scale_key, (out_features, 1)))
        self.in_features = in_features
        self.out_features = out_features

    def get_normalised_weights(self):
        "Carries out weight normalisation."
        W = jnp.exp(self.W) * self.b_diag_mask + self.W * self.b_tril_mask
        W_norms = jnp.linalg.norm(W, axis=-1, keepdims=True)
        return jnp.exp(self.W_log_scale) * W / W_norms

    def __call__(self, x, condition=None):
        "returns output y, and components of weight matrix needed log_det component (n_blocks, block_shape[0], block_shape[1])"
        W = self.get_normalised_weights()
        if condition is not None:
            x = jnp.concatenate((condition, x))
        y = W @ x + self.bias
        jac_3d = W[self.b_diag_mask_idxs].reshape(self.n_blocks, *self.block_shape)
        return y, jnp.log(jac_3d)


def logmatmulexp(x, y):
    """
    Numerically stable version of ``(x.log() @ y.log()).exp()``. From numpyro https://github.com/pyro-ppl/numpyro/blob/f2ff89a3a7147617e185eb51148eb15d56d44661/numpyro/distributions/util.py#L387
    """
    x_shift = jax.lax.stop_gradient(jnp.amax(x, -1, keepdims=True))
    y_shift = jax.lax.stop_gradient(jnp.amax(y, -2, keepdims=True))
    xy = jnp.log(jnp.matmul(jnp.exp(x - x_shift), jnp.exp(y - y_shift)))
    return xy + x_shift + y_shift


class TanhBNAF:
    """
    Tanh transformation compatible with BNAF (log_abs_det provided as 3D array).
    """

    def __init__(self, n_blocks: int):
        self.n_blocks = n_blocks

    def __call__(self, x):
        """Applies the activation and computes the Jacobian. Jacobian shape is
        (n_blocks, *block_size).

        Returns:
            Tuple: output, jacobian
        """
        d = x.shape[0] // self.n_blocks
        log_det_vals = -2 * (x + jax.nn.softplus(-2 * x) - jnp.log(2.0))
        log_det = jnp.full((self.n_blocks, d, d), -jnp.inf)
        log_det = log_det.at[:, jnp.arange(d), jnp.arange(d)].set(
            log_det_vals.reshape(self.n_blocks, d)
        )
        return jnp.tanh(x), log_det


class BlockAutoregressiveNetwork(Bijection):
    depth: int
    layers: list
    cond_dim: int
    block_dim: int
    activation: Callable

    def __init__(
        self,
        key: KeyArray,
        dim: int,
        cond_dim: int,
        depth: int,
        block_dim: int,
        activation: Callable = None,
    ):
        """Block Neural Autoregressive Network (see https://arxiv.org/abs/1904.04676).

        Args:
            key (KeyArray): Jax PRNGKey
            dim (int): Dimension of the distribution.
            cond_dim (int): Dimension of extra conditioning variables.
            depth (int): Number of hidden layers in the network.
            block_dim (int): Block dimension (hidden layer size is roughly dim*block_dim).
            activation (Callable, optional): Activation function. Defaults to TanhBNAF.
        """
                
        activation = TanhBNAF(dim) if activation is None else activation
        layers = []
        if depth == 0:
            layers.append(BlockAutoregressiveLinear(key, dim, (1, 1), cond_dim))
        else:
            keys = random.split(key, depth + 1)
            block_shapes = [(block_dim, 1), *(block_dim, block_dim)*(depth-1), (1, block_dim)]
            cond_dims = [cond_dim] + [0]*depth

            for key, block_shape, cd in zip(keys, block_shapes, cond_dims):
                layers.extend([
                    BlockAutoregressiveLinear(key, dim, block_shape, cd),
                    activation
                ])
            layers = layers[:-1] # remove last activation
                    
        self.depth = depth
        self.layers = layers
        self.cond_dim = cond_dim
        self.block_dim = block_dim
        self.activation = activation

    def transform(self, x, condition=None):
        x = self.layers[0](x, condition)[0]
        for layer in self.layers[1:]:
            x = layer(x)[0]
        return x

    def transform_and_log_abs_det_jacobian(self, x, condition=None):
        x, log_det_3d_0 = self.layers[0](x, condition)
        log_det_3ds = [log_det_3d_0]
        for layer in self.layers[1:]:
            x, log_det_3d = layer(x)
            log_det_3ds.append(log_det_3d)

        logdet = log_det_3ds[-1]
        for ld in reversed(log_det_3ds[:-1]):
            logdet = logmatmulexp(logdet, ld)
        return x, logdet.sum()

    def inverse(self, *args, **kwargs):
        raise NotImplementedError(
            "This transform would require numerical methods for inversion."
        )

    def inverse_and_log_abs_det_jacobian(self, *args, **kwargs):
        raise NotImplementedError(
            "This transform would require numerical methods for inversion."
        )
