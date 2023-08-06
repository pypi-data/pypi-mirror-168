from __future__ import annotations

from enum import Enum
from typing import Any, Dict, Generic, Iterable, List, Optional, Tuple, TypeVar, Union

import pydantic
from pydantic import BaseModel
from pydantic.generics import GenericModel
from typing_extensions import Literal

from classiq.interface.generator.arith.arithmetic_operations import (
    ArithmeticOperationParams,
)
from classiq.interface.generator.arith.fix_point_number import FixPointNumber
from classiq.interface.generator.arith.register_user_input import RegisterUserInput

DEFAULT_RIGHT_ARG_NAME = "right_arg"
DEFAULT_LEFT_ARG_NAME = "left_arg"
MIN_OUTPUT_NAME = "min_value"
MAX_OUTPUT_NAME = "max_value"
LeftDataT = TypeVar("LeftDataT")
RightDataT = TypeVar("RightDataT")
_NumericArgumentInplaceErrorMessage = "Cannot inplace the numeric argument {}"
Numeric = (float, int)


class ArgToInplace(str, Enum):
    LEFT = "left"
    RIGHT = "right"


class BinaryOpParams(
    GenericModel, ArithmeticOperationParams, Generic[LeftDataT, RightDataT]
):
    left_arg: LeftDataT
    right_arg: RightDataT

    @pydantic.validator("left_arg")
    def set_left_arg_name(cls, left_arg: LeftDataT):
        if isinstance(left_arg, RegisterUserInput):
            left_arg.name = left_arg.name or DEFAULT_LEFT_ARG_NAME
        return left_arg

    @pydantic.validator("right_arg")
    def set_right_arg_name(cls, right_arg: RightDataT):
        if isinstance(right_arg, RegisterUserInput):
            right_arg.name = right_arg.name or DEFAULT_RIGHT_ARG_NAME
        return right_arg

    @pydantic.root_validator(pre=True)
    def validate_one_is_register(cls, values: Dict[str, Any]):
        left_arg = values.get("left_arg")
        right_arg = values.get("right_arg")
        if isinstance(left_arg, Numeric) and isinstance(right_arg, Numeric):
            raise ValueError("One argument must be a register")
        if left_arg is right_arg and isinstance(left_arg, BaseModel):
            # In case both arguments refer to the same object, copy it.
            # This prevents changes performed on one argument to affect the other.
            values["right_arg"] = left_arg.copy(deep=True)
        inplace_arg: Optional[ArgToInplace] = values.get("inplace_arg")
        if inplace_arg == ArgToInplace.RIGHT and isinstance(right_arg, Numeric):
            raise ValueError(_NumericArgumentInplaceErrorMessage.format(right_arg))
        elif inplace_arg == ArgToInplace.LEFT and isinstance(left_arg, Numeric):
            raise ValueError(_NumericArgumentInplaceErrorMessage.format(left_arg))
        return values

    def _create_io_names(self):
        self._create_input_names()
        self._create_output_names()

    def _create_input_names(self) -> None:
        input_name_list = self._input_register_name_list(
            [self.left_arg, self.right_arg, getattr(self, "target", None)]
        )
        assert input_name_list, "At least one argument should be a register"
        self._input_names = input_name_list

    def _create_output_names(self) -> None:
        output_name_list: List[str] = (
            self._carried_inputs_name_dict()
            + self._garbage_output_names()
            + [self.output_name]
        )
        self._output_names = output_name_list

    def _garbage_output_names(self) -> List[str]:
        return list()

    def _carried_inputs_name_dict(self) -> List[str]:
        return self._input_register_name_list(list(self._carried_arguments()))

    def _carried_arguments(self) -> Tuple[Optional[LeftDataT], Optional[RightDataT]]:
        inplace_arg = getattr(self, "inplace_arg", None)
        if inplace_arg == ArgToInplace.RIGHT and isinstance(
            self.left_arg, RegisterUserInput
        ):
            return self.left_arg, None  # type: ignore[return-value]
        elif inplace_arg == ArgToInplace.LEFT and isinstance(
            self.right_arg, RegisterUserInput
        ):
            return None, self.right_arg  # type: ignore[return-value]
        elif inplace_arg is not None:
            return None, None
        return self.left_arg, self.right_arg

    @staticmethod
    def _input_register_name_list(possible_register_args: List[Any]) -> List[str]:
        return [
            arg.name
            for arg in possible_register_args
            if isinstance(arg, RegisterUserInput) and arg.name
        ]

    def is_inplaced(self) -> bool:
        return getattr(self, "inplace_arg", None) is not None

    def _get_binary_op_inplace_options(self) -> Iterable[ArgToInplace]:
        right_arg = getattr(self, "right_arg", None)
        left_arg = getattr(self, "left_arg", None)
        if isinstance(right_arg, RegisterUserInput) and isinstance(
            left_arg, RegisterUserInput
        ):
            if left_arg.size > right_arg.size:
                yield ArgToInplace.LEFT
                yield ArgToInplace.RIGHT
            else:
                yield ArgToInplace.RIGHT
                yield ArgToInplace.LEFT
        elif isinstance(right_arg, RegisterUserInput):
            yield ArgToInplace.RIGHT
        elif isinstance(left_arg, RegisterUserInput):
            yield ArgToInplace.LEFT

    def get_params_inplace_options(self) -> Iterable[BinaryOpParams]:
        params_kwargs = self.copy().__dict__
        if not hasattr(self, "inplace_arg"):
            return
        for inplace_arg in self._get_binary_op_inplace_options():
            params_kwargs["inplace_arg"] = inplace_arg
            yield self.__class__(**params_kwargs)

    class Config:
        arbitrary_types_allowed = True


class BinaryOpWithIntInputs(
    BinaryOpParams[Union[int, RegisterUserInput], Union[int, RegisterUserInput]]
):
    @pydantic.root_validator()
    def validate_int_registers(cls, values):
        left_arg = values.get("left_arg")
        is_left_arg_float_register = (
            isinstance(left_arg, RegisterUserInput) and left_arg.fraction_places > 0
        )
        right_arg = values.get("right_arg")
        is_right_arg_float_register = (
            isinstance(right_arg, RegisterUserInput) and right_arg.fraction_places > 0
        )
        if is_left_arg_float_register or is_right_arg_float_register:
            raise ValueError("Boolean operation are defined only for integer")

        return values


class BinaryOpWithFloatInputs(
    BinaryOpParams[
        Union[float, FixPointNumber, RegisterUserInput],
        Union[float, FixPointNumber, RegisterUserInput],
    ]
):
    @pydantic.validator("left_arg", "right_arg")
    def convert_numeric_to_fix_point_number(cls, val):
        if isinstance(val, Numeric):
            val = FixPointNumber(float_value=val)
        return val


class BitwiseAnd(BinaryOpWithIntInputs):
    output_name: str = "bitwise_and"


class BitwiseOr(BinaryOpWithIntInputs):
    output_name: str = "bitwise_or"


class BitwiseXor(BinaryOpWithIntInputs):
    output_name: str = "bitwise_xor"
    inplace_arg: Optional[ArgToInplace] = None

    def _garbage_output_names(self) -> List[str]:
        if self.output_size is None:
            return list()
        elif (
            self.inplace_arg == ArgToInplace.RIGHT
            and self.output_size < self.right_arg.size  # type: ignore[union-attr]
        ) or (
            self.inplace_arg == ArgToInplace.LEFT
            and self.output_size < self.left_arg.size  # type: ignore[union-attr]
        ):
            return [self.garbage_output_name]
        return list()


class Adder(BinaryOpWithFloatInputs):
    output_name: str = "sum"
    inplace_arg: Optional[ArgToInplace] = None

    def _garbage_output_names(self) -> List[str]:
        if self.output_size is None:
            return list()
        if (
            self.inplace_arg == ArgToInplace.RIGHT
            and self.output_size < self.right_arg.size  # type: ignore[union-attr]
        ) or (
            self.inplace_arg == ArgToInplace.LEFT
            and self.output_size < self.left_arg.size  # type: ignore[union-attr]
        ):
            return [self.garbage_output_name]
        return list()


class Subtractor(BinaryOpWithFloatInputs):
    output_name: str = "difference"
    inplace_arg: Optional[ArgToInplace] = None


class Multiplier(BinaryOpWithFloatInputs):
    output_name: str = "product"


class Comparator(BinaryOpWithFloatInputs):
    output_size: Literal[1] = 1
    _include_equal: bool = pydantic.PrivateAttr(default=True)
    target: Optional[RegisterUserInput]

    @pydantic.validator("target", always=True)
    def _validate_target(
        cls, target: Optional[RegisterUserInput], values: Dict[str, Any]
    ) -> Optional[RegisterUserInput]:
        if target:
            cls._assert_boolean_register(target)
            target.name = target.name or values.get("output_name", "")
        return target


class Equal(Comparator):
    output_name: str = "is_equal"


class NotEqual(Comparator):
    output_name: str = "is_not_equal"


class GreaterThan(Comparator):
    output_name: str = "is_greater_than"


class GreaterEqual(Comparator):
    output_name: str = "is_greater_equal"


class LessThan(Comparator):
    output_name: str = "is_less_than"


class LessEqual(Comparator):
    output_name: str = "is_less_equal"


class Extremum(BinaryOpWithFloatInputs):
    _is_min: bool = pydantic.PrivateAttr(default=True)


class Min(Extremum):
    output_name: str = MIN_OUTPUT_NAME


class Max(Extremum):
    output_name: str = MAX_OUTPUT_NAME


class LShift(BinaryOpParams[RegisterUserInput, pydantic.NonNegativeInt]):
    output_name: str = "left_shifted"
    inplace_arg: Optional[ArgToInplace] = ArgToInplace.LEFT


class RShift(BinaryOpParams[RegisterUserInput, pydantic.NonNegativeInt]):
    output_name: str = "right_shifted"
    inplace_arg: Optional[ArgToInplace] = ArgToInplace.LEFT

    def _garbage_output_names(self) -> List[str]:
        if min(self.left_arg.size, self.right_arg) and self.inplace_arg:
            return [self.garbage_output_name]
        return list()


class CyclicShift(BinaryOpParams[RegisterUserInput, int]):
    output_name: str = "cyclic_shifted"
    inplace_arg: Optional[ArgToInplace] = ArgToInplace.LEFT
