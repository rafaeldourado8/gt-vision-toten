"""Register attendance use case."""
from uuid import UUID
from src.core.application.base import UseCase, Result
from src.attendance.domain import (
    AttendanceRecord,
    AttendanceRepository,
    DuplicateDetector,
)
from ..dtos.attendance_dtos import RegisterAttendanceDTO, AttendanceRecordDTO
from ..mappers.attendance_mapper import AttendanceMapper


class RegisterAttendanceUseCase(UseCase[RegisterAttendanceDTO, Result[AttendanceRecordDTO]]):
    """Register attendance use case."""

    def __init__(self, attendance_repository: AttendanceRepository) -> None:
        self._repository = attendance_repository

    async def execute(self, input_dto: RegisterAttendanceDTO) -> Result[AttendanceRecordDTO]:
        """Execute use case."""
        try:
            student_id = UUID(input_dto.student_id)
            camera_id = UUID(input_dto.camera_id)

            # Check for duplicates (last 60 minutes)
            recent_records = await self._repository.find_recent_by_student(
                student_id, minutes=60
            )

            # Create new record
            new_record = AttendanceRecord.create(
                student_id=student_id,
                camera_id=camera_id,
                confidence=input_dto.confidence,
            )

            # Check if duplicate
            if DuplicateDetector.is_duplicate(new_record, recent_records):
                return Result.fail(f"Duplicate attendance for student: {input_dto.student_id}")

            # Save
            await self._repository.save(new_record)

            return Result.ok(AttendanceMapper.to_dto(new_record))

        except ValueError:
            return Result.fail("Invalid student or camera ID")
        except Exception as e:
            return Result.fail(str(e))
