"""Student aggregate root."""
from uuid import UUID
from src.core.domain.base import AggregateRoot
from src.core.domain.errors import ValidationException
from ..value_objects.student_name import StudentName
from ..value_objects.class_room import ClassRoom
from ..value_objects.face_profile import FaceProfile


class Student(AggregateRoot):
    """Student aggregate root."""

    def __init__(
        self,
        entity_id: UUID | None = None,
        name: StudentName | None = None,
        class_room: ClassRoom | None = None,
        face_profile: FaceProfile | None = None,
        is_active: bool = True,
    ) -> None:
        super().__init__(entity_id)
        
        if name is None:
            raise ValidationException("Student name is required")
        if class_room is None:
            raise ValidationException("Class room is required")
        
        self.name = name
        self.class_room = class_room
        self.face_profile = face_profile
        self.is_active = is_active

    @staticmethod
    def create(
        name: StudentName,
        class_room: ClassRoom,
        face_profile: FaceProfile | None = None,
    ) -> "Student":
        """Create new student."""
        return Student(
            name=name,
            class_room=class_room,
            face_profile=face_profile,
            is_active=True,
        )

    def update_face_profile(self, face_profile: FaceProfile) -> None:
        """Update face profile."""
        self.face_profile = face_profile
        self._touch()

    def deactivate(self) -> None:
        """Deactivate student."""
        self.is_active = False
        self._touch()

    def activate(self) -> None:
        """Activate student."""
        self.is_active = True
        self._touch()

    @property
    def has_face_profile(self) -> bool:
        """Check if student has face profile."""
        return self.face_profile is not None

    @property
    def has_face_encoding(self) -> bool:
        """Check if student has face encoding."""
        return self.face_profile is not None and self.face_profile.has_encoding
