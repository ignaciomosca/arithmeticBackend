from math import sqrt
from typing import Optional, cast

from fastapi import Depends

from arithmetic.db.dao.operation_dao import OperationDAO
from arithmetic.services.random_service import generate_random_string
from arithmetic.web.api.operation.schema import OperationDTO, OperationEnum


class OperationService:
    """Service class to implement operation functionalities."""

    def __init__(self, operation_dao: OperationDAO = Depends()) -> None:
        self.operation_dao = operation_dao

    async def get_operation_cost(self, operation_type: OperationEnum) -> OperationDTO:
        """Given an operation type return the operation id and it's cost."""
        operation_model = await self.operation_dao.get_operation(
            str(operation_type.value),
        )
        return OperationDTO(operation_id=operation_model.id, cost=operation_model.cost)

    async def perform_operation(
        self,
        balance: int,
        type: OperationEnum,
        first_term: Optional[int],
        second_term: Optional[int],
    ) -> str:
        """Perform operation based on the parameters provided by the user."""
        if balance <= 0:
            raise Exception("Not enough balance.")
        # I ignore types since parameters were already validated by using
        # a pydantic validator
        match type:
            case OperationEnum.ADDITION:
                return str(first_term + second_term)  # type: ignore[operator]
            case OperationEnum.SUBTRACTION:
                return str(first_term - second_term)  # type: ignore[operator]
            case OperationEnum.MULTIPLICATION:
                return str(first_term * second_term)  # type: ignore[operator]
            case OperationEnum.DIVISION:
                return str(first_term / second_term)  # type: ignore[operator]
            case OperationEnum.SQUARE:
                return str(sqrt(float(cast(int, first_term))))  # type: ignore[operator]
            case OperationEnum.RANDOM:
                return await generate_random_string()

    def get_operation_text(
        self,
        type: OperationEnum,
        first_term: Optional[int],
        second_term: Optional[int],
    ) -> str:
        """Get the operation text based on the type and the terms."""
        match type:
            case OperationEnum.ADDITION:
                return f"{first_term}+{second_term}"
            case OperationEnum.SUBTRACTION:
                return f"{first_term}-{second_term}"
            case OperationEnum.MULTIPLICATION:
                return f"{first_term}*{second_term}"
            case OperationEnum.DIVISION:
                return f"{first_term}/{second_term}"
            case OperationEnum.SQUARE:
                return f"sqrt({first_term})"
            case OperationEnum.RANDOM:
                return "random"
