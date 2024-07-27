from datetime import datetime, timedelta

import jwt
from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from starlette import status

from arithmetic.db.dao.user_dao import UserDAO
from arithmetic.settings import settings
from arithmetic.web.api.auth.schema import Token, UserRequest

router = APIRouter()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
BEARER = "bearer"


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    new_user: UserRequest,
    user_dao: UserDAO = Depends(),
) -> None:
    """
    Creates a new user in the database.

    :param new_user: new user model.
    :param user_dao: DAO for user models.
    """
    hashed_password = bcrypt_context.hash(new_user.password)
    await user_dao.create_user(new_user.username, hashed_password)


@router.post("/token", response_model=Token)
async def login_for_access_token(
    login_user: UserRequest,
    user_dao: UserDAO = Depends(),
) -> Token:
    """
    Create a new user in the database.

    :param new_user: new user model.
    :param user_dao: DAO for user models.
    """
    user = await user_dao.get_user(login_user.username)
    if not user or not bcrypt_context.verify(login_user.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user",
        )
    token = await create_access_token(
        login_user.username,
        user.id,
        user.balance,
        timedelta(minutes=20),
    )
    return Token(access_token=token, token_type=BEARER)


async def create_access_token(
    username: str,
    user_id: int,
    user_balance: int,
    expires_delta: timedelta,
) -> str:
    """
    Create access token for a user.

    :param username: username of the user.
    :param user_id: id of the user.
    :param expires_delta: amount of time it takes for the token to expire.
    """
    encode = {"sub": username, "id": user_id, "balance": user_balance}
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, settings.secret_key, algorithm=settings.algorithm)
