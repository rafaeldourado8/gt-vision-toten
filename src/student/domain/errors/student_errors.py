"""Student domain errors."""
from src.core.domain.errors import DomainException, NotFoundException


class StudentNotFoundError(NotFoundException):
    """Student not found error."""

    def __init__(self, student_id: str) -> None:
        super().__init__(f"Student not found: {student_id}")


class DuplicateStudentError(DomainException):
    """Duplicate student error."""

    def __init__(self, name: str) -> None:
        super().__init__(f"Student already exists: {name}")


class InvalidPhotoError(DomainException):
    """Invalid photo error."""

    def __init__(self, reason: str = "") -> None:
        super().__init__(f"Invalid photo: {reason}" if reason else "Invalid photo")
