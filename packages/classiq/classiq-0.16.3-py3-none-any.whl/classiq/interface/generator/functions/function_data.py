import enum
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import pydantic
from pydantic import BaseModel

from classiq.interface.generator.function_call import FunctionCall, WireName
from classiq.interface.generator.function_params import IOName
from classiq.interface.generator.functions.function_implementation import (
    FunctionImplementation,
)
from classiq.interface.generator.functions.function_interface_data import (
    FunctionInterfaceData,
)
from classiq.interface.helpers.custom_pydantic_types import PydanticFunctionNameStr

ImplementationsType = Union[Tuple[FunctionImplementation, ...], FunctionImplementation]


class FunctionType(str, enum.Enum):
    ElementaryFunction = "ElementaryFunction"
    CompositeFunction = "CompositeFunction"


def _first_impl(impl_type: ImplementationsType) -> FunctionImplementation:
    if isinstance(impl_type, FunctionImplementation):
        return impl_type
    else:
        return impl_type[0]


class FunctionData(BaseModel):
    """
    Facilitates the creation of a user-defined custom function
    """

    name: PydanticFunctionNameStr = pydantic.Field(
        description="The name of a custom function"
    )
    interface: FunctionInterfaceData = pydantic.Field(
        default_factory=FunctionInterfaceData,
        description="The IO data that is common to all implementations of the function",
    )
    implementations: Optional[ImplementationsType] = pydantic.Field(
        description="The implementations of the custom function",
    )
    logic_flow: List[FunctionCall] = pydantic.Field(
        default=list(), description="List of function calls to perform."
    )
    inputs: Dict[IOName, WireName] = pydantic.Field(
        default_factory=dict,
        description="A mapping from the input name to the inner wire it connects to",
    )
    outputs: Dict[IOName, WireName] = pydantic.Field(
        default_factory=dict,
        description="A mapping from the output name to the inner wire it connects to",
    )

    _function_type: FunctionType = pydantic.PrivateAttr(default=None)
    _input_set: Set[IOName] = pydantic.PrivateAttr(default_factory=set)
    _output_set: Set[IOName] = pydantic.PrivateAttr(default_factory=set)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.logic_flow:
            self._function_type = FunctionType.CompositeFunction
            self._input_set = set(self.inputs.keys())
            self._output_set = set(self.outputs.keys())
            return

        self._function_type = FunctionType.ElementaryFunction
        self._input_set = set(self.interface.input_names)
        self._output_set = set(self.interface.output_names)
        if not self.interface.output_registers:
            raise ValueError("The outputs of a custom function must be non-empty")

    @property
    def input_set(self) -> Set[IOName]:
        return self._input_set

    @property
    def output_set(self) -> Set[IOName]:
        return self._output_set

    @property
    def function_type(self) -> FunctionType:
        return self._function_type

    @pydantic.validator("name")
    def validate_name(cls, name: str):
        validate_name_end_not_newline(name=name)
        return name

    @pydantic.validator("implementations")
    def validate_implementations(
        cls, implementations: Optional[ImplementationsType], values: Dict[str, Any]
    ):
        if implementations is None:
            return implementations

        if not implementations:
            raise ValueError(
                "The implementations of a custom function must be non-empty."
            )

        if isinstance(implementations, FunctionImplementation):
            implementations = (implementations,)

        interface = values.get("interface")
        assert isinstance(interface, FunctionInterfaceData)
        for impl in implementations:
            impl.validate_ranges_of_all_registers(interface=interface)

        return implementations

    @pydantic.validator("logic_flow")
    def validate_logic_flow_call_names(cls, logic_flow):
        function_call_names = {call.name for call in logic_flow}
        if len(function_call_names) != len(logic_flow):
            raise ValueError("Cannot have two function calls with the same name")

        return logic_flow

    @pydantic.root_validator
    def validate_elementary_or_composite(cls, values):
        implementations = values.get("implementations")
        logic_flow = values.get("logic_flow")
        elementary = bool(implementations is not None)
        composite = bool(len(logic_flow) > 0)
        if elementary == composite:
            raise ValueError(
                "Function must contain either implementations or calls, but not both"
            )

        return values


def validate_name_end_not_newline(name: str):
    _new_line = "\n"
    if name.endswith(_new_line):
        raise ValueError("Function name cannot end in a newline character")
