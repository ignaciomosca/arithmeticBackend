from typing import List

from fastapi import Depends

from arithmetic.db.dao.record_dao import RecordDAO
from arithmetic.db.dao.user_dao import UserDAO
from arithmetic.db.models.record_model import RecordModel
from arithmetic.web.api.operation.schema import RecordDTO


class RecordService:
    """Service class to interact with the records DAO."""

    def __init__(
        self,
        record_dao: RecordDAO = Depends(),
        user_dao: UserDAO = Depends(),
    ) -> None:
        self.record_dao = record_dao
        self.user_dao = user_dao

    async def create_record(
        self,
        user_id: int,
        operation_id: int,
        amount: int,
        user_balance: int,
        operation_text: str,
        operation_response: str,
    ) -> None:
        """Call the DAO to save a record."""
        record = RecordModel(
            user_id=user_id,
            operation_id=operation_id,
            amount=amount,
            user_balance=user_balance,
            operation_response=operation_response,
            operation_text=operation_text,
        )
        await self.record_dao.create_record(record)
        await self.user_dao.update_user_balance(user_id, user_balance)

    async def get_records(
        self,
        user_id: int,
        limit: int,
        offset: int,
    ) -> List[RecordDTO]:
        """Call the DAO to fetch the records."""
        records = await self.record_dao.get_all_records(user_id, limit, offset)
        return self.__convert_records_to_dtos(records)

    async def delete_record(self, record_id: int) -> None:
        """Deletes a record."""
        await self.record_dao.delete_record(record_id)

    async def search(self, term: str, limit: int, offset: int) -> List[RecordDTO]:
        """Search a term in the records table."""
        records = await self.record_dao.search(term, limit, offset)
        return self.__convert_records_to_dtos(records)

    def __convert_records_to_dtos(self, records: List[RecordModel]) -> List[RecordDTO]:
        return [
            RecordDTO(
                id=record.id,
                user_id=record.user_id,
                amount=record.amount,
                user_balance=record.user_balance,
                operation_response=record.operation_response,
                operation_text=record.operation_text,
                date=record.date.strftime("%Y-%m-%d"),  # Format date as YYYY-MM-DD
            )
            for record in records
        ]
