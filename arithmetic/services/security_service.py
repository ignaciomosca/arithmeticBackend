from datetime import datetime, timedelta
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from arithmetic.settings import settings
from arithmetic.web.api.auth.schema import ValidatedUser

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

BEARER = "Bearer"

jwt_error = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate user",
)


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


async def get_current_user(
    token: Annotated[str, Depends(oauth2_bearer)],
) -> ValidatedUser:
    """
    Gets a user from an OAuth token.

    :param token: the users token.
    """
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        balance: int = payload.get("balance")
        return ValidatedUser(username=username, user_id=user_id, balance=balance)
    except jwt.ExpiredSignatureError as err:
        raise jwt_error from err
    except jwt.InvalidTokenError as err:
        raise jwt_error from err


user_dependency = Annotated[ValidatedUser, Depends(get_current_user)]
