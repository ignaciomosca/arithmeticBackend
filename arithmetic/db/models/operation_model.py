from enum import Enum as PyEnum

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import Enum, Integer

from arithmetic.db.base import Base


class OperationEnum(PyEnum):
    """Model for operation types."""

    ADDITION = "addition"
    SUBSTRACTION = "substraction"
    MULTIPLICATION = "multiplication"
    DIVISION = "division"
    SQUARE = "squareRoot"
    RANDOM = "randomString"


class OperationModel(Base):
    """Model for Operations."""

    __tablename__ = "operations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type: Mapped[OperationEnum] = mapped_column(
        Enum(OperationEnum),
        default=OperationEnum.RANDOM,
    )
    cost: Mapped[int] = mapped_column(Integer)
