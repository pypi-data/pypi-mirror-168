import abc
from typing import Callable

from torch import Tensor

from classiq.applications.qnn.qasm3_utils import (
    QASM3_ARGUMENTS_TENSOR,
    QASM3_TYPE,
    QASM3PARSER_LIKE,
    to_qasm3_parser,
)

EXECUTE_FUNCTION = Callable[[QASM3_TYPE, QASM3_ARGUMENTS_TENSOR], Tensor]


class QuantumGradient(abc.ABC):
    def __init__(
        self, execute: EXECUTE_FUNCTION, qasm3_parser: QASM3PARSER_LIKE, *args, **kwargs
    ):
        self._execution_function = execute
        self.qasm3_parser = to_qasm3_parser(qasm3_parser)

    def execute(self, inputs: Tensor, weights: Tensor) -> Tensor:
        return self._execution_function(
            self.qasm3_parser.qcode, self.qasm3_parser._map_parameters(inputs, weights)
        )

    @abc.abstractmethod
    def gradient(self, inputs: Tensor, weights: Tensor, *args, **kwargs) -> Tensor:
        raise NotImplementedError
