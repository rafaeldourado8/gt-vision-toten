"""Face detection repository interface."""
from abc import ABC, abstractmethod
from uuid import UUID
from datetime import datetime
from typing import List
from ..entities.face_detection import FaceDetection


class FaceDetectionRepository(ABC):
    """Face detection repository interface."""

    @abstractmethod
    async def save(self, detection: FaceDetection) -> None:
        """Save face detection."""
        pass

    @abstractmethod
    async def find_by_id(self, detection_id: UUID) -> FaceDetection | None:
        """Find detection by ID."""
        pass

    @abstractmethod
    async def find_by_camera(
        self, 
        camera_id: UUID, 
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> List[FaceDetection]:
        """Find detections by camera."""
        pass

    @abstractmethod
    async def find_recent(self, camera_id: UUID, limit: int = 10) -> List[FaceDetection]:
        """Find recent detections."""
        pass

    @abstractmethod
    async def delete(self, detection_id: UUID) -> None:
        """Delete detection."""
        pass
