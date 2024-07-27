from math import sqrt
from typing import Optional, cast

from fastapi import Depends

from arithmetic.db.dao.operation_dao import OperationDAO
from arithmetic.db.models.operation_model import OperationEnum as ModelOperationEnum
from arithmetic.services.random_service import generate_random_string
from arithmetic.web.api.operation.schema import OperationDTO, OperationEnum


class OperationService:
    """Service class to implement operation functionalities."""

    def __init__(self, operation_dao: OperationDAO = Depends()) -> None:
        self.operation_dao = operation_dao

    async def get_operation_cost(self, operation_type: OperationEnum) -> OperationDTO:
        """Given an operation type return the operation id and it's cost."""
        operation_model = await self.operation_dao.get_operation(
            self._to_model_operation_enum(operation_type),
        )
        return OperationDTO(operation_id=operation_model.id, cost=operation_model.cost)

    def _to_model_operation_enum(
        self,
        operation_type: OperationEnum,
    ) -> ModelOperationEnum:
        match operation_type:
            case OperationEnum.ADDITION:
                return ModelOperationEnum.ADDITION
            case OperationEnum.SUBTRACTION:
                return ModelOperationEnum.SUBTRACTION
            case OperationEnum.MULTIPLICATION:
                return ModelOperationEnum.MULTIPLICATION
            case OperationEnum.DIVISION:
                return ModelOperationEnum.DIVISION
            case OperationEnum.SQUARE:
                return ModelOperationEnum.SQUARE
            case OperationEnum.RANDOM:
                return ModelOperationEnum.RANDOM

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
