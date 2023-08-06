from typing import List

import pydantic


class FermionicOperator(pydantic.BaseModel):
    """
    Specification of a Fermionic operator.
    Input:
    List of ladder operators, each ladder operator is described by a tuple of its
    index and a character indicating if it's a creation ('+') or annihilation operator ('-').
    """

    op_list: List = pydantic.Field(
        description="A list of tuples each containing an index and a character; for example [('+', 0), ('-', 1)].",
    )

    @pydantic.validator("op_list")
    def validate_op_list(cls, op_list):
        for op in op_list:
            if len(op) != 2:
                raise ValueError(
                    "Ladder operator tuple should be of length two; for example (1, '+')."
                )
            if op[0] not in ("+", "-"):
                raise ValueError(
                    "The first term in a ladder operator tuple indicates if its a raising ('+')"
                    " or lowering ('-') operator. Allowed input is: '+' or '-'."
                )
            if not isinstance(op[1], int):
                raise ValueError(
                    "The second term in a ladder operator tuple indicates its index and should be of type int"
                )
        return op_list

    def __mul__(self, coeff):
        if isinstance(coeff, float):
            return SummedFermionicOperator(
                op_list=[(self, coeff)]
            )  # a list of length 1
        else:
            raise ValueError(
                "The coefficient multiplying Fermionic Operator should be of type float"
            )

    __rmul__ = __mul__

    def __add__(self, other):
        if isinstance(other, SummedFermionicOperator):
            return SummedFermionicOperator(op_list=[(self, 1.0)] + other.op_list)
        elif isinstance(other, FermionicOperator):
            return SummedFermionicOperator(op_list=[(self, 1.0)] + [(other, 1.0)])
        else:
            raise ValueError(
                "FermionicOperator can be summed together only with type FermionicOperator or SummedFermionicOperator"
            )


class SummedFermionicOperator(pydantic.BaseModel):
    """
    Specification of a summed Fermionic operator.
    Input:
    List of fermionic operators tuples, The first term in the tuple is the FermionicOperator and the second term is its coefficient.
    For example:
    op1 = FermionicOperator(op_list=[(0, '+'), (1, '-')])
    op2 = FermionicOperator(op_list=[(0, '-'), (1, '-')])
    summed_operator = SummedFermionicOperator(op_list=[(op1, 0.2), (op2, 6.7)])
    """

    op_list: list = pydantic.Field(
        description="A list of tuples each containing a FermionicOperator and a coefficient.",
    )

    @pydantic.validator("op_list")
    def validate_op_list(cls, op_list):
        for op in op_list:
            if len(op) != 2:
                raise ValueError("operator tuple should be of length two.")
            if type(op[0]) != FermionicOperator:
                raise ValueError(
                    "The first term in the operator tuple should be an instance of the FermionicOperator class"
                )
            if type(op[1]) != float:
                raise ValueError(
                    "The second term in the operator tuple indicates its coefficient and should be of type float"
                )
        return op_list

    def __add__(self, other):
        if isinstance(other, SummedFermionicOperator):
            return SummedFermionicOperator(op_list=self.op_list + other.op_list)
        elif isinstance(other, FermionicOperator):
            return SummedFermionicOperator(op_list=self.op_list + [(other, 1.0)])
        else:
            raise ValueError(
                "FermionicOperator can be summed together only with type FermionicOperator or SummedFermionicOperator"
            )
