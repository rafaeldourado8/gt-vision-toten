"""Register student use case."""
from src.core.application.base import UseCase, Result
from src.student.domain import Student, StudentName, ClassRoom, StudentRepository
from ..dtos.student_dtos import RegisterStudentDTO, StudentDTO
from ..mappers.student_mapper import StudentMapper


class RegisterStudentUseCase(UseCase[RegisterStudentDTO, Result[StudentDTO]]):
    """Register student use case."""

    def __init__(self, student_repository: StudentRepository) -> None:
        self._repository = student_repository

    async def execute(self, input_dto: RegisterStudentDTO) -> Result[StudentDTO]:
        """Execute use case."""
        try:
            # Create value objects
            name = StudentName(input_dto.name)
            class_room = ClassRoom(input_dto.grade, input_dto.section)

            # Create student
            student = Student.create(name=name, class_room=class_room)

            # Save
            await self._repository.save(student)

            return Result.ok(StudentMapper.to_dto(student))

        except Exception as e:
            return Result.fail(str(e))
