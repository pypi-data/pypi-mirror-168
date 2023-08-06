import abc
import collections.abc
import functools
import re
from typing import (
    Collection,
    Dict,
    Iterable,
    List,
    Match,
    Optional,
    Set,
    Tuple,
    Type,
    Union,
    cast,
)

from classiq.interface.generator import (
    function_call,
    function_param_list,
    function_params,
)
from classiq.interface.generator.control_state import ControlState
from classiq.interface.generator.function_params import IOName
from classiq.interface.generator.user_defined_function_params import CustomFunction

from classiq.exceptions import ClassiqValueError, ClassiqWiringError
from classiq.model_designer.wire import Wire
from classiq.quantum_functions.function_library import (
    FunctionData,
    FunctionLibrary,
    QuantumFunction,
)
from classiq.quantum_register import QReg as QuantumRegister

QregOrWire = Union[QuantumRegister, Wire]
WireOrWires = Union[Wire, Iterable[Wire]]
SupportedIOUnion = Union[
    Dict[str, QregOrWire],
    Collection[QuantumRegister],
    QuantumRegister,
]

_SAME_INPUT_NAME_ERROR_MSG: str = "Cannot create multiple inputs with the same name"
_INPUT_AS_OUTPUT_ERROR_MSG: str = "Can't connect input directly to output"


class LogicFlowInputWire(Wire):
    def __init__(self, input_name: IOName) -> None:
        super().__init__()
        self._initialize_wire_name(wire_name=input_name)

    @property
    def is_connected(self) -> bool:
        return self.is_ended

    @property
    def is_ended(self) -> bool:
        return self._end_call is not None


class FunctionHandler(abc.ABC):
    def __init__(self) -> None:
        self._generated_wires: Set[Wire] = set()
        self._function_library: Optional[FunctionLibrary] = None
        self._generated_inputs: Dict[IOName, Wire] = dict()
        self._generated_outputs: Dict[IOName, Wire] = dict()

    def _verify_legal_wires(self, wires: WireOrWires) -> None:
        if isinstance(wires, Wire):
            wires = [wires]
        if not all(wire in self._generated_wires for wire in wires):
            raise ClassiqWiringError("Wire does not belong to this generator")

    def _update_generated_wires(self, wires: WireOrWires) -> None:
        if isinstance(wires, Wire):
            wires = [wires]
        self._generated_wires.update(wires)

    @staticmethod
    def _parse_control_states(
        control_states: Optional[Union[ControlState, Iterable[ControlState]]] = None
    ) -> List[ControlState]:
        if control_states is None:
            return list()
        elif isinstance(control_states, ControlState):
            return [control_states]
        return list(control_states)

    def create_inputs(
        self, input_names: Iterable[IOName]
    ) -> Dict[IOName, LogicFlowInputWire]:
        wire_dict = {}

        for name in input_names:
            if name in wire_dict:
                raise ClassiqWiringError(_SAME_INPUT_NAME_ERROR_MSG)
            wire_dict[name] = LogicFlowInputWire(input_name=name)

        self._update_generated_wires(wires=wire_dict.values())
        if any(name in self._generated_inputs for name in wire_dict):
            raise ClassiqWiringError(_SAME_INPUT_NAME_ERROR_MSG)
        self._generated_inputs.update(wire_dict)

        return wire_dict

    def set_outputs(self, outputs: Dict[IOName, Wire]) -> None:
        self._verify_legal_wires(wires=outputs.values())

        for output_name, output_wire in outputs.items():
            if isinstance(output_wire, LogicFlowInputWire):
                raise ClassiqWiringError(f"{_INPUT_AS_OUTPUT_ERROR_MSG} {output_name}")
            output_wire.set_as_output(output_wire_name=output_wire.wire_name)
            self._generated_outputs[output_name] = output_wire

    def apply(
        self,
        function_name: Union[
            str,
            FunctionData,
            QuantumFunction,
        ],
        in_wires: Optional[Union[Dict[str, QregOrWire], QuantumRegister]] = None,
        out_wires: Optional[Union[Dict[str, QregOrWire], QuantumRegister]] = None,
        is_inverse: bool = False,
        control_states: Optional[Union[ControlState, Iterable[ControlState]]] = None,
        should_control: bool = True,
        power: int = 1,
        call_name: Optional[str] = None,
    ) -> Dict[str, Wire]:
        # if there's no function library, create one
        if self._function_library is None:
            self.include_library(FunctionLibrary())

        if isinstance(function_name, FunctionData):
            function_data = function_name
        elif isinstance(function_name, QuantumFunction):
            function_data = function_name.function_data
        else:
            function_data = None

        if function_data:
            if function_data not in self._function_library.data:  # type: ignore[union-attr]
                self._function_library.add_function(function_data)  # type: ignore[union-attr]

            function_name = function_data.name

        return self._function_call_handler(
            CustomFunction.__name__,
            self._function_library.get_function(cast(str, function_name)),  # type: ignore[union-attr]
            in_wires=in_wires,
            out_wires=out_wires,
            is_inverse=is_inverse,
            control_states=control_states,
            should_control=should_control,
            power=power,
            call_name=call_name,
        )

    def _function_call_handler(
        self,
        function: str,
        params: function_params.FunctionParams,
        control_states: Optional[Union[ControlState, Iterable[ControlState]]] = None,
        in_wires: Optional[Union[Dict[str, QregOrWire], QuantumRegister]] = None,
        out_wires: Optional[Union[Dict[str, QregOrWire], QuantumRegister]] = None,
        is_inverse: bool = False,
        should_control: bool = True,
        power: int = 1,
        call_name: Optional[str] = None,
    ) -> Dict[str, Wire]:
        if function != type(params).__name__:
            raise ClassiqValueError(
                "The FunctionParams type does not match function name"
            )

        if (
            isinstance(params, CustomFunction)
            and self._function_library
            and params not in self._function_library.data
        ):
            raise ClassiqValueError("The function is not found in included library.")

        call = function_call.FunctionCall(
            function=function,
            function_params=params,
            is_inverse=is_inverse ^ (power < 0),
            control_states=self._parse_control_states(control_states),
            should_control=should_control,
            power=abs(power),
            name=call_name,
        )

        if in_wires is not None:
            self._connect_in_wires(call=call, in_wires=in_wires)

        self._logic_flow.append(call)

        return self._connect_out_wires(
            call=call,
            out_wires=out_wires or {},
        )

    def _connect_in_wires(
        self,
        call: function_call.FunctionCall,
        in_wires: SupportedIOUnion,
    ) -> None:
        if isinstance(in_wires, dict):
            self._connect_named_in_wires(call=call, in_wires=in_wires)
        elif isinstance(in_wires, QuantumRegister):
            self._connect_unnamed_in_quantum_registers(
                call=call, quantum_registers=[in_wires]
            )
        elif isinstance(in_wires, collections.abc.Collection):
            self._connect_unnamed_in_quantum_registers(
                # mypy doesn't recognize that `dict` wouldn't reach this point
                call=call,
                quantum_registers=in_wires,  # type: ignore[arg-type]
            )
        else:
            raise ClassiqWiringError(
                f"Invalid in_wires type: {type(in_wires).__name__}"
            )

    def _connect_unnamed_in_quantum_registers(
        self,
        call: function_call.FunctionCall,
        quantum_registers: Collection[QuantumRegister],
    ) -> None:
        self._verify_legal_wires(i.wire for i in quantum_registers)

        call_inputs = call.function_params.get_io_names(
            function_params.IO.Input, call.is_inverse, call.control_states
        )

        if len(call_inputs) != len(quantum_registers):
            raise ClassiqWiringError(
                f'A call to "{call.name}" requires {len(call_inputs)} items, but {len(quantum_registers)} were given'
            )

        for input_name, quantum_register in zip(call_inputs, quantum_registers):
            quantum_register.consume()
            quantum_register.wire.connect_wire_end(end_call=call, input_name=input_name)

    def _connect_named_in_wires(
        self, call: function_call.FunctionCall, in_wires: Dict[str, QregOrWire]
    ) -> None:
        self._verify_legal_wires(
            [
                in_wire.wire if isinstance(in_wire, QuantumRegister) else in_wire
                for in_wire in in_wires.values()
            ]
        )

        for input_name, in_wire in in_wires.items():
            if isinstance(in_wire, QuantumRegister):
                in_wire.consume()
                in_wire = in_wire.wire

            in_wire.connect_wire_end(end_call=call, input_name=input_name)

    def _connect_out_wires(
        self,
        call: function_call.FunctionCall,
        out_wires: SupportedIOUnion,
    ) -> Dict[str, Wire]:
        if isinstance(out_wires, dict):
            wire_dict = self._connect_named_out_wires(call=call, out_wires=out_wires)
        elif isinstance(out_wires, QuantumRegister):
            wire_dict = self._connect_unnamed_out_quantum_registers(
                call=call, quantum_registers=[out_wires]
            )
        elif isinstance(out_wires, collections.abc.Collection):
            if not all(isinstance(i, QuantumRegister) for i in out_wires):
                raise ClassiqWiringError(
                    "When supplying and iterable, all items must be instances of QReg"
                )
            wire_dict = self._connect_unnamed_out_quantum_registers(
                call=call, quantum_registers=out_wires  # type: ignore[arg-type]
            )
        else:
            raise ClassiqWiringError(
                f"Invalid out_wires type: {type(out_wires).__name__}"
            )

        self._update_generated_wires(wire_dict.values())
        return wire_dict

    def _connect_named_out_wires(
        self,
        call: function_call.FunctionCall,
        out_wires: Dict[str, QregOrWire],
    ) -> Dict[str, Wire]:
        wire_dict: Dict[str, Wire] = {}
        output_names = call.function_params.get_io_names(
            function_params.IO.Output, call.is_inverse, call.control_states
        )

        specified_outputs: List[Tuple[str, str]] = list(tuple())
        for specified_output in out_wires.keys():
            match: Optional[Match] = re.fullmatch(
                function_call.IO_REGEX, specified_output
            )
            if match is None:
                raise ClassiqWiringError(
                    f"Output ({specified_output}) is not a valid expression"
                )
            name = match.groupdict().get(function_call.NAME)
            slicing = match.groupdict().get(function_call.SLICING)
            if name is None or name not in output_names:
                raise ClassiqWiringError(
                    f"Output name ({name}) does not belong to this function call"
                )
            if (
                slicing is not None
                and re.fullmatch(function_call.LEGAL_SLICING, slicing) is None
            ):
                raise ClassiqWiringError(
                    f"Slicing / indexing expression ({slicing}) is illegal"
                )

            specified_outputs.append(
                (name, f"[{slicing}]" if slicing is not None else "")
            )

        for output_name in output_names:
            connected_outputs = [
                name + slicing
                for name, slicing in specified_outputs
                if output_name == name
            ]

            if not connected_outputs:
                wire_dict[output_name] = self._output_wire_type(
                    start_call=call, output_name=output_name
                )
                continue

            for specified_output in connected_outputs:
                out_wire = out_wires[specified_output]
                if isinstance(out_wire, QuantumRegister):
                    out_wire = out_wire.wire

                out_wire.connect_wire_start(
                    start_call=call, output_name=specified_output
                )
                wire_dict[specified_output] = out_wire

        return wire_dict

    def _connect_unnamed_out_quantum_registers(
        self,
        call: function_call.FunctionCall,
        quantum_registers: Collection[QuantumRegister],
    ) -> Dict[str, Wire]:
        wire_dict: Dict[str, Wire] = {}
        output_names = call.function_params.get_io_names(
            function_params.IO.Output, call.is_inverse, call.control_states
        )

        for quantum_register, output_name in zip(quantum_registers, output_names):
            quantum_register.wire.connect_wire_start(
                start_call=call, output_name=output_name
            )
            wire_dict[output_name] = quantum_register.wire

        return wire_dict

    def __getattr__(self, item):
        is_builtin_function_name = any(
            item == func.__name__
            for func in function_param_list.function_param_library.param_list
        )

        if is_builtin_function_name:
            return functools.partial(self._function_call_handler, item)

        is_user_function_name = (
            self._function_library is not None
            and item in self._function_library.function_names
        )

        if is_user_function_name:
            return functools.partial(self.apply, item)

        if (
            self._function_library is not None
            and item in self._function_library.function_factory_names
        ):
            return functools.partial(
                self._function_library.get_function_factory(item),
                add_method=functools.partial(
                    self._function_library.add_function,
                    override_existing_functions=True,
                ),
                apply_method=self.apply,
            )

        raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{item}'")

    def __dir__(self):
        builtin_func_name = [
            func.__name__
            for func in function_param_list.function_param_library.param_list
        ]
        user_func_names = (
            list(self._function_library.function_names)
            if self._function_library is not None
            else list()
        )
        return list(super().__dir__()) + builtin_func_name + user_func_names

    def include_library(self, library: FunctionLibrary) -> None:
        """Includes a function library.

        Args:
            library (FunctionLibrary): The function library.
        """
        if self._function_library is not None:
            raise ClassiqValueError("Another function library is already included.")

        self._function_library = library

    @property
    @abc.abstractmethod
    def _logic_flow(self) -> List[function_call.FunctionCall]:
        pass

    @property
    @abc.abstractmethod
    def _output_wire_type(self) -> Type[Wire]:
        pass
