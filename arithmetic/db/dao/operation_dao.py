from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from arithmetic.db.dependencies import get_db_session


class OperationDAO:
    """Class for accessing operations table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:
        self.session = session

    async def perform_operation(self) -> None:
        """Add single operation to session."""
