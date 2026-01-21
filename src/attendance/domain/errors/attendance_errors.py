"""Attendance domain errors."""
from src.core.domain.errors import DomainException, NotFoundException


class AttendanceNotFoundError(NotFoundException):
    """Attendance not found error."""

    def __init__(self, record_id: str) -> None:
        super().__init__(f"Attendance record not found: {record_id}")


class DuplicateAttendanceError(DomainException):
    """Duplicate attendance error."""

    def __init__(self, student_id: str) -> None:
        super().__init__(f"Duplicate attendance for student: {student_id}")
