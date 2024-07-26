from math import sqrt
from typing import Optional, cast

from arithmetic.services.random_service import generate_random_string
from arithmetic.web.api.operation.schema import OperationEnum


async def perform_operation(
    balance: int,
    type: OperationEnum,
    first_term: Optional[int],
    second_term: Optional[int],
) -> str:
    """Perform operation based on the parameters provided by the user."""
    if balance <= 0:
        raise Exception("Not enough balance.")
    # I ignore types since parameters were already validated by using pydantic validator
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
