from typing import List

from fastapi import Depends
from sqlalchemy import func, not_, select
from sqlalchemy.ext.asyncio import AsyncSession

from arithmetic.db.dao.record_response import RecordResponse
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

    async def get_all_records(
        self,
        user_id: int,
        limit: int,
        offset: int,
    ) -> RecordResponse:
        """
        Returns all records.

        :param user_id: id of the user.
        :param limit: limit of records.
        :param offset: offset of records.
        :return: stream of records.
        """

        total_records = await self.session.execute(
            select(func.count(RecordModel.id))
            .where((RecordModel.user_id == user_id))
            .filter(not_(RecordModel.deleted)),
        )
        total_count = total_records.scalar() or 0

        records = await self.session.execute(
            select(RecordModel)
            .where((RecordModel.user_id == user_id))
            .filter(not_(RecordModel.deleted))
            .limit(limit)
            .offset(offset),
        )

        return RecordResponse(
            records=list(records.scalars().fetchall()),
            total_count=total_count,
        )

    async def delete_record(self, record_id: int) -> None:
        """
        Soft deletes a record by setting its deleted_at field to the current timestamp.

        :param record_id: id of the record.
        """
        record = await self.session.get(RecordModel, record_id)
        if record:
            record.deleted = True
            await self.session.commit()

    async def search(
        self,
        term: str,
        limit: int,
        offset: int,
    ) -> List[RecordModel]:
        """
        Search records by term.

        :param term: search term.
        :param limit: limit of records.
        :param offset: offset of records.
        :return: stream of records.
        """
        records = await self.session.execute(
            select(RecordModel)
            .where(RecordModel.operation_text.like(f"%{term}%"))
            .filter(not_(RecordModel.deleted))
            .limit(limit)
            .offset(offset),
        )

        return list(records.scalars().fetchall())
