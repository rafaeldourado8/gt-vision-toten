"""Student DTOs."""
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class RegisterStudentDTO:
    """Register student input DTO."""

    name: str
    grade: str
    section: str = ""


@dataclass(frozen=True)
class StudentDTO:
    """Student output DTO."""

    id: str
    name: str
    grade: str
    section: str
    class_room: str
    has_face_profile: bool
    has_face_encoding: bool
    is_active: bool
    created_at: str
    updated_at: str


@dataclass(frozen=True)
class UpdatePhotoDTO:
    """Update photo input DTO."""

    student_id: str
    photo_bytes: bytes


@dataclass(frozen=True)
class ImportStudentDTO:
    """Import student DTO."""

    name: str
    grade: str
    section: str = ""
