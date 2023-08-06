from typing import Any, Dict

import pydantic

from classiq.interface.generator.automatic_rename import automatic_rename
from classiq.interface.generator.exponentiation import (
    Exponentiation,
    ExponentiationOptimization,
)
from classiq.interface.generator.function_param_list_without_self_reference import (
    function_param_library_without_self_reference,
)
from classiq.interface.generator.function_params import (
    IO,
    FunctionParams,
    IOName,
    parse_function_params_values,
)

PHASE_ESTIMATION_DEFAULT_OUTPUT_NAME = "PHASE_ESTIMATION"


class PhaseEstimation(FunctionParams):
    """
    Quantum phase estimation of a given unitary function.
    """

    size: pydantic.NonNegativeInt = pydantic.Field(
        description="The number of qubits storing the estimated phase."
    )
    unitary: str = pydantic.Field(
        default="",
        description="The unitary function for phase estimation.",
    )
    unitary_params: FunctionParams = pydantic.Field(
        description="The unitary function parameters."
    )

    _output_name: IOName = pydantic.PrivateAttr(
        default=PHASE_ESTIMATION_DEFAULT_OUTPUT_NAME
    )

    @property
    def output_name(self) -> str:
        return self._output_name

    def _create_io_names(self) -> None:
        self._input_names = self.unitary_params.get_io_names(
            io=IO.Input,
        )
        self._output_names = self.unitary_params.get_io_names(
            io=IO.Output,
        )
        self._update_output_name()
        self._output_names.append(self._output_name)

    def _update_output_name(self) -> None:
        self._output_name = automatic_rename(
            name=self._output_name, names=self._output_names
        )

    @pydantic.root_validator(pre=True)
    def parse_function_params(cls, values: Dict[str, Any]):
        parse_function_params_values(
            values=values,
            params_key="unitary_params",
            discriminator_key="unitary",
            param_classes=function_param_library_without_self_reference.param_list,
        )
        return values

    @pydantic.validator("unitary_params")
    def validate_unitary_params(cls, unitary_params: FunctionParams):
        if not unitary_params.is_powerable():
            raise ValueError(
                f"Phase estimation of {unitary_params.discriminator()} is currently not supported."
            )
        if isinstance(unitary_params, Exponentiation):
            if unitary_params.constraints.max_depth is not None:
                raise ValueError(
                    "max_depth is currently not supported for phase estimation of exponentiation."
                )
            if (
                unitary_params.optimization
                is not ExponentiationOptimization.MINIMIZE_DEPTH
            ):
                raise ValueError(
                    "Only MINIMIZE_DEPTH is currently supported for phase estimation of exponentiation."
                )
        return unitary_params
