"""Duplicate detector domain service."""
from datetime import datetime, timedelta
from typing import List
from ..entities.attendance_record import AttendanceRecord


class DuplicateDetector:
    """Duplicate detector service."""

    DUPLICATE_WINDOW_SECONDS = 60  # 60 seconds

    @staticmethod
    def is_duplicate(
        new_record: AttendanceRecord,
        existing_records: List[AttendanceRecord],
    ) -> bool:
        """Check if record is duplicate."""
        for record in existing_records:
            # Same student
            if record.student_id != new_record.student_id:
                continue
            
            # Within time window
            time_diff = abs((new_record.timestamp - record.timestamp).total_seconds())
            if time_diff <= DuplicateDetector.DUPLICATE_WINDOW_SECONDS:
                return True
        
        return False

    @staticmethod
    def filter_duplicates(
        records: List[AttendanceRecord],
    ) -> List[AttendanceRecord]:
        """Filter duplicate records."""
        unique_records = []
        
        for record in records:
            if not DuplicateDetector.is_duplicate(record, unique_records):
                unique_records.append(record)
        
        return unique_records
