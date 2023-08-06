from collections.abc import Sized
from functools import reduce
from typing import Callable, Union

import torch
import torch.nn as nn
from torch import Tensor

from classiq.exceptions import ClassiqValueError


def get_shape_second_dimension(shape: torch.Size):
    if not isinstance(shape, Sized):
        raise ClassiqValueError("Invalid shape type - must have `__len__`")

    if len(shape) == 1:
        return 1
    elif len(shape) == 2:
        return shape[1]
    else:
        raise ClassiqValueError("Invalid shape dimension - must be 1D or 2D")


def get_shape_first_dimension(shape: torch.Size):
    if not isinstance(shape, Sized):
        raise ClassiqValueError("Invalid shape type - must have `__len__`")

    if len(shape) in (1, 2):
        return shape[0]
    else:
        raise ClassiqValueError("Invalid shape dimension - must be 1D or 2D")


def iter_inputs_weights(
    function: Callable[[Tensor, Tensor], Union[Tensor, float]],
    inputs: Tensor,
    weights: Tensor,
) -> Tensor:
    """
    inputs is of shape (batch_size, in_features)
    weights is of shape (out_features, in_features)
    the result is of shape (batch_size, out_features)
    """
    if get_shape_second_dimension(inputs.shape) != get_shape_second_dimension(
        weights.shape
    ):
        raise ClassiqValueError(
            "Shape mismatch! the 2nd dimension of both the inputs and the weights should be the same"
        )

    outer_list = []
    for batch_item in inputs:
        inner_list = []
        for out_weight in weights:
            res = function(batch_item, out_weight)
            inner_list.append(res)
        outer_list.append(inner_list)

    return (
        torch.Tensor(outer_list)
        .reshape(
            get_shape_first_dimension(inputs.shape),
            get_shape_first_dimension(weights.shape),
        )
        .requires_grad_(inputs.requires_grad or weights.requires_grad)
    )


def calculate_amount_of_parameters(net: nn.Module) -> int:
    return sum(  # sum over all parameters
        reduce(int.__mul__, i.shape)  # multiply all dimensions
        for i in net.parameters()
    )
