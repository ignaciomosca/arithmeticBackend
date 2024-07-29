from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from arithmetic.db.dependencies import get_db_session
from arithmetic.db.models.operation_model import OperationEnum, OperationModel


class OperationDAO:
    """Class for accessing operations table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:
        self.session = session

    async def get_operation(self, type: OperationEnum) -> OperationModel:
        """
        Get a single operation model by its type.

        :param type: type of the operation.
        :return: OperationModel instance if found, None otherwise.
        """
        try:
            query = select(OperationModel).where(OperationModel.type == "addition")
            result = await self.session.execute(query)
            return result.scalar_one()
        except NoResultFound as err:
            raise Exception(f"Invalid Type {type.name} {type.value}") from err
        except Exception as e:
            raise e
