"""In-memory camera repository for tests."""
from typing import Dict, List
from uuid import UUID
from src.streaming.domain import Camera, CameraRepository


class InMemoryCameraRepository(CameraRepository):
    """In-memory camera repository."""

    def __init__(self) -> None:
        self._cameras: Dict[UUID, Camera] = {}

    async def save(self, camera: Camera) -> None:
        """Save camera."""
        self._cameras[camera.id] = camera

    async def find_by_id(self, camera_id: UUID) -> Camera | None:
        """Find camera by ID."""
        return self._cameras.get(camera_id)

    async def find_by_stream_path(self, stream_path: str) -> Camera | None:
        """Find camera by stream path."""
        for camera in self._cameras.values():
            if str(camera.stream_path) == stream_path:
                return camera
        return None

    async def find_all(self) -> List[Camera]:
        """Find all cameras."""
        return list(self._cameras.values())

    async def delete(self, camera_id: UUID) -> None:
        """Delete camera."""
        if camera_id in self._cameras:
            del self._cameras[camera_id]
