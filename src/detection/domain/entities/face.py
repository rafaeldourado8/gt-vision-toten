"""Face entity."""
from uuid import UUID, uuid4
from src.core.domain.base import Entity
from ..value_objects.bounding_box import BoundingBox
from ..value_objects.confidence import Confidence
from ..value_objects.face_encoding import FaceEncoding


class Face(Entity):
    """Face entity."""

    def __init__(
        self,
        entity_id: UUID | None = None,
        bounding_box: BoundingBox | None = None,
        confidence: Confidence | None = None,
        encoding: FaceEncoding | None = None,
    ) -> None:
        super().__init__(entity_id)
        self.bounding_box = bounding_box
        self.confidence = confidence
        self.encoding = encoding

    @staticmethod
    def create(
        bounding_box: BoundingBox,
        confidence: Confidence,
        encoding: FaceEncoding | None = None,
    ) -> "Face":
        """Create new face."""
        return Face(
            entity_id=uuid4(),
            bounding_box=bounding_box,
            confidence=confidence,
            encoding=encoding,
        )

    @property
    def has_encoding(self) -> bool:
        """Check if face has encoding."""
        return self.encoding is not None

    @property
    def is_high_quality(self) -> bool:
        """Check if face detection is high quality."""
        return self.confidence.is_high if self.confidence else False
