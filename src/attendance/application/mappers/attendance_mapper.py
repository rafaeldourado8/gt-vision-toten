"""Attendance mapper."""
from src.attendance.domain import AttendanceRecord
from ..dtos.attendance_dtos import AttendanceRecordDTO


class AttendanceMapper:
    """Attendance mapper."""

    @staticmethod
    def to_dto(record: AttendanceRecord) -> AttendanceRecordDTO:
        """Convert record to DTO."""
        return AttendanceRecordDTO(
            id=str(record.id),
            student_id=str(record.student_id),
            camera_id=str(record.camera_id),
            timestamp=record.timestamp.isoformat(),
            status=record.status.value,
            confidence=record.confidence,
            is_high_confidence=record.is_high_confidence,
        )
