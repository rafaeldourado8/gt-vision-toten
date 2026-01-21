"""Class room value object."""
from src.core.domain.base import ValueObject
from src.core.domain.errors import ValidationException


class ClassRoom(ValueObject):
    """Class room value object."""

    def __init__(self, grade: str, section: str = "") -> None:
        if not grade:
            raise ValidationException("Grade is required")
        self._grade = grade.strip()
        self._section = section.strip()

    @property
    def grade(self) -> str:
        return self._grade

    @property
    def section(self) -> str:
        return self._section

    @property
    def full_name(self) -> str:
        """Get full class room name."""
        if self._section:
            return f"{self._grade} - {self._section}"
        return self._grade

    def __str__(self) -> str:
        return self.full_name
