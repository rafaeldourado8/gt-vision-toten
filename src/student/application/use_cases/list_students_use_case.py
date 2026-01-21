"""List students use case."""
from typing import List
from src.core.application.base import UseCase, Result
from src.student.domain import StudentRepository
from ..dtos.student_dtos import StudentDTO
from ..mappers.student_mapper import StudentMapper


class ListStudentsUseCase(UseCase[None, Result[List[StudentDTO]]]):
    """List students use case."""

    def __init__(self, student_repository: StudentRepository) -> None:
        self._repository = student_repository

    async def execute(self, _: None = None) -> Result[List[StudentDTO]]:
        """Execute use case."""
        try:
            students = await self._repository.find_all(active_only=True)
            dtos = [StudentMapper.to_dto(s) for s in students]
            return Result.ok(dtos)

        except Exception as e:
            return Result.fail(str(e))
