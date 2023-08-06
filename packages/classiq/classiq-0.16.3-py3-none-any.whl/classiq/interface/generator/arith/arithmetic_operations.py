from __future__ import annotations

import abc
from typing import Any, Dict, Iterable, Optional, Set

import pydantic

from classiq.interface.generator.function_params import IO, FunctionParams, IOName

_DEFAULT_GARBAGE_OUT_NAME = "extra_qubits"
_IDENTICAL_GARBAGE_OUTPUT_NAME_ERROR_MSG = "Output and garbage names cannot be the same"


class ArithmeticOperationParams(FunctionParams):
    output_size: Optional[pydantic.PositiveInt]
    output_name: str
    garbage_output_name: str = _DEFAULT_GARBAGE_OUT_NAME

    @pydantic.validator("garbage_output_name")
    def _validate_garbage_output_name(
        cls, garbage_output_name: str, values: Dict[str, Any]
    ) -> str:
        output_name: Optional[str] = values.get("output_name")
        if garbage_output_name == output_name:
            raise ValueError(_IDENTICAL_GARBAGE_OUTPUT_NAME_ERROR_MSG)
        return garbage_output_name

    @abc.abstractmethod
    def is_inplaced(self) -> bool:
        pass

    @abc.abstractmethod
    def get_params_inplace_options(self) -> Iterable[ArithmeticOperationParams]:
        pass

    def output_name_set(self) -> Set[IOName]:
        return set(self.get_io_names(io=IO.Output, is_inverse=False))
