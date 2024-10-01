from asyncio import Lock
from typing import Dict


class UserLevelLock:
    """A Class to prevent several race conditions when performing operations."""

    def __init__(self) -> None:
        self.locks: Dict[int, Lock] = {}
        self.global_lock = Lock()

    async def acquire(self, user_id: int) -> Lock:
        """Acquires the lock."""
        async with self.global_lock:
            if user_id not in self.locks:
                self.locks[user_id] = Lock()
        return self.locks[user_id]

    async def release(self, user_id: int) -> None:
        """Releases the lock."""
        async with self.global_lock:
            if user_id in self.locks and not self.locks[user_id].locked():
                del self.locks[user_id]
