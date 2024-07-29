from datetime import datetime, timedelta
import jwt
from fastapi import HTTPException
from starlette import status
from arithmetic.settings import settings


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
