from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import String

from arithmetic.db.base import Base


class OperationModel(Base):
    """Model for Operations."""

    __tablename__ = "operations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    operation_type: Mapped[str] = mapped_column(String(length=40))
    cost: Mapped[int] = mapped_column(Integer, nullable=False)
