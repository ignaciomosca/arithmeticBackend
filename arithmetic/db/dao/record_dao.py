from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from arithmetic.db.dependencies import get_db_session
from arithmetic.db.models.record_model import RecordModel


class RecordDAO:
    """Class for accessing records table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:
        self.session = session

    async def create_record(self, record: RecordModel) -> None:
        """
        Add single record to session.

        :param record: record to be saved.
        """
        self.session.add(record)
