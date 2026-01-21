"""Camera repository interface."""
from abc import ABC, abstractmethod
from uuid import UUID
from typing import List
from ..entities.camera import Camera


class CameraRepository(ABC):
    """Camera repository interface."""

    @abstractmethod
    async def save(self, camera: Camera) -> None:
        """Save camera."""
        pass

    @abstractmethod
    async def find_by_id(self, camera_id: UUID) -> Camera | None:
        """Find camera by ID."""
        pass

    @abstractmethod
    async def find_by_stream_path(self, stream_path: str) -> Camera | None:
        """Find camera by stream path."""
        pass

    @abstractmethod
    async def find_all(self) -> List[Camera]:
        """Find all cameras."""
        pass

    @abstractmethod
    async def delete(self, camera_id: UUID) -> None:
        """Delete camera."""
        pass
