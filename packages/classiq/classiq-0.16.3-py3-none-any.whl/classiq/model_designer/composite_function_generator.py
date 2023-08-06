from typing import List, Set, Type

from classiq.interface.generator.function_call import FunctionCall
from classiq.interface.generator.function_params import IOName
from classiq.interface.generator.functions import FunctionData

from classiq.model_designer import function_handler, wire


class CompositeFunctionOutputWire(wire.Wire):
    @property
    def is_ended(self) -> bool:
        return self.is_started and self._start_name in self._start_call.outputs  # type: ignore[union-attr]


class CompositeFunctionGenerator(function_handler.FunctionHandler):
    def __init__(self, function_name: str) -> None:
        super().__init__()
        self._name = function_name
        self._logic_flow_list: List[FunctionCall] = list()
        self._input_names: Set[IOName] = set()

    @property
    def _logic_flow(self) -> List[FunctionCall]:
        return self._logic_flow_list

    @property
    def _output_wire_type(self) -> Type[wire.Wire]:
        return CompositeFunctionOutputWire

    def to_function_data(self) -> FunctionData:
        inputs = {name: wire.wire_name for name, wire in self._generated_inputs.items()}
        outputs = {
            name: wire.wire_name for name, wire in self._generated_outputs.items()
        }
        return FunctionData(
            name=self._name, logic_flow=self._logic_flow, inputs=inputs, outputs=outputs
        )
