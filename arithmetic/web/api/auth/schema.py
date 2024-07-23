from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    """Create user request model."""

    username: str
    password: str


class Token(BaseModel):
    """JWT token model."""

    access_token: str
    token_type: str
