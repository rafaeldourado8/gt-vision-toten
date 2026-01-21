"""Update student photo use case."""
from uuid import UUID
from pathlib import Path
from src.core.application.base import UseCase, Result
from src.student.domain import StudentRepository, FaceProfile
from ..dtos.student_dtos import UpdatePhotoDTO, StudentDTO
from ..mappers.student_mapper import StudentMapper


class UpdateStudentPhotoUseCase(UseCase[UpdatePhotoDTO, Result[StudentDTO]]):
    """Update student photo use case."""

    def __init__(
        self,
        student_repository: StudentRepository,
        storage_path: str,
        face_encoder,  # DeepFaceAdapter
    ) -> None:
        self._repository = student_repository
        self._storage_path = Path(storage_path)
        self._encoder = face_encoder

    async def execute(self, input_dto: UpdatePhotoDTO) -> Result[StudentDTO]:
        """Execute use case."""
        try:
            student_id = UUID(input_dto.student_id)

            # Find student
            student = await self._repository.find_by_id(student_id)
            if not student:
                return Result.fail(f"Student not found: {input_dto.student_id}")

            # Save photo
            photo_path = self._storage_path / f"{student_id}.jpg"
            photo_path.parent.mkdir(parents=True, exist_ok=True)
            photo_path.write_bytes(input_dto.photo_bytes)

            # Extract face encoding
            encoding_obj = await self._encoder.extract_embedding(input_dto.photo_bytes)
            encoding = encoding_obj.embedding if encoding_obj else []

            # Update face profile
            face_profile = FaceProfile(str(photo_path), encoding)
            student.update_face_profile(face_profile)

            # Save
            await self._repository.save(student)

            return Result.ok(StudentMapper.to_dto(student))

        except ValueError:
            return Result.fail(f"Invalid student ID: {input_dto.student_id}")
        except Exception as e:
            return Result.fail(str(e))
