from typing import List, Union

import numpy as np
import pydantic

from classiq.interface.generator import complex_type, function_params

DataNumber = Union[complex_type.Complex, float, int]
DataArray = List[List[DataNumber]]

UNITARY_GATE_INPUT: str = "TARGET_IN"
UNITARY_GATE_OUTPUT: str = "TARGET_OUT"


class UnitaryGate(function_params.FunctionParams):
    """
    Creates a circuit implementing a specified 2**n * 2**n unitary transformation.
    """

    # TODO - add support to numpy array-like (requires custom pydantic type definition)
    data: DataArray = pydantic.Field(
        description="A 2**n * 2**n (n positive integer) unitary matrix."
    )

    # TODO - decide if to include assertion on the unitarity of the matrix. It is already done in Qiskit and could be computationally expensive
    @pydantic.validator("data")
    def validate_data(cls, data):
        data_np = np.array(data, dtype=object)
        if data_np.ndim != 2:
            raise ValueError("Data must me two dimensional")
        if data_np.shape[0] != data_np.shape[1]:
            raise ValueError("Matrix must be square")
        if not np.mod(np.log2(data_np.shape[0]), 1) == 0:
            raise ValueError("Matrix dimensions must be an integer exponent of 2")
        return data

    def _create_io_names(self):
        self._input_names = [UNITARY_GATE_INPUT]
        self._output_names = [UNITARY_GATE_OUTPUT]
