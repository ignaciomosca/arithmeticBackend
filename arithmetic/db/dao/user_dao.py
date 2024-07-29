from typing import Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from arithmetic.db.dependencies import get_db_session
from arithmetic.db.models.user_model import UserModel


class UserDAO:
    """Class for accessing users table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:
        self.session = session

    async def update_user_balance(self, user_id: int, balance: int) -> None:
        """
        Update the balance of a user.

        :param user_id: ID of the user.
        :param new_balance: New balance to be set for the user.
        """
        user = await self.get_user_by_id(user_id)
        if user:
            user.balance = balance
            await self.session.commit()

    async def create_user(self, username: str, password: str) -> None:
        """
        Add single user to session.

        :param username: username of a user.
        :param password: password of a user.
        """
        self.session.add(UserModel(username=username, password=password))

    async def get_user_by_id(self, user_id: int) -> Optional[UserModel]:
        """
        Get a single user model by its user_id.

        :param user_id: id of the user.
        :return: UserModel instance if found, None otherwise.
        """
        try:
            result = await self.session.execute(
                select(UserModel).filter_by(id=user_id),
            )
            return result.scalar_one()
        except NoResultFound:
            return None
        except Exception as e:
            raise e

    async def get_user(self, username: str) -> Optional[UserModel]:
        """
        Get a single user model by its username.

        :param username: username of the user.
        :return: UserModel instance if found, None otherwise.
        """
        try:
            result = await self.session.execute(
                select(UserModel).filter_by(username=username),
            )
            return result.scalar_one()
        except NoResultFound:
            return None
        except Exception as e:
            raise e
