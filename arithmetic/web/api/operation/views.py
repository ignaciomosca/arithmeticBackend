from fastapi import APIRouter
from starlette import status

from arithmetic.services.operation_service import perform_operation
from arithmetic.services.security_service import user_dependency
from arithmetic.web.api.operation.schema import OperationBase

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def new_operation(user: user_dependency, new_operation: OperationBase) -> str:
    """
    Create and record a new operation.

    :param operation_dao: DAO for operation models.
    :return: list of operation objects from database.
    """
    # store operation
    # store relationship
    return await perform_operation(
        user.balance,
        new_operation.type,
        new_operation.first_term,
        new_operation.second_term,
    )
