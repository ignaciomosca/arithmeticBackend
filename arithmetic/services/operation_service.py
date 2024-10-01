from math import sqrt
from typing import Optional, cast

from fastapi import Depends

from arithmetic.db.dao.operation_dao import OperationDAO
from arithmetic.services.random_service import generate_random_string
from arithmetic.services.record_service import RecordService
from arithmetic.services.user_service import UserService
from arithmetic.web.api.operation.schema import OperationEnum


class OperationService:
    """Service class to implement operation functionalities."""

    def __init__(
        self,
        operation_dao: OperationDAO = Depends(),
        user_service: UserService = Depends(),
        record_service: RecordService = Depends(),
    ) -> None:
        self.operation_dao = operation_dao
        self.user_service = user_service
        self.record_service = record_service

    async def perform_operation(
        self,
        user_id: int,
        type: OperationEnum,
        first_term: Optional[int],
        second_term: Optional[int],
    ) -> str:
        """Perform the operation."""
        user = await self.user_service.get_user_by_id(user_id)
        operation = await self.operation_dao.get_operation(str(type.value))
        if user.balance < operation.cost:
            raise Exception("Not enough balance.")
        # I ignore types since parameters were already validated by using
        # a pydantic validator
        result = await self.calculate_result(type, first_term, second_term)
        await self.record_service.create_record(
            user_id=user.id,
            operation_id=operation.id,
            amount=operation.cost,
            user_balance=user.balance - operation.cost,
            operation_text=self.get_operation_text(
                type,
                first_term,
                second_term,
            ),
            operation_response=result,
        )
        return result

    async def calculate_result(
        self,
        type: OperationEnum,
        first_term: Optional[int],
        second_term: Optional[int],
    ) -> str:
        """Perform operation based on the type and parameters provided by the user."""
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
