from fastapi import APIRouter
from fastapi.param_functions import Depends
from starlette import status

from arithmetic.db.dao.operation_dao import OperationDAO

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def new_operation(
    operation_dao: OperationDAO = Depends(),
) -> None:
    """
    Create and record a new operation.

    :param operation_dao: DAO for operation models.
    :return: list of operation objects from database.
    """
    # obtain user
    # store operation
    # store relationship
    await operation_dao.perform_operation()
