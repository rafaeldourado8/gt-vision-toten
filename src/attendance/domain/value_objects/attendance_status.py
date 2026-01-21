"""Attendance status value object."""
from enum import Enum


class AttendanceStatus(str, Enum):
    """Attendance status."""

    PRESENT = "PRESENT"
    ABSENT = "ABSENT"
    LATE = "LATE"
