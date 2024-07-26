from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from starlette import status

from arithmetic.settings import settings
from arithmetic.web.api.auth.schema import ValidatedUser

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


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
    except JWTError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user",
        ) from err


user_dependency = Annotated[ValidatedUser, Depends(get_current_user)]
