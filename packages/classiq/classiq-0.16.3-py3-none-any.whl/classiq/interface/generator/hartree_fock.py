from typing import Union

import pydantic
from typing_extensions import Literal

from classiq.interface.chemistry.ground_state_problem import (
    CHEMISTRY_PROBLEMS,
    CHEMISTRY_PROBLEMS_TYPE,
)
from classiq.interface.generator import function_params


class HartreeFock(function_params.FunctionParams):
    gs_problem: Union[CHEMISTRY_PROBLEMS_TYPE, Literal["ground_state_problem"]]
    _input_names = pydantic.PrivateAttr(default=[function_params.DEFAULT_INPUT_NAME])
    _output_names = pydantic.PrivateAttr(default=[function_params.DEFAULT_OUTPUT_NAME])

    @pydantic.validator("gs_problem")
    def validate_gs_problem(cls, gs_problem):
        if not isinstance(gs_problem, CHEMISTRY_PROBLEMS):
            raise ValueError(
                f"ground state problem must be of type {CHEMISTRY_PROBLEMS}"
            )
        return gs_problem
