"""Camera mapper."""
from src.streaming.domain import Camera
from ..dtos.camera_dtos import CameraDTO, CameraStatusDTO


class CameraMapper:
    """Camera mapper."""

    @staticmethod
    def to_dto(camera: Camera) -> CameraDTO:
        """Convert camera entity to DTO."""
        return CameraDTO(
            id=str(camera.id),
            name=camera.name,
            rtsp_url=str(camera.rtsp_url),
            stream_path=str(camera.stream_path),
            status=camera.status.value,
            location=camera.location,
            created_at=camera.created_at.isoformat(),
            updated_at=camera.updated_at.isoformat(),
        )

    @staticmethod
    def to_status_dto(camera: Camera) -> CameraStatusDTO:
        """Convert camera to status DTO."""
        return CameraStatusDTO(
            id=str(camera.id),
            name=camera.name,
            status=camera.status.value,
            is_online=camera.is_online,
        )
