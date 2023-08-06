from typing import Callable, Collection, Optional, Tuple

import torch
import torch.nn as nn
from torch import Tensor
from torch.nn.parameter import Parameter

from classiq.applications.qnn.gradients.quantum_gradient import EXECUTE_FUNCTION
from classiq.applications.qnn.gradients.simple_quantum_gradient import (
    SimpleQuantumGradient,
)
from classiq.applications.qnn.qasm3_utils import (
    QASM3_TYPE,
    QASM3PARSER_LIKE,
    to_qasm3_parser,
)
from classiq.applications.qnn.torch_utils import iter_inputs_weights
from classiq.exceptions import ClassiqTorchError


class QLayerFunction(torch.autograd.Function):
    @staticmethod
    def forward(  # type: ignore[override]
        ctx,
        inputs: Tensor,
        weights: Tensor,
        qcode: QASM3PARSER_LIKE,
        execution_function: EXECUTE_FUNCTION,
    ) -> Tensor:
        """
        This function receives:
            inputs: a 2D Tensor of floats - (batch_size, in_features)
            weights: a 2D Tensor of floats - (out_features, in_features)
            qcode: a string of parametric OpenQASM3 code
                (or a `QASM3Parser` object, which is like a parsed OpenQASM)
            execution_function: a function taking `qcode, arguments`,
                and returning a result (of type Tensor)
                where `arguments` is of type `EXECUTE_FUNCTION`
                    (from `classiq.applications.qnn.gradients`)
        """
        qasm3_parser = to_qasm3_parser(qcode)

        # save for backward
        ctx.save_for_backward(inputs, weights)
        ctx.execution_function = execution_function
        ctx.qasm3_parser = qasm3_parser
        ctx.quantum_gradient = SimpleQuantumGradient(execution_function, qasm3_parser)

        def _execute(inputs_: Tensor, weights_: Tensor) -> Tensor:
            return execution_function(
                qasm3_parser.qcode, qasm3_parser._map_parameters(inputs_, weights_)
            )

        return iter_inputs_weights(_execute, inputs, weights)

    @staticmethod
    def backward(  # type: ignore[override]
        ctx, grad_output: Tensor
    ) -> Tuple[Optional[Tensor], Optional[Tensor], None, None]:
        inputs, weights = ctx.saved_tensors

        grad_weights = grad_inputs = grad_qcode = grad_execution_function = None

        if ctx.needs_input_grad[1]:
            grad_weights = iter_inputs_weights(
                ctx.quantum_gradient.gradient, inputs, weights
            )

            grad_weights = grad_weights * grad_output

        if any(ctx.needs_input_grad[i] for i in (0, 2, 3)):
            raise ClassiqTorchError(
                f"Grad required for unknown type: {ctx.needs_input_grad}"
            )

        return grad_inputs, grad_weights, grad_qcode, grad_execution_function


Qubit = str  # like "q[0]"
Qubits = Collection[Qubit]
CalcNumOutFeatures = Callable[[Qubits], int]


def calc_num_out_features_single_output(measured_qubits: Qubits) -> int:
    return 1


# Todo: extend the input to allow for multiple `qcode` - one for each output
#   thus allowing (something X n) instead of (something X 1) output
class QLayer(nn.Module):
    def __init__(
        self,
        qcode: QASM3_TYPE,
        execution_function: EXECUTE_FUNCTION,
        head_start: Optional[float] = None,
        calc_num_out_features: CalcNumOutFeatures = calc_num_out_features_single_output,
    ):
        super().__init__()

        self._execution_function = execution_function
        self._head_start = head_start

        self._qasm3_parser = to_qasm3_parser(qcode)
        self.in_features = len(self._qasm3_parser._qcode_parameters_weights)
        self.out_features = calc_num_out_features(
            self._qasm3_parser._qcode_measured_qubits
        )

        self._initialize_parameters()

    def _initialize_parameters(self) -> None:
        shape = (self.out_features, self.in_features)
        if self._head_start is None:
            value = torch.rand(shape)
        else:
            value = torch.zeros(shape) + self._head_start

        self.weight = Parameter(value)

    def forward(self, x: Tensor) -> Tensor:
        return QLayerFunction.apply(
            x, self.weight, self._qasm3_parser, self._execution_function
        )
