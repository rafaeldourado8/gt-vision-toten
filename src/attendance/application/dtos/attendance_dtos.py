"""Attendance DTOs."""
from dataclasses import dataclass
from typing import List
from datetime import date


@dataclass(frozen=True)
class RegisterAttendanceDTO:
    """Register attendance input DTO."""

    student_id: str
    camera_id: str
    confidence: float


@dataclass(frozen=True)
class AttendanceRecordDTO:
    """Attendance record output DTO."""

    id: str
    student_id: str
    camera_id: str
    timestamp: str
    status: str
    confidence: float
    is_high_confidence: bool


@dataclass(frozen=True)
class AttendanceReportDTO:
    """Attendance report DTO."""

    date: str
    total_students: int
    present_count: int
    absent_count: int
    late_count: int
    records: List[AttendanceRecordDTO]
