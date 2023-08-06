from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union

import pydantic
from pydantic import BaseModel

from classiq.interface.backend.ionq import ionq_quantum_program
from classiq.interface.backend.pydantic_backend import PydanticArgumentNameType
from classiq.interface.executor.quantum_instruction_set import QuantumInstructionSet

Arguments = Dict[PydanticArgumentNameType, float]
CodeType = Union[str, ionq_quantum_program.IonqQuantumCircuit]


class QuantumProgram(BaseModel):
    syntax: QuantumInstructionSet = pydantic.Field(
        default=QuantumInstructionSet.QASM, description="The syntax of the program."
    )
    code: CodeType = pydantic.Field(
        ..., description="The textual representation of the program"
    )
    arguments: Optional[Arguments] = pydantic.Field(
        default=None,
        description="The parameters dictionary for a parametrized quantum program. "
        "Relevant for Q# programs only.",
    )
    output_qubits_map: Dict[str, Tuple[int, ...]] = pydantic.Field(
        default_factory=dict,
        description="The map of outputs to their qubits in the circuit.",
    )

    @pydantic.validator("code")
    def load_quantum_program(cls, code: CodeType, values: Dict[str, Any]) -> CodeType:
        if not isinstance(code, str):
            return code

        syntax = values.get("syntax")
        if syntax == QuantumInstructionSet.IONQ:
            return ionq_quantum_program.IonqQuantumCircuit.from_string(code)
        return code

    @pydantic.validator("arguments")
    def validate_arguments(cls, arguments: Optional[Arguments], values: Dict[str, Any]):
        if arguments and values.get("syntax") not in (
            QuantumInstructionSet.QSHARP,
            QuantumInstructionSet.QASM,
        ):
            raise ValueError("Only QASM or Q# programs support arguments")
        return arguments

    @staticmethod
    def from_file(
        file_path: Union[str, Path],
        syntax: Optional[Union[str, QuantumInstructionSet]] = None,
        arguments: Optional[Arguments] = None,
    ) -> QuantumProgram:
        path = Path(file_path)
        code = path.read_text()
        if syntax is None:
            syntax = path.suffix.lstrip(".")
        return QuantumProgram(syntax=syntax, code=code, arguments=arguments)
