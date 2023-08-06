from __future__ import annotations

import functools
import random
import re
import string
from typing import Any, Dict, Iterable, List, Match, Optional, Tuple, Union

import pydantic
from pydantic import BaseModel

from classiq.interface.generator import function_param_list, function_params as f_params
from classiq.interface.generator.control_state import ControlState
from classiq.interface.generator.function_params import NAME_REGEX, IOName
from classiq.interface.generator.mcx import Mcx
from classiq.interface.generator.user_defined_function_params import CustomFunction
from classiq.interface.helpers.custom_pydantic_types import PydanticNonEmptyString

DEFAULT_SUFFIX_LEN: int = 6
BAD_INPUT_ERROR_MSG = "Bad input name given"
BAD_OUTPUT_ERROR_MSG = "Bad output name given"
BAD_INPUT_EXPRESSION_MSG = "Bad input expression given"
BAD_OUTPUT_EXPRESSION_MSG = "Bad output expression given"
BAD_INPUT_SLICING_MSG = "Bad input slicing / indexing given"
BAD_OUTPUT_SLICING_MSG = "Bad output slicing / indexing given"
BAD_CALL_NAME_ERROR_MSG = "Call name must be in snake_case and begin with a letter"
CUSTOM_FUNCTION_SINGLE_IO_ERROR = (
    "Custom function currently supports explicit IO specification only via dictionary"
)


NAME = "name"
SLICING = "slicing"
SEPARATOR = ":"
SLICING_CHARS = rf"[0-9\-{SEPARATOR}]+"
IO_REGEX = rf"(?P<{NAME}>{NAME_REGEX})(\[(?P<{SLICING}>{SLICING_CHARS})\])?"
LEGAL_SLICING = rf"(\-?\d+)?({SEPARATOR}(\-?\d+)?)?({SEPARATOR}(\-?\d+)?)?"

_ALPHANUM_CHARACTERS = string.ascii_letters + string.digits

RegNameAndSlice = Tuple[str, slice]
ParsedIOs = Iterable[Tuple[str, slice, str]]

ZERO_INDICATOR = "0"
INVERSE_SUFFIX = "_qinverse"

WireName = PydanticNonEmptyString
IOType = Union[Dict[IOName, WireName], WireName]


def randomize_suffix(suffix_len: int = DEFAULT_SUFFIX_LEN) -> str:
    return "".join(
        random.choice(_ALPHANUM_CHARACTERS) for _ in range(suffix_len)  # nosec B311
    )


class FunctionCall(BaseModel):
    function: str = pydantic.Field(
        default="", description="The function that is called"
    )
    function_params: f_params.FunctionParams = pydantic.Field(
        description="The parameters necessary for defining the function"
    )
    is_inverse: bool = pydantic.Field(
        default=False, description="Call the function inverse."
    )
    control_states: List[ControlState] = pydantic.Field(
        default_factory=list,
        description="Call the controlled function with the given controlled states.",
    )
    should_control: bool = pydantic.Field(
        default=True,
        description="False value indicates this call shouldn't be controlled even if the flow is controlled.",
    )
    inputs: IOType = pydantic.Field(
        default_factory=dict,
        description="A mapping from the input name to the wire it connects to",
    )
    outputs: IOType = pydantic.Field(
        default_factory=dict,
        description="A mapping from the output name to the wire it connects to",
    )
    power: pydantic.PositiveInt = pydantic.Field(
        default=1, description="Number of successive calls to the operation"
    )

    name: PydanticNonEmptyString = pydantic.Field(
        default=None,
        description="The name of the function instance. "
        "If not set, determined automatically.",
    )

    _non_zero_input_wires: List[WireName] = pydantic.PrivateAttr(default_factory=list)
    _non_zero_output_wires: List[WireName] = pydantic.PrivateAttr(default_factory=list)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._non_zero_input_wires = self._non_zero_wires(self.inputs_dict.values())
        self._non_zero_output_wires = self._non_zero_wires(self.outputs_dict.values())

    @property
    def non_zero_input_wires(self) -> List[WireName]:
        return self._non_zero_input_wires

    @property
    def non_zero_output_wires(self) -> List[WireName]:
        return self._non_zero_output_wires

    @property
    def inputs_dict(self) -> Dict[IOName, WireName]:
        assert isinstance(self.inputs, dict)
        return self.inputs

    @property
    def outputs_dict(self) -> Dict[IOName, WireName]:
        assert isinstance(self.outputs, dict)
        return self.outputs

    @pydantic.validator("name", pre=True, always=True)
    def create_name(cls, name: Optional[str], values: Dict[str, Any]):
        if name is not None:
            match = re.fullmatch(pattern=NAME_REGEX, string=name)
            if match is None:
                raise ValueError(BAD_CALL_NAME_ERROR_MSG)
            return name

        function = values.get("function")
        params = values.get("function_params")
        suffix = randomize_suffix()
        if not function or params is None:
            return name if name else suffix

        if isinstance(params, CustomFunction):
            return f"{params.name}_{suffix}"
        return f"{function}_{suffix}"

    @pydantic.root_validator(pre=True)
    def parse_function_params(cls, values: Dict[str, Any]):
        f_params.parse_function_params_values(
            values=values,
            params_key="function_params",
            discriminator_key="function",
            param_classes=function_param_list.function_param_library.param_list,
        )
        return values

    # TODO: note that this checks FunctionCall input register names
    # are PARTIAL to FuncionParams input register names, not EQUAL.
    # We might want to change that.
    @staticmethod
    def _validate_input_names(
        params: f_params.FunctionParams,
        inputs: Dict[IOName, WireName],
        is_inverse: bool,
        control_states: List[ControlState],
    ) -> None:
        (
            invalid_expressions,
            invalid_slicings,
            invalid_names,
        ) = FunctionCall._get_invalid_ios(
            inputs.keys(), params, f_params.input_io(is_inverse), control_states
        )
        error_msg = []
        if invalid_expressions:
            error_msg.append(f"{BAD_INPUT_EXPRESSION_MSG}: {invalid_expressions}")
        if invalid_names:
            error_msg.append(f"{BAD_INPUT_ERROR_MSG}: {invalid_names}")
        if invalid_slicings:
            error_msg.append(f"{BAD_INPUT_SLICING_MSG}: {invalid_slicings}")
        if error_msg:
            raise ValueError("\n".join(error_msg))

    @pydantic.validator("inputs")
    def validate_inputs(cls, inputs: IOType, values) -> Dict[IOName, WireName]:
        params = values.get("function_params")
        is_inverse = values.get("is_inverse")
        if params is None:
            return dict()
        if isinstance(params, CustomFunction):
            if not isinstance(inputs, dict):
                raise ValueError(CUSTOM_FUNCTION_SINGLE_IO_ERROR)
            return inputs

        if isinstance(inputs, str):
            inputs = FunctionCall._single_wire_to_dict(
                io=f_params.IO.Input,
                is_inverse=is_inverse,
                io_wire=inputs,
                params=params,
            )

        cls._validate_input_names(
            params=params,
            inputs=inputs,
            is_inverse=is_inverse,
            control_states=values.get("control_states"),
        )
        return inputs

    @staticmethod
    def _validate_output_names(
        params: f_params.FunctionParams,
        outputs: Dict[IOName, WireName],
        is_inverse: bool,
        control_states: List[ControlState],
    ) -> None:
        (
            invalid_expressions,
            invalid_slicings,
            invalid_names,
        ) = FunctionCall._get_invalid_ios(
            outputs.keys(),
            params,
            f_params.output_io(is_inverse),
            control_states,
        )
        error_msg = []
        if invalid_expressions:
            error_msg.append(f"{BAD_OUTPUT_EXPRESSION_MSG}: {invalid_expressions}")
        if invalid_names:
            error_msg.append(f"{BAD_OUTPUT_ERROR_MSG}: {invalid_names}")
        if invalid_slicings:
            error_msg.append(f"{BAD_OUTPUT_SLICING_MSG}: {invalid_slicings}")
        if error_msg:
            raise ValueError("\n".join(error_msg))

    @pydantic.validator("outputs")
    def validate_outputs(cls, outputs, values):
        params = values.get("function_params")
        is_inverse = values.get("is_inverse")
        if params is None:
            return outputs
        if isinstance(params, CustomFunction):
            if not isinstance(outputs, dict):
                raise ValueError(CUSTOM_FUNCTION_SINGLE_IO_ERROR)
            return outputs

        if isinstance(outputs, str):
            outputs = FunctionCall._single_wire_to_dict(
                io=f_params.IO.Output,
                is_inverse=is_inverse,
                io_wire=outputs,
                params=params,
            )

        cls._validate_output_names(
            params=params,
            outputs=outputs,
            is_inverse=is_inverse,
            control_states=values.get("control_states"),
        )
        return outputs

    @pydantic.validator("power", always=True)
    def _validate_power(
        cls, power: pydantic.PositiveInt, values: Dict[str, Any]
    ) -> pydantic.PositiveInt:
        function_params = values.get("function_params")
        if function_params is None:
            return power
        if power > 1 and not function_params.is_powerable():
            raise ValueError("Cannot power this operator")
        return power

    @staticmethod
    def _single_wire_to_dict(
        io: f_params.IO,
        is_inverse: bool,
        io_wire: WireName,
        params: f_params.FunctionParams,
    ) -> Dict[IOName, WireName]:
        params_io = params.get_io_names(io=io, is_inverse=is_inverse)
        io_str = "input" if io == f_params.IO.Input else "output"
        if len(params_io) != 1:
            raise ValueError(
                _generate_single_io_err(
                    io_str, params_io, io_wire, type(params).__name__
                )
            )
        return {params_io[0]: io_wire}

    @staticmethod
    def _get_invalid_ios(
        expressions: Iterable[str],
        params: f_params.FunctionParams,
        io: f_params.IO,
        control_states: List[ControlState],
    ) -> Tuple[List[str], List[str], List[str]]:

        expression_matches: Iterable[Optional[Match]] = map(
            functools.partial(re.fullmatch, IO_REGEX), expressions
        )

        valid_matches: List[Match] = []
        invalid_expressions: List[str] = []
        for expression, expression_match in zip(expressions, expression_matches):
            invalid_expressions.append(
                expression
            ) if expression_match is None else valid_matches.append(expression_match)

        invalid_slicings: List[str] = []
        invalid_names: List[str] = []
        for match in valid_matches:
            name = match.groupdict().get(NAME)
            if name is None:
                raise AssertionError("Input/output name validation error")

            slicing = match.groupdict().get(SLICING)
            if slicing is not None and re.fullmatch(LEGAL_SLICING, slicing) is None:
                invalid_slicings.append(match.string)

            if params.is_valid_io_name(name, io):
                continue
            elif all(state.name != name for state in control_states):
                invalid_names.append(name)

        return invalid_expressions, invalid_slicings, invalid_names

    def validate_custom_function_io(self) -> None:
        if not isinstance(self.function_params, CustomFunction):
            raise AssertionError("CustomFunction object expected.")
        FunctionCall._validate_input_names(
            params=self.function_params,
            inputs=self.inputs_dict,
            is_inverse=self.is_inverse,
            control_states=self.control_states,
        )
        FunctionCall._validate_output_names(
            params=self.function_params,
            outputs=self.outputs_dict,
            is_inverse=self.is_inverse,
            control_states=self.control_states,
        )

    def parse_inputs(self) -> ParsedIOs:
        reg_names_and_slices = zip(*map(self.parse_io_slicing, self.inputs_dict.keys()))
        wire_names = self.inputs_dict.values()
        # types cannot be resolved from zip
        return zip(*reg_names_and_slices, wire_names)  # type: ignore[return-value]

    def parse_outputs(self) -> ParsedIOs:
        reg_names_and_slices = zip(
            *map(self.parse_io_slicing, self.outputs_dict.keys())
        )
        wire_names = self.outputs_dict.values()
        # types cannot be resolved from zip
        return zip(*reg_names_and_slices, wire_names)  # type: ignore[return-value]

    @staticmethod
    def parse_io_slicing(io_str: str) -> RegNameAndSlice:
        name, slicing = FunctionCall.separate_name_and_slice(io_str)
        return name, _get_slice(slicing)

    @staticmethod
    def separate_name_and_slice(io_str: str) -> Tuple[str, Optional[str]]:
        match: Optional[Match] = re.fullmatch(IO_REGEX, io_str)
        if match is None:
            raise AssertionError("Input/output name validation error")
        name, slicing = (match.groupdict().get(x) for x in [NAME, SLICING])
        if name is None:
            raise AssertionError("Input/output name validation error")
        return name, slicing

    @staticmethod
    def _non_zero_wires(wires: Iterable[WireName]) -> List[WireName]:
        return [wire for wire in wires if wire != ZERO_INDICATOR]

    def _call_dict_copy(self) -> Dict[str, Any]:
        return self.__dict__.copy()

    def prefixed_wires_copy(self, prefix) -> FunctionCall:
        call_kwargs = self._call_dict_copy()
        call_kwargs["inputs"] = add_prefix_to_wire_dict(self.inputs_dict, prefix)
        call_kwargs["outputs"] = add_prefix_to_wire_dict(self.outputs_dict, prefix)
        return FunctionCall(**call_kwargs)

    def inverse(self) -> FunctionCall:
        call_kwargs = self._call_dict_copy()
        call_kwargs["inputs"] = self.outputs_dict
        call_kwargs["outputs"] = self.inputs_dict
        call_kwargs["name"] = self._inverse_name(self.name)
        call_kwargs["is_inverse"] = not self.is_inverse
        return FunctionCall(**call_kwargs)

    @staticmethod
    def _inverse_name(name: str):
        if name.endswith(INVERSE_SUFFIX):
            return name[: -len(INVERSE_SUFFIX)]
        return f"{name}{INVERSE_SUFFIX}"

    def can_extend_control(self) -> bool:
        return self.should_control and (
            bool(self.control_states) or type(self.function_params) == Mcx
        )

    def control(
        self, control_state: ControlState, input_wire: WireName, output_wire: WireName
    ) -> FunctionCall:
        if (
            control_state.name in self.inputs_dict
            or control_state.name in self.outputs_dict
        ):
            raise ValueError(f"Control name: {control_state.name} already exists")

        inputs, outputs = self.inputs_dict.copy(), self.outputs_dict.copy()
        inputs.update({control_state.name: input_wire})
        outputs.update({control_state.name: output_wire})

        call_kwargs = self._call_dict_copy()
        call_kwargs["inputs"] = inputs
        call_kwargs["outputs"] = outputs
        call_kwargs[
            "name"
        ] = f"{self.name}_{control_state.name}_{control_state.ctrl_state}"
        call_kwargs["control_states"] = self.control_states + [control_state]
        return FunctionCall(**call_kwargs)


def add_prefix_to_wire_dict(
    wire_dict: Dict[IOName, WireName], prefix: str
) -> Dict[IOName, WireName]:
    def _prefix_wire(wire_name: WireName) -> WireName:
        if wire_name == ZERO_INDICATOR:
            return ZERO_INDICATOR
        return prefix + wire_name

    return {
        io_name: _prefix_wire(wire_name) for io_name, wire_name in wire_dict.items()
    }


def _get_slice(slicing: Optional[str]) -> slice:
    if slicing is None:
        return slice(None)

    split = slicing.split(":")

    if len(split) == 1:
        index_block = split[0]
        # failing int raises ValueError which Pydantic captures
        # RegEx matching should deem this scenario impossible
        index = int(index_block)
        stop = index + 1 if index != -1 else None
        return slice(index, stop, None)

    elif len(split) == 2:
        start_block, stop_block = split
        start = _int_or_none(start_block)
        stop = _int_or_none(stop_block)
        return slice(start, stop, None)

    elif len(split) == 3:
        start_block, stop_block, step_block = split
        start = _int_or_none(start_block)
        stop = _int_or_none(stop_block)
        step = _int_or_none(step_block)
        return slice(start, stop, step)

    else:
        raise AssertionError("Input/output slicing validation error")


def _int_or_none(v: str) -> Optional[int]:
    return int(v) if v else None


def _generate_single_io_err(
    io_str: str, io_regs: Iterable[str], io_wire: str, function_name: str
) -> str:
    if not io_regs:
        return (
            f'Cannot create {io_str} wire "{io_wire}". '
            f"Function {function_name} has no {io_str} registers."
        )

    return (
        f"Cannot use a single {io_str} wire. "
        f"Function {function_name} has multiple {io_str} registers: {io_regs}."
    )
