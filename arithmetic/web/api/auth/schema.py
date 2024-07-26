from pydantic import BaseModel


class UserRequest(BaseModel):
    """Create user request model."""

    username: str
    password: str


class Token(BaseModel):
    """JWT token model."""

    access_token: str
    token_type: str


class ValidatedUser(BaseModel):
    """Create a validated user model."""

    user_id: int
    username: str
    balance: int
