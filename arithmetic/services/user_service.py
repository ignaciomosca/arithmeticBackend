from fastapi import Depends

from arithmetic.db.dao.user_dao import UserDAO
from arithmetic.db.models.user_model import UserModel


class UserService:
    """Service class to implement user functionalities."""

    def __init__(self, user_dao: UserDAO = Depends()) -> None:
        self.user_dao = user_dao

    async def get_user_by_id(self, user_id: int) -> UserModel:
        """Given a user_id return the user model."""
        return await self.user_dao.get_user_by_id(user_id)
