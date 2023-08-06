from __future__ import annotations

import abc
from typing import Any, Dict, Iterable

import pydantic

from classiq.interface.generator.arith.arithmetic import DEFAULT_ARG_NAME
from classiq.interface.generator.arith.arithmetic_operations import (
    ArithmeticOperationParams,
)
from classiq.interface.generator.arith.fix_point_number import FixPointNumber
from classiq.interface.generator.arith.register_user_input import RegisterUserInput


class UnaryOpParams(ArithmeticOperationParams):
    arg: RegisterUserInput
    inplace: bool = False

    @pydantic.validator("arg")
    def _validate_argument(cls, arg: RegisterUserInput) -> RegisterUserInput:
        arg.name = arg.name or DEFAULT_ARG_NAME
        return arg

    @classmethod
    @abc.abstractmethod
    def _expected_result_size(cls, arg: RegisterUserInput) -> int:
        pass

    @abc.abstractmethod
    def _should_add_garbage_name(self) -> bool:
        pass

    def _create_io_names(self) -> None:
        arg_name: str = self.arg.name
        self._input_names = [arg_name]
        self._output_names = [self.output_name]

        if not self.inplace:
            self._output_names.append(arg_name)

        if self._should_add_garbage_name():
            self._output_names.append(self.garbage_output_name)

    def is_inplaced(self) -> bool:
        return self.inplace

    def get_params_inplace_options(self) -> Iterable[UnaryOpParams]:
        params_kwargs = self.copy().__dict__
        params_kwargs["inplace"] = True
        yield self.__class__(**params_kwargs)

    class Config:
        arbitrary_types_allowed = True


class BitwiseInvert(UnaryOpParams):
    output_name: str = "inverted"

    @classmethod
    def _expected_result_size(cls, arg: RegisterUserInput) -> int:
        return arg.size

    def _should_add_garbage_name(self) -> bool:
        return (
            self.inplace
            and (self.output_size is not None)
            and self.output_size < self._expected_result_size(self.arg)
        )


class Negation(UnaryOpParams):
    output_name: str = "negated"

    @classmethod
    def _expected_result_size(cls, arg: RegisterUserInput) -> int:
        return arg.size + int(arg.size > 1 and not arg.is_signed)

    def _should_add_garbage_name(self) -> bool:
        return (
            (self.output_size == 1)
            and self.inplace
            and self.output_size < self._expected_result_size(self.arg)
        )

    @pydantic.root_validator
    def _validate_output_size(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        output_size = values.get("output_size")
        arg = values.get("arg")
        assert isinstance(arg, RegisterUserInput), "Negation must have an argument"
        assert arg.bounds, "Negation argument must have bounds"

        values["output_size"] = output_size or (
            FixPointNumber.bounds_to_integer_part_size(
                lb=-max(arg.bounds), ub=-min(arg.bounds)
            )
            + arg.fraction_places
        )
        return values
