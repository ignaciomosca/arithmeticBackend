from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import DateTime, Integer, String

from arithmetic.db.base import Base


class RecordModel(Base):
    """Model for Records."""

    __tablename__ = "records"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    operation_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("operations.id"),
        nullable=False,
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    user_balance: Mapped[int] = mapped_column(Integer, nullable=False)
    operation_response: Mapped[str] = mapped_column(String(length=200))
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    operation = relationship("OperationModel", backref="records")
    user = relationship("UserModel", backref="records")
