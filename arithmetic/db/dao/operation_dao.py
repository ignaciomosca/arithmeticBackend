from typing import List

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from arithmetic.db.dependencies import get_db_session
from arithmetic.db.models.operation_model import OperationModel


class OperationDAO:
    """Class for accessing operations table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:
        self.session = session

    async def add_new_operation(self, operation_type: str, cost: int) -> None:
        """
        Add a new operation.

        :param operation_type: type of the operation.
        :param cost: cost of the operation.
        """
        new_operation = OperationModel(operation_type=operation_type, cost=cost)
        self.session.add(new_operation)

    async def get_all_operations(self) -> List[OperationModel]:
        """
        Get all operations.

        :return: oeprations models.
        """
        query = select(OperationModel)
        rows = await self.session.execute(query)
        return list(rows.scalars().fetchall())

    async def get_operation(self, type: str) -> OperationModel:
        """
        Get a single operation model by its type.

        :param type: type of the operation.
        :return: OperationModel instance if found, None otherwise.
        """
        try:
            query = select(OperationModel).where(
                OperationModel.operation_type == type,
            )
            result = await self.session.execute(query)
            return result.scalar_one()
        except NoResultFound as err:
            raise Exception(f"Invalid Type {type}") from err
        except Exception as e:
            raise e
