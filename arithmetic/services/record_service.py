from fastapi import Depends

from arithmetic.db.dao.record_dao import RecordDAO
from arithmetic.db.dao.user_dao import UserDAO
from arithmetic.db.models.record_model import RecordModel


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
        operation_response: str,
    ) -> None:
        """Call the DAO to save a record."""
        record = RecordModel(
            user_id=user_id,
            operation_id=operation_id,
            amount=amount,
            user_balance=user_balance,
            operation_response=operation_response,
        )
        await self.record_dao.create_record(record)
        await self.user_dao.update_user_balance(user_id, user_balance)
