"""Get attendance report use case."""
from datetime import date
from typing import List
from src.core.application.base import UseCase, Result
from src.attendance.domain import AttendanceRepository, AttendanceStatus
from ..dtos.attendance_dtos import AttendanceReportDTO, AttendanceRecordDTO
from ..mappers.attendance_mapper import AttendanceMapper


class GetAttendanceReportUseCase(UseCase[str, Result[AttendanceReportDTO]]):
    """Get attendance report use case."""

    def __init__(self, attendance_repository: AttendanceRepository) -> None:
        self._repository = attendance_repository

    async def execute(self, date_str: str) -> Result[AttendanceReportDTO]:
        """Execute use case."""
        try:
            target_date = date.fromisoformat(date_str)

            # Get all records for date
            records = await self._repository.find_by_date(target_date)

            # Convert to DTOs
            record_dtos = [AttendanceMapper.to_dto(r) for r in records]

            # Calculate stats
            present_count = sum(1 for r in records if r.status == AttendanceStatus.PRESENT)
            late_count = sum(1 for r in records if r.status == AttendanceStatus.LATE)
            absent_count = sum(1 for r in records if r.status == AttendanceStatus.ABSENT)

            report = AttendanceReportDTO(
                date=date_str,
                total_students=len(records),
                present_count=present_count,
                absent_count=absent_count,
                late_count=late_count,
                records=record_dtos,
            )

            return Result.ok(report)

        except ValueError:
            return Result.fail(f"Invalid date format: {date_str}")
        except Exception as e:
            return Result.fail(str(e))
