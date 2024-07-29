from typing import List

from fastapi import Depends
from sqlalchemy import select
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

    async def get_all_records(self, limit: int, offset: int) -> List[RecordModel]:
        """
        Returns all records.

        :param limit: limit of records.
        :param offset: offset of records.
        :return: stream of records.
        """
        raw_dummies = await self.session.execute(
            select(RecordModel).limit(limit).offset(offset),
        )

        return list(raw_dummies.scalars().fetchall())
