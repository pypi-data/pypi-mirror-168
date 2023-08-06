from __future__ import annotations

import functools as ft
from typing import Any, Callable

import jax
import jax.numpy as jnp

from kernex._src.utils import ZIP

# ---------------------- resolve_arguments ------------------------ #


def _resolve_padding_argument(
    input_argument: tuple[int | tuple[int, int] | str, ...] | int | str,
    kernel_size: tuple[int, ...],
):
    """Helper function to generate padding"""

    if isinstance(input_argument, tuple):
        same = lambda wi: ((wi - 1) // 2, wi // 2)

        assert len(input_argument) == len(kernel_size), (
            "kernel_size dimension != padding dimension.",
            f"Found length(kernel_size)={len(kernel_size)} length(padding)={len(input_argument)}",
        )

        padding = [[]] * len(kernel_size)

        for i, item in enumerate(input_argument):
            if isinstance(item, int):
                padding[i] = (item, item)

            elif isinstance(item, tuple):
                padding[i] = item

            elif isinstance(item, str):
                if item in ["same", "SAME"]:
                    padding[i] = same(kernel_size[i])

                elif item in ["valid", "VALID"]:
                    padding[i] = (0, 0)

                else:
                    raise ValueError(
                        f'string argument must be in ["same","SAME","VALID","valid"].Found {item}'
                    )
        return tuple(padding)

    elif isinstance(input_argument, int):
        return ((input_argument, input_argument),) * len(kernel_size)

    elif isinstance(input_argument, str):
        same = lambda wi: ((wi - 1) // 2, wi // 2)

        if input_argument.lower() == "same":
            return tuple(same(wi) for wi in kernel_size)

        elif input_argument.lower() == "valid":
            return ((0, 0),) * len(kernel_size)

        else:
            raise ValueError(
                f'string argument must be in ["same","SAME","VALID","valid"].Found {input_argument}'
            )


def _resolve_dict_argument(
    input_dict: dict[str, int], dim: int, default: Any
) -> dict[Any:Any]:
    """return a tuple that map values of dict into tuple

    Args:
        input_dict (dict[str, int]): named_axis dict
        dim (int): dimension of the output tuple
        default (Any): default value of the output tuple

    Example:
        >>> _resolve_dict_argument({0:1,1:2,2:3},dim=3,default=0) -> (1,2,3)
        >>> _resolve_dict_argument({1:2,0:1,2:3},dim=3,default=0) -> (1,2,3)
        >>> _resolve_dict_argument({0:1},dim=3,default=0) -> (1,0,0)
        >>> _resolve_dict_argument({0:(1,0)},dim=3,default=0) -> ((1,0),(0,0),(0,0)) # tuple is inferred
    """
    # assign mutable list
    temp = [default] * dim

    for dim, val in input_dict.items():
        temp[dim] = val

    return tuple(temp)


def _resolve_offset_argument(input_argument, kernel_size):

    if isinstance(input_argument, (tuple, list)):
        offset = [[]] * len(kernel_size)

        for i, item in enumerate(input_argument):
            offset[i] = (item, item) if isinstance(item, int) else item

        return offset

    elif isinstance(input_argument, int):
        return [(input_argument, input_argument)] * len(kernel_size)

    else:
        raise NotImplementedError(
            "input_argument type={} is not implemented".format(type(input_argument))
        )


def _resolve_index(index, shape):
    """Resolve index to a tuple of int"""

    def _resolve_single_index(index, shape):
        if isinstance(index, int):
            index += shape if index < 0 else 0
            return index

        elif isinstance(index, slice):
            start, end, step = index.start, index.stop, index.step

            start = start or 0
            start += shape if start < 0 else 0

            end = end or shape
            end += shape if end < 0 else 0

            step = step or 1

            return (start, end, step)

        elif isinstance(index, (list, tuple)):
            assert all(
                isinstance(i, int) for i in jax.tree_util.tree_leaves(index)
            ), "All items in tuple must be int"
            return index

        else:
            raise NotImplementedError(f"index type={type(index)} is not implemented")

    index = [index] if not isinstance(index, tuple) else index
    resolved_index = [[]] * len(index)

    for i, (item, in_dim) in enumerate(zip(index, shape)):
        resolved_index[i] = _resolve_single_index(item, in_dim)

    return resolved_index


def _normalize_slices(
    container: dict[Callable[Any], jnp.ndarray], in_dim: tuple[int, ...]
) -> dict[Callable[Any], jnp.ndarray]:
    """Convert slice with partial range to tuple with determined range"""

    for func, slices in container.items():
        slices = [_resolve_index(index, in_dim) for index in slices]
        container[func] = slices
    return container


@ft.lru_cache(maxsize=None)
def _resolve_kernel_size(arg, in_dim):

    kw = "kernel_size"

    if isinstance(arg, tuple):
        assert all(isinstance(wi, int) for wi in arg), (
            f"{kw}  input must be a tuple of int.\n"
            f"Found {tuple(type(wi) for wi in arg  )}"
        )

        assert len(arg) == len(in_dim), (
            f"{kw}  dimension must be equal to array dimension.",
            f"Found len({arg }) != len{(in_dim)}",
        )

        assert all(ai <= si for (ai, si) in zip(arg, in_dim)), (
            f"{kw} shape must be less than array shape.\n",
            f"Found {kw}  = {arg } array shape = {in_dim} ",
        )

        return tuple(si if wi == -1 else wi for si, wi in ZIP(in_dim, arg))

    elif isinstance(arg, int):
        return (in_dim if arg == -1 else arg) * len(in_dim)

    else:
        raise ValueError(f"{kw}  must be instance of int or tuple. Found {type(arg)}")


@ft.lru_cache(maxsize=None)
def _resolve_strides(arg, in_dim):

    kw = "strides"

    if isinstance(arg, tuple):
        assert all(isinstance(wi, int) for wi in arg), (
            f"{kw}  input must be a tuple of int.\n"
            f"Found {tuple(type(wi) for wi in arg  )}"
        )

        assert len(arg) == len(in_dim), (
            f"{kw}  dimension must be equal to array dimension.",
            f"Found len({arg }) != len{(in_dim)}",
        )

        assert all(ai <= si for (ai, si) in zip(arg, in_dim)), (
            f"{kw} shape must be less than array shape.\n",
            f"Found {kw}  = {arg } array shape = {in_dim} ",
        )

        return arg

    elif isinstance(arg, int):
        return (arg,) * len(in_dim)

    else:
        raise ValueError(f"{kw}  must be instance of int or tuple. Found {type(arg)}")
