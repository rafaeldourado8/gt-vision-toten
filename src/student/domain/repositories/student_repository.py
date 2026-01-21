"""Student repository interface."""
from abc import ABC, abstractmethod
from uuid import UUID
from typing import List
from ..entities.student import Student


class StudentRepository(ABC):
    """Student repository interface."""

    @abstractmethod
    async def save(self, student: Student) -> None:
        """Save student."""
        pass

    @abstractmethod
    async def find_by_id(self, student_id: UUID) -> Student | None:
        """Find student by ID."""
        pass

    @abstractmethod
    async def find_by_class(self, grade: str, section: str = "") -> List[Student]:
        """Find students by class."""
        pass

    @abstractmethod
    async def find_all(self, active_only: bool = True) -> List[Student]:
        """Find all students."""
        pass

    @abstractmethod
    async def delete(self, student_id: UUID) -> None:
        """Delete student."""
        pass

    @abstractmethod
    async def search_by_name(self, name: str) -> List[Student]:
        """Search students by name."""
        pass
