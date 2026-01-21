"""Attendance record aggregate root."""
from uuid import UUID
from datetime import datetime, time
from src.core.domain.base import AggregateRoot
from src.core.domain.errors import ValidationException
from ..value_objects.attendance_status import AttendanceStatus


class AttendanceRecord(AggregateRoot):
    """Attendance record aggregate root."""

    LATE_THRESHOLD = time(8, 0)  # 8:00 AM

    def __init__(
        self,
        entity_id: UUID | None = None,
        student_id: UUID | None = None,
        camera_id: UUID | None = None,
        timestamp: datetime | None = None,
        status: AttendanceStatus = AttendanceStatus.PRESENT,
        confidence: float = 0.0,
    ) -> None:
        super().__init__(entity_id)
        
        if student_id is None:
            raise ValidationException("Student ID is required")
        if camera_id is None:
            raise ValidationException("Camera ID is required")
        
        self.student_id = student_id
        self.camera_id = camera_id
        self.timestamp = timestamp or datetime.utcnow()
        self.status = status
        self.confidence = confidence

    @staticmethod
    def create(
        student_id: UUID,
        camera_id: UUID,
        confidence: float,
        timestamp: datetime | None = None,
    ) -> "AttendanceRecord":
        """Create new attendance record."""
        timestamp = timestamp or datetime.utcnow()
        
        # Determine status based on time
        status = AttendanceStatus.PRESENT
        if timestamp.time() > AttendanceRecord.LATE_THRESHOLD:
            status = AttendanceStatus.LATE
        
        return AttendanceRecord(
            student_id=student_id,
            camera_id=camera_id,
            timestamp=timestamp,
            status=status,
            confidence=confidence,
        )

    def mark_as_late(self) -> None:
        """Mark attendance as late."""
        self.status = AttendanceStatus.LATE
        self._touch()

    def mark_as_absent(self) -> None:
        """Mark attendance as absent."""
        self.status = AttendanceStatus.ABSENT
        self._touch()

    @property
    def is_present(self) -> bool:
        """Check if student is present."""
        return self.status == AttendanceStatus.PRESENT

    @property
    def is_late(self) -> bool:
        """Check if student is late."""
        return self.status == AttendanceStatus.LATE

    @property
    def is_high_confidence(self) -> bool:
        """Check if detection has high confidence."""
        return self.confidence >= 0.8
