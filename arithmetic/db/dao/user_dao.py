from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from arithmetic.db.dependencies import get_db_session
from arithmetic.db.models.user_model import UserModel


class UserDAO:
    """Class for accessing users table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:
        self.session = session

    async def create_user(self, username: str, password: str) -> None:
        """
        Add single user to session.

        :param name: name of a user.
        """
        self.session.add(UserModel(username=username, password=password))
