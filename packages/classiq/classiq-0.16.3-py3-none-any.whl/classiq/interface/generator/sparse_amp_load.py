from typing import List

import pydantic

from classiq.interface.generator import function_params
from classiq.interface.generator.complex_type import Complex
from classiq.interface.generator.validations.validator_functions import (
    validate_amplitudes,
)

OUTPUT_STATE = "OUTPUT_STATE"
EXTRA_QUBITS = "EXTRA_QUBITS"


class SparseAmpLoad(function_params.FunctionParams):
    """
    loads a sparse amplitudes vector
    """

    num_qubits: pydantic.PositiveInt = pydantic.Field(
        description="The number of qubits in the circuit."
    )
    amplitudes: List[Complex] = pydantic.Field(description="amplitudes vector to load")

    _validate_amplitudes = pydantic.validator("amplitudes", allow_reuse=True)(
        validate_amplitudes
    )

    @property
    def state_qubits_num(self) -> int:
        return len(self.amplitudes).bit_length() - 1

    @property
    def has_extra_qubits(self) -> bool:
        return self.num_qubits > self.state_qubits_num

    def _create_io_names(self) -> None:
        self._input_names = list()
        self._output_names = [OUTPUT_STATE]
        if self.has_extra_qubits:
            self._output_names.append(EXTRA_QUBITS)
