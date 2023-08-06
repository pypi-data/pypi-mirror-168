import re
from collections.abc import Collection
from operator import itemgetter
from typing import Dict, Tuple, Union

from torch import Tensor

from classiq.exceptions import ClassiqValueError

QASM3_TYPE = str
QASM3_ARGUMENTS = Dict[str, float]
QASM3_ARGUMENTS_TENSOR = Dict[str, Tensor]

_QASM3_INTRO = re.compile('OPENQASM\\s+3(\\.\\d)?;\ninclude\\s+"stdgates\\.inc";\n')
# _QASM3_PARAMETER = re.compile("input\\s+(float|angle)\\[\\d+\\]\\s+(.*?)\\s*;")
_QASM3_PARAMETER_INPUT = re.compile(
    "input\\s+(float|angle)\\[\\d+\\]\\s+(i(nput)?_(.*?))\\s*;"
)
_QASM3_PARAMETER_WEIGHT = re.compile(
    "input\\s+(float|angle)\\[\\d+\\]\\s+(w(eight)?_(.*?))\\s*;"
)
_QASM3_PARAMETER_GETTER = itemgetter(1)
_QASM3_MEASUREMENTS = re.compile("\\s*\\=\\s*measure\\s+(\\w+\\[\\d+\\])")

_number_types = (int, float)
_single_item_shape = Tensor([1])[0].shape


class QASM3Parser:
    def __init__(self, qcode: str):
        self._process_qcode(qcode)

    def _process_qcode(self, qcode: str):
        # validate qcode
        if not _QASM3_INTRO.match(qcode):
            raise ClassiqValueError(
                "Invalid qcode given. Please supply a valid OpenQASM3 string"
            )
        # store qcode
        self.qcode = qcode

        self._extract_parameters()
        self._extract_measurements()

    def _extract_parameters(self) -> None:
        self._qcode_parameters_inputs: Tuple[str, ...] = tuple(
            map(_QASM3_PARAMETER_GETTER, _QASM3_PARAMETER_INPUT.findall(self.qcode))
        )
        self._qcode_parameters_weights: Tuple[str, ...] = tuple(
            map(_QASM3_PARAMETER_GETTER, _QASM3_PARAMETER_WEIGHT.findall(self.qcode))
        )

    def _extract_measurements(self) -> None:
        self._qcode_measured_qubits: Tuple[str, ...] = tuple(
            set(_QASM3_MEASUREMENTS.findall(self.qcode))
        )

    def _map_parameters(
        self, inputs: Tensor, weights: Tensor
    ) -> QASM3_ARGUMENTS_TENSOR:
        if not isinstance(inputs, Collection):
            raise ClassiqValueError(
                f'Invalid inputs type. "Tensor" expected. Got {inputs.__class__.__name__}'
            )
        for i in inputs:
            if (
                (not isinstance(i, Tensor))
                or (i.shape != _single_item_shape)
                or (not isinstance(i.item(), _number_types))
            ):
                raise ClassiqValueError(
                    f'Invalid inputs type. "Tensor" of "float" expected. Got {inputs[0].__class__.__name__}'
                )
        if len(inputs) != len(self._qcode_parameters_inputs):
            raise ClassiqValueError(
                f"Length mismatch. {len(inputs)} inputs were given, were only {len(self._qcode_parameters_inputs)} are expected"
            )

        if not isinstance(weights, Collection):
            raise ClassiqValueError(
                f'Invalid weights type. "Tensor" expected. Got {weights.__class__.__name__}'
            )
        for i in weights:
            if (
                (not isinstance(i, Tensor))
                or (i.shape != _single_item_shape)
                or (not isinstance(i.item(), _number_types))
            ):
                raise ClassiqValueError(
                    f'Invalid inputs type. "Tensor" of "float" expected. Got {inputs[0].__class__.__name__}'
                )
        if len(weights) != len(self._qcode_parameters_weights):
            raise ClassiqValueError(
                f"Length mismatch. {len(weights)} weights were given, were only {len(self._qcode_parameters_weights)} are expected"
            )

        return {
            **dict(zip(self._qcode_parameters_inputs, inputs)),
            **dict(zip(self._qcode_parameters_weights, weights)),
        }


QASM3PARSER_LIKE = Union[QASM3_TYPE, QASM3Parser]


def to_qasm3_parser(obj: QASM3PARSER_LIKE) -> QASM3Parser:
    if isinstance(obj, QASM3_TYPE):
        return QASM3Parser(obj)
    elif isinstance(obj, QASM3Parser):
        return obj
    else:
        raise ClassiqValueError("Invalid qasm3_parser_like object")
