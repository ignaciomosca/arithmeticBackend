from enum import Enum
from typing import Any, List, Optional

from pydantic import BaseModel, Field, model_validator


class OperationEnum(str, Enum):
    """Pydantic model for operation types."""

    ADDITION = "addition"
    SUBTRACTION = "subtraction"
    MULTIPLICATION = "multiplication"
    DIVISION = "division"
    SQUARE = "squareRoot"
    RANDOM = "randomString"


class OperationDTO(BaseModel):
    """DTO that represents and operation id and its cost."""

    operation_id: int
    cost: int


class RecordDTO(BaseModel):
    """DTO that represents a record."""

    id: int
    user_id: int
    amount: int
    user_balance: int
    operation_response: str
    operation_text: str
    date: str


class RecordsDTO(BaseModel):
    """DTO that represents a list of records."""

    records: List[RecordDTO]
    total_count: int


class OperationBase(BaseModel):
    """Base Pydantic model for Operation."""

    type: OperationEnum
    first_term: Optional[int] = Field(None)
    second_term: Optional[int] = Field(None)

    @model_validator(mode="after")
    def check_terms(self, values: Any) -> Any:
        """Validates the inputs of the operation function."""
        type_ = self.type
        first_term = self.first_term
        second_term = self.second_term

        if type_ in {
            OperationEnum.ADDITION,
            OperationEnum.SUBTRACTION,
            OperationEnum.MULTIPLICATION,
            OperationEnum.DIVISION,
        }:
            if first_term is None or second_term is None:
                raise ValueError(
                    f"For operation type '{type_}',"
                    f"both first_term and second_term are required.",
                )
            if second_term == 0:
                raise ValueError(
                    f"For operation type '{type_}',Division by Zero error.",
                )
        elif type_ == OperationEnum.SQUARE:
            if first_term is None:
                raise ValueError(
                    f"For operation type '{type_}',first_term is required.",
                )
            if second_term is not None:
                raise ValueError(
                    f"For operation type '{type_}',"
                    f"second_term should not be provided.",
                )
            if first_term < 0:
                raise ValueError(
                    f"For operation type '{type_}',"
                    f"Square root of a negative number.",
                )
        elif type_ == OperationEnum.RANDOM and (
            first_term is not None or second_term is not None
        ):
            raise ValueError(
                f"For operation type '{type_}', no terms are required.",
            )
        return self
