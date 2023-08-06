import abc
import re
from enum import Enum
from typing import Any, Collection, Dict, Iterable, List, Optional, Type

import pydantic
from pydantic import BaseModel
from pydantic.fields import ModelPrivateAttr

from classiq.interface.generator.arith.register_user_input import RegisterUserInput
from classiq.interface.generator.control_state import ControlState
from classiq.interface.helpers.custom_pydantic_types import PydanticNonEmptyString

FunctionParamsDiscriminator = str

IOName = PydanticNonEmptyString

DEFAULT_OUTPUT_NAME = "OUT"
DEFAULT_INPUT_NAME = "IN"

BAD_FUNCTION_ERROR_MSG = "field must be provided to deduce"
NO_DISCRIMINATOR_ERROR_MSG = "Unknown"

BAD_INPUT_REGISTER_ERROR_MSG = "Bad input register name given"
BAD_OUTPUT_REGISTER_ERROR_MSG = "Bad output register name given"
END_BAD_REGISTER_ERROR_MSG = (
    "Register name must be in snake_case and begin with a letter."
)

ALPHANUM_AND_UNDERSCORE = r"[0-9a-zA-Z_]*"
NAME_REGEX = rf"[a-zA-Z]{ALPHANUM_AND_UNDERSCORE}"


class IO(Enum):
    Input = "Input"
    Output = "Output"


def input_io(is_inverse: bool) -> IO:
    if is_inverse:
        return IO.Output
    return IO.Input


def output_io(is_inverse: bool) -> IO:
    if is_inverse:
        return IO.Input
    return IO.Output


class ParamMetadata(BaseModel):
    metadata_type: str


class FunctionParams(BaseModel, abc.ABC):
    _input_names: List[IOName] = pydantic.PrivateAttr(default_factory=list)
    _output_names: List[IOName] = pydantic.PrivateAttr(default=[DEFAULT_OUTPUT_NAME])

    def __init__(self, **data: Any):
        super().__init__(**data)
        self._create_io_names()
        self._validate_io_names()

    def get_io_names(
        self,
        io: IO,
        is_inverse: bool = False,
        control_states: Optional[List[ControlState]] = None,
    ) -> List[IOName]:
        assert io == IO.Input or io == IO.Output, "Unsupported IO type"
        control_ios = (state.name for state in control_states) if control_states else ()
        if (io == IO.Input) ^ is_inverse:
            return [*self._input_names, *control_ios]
        else:
            return [*self._output_names, *control_ios]

    def is_powerable(self) -> bool:
        input_names = set(self.get_io_names(IO.Input))
        output_names = set(self.get_io_names(IO.Output))
        return (
            len(input_names) == len(output_names)
            and (len(input_names - output_names) <= 1)
            and (len(output_names - input_names) <= 1)
        )

    def _create_io_names(self) -> None:
        pass

    def _validate_io_names(self) -> None:
        error_msg: List[str] = []
        error_msg += self._get_error_msg(
            self._input_names, BAD_INPUT_REGISTER_ERROR_MSG
        )
        error_msg += self._get_error_msg(
            self._output_names, BAD_OUTPUT_REGISTER_ERROR_MSG
        )
        if error_msg:
            error_msg += [END_BAD_REGISTER_ERROR_MSG]
            raise ValueError("\n".join(error_msg))

    def _get_error_msg(self, names: Iterable[IOName], msg: str) -> List[str]:
        bad_names = [name for name in names if re.fullmatch(NAME_REGEX, name) is None]
        return [f"{msg}: {bad_names}"] if bad_names else []

    def is_valid_io_name(self, name: IOName, io: IO) -> bool:
        return name in self.get_io_names(io)

    @classmethod
    def get_default_input_names(cls) -> Optional[List[IOName]]:
        return cls._get_io_name_default_if_exists(io_attr_name="_input_names")

    @classmethod
    def get_default_output_names(cls) -> Optional[List[IOName]]:
        return cls._get_io_name_default_if_exists(io_attr_name="_output_names")

    @classmethod
    def _is_default_create_io_method(cls) -> bool:
        return cls._create_io_names == FunctionParams._create_io_names

    @classmethod
    def _get_io_name_default_if_exists(
        cls, io_attr_name: str
    ) -> Optional[List[IOName]]:
        if not cls._is_default_create_io_method():
            return None

        attr: ModelPrivateAttr = cls.__private_attributes__[io_attr_name]
        return attr.get_default()

    @staticmethod
    def _assert_boolean_register(reg: RegisterUserInput) -> None:
        if reg.is_boolean_register():
            return
        raise ValueError("Register doesn't match a boolean variable")

    def get_metadata(self) -> Optional[ParamMetadata]:
        return None

    @classmethod
    def discriminator(
        cls,
    ) -> FunctionParamsDiscriminator:
        return cls.__name__


def parse_function_params(
    params: Any,
    discriminator: Any,
    param_classes: Collection[Type[FunctionParams]],
    no_discriminator_error: Exception,
    bad_function_error: Exception,
) -> FunctionParams:  # Any is for use in pydantic validators.
    if not discriminator:
        raise no_discriminator_error

    matching_classes = [
        param_class
        for param_class in param_classes
        if param_class.discriminator() == discriminator
    ]

    if len(matching_classes) != 1:
        raise bad_function_error

    return matching_classes[0].parse_obj(params)


def parse_function_params_values(
    values: Dict[str, Any],
    params_key: str,
    discriminator_key: str,
    param_classes: Collection[Type[FunctionParams]],
) -> None:
    params = values.get(params_key)
    if isinstance(params, FunctionParams):
        values[discriminator_key] = params.discriminator()
        return
    discriminator = values.get(discriminator_key)
    values[params_key] = parse_function_params(
        params=params,
        discriminator=discriminator,
        param_classes=param_classes,
        no_discriminator_error=ValueError(
            f"The {discriminator_key} {NO_DISCRIMINATOR_ERROR_MSG} {params_key} type."
        ),
        bad_function_error=ValueError(
            f"{BAD_FUNCTION_ERROR_MSG} {discriminator_key}: {discriminator}"
        ),
    )
