from __future__ import annotations

from collections.abc import Sequence
from enum import Enum
from numbers import Number
from typing import Any, Dict, Optional, Tuple, Union

import numpy as np
import pydantic
from numpy.typing import ArrayLike
from pydantic import BaseModel

from classiq.interface.generator.function_params import FunctionParams
from classiq.interface.generator.preferences.optimization import (
    StatePrepOptimizationMethod,
)
from classiq.interface.generator.range_types import NonNegativeFloatRange, Range
from classiq.interface.generator.validations.validator_functions import (
    validate_probabilities,
)
from classiq.interface.helpers.custom_pydantic_types import PydanticProbabilityFloat


class Metrics(str, Enum):
    KL = "KL"
    L2 = "L2"
    L1 = "L1"
    MAX_PROBABILITY = "MAX_PROBABILITY"
    LOSS_OF_FIDELITY = "LOSS_OF_FIDELITY"

    @classmethod
    def from_sp_optimization_method(
        cls, sp_opt_method: StatePrepOptimizationMethod
    ) -> Metrics:
        try:
            return Metrics(sp_opt_method.value)
        except ValueError:
            raise ValueError(f"Failed to convert {sp_opt_method} to an error metric")


class PMF(BaseModel):
    pmf: Tuple[PydanticProbabilityFloat, ...]

    _validate_amplitudes = pydantic.validator("pmf", allow_reuse=True)(
        validate_probabilities
    )


class GaussianMoments(BaseModel):
    mu: float
    sigma: pydantic.PositiveFloat


class GaussianMixture(BaseModel):
    gaussian_moment_list: Tuple[GaussianMoments, ...]


class HardwareConstraints(BaseModel):
    # this will be moved to model preferences
    # it will be a dictionary of gates and their corresponding errors
    two_qubit_gate_error: Optional[PydanticProbabilityFloat]


PossibleProbabilities = Union[PMF, GaussianMixture]
PydanticObjectNonNegativeFloatRange = Dict[str, Any]

FlexibleNonNegativeFloatRange = Optional[
    Union[Number, PydanticObjectNonNegativeFloatRange, ArrayLike, NonNegativeFloatRange]
]
FlexiblePossibleProbabilities = Union[PossibleProbabilities, ArrayLike, dict]


class StatePreparation(FunctionParams):
    def __init__(
        self,
        depth_range: FlexibleNonNegativeFloatRange = None,
        cnot_count_range: FlexibleNonNegativeFloatRange = None,
        **kwargs,
    ):
        super().__init__(
            depth_range=self._initialize_flexible_non_negative_float_range(depth_range),
            cnot_count_range=self._initialize_flexible_non_negative_float_range(
                cnot_count_range
            ),
            **kwargs,
        )

    probabilities: Union[PMF, GaussianMixture]
    depth_range: NonNegativeFloatRange = NonNegativeFloatRange(
        lower_bound=0, upper_bound=1e100
    )
    cnot_count_range: NonNegativeFloatRange = NonNegativeFloatRange(
        lower_bound=0, upper_bound=1e100
    )
    error_metric: Dict[Metrics, NonNegativeFloatRange] = pydantic.Field(
        default_factory=lambda: {
            Metrics.KL: NonNegativeFloatRange(lower_bound=0, upper_bound=1e100)
        }
    )
    optimization_method: StatePrepOptimizationMethod = StatePrepOptimizationMethod.KL
    # This will be fixed by the validator.
    # See https://github.com/samuelcolvin/pydantic/issues/259#issuecomment-420341797
    num_qubits: int = None  # type: ignore[assignment]
    is_uniform_start: bool = True
    hardware_constraints: HardwareConstraints = pydantic.Field(
        default_factory=HardwareConstraints
    )

    @pydantic.validator("probabilities", always=True, pre=True)
    def _initialize_probabilities(
        cls,
        probabilities: FlexiblePossibleProbabilities,
    ) -> Union[PMF, GaussianMixture, dict]:
        if isinstance(probabilities, PossibleProbabilities.__args__):  # type: ignore[attr-defined]
            return probabilities
        if isinstance(probabilities, dict):  # a pydantic object
            return probabilities
        probabilities = np.array(probabilities).squeeze()
        if probabilities.ndim == 1:
            return PMF(pmf=probabilities.tolist())

        raise ValueError("Invalid probabilities was given")

    @pydantic.validator("error_metric", always=True, pre=True)
    def use_fidelity_with_hw_constraints(cls, error_metric, values):
        if values.get("hardware_constraints") is None:
            return error_metric
        error_metrics = {
            error_metric
            for error_metric in error_metric.keys()
            if error_metric is not Metrics.LOSS_OF_FIDELITY
        }
        if error_metrics:
            raise ValueError(
                "Enabling hardware constraints requires the use of only the loss of fidelity as an error metric"
            )

    @pydantic.validator("num_qubits", always=True, pre=True)
    def validate_num_qubits(cls, num_qubits, values):
        assert isinstance(num_qubits, int) or num_qubits is None
        probabilities: Optional[Union[PMF, GaussianMixture]] = values.get(
            "probabilities"
        )
        if probabilities is None:
            raise ValueError("Can't validate num_qubits without valid probabilities")
        if isinstance(probabilities, GaussianMixture):
            if num_qubits is None:
                raise ValueError("num_qubits must be set when using gaussian mixture")
            return num_qubits
        num_state_qubits = len(probabilities.pmf).bit_length() - 1
        if num_qubits is None:
            num_qubits = max(
                2 * num_state_qubits - 2, 1
            )  # Maximum with MCMT auxiliary requirements
        if num_qubits < num_state_qubits:
            raise ValueError(
                f"Minimum of {num_state_qubits} qubits needed, got {num_qubits}"
            )
        return num_qubits

    @staticmethod
    def _initialize_flexible_non_negative_float_range(
        attribute_value: FlexibleNonNegativeFloatRange,
    ) -> NonNegativeFloatRange:
        if attribute_value is None:
            return NonNegativeFloatRange(lower_bound=0, upper_bound=1e100)
        elif isinstance(attribute_value, Number):
            return NonNegativeFloatRange(lower_bound=0, upper_bound=attribute_value)
        # This should be `isinstance(obj, NonNegativeFloatRange)`, but mypy...
        elif isinstance(attribute_value, Range):
            return attribute_value
        elif isinstance(attribute_value, dict):  # a pydantic object
            return attribute_value  # type: ignore[return-value]
        elif isinstance(attribute_value, Sequence):
            if len(attribute_value) == 1:
                return NonNegativeFloatRange(
                    lower_bound=0, upper_bound=attribute_value[0]
                )
            elif len(attribute_value) == 2:
                return NonNegativeFloatRange(
                    lower_bound=attribute_value[0], upper_bound=attribute_value[1]
                )
        raise ValueError("Invalid NonNegativeFloatRange was given")
