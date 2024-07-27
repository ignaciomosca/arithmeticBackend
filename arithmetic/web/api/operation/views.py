from fastapi import APIRouter, Depends
from starlette import status

from arithmetic.services.operation_service import OperationService
from arithmetic.services.record_service import RecordService
from arithmetic.services.security_service import user_dependency
from arithmetic.web.api.operation.schema import OperationBase

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def new_operation(
    new_operation: OperationBase,
    user: user_dependency,
    operation_service: OperationService = Depends(),
    record_service: RecordService = Depends(),
) -> str:
    """
    Create and record a new operation.

    :param operation_dao: DAO for operation models.
    :return: list of operation objects from database.
    """
    operation = await operation_service.get_operation_cost(new_operation.type)
    operation_response = await operation_service.perform_operation(
        user.balance,
        new_operation.type,
        new_operation.first_term,
        new_operation.second_term,
    )
    await record_service.create_record(
        user_id=user.user_id,
        operation_id=operation.operation_id,
        amount=operation.cost,
        user_balance=user.balance - operation.cost,
        operation_response=operation_response,
    )
    return operation_response
