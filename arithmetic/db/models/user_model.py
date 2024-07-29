from enum import Enum as PyEnum

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import Integer, String

from arithmetic.db.base import Base


class StatusEnum(PyEnum):
    """Model for status types."""

    ACTIVE = "active"
    INACTIVE = "inactive"


class UserModel(Base):
    """Model for users."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(length=200), unique=True)
    password: Mapped[str] = mapped_column(String(length=200))
    status: Mapped[str] = mapped_column(String(length=10), default="active")
    balance: Mapped[int] = mapped_column(Integer, default=100)
