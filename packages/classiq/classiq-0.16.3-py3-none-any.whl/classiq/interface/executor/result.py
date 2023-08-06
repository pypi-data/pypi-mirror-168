from collections import defaultdict
from typing import Any, DefaultDict, Dict, List, Optional, Tuple, Union

import pydantic
from pydantic import BaseModel

from classiq.interface.helpers.versioned_model import VersionedModel

from classiq.exceptions import ClassiqError

_ILLEGAL_QUBIT_ERROR_MSG: str = "Illegal qubit index requested"
_REPEATED_QUBIT_ERROR_MSG: str = "Requested a qubit more than once"
_UNAVAILABLE_OUTPUT_ERROR_MSG: str = "Requested output doesn't exist in the circuit"

State = str
Name = str
Qubits = Tuple[int, ...]


class VaRResult(BaseModel):
    var: Optional[float] = None
    alpha: Optional[float] = None


class FinanceSimulationResults(VersionedModel):
    var_results: Optional[VaRResult] = None
    result: Optional[float] = None

    @pydantic.root_validator()
    def validate_atleast_one_field(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        is_var_results_defined = values.get("var_results") is not None
        is_result_defined = values.get("result") is not None

        if not is_var_results_defined and not is_result_defined:
            raise ValueError(
                "At least one of var_results and result should be defined."
            )

        return values


class GroverSimulationResults(VersionedModel):
    result: Dict[str, Union[float, int]]


class ExecutionDetails(VersionedModel):
    vendor_format_result: Dict[str, Any] = pydantic.Field(
        ..., description="Result in proprietary vendor format"
    )
    counts: Dict[State, pydantic.NonNegativeInt] = pydantic.Field(
        default_factory=dict, description="Number of counts per state"
    )
    histogram: Optional[Dict[State, pydantic.NonNegativeFloat]] = pydantic.Field(
        None,
        description="Histogram of probability per state (an alternative to counts)",
    )
    output_qubits_map: Dict[Name, Qubits] = pydantic.Field(
        default_factory=dict,
        description="The map of outputs to their qubits in the circuit.",
    )

    def counts_of_qubits(self, qubits: Qubits) -> Dict[State, pydantic.NonNegativeInt]:
        if not qubits or max(qubits) >= len(list(self.counts.keys())[0]):
            raise ClassiqError(_ILLEGAL_QUBIT_ERROR_MSG)
        if len(set(qubits)) < len(qubits):
            raise ClassiqError(_REPEATED_QUBIT_ERROR_MSG)
        reduced_counts: DefaultDict[State, int] = defaultdict(int)
        for state_str, state_count in self.counts.items():
            reduced_str = "".join(state_str[qubit_index] for qubit_index in qubits)
            reduced_counts[reduced_str] += state_count
        return dict(reduced_counts)

    def counts_of_output(
        self, output_name: Name
    ) -> Dict[State, pydantic.NonNegativeInt]:
        if output_name not in self.output_qubits_map:
            raise ClassiqError(_UNAVAILABLE_OUTPUT_ERROR_MSG)
        return self.counts_of_qubits(qubits=self.output_qubits_map[output_name])

    def counts_of_multiple_outputs(
        self, output_names: Tuple[Name, ...]
    ) -> Dict[Tuple[State, ...], pydantic.NonNegativeInt]:
        if any(name not in self.output_qubits_map for name in output_names):
            raise ClassiqError(_UNAVAILABLE_OUTPUT_ERROR_MSG)

        output_regs: Tuple[Qubits, ...] = tuple(
            self.output_qubits_map[name] for name in output_names
        )
        reduced_counts: DefaultDict[Tuple[State, ...], int] = defaultdict(int)
        for state_str, state_count in self.counts.items():
            reduced_strs = tuple(
                "".join(state_str[qubit_index] for qubit_index in reg)
                for reg in output_regs
            )
            reduced_counts[reduced_strs] += state_count
        return dict(reduced_counts)


class GroverAdaptiveSearchResult(VersionedModel):
    opt_x_string: List[int] = pydantic.Field(
        ..., description="Result in proprietary vendor format"
    )
    min_value: float = pydantic.Field(
        ..., description="Result in proprietary vendor format"
    )
