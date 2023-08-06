from enum import Enum

from pydantic import BaseModel

from classiq.interface.helpers.custom_pydantic_types import (
    PydanticNonOneProbabilityFloat,
)


class StatePrepOptimizationMethod(str, Enum):
    KL = "KL"
    L2 = "L2"
    L1 = "L1"
    LOSS_OF_FIDELITY = "LOSS_OF_FIDELITY"
    MAX_PROBABILITY = "MAX_PROBABILITY"
    RANDOM = "RANDOM"


class OptimizationType(str, Enum):
    DEPTH = "depth"
    TWO_QUBIT_GATES = "two_qubit_gates"


class Optimization(BaseModel):
    approximation_error: PydanticNonOneProbabilityFloat = 0.0
    optimization_type: OptimizationType = OptimizationType.DEPTH
