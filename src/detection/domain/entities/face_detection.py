"""Face detection aggregate root."""
from uuid import UUID
from datetime import datetime
from typing import List
from src.core.domain.base import AggregateRoot
from src.core.domain.errors import ValidationException
from .face import Face


class FaceDetection(AggregateRoot):
    """Face detection aggregate root."""

    def __init__(
        self,
        entity_id: UUID | None = None,
        camera_id: UUID | None = None,
        timestamp: datetime | None = None,
        faces: List[Face] | None = None,
        frame_id: str = "",
    ) -> None:
        super().__init__(entity_id)
        
        if camera_id is None:
            raise ValidationException("Camera ID is required")
        
        self.camera_id = camera_id
        self.timestamp = timestamp or datetime.utcnow()
        self.faces = faces or []
        self.frame_id = frame_id

    @staticmethod
    def create(
        camera_id: UUID,
        faces: List[Face],
        frame_id: str = "",
    ) -> "FaceDetection":
        """Create new face detection."""
        return FaceDetection(
            camera_id=camera_id,
            timestamp=datetime.utcnow(),
            faces=faces,
            frame_id=frame_id,
        )

    def add_face(self, face: Face) -> None:
        """Add face to detection."""
        self.faces.append(face)
        self._touch()

    def get_best_face(self) -> Face | None:
        """Get face with highest confidence."""
        if not self.faces:
            return None
        return max(self.faces, key=lambda f: f.confidence.value if f.confidence else 0.0)

    @property
    def face_count(self) -> int:
        """Get number of detected faces."""
        return len(self.faces)

    @property
    def has_faces(self) -> bool:
        """Check if detection has faces."""
        return len(self.faces) > 0

    @property
    def high_quality_faces(self) -> List[Face]:
        """Get only high quality faces."""
        return [f for f in self.faces if f.is_high_quality]
