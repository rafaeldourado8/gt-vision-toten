"""Attendance repository interface."""
from abc import ABC, abstractmethod
from uuid import UUID
from datetime import datetime, date
from typing import List
from ..entities.attendance_record import AttendanceRecord


class AttendanceRepository(ABC):
    """Attendance repository interface."""

    @abstractmethod
    async def save(self, record: AttendanceRecord) -> None:
        """Save attendance record."""
        pass

    @abstractmethod
    async def find_by_id(self, record_id: UUID) -> AttendanceRecord | None:
        """Find record by ID."""
        pass

    @abstractmethod
    async def find_by_student(
        self,
        student_id: UUID,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> List[AttendanceRecord]:
        """Find records by student."""
        pass

    @abstractmethod
    async def find_by_date(self, target_date: date) -> List[AttendanceRecord]:
        """Find records by date."""
        pass

    @abstractmethod
    async def find_recent_by_student(
        self,
        student_id: UUID,
        minutes: int = 60,
    ) -> List[AttendanceRecord]:
        """Find recent records by student (for duplicate detection)."""
        pass

    @abstractmethod
    async def delete(self, record_id: UUID) -> None:
        """Delete record."""
        pass
