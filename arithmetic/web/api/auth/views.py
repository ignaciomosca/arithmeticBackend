from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from starlette import status

from arithmetic.db.dao.user_dao import UserDAO
from arithmetic.web.api.auth.schema import CreateUserRequest

router = APIRouter()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    new_user: CreateUserRequest,
    user_dao: UserDAO = Depends(),
) -> None:
    """
    Creates a new user in the database.

    :param new_user: new user model.
    :param user_dao: DAO for user models.
    """
    await user_dao.create_user(new_user.username, new_user.password)
