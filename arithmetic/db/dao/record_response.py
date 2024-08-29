from typing import List

from arithmetic.db.models.record_model import RecordModel


class RecordResponse:
    """Represents a return object to include the total count for pagination purposes."""

    def __init__(self, records: List[RecordModel], total_count: int) -> None:
        self.records = records
        self.total_count = total_count
