"""Student mapper."""
from src.student.domain import Student
from ..dtos.student_dtos import StudentDTO


class StudentMapper:
    """Student mapper."""

    @staticmethod
    def to_dto(student: Student) -> StudentDTO:
        """Convert student entity to DTO."""
        return StudentDTO(
            id=str(student.id),
            name=str(student.name),
            grade=student.class_room.grade,
            section=student.class_room.section,
            class_room=str(student.class_room),
            has_face_profile=student.has_face_profile,
            has_face_encoding=student.has_face_encoding,
            is_active=student.is_active,
            created_at=student.created_at.isoformat(),
            updated_at=student.updated_at.isoformat(),
        )
