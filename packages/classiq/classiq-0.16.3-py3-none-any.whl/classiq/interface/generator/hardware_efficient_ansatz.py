import enum
import itertools
from typing import List, Optional, Union

import pydantic

from classiq.interface.generator import function_params
from classiq.interface.helpers.custom_pydantic_types import PydanticNonNegIntTuple

ConnectivityMap = List[PydanticNonNegIntTuple]


class SupportedConnectivityMaps(str, enum.Enum):
    FULL = "full"
    LINEAR = "linear"
    CIRCULAR = "circular"
    PAIRWISE = "pairwise"


ConnectivityMapType = Union[ConnectivityMap, SupportedConnectivityMaps, None]


class HardwareEfficientAnsatz(function_params.FunctionParams):
    _input_names = pydantic.PrivateAttr(default=[function_params.DEFAULT_INPUT_NAME])
    _output_names = pydantic.PrivateAttr(default=[function_params.DEFAULT_OUTPUT_NAME])

    num_qubits: Optional[pydantic.PositiveInt] = pydantic.Field(
        default=None,
        description="Number of qubits in the ansatz. If none specified - use all qubits from the connectivity map",
    )
    connectivity_map: ConnectivityMapType = pydantic.Field(
        default=None,
        description="Hardware's connectivity map, in the form [ [x0, x1], [x1, x2],...]. "
        "If none specified - use connectivity map from the model hardware settings. "
        "If none specified as well, all qubit pairs will be connected.",
    )
    reps: pydantic.PositiveInt = pydantic.Field(
        default=1, description="Number of layers in the Ansatz"
    )

    one_qubit_gates: Union[str, List[str]] = pydantic.Field(
        default=["x", "ry"],
        description='List of gates for the one qubit gates layer, e.g. ["x", "ry"]',
    )
    two_qubit_gates: Union[str, List[str]] = pydantic.Field(
        default=["cx"],
        description='List of gates for the two qubit gates entangling layer, e.g. ["cx", "cry"]',
    )

    @pydantic.validator("connectivity_map")
    def validate_max_index(cls, connectivity_map, values):
        num_qubits = values.get("num_qubits")

        if num_qubits is None and isinstance(
            connectivity_map, (SupportedConnectivityMaps, str)
        ):
            raise ValueError(
                "When passing `connectivity_map` as `str`/`enum`, `num_qubits` must be provided."
            )
        if num_qubits is None or connectivity_map is None:
            return connectivity_map
        invalid_qubits = {
            qubit
            for qubit in itertools.chain.from_iterable(connectivity_map)
            if qubit >= num_qubits
        }
        if invalid_qubits:
            raise ValueError(
                f"Invalid qubits: {invalid_qubits} "
                f"out of range specified by num_qubits: [0, {num_qubits - 1}]"
            )
        return connectivity_map
