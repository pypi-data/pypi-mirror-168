from __future__ import annotations

from typing import Any, Dict, Optional

import pydantic

from classiq.interface.helpers.custom_pydantic_types import PydanticFloatTuple


class RegisterUserInput(pydantic.BaseModel):
    size: pydantic.PositiveInt
    name: str = pydantic.Field(default="")
    is_signed: bool = pydantic.Field(default=False)
    fraction_places: pydantic.NonNegativeInt = pydantic.Field(default=0)
    bounds: Optional[PydanticFloatTuple] = pydantic.Field(default=None)

    def is_boolean_register(self) -> bool:
        return (not self.is_signed) and (self.size == 1) and (self.fraction_places == 0)

    @pydantic.validator("bounds", always=True)
    def _validate_bounds(
        cls, bounds: Optional[PydanticFloatTuple], values: Dict[str, Any]
    ) -> PydanticFloatTuple:
        if bounds is not None:
            return bounds
        size = values.get("size")
        if not isinstance(size, int):
            raise ValueError("RegisterUserInput must have an integer size")
        is_signed: bool = values.get("is_signed", False)
        lb = 0 if not is_signed else -(2 ** (size - 1))
        ub = 2**size - 1 if not is_signed else 2 ** (size - 1) - 1
        fraction_factor = float(2 ** -values.get("fraction_places", 0))
        return (lb * fraction_factor, ub * fraction_factor)

    @property
    def integer_part_size(self):
        return self.size - self.fraction_places

    def to_register_user_input(self) -> RegisterUserInput:
        return RegisterUserInput(**self.dict())
