from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from arithmetic.services.operation_service import OperationService
from arithmetic.services.record_service import RecordService
from arithmetic.services.security_service import user_dependency
from arithmetic.services.user_service import UserService
from arithmetic.web.api.operation.schema import OperationBase, RecordDTO

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def new_operation(
    new_operation: OperationBase,
    validated_user: user_dependency,
    user_service: UserService = Depends(),
    operation_service: OperationService = Depends(),
    record_service: RecordService = Depends(),
) -> str:
    """
    Create and record a new operation.

    :param operation_dao: DAO for operation models.
    :return: list of operation objects from database.
    """
    operation = await operation_service.get_operation_cost(new_operation.type)
    user = await user_service.get_user_by_id(validated_user.user_id)
    operation_response = await operation_service.perform_operation(
        user.balance,
        new_operation.type,
        new_operation.first_term,
        new_operation.second_term,
    )
    await record_service.create_record(
        user_id=user.id,
        operation_id=operation.operation_id,
        amount=operation.cost,
        user_balance=user.balance - operation.cost,
        operation_response=operation_response,
    )
    return operation_response


@router.get("/", status_code=status.HTTP_200_OK)
async def get_records(
    validated_user: user_dependency,
    limit: int = 10,
    offset: int = 0,
    user_service: UserService = Depends(),
    record_service: RecordService = Depends(),
) -> List[RecordDTO]:
    """
    Create and record a new operation.

    :param operation_dao: DAO for operation models.
    :return: list of operation objects from database.
    """
    user = await user_service.get_user_by_id(validated_user.user_id)
    return await record_service.get_records(
        user_id=user.id,
        limit=limit,
        offset=offset,
    )


@router.delete("/{record_id}", status_code=status.HTTP_200_OK)
async def delete_record(
    _validated_user: user_dependency,
    record_id: int,
    record_service: RecordService = Depends(),
) -> None:
    """
    Create and record a new operation.

    :param operation_dao: DAO for operation models.
    :return: list of operation objects from database.
    """
    return await record_service.delete_record(record_id)
