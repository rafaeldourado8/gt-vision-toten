"""Camera aggregate root."""
from uuid import UUID
from src.core.domain.base import AggregateRoot
from src.core.domain.errors import ValidationException
from ..value_objects.rtsp_url import RtspUrl
from ..value_objects.stream_path import StreamPath
from ..value_objects.camera_status import CameraStatus


class Camera(AggregateRoot):
    """Camera aggregate root."""

    def __init__(
        self,
        entity_id: UUID | None = None,
        name: str = "",
        rtsp_url: RtspUrl | None = None,
        stream_path: StreamPath | None = None,
        location: str = "",
        status: CameraStatus = CameraStatus.OFFLINE,
    ) -> None:
        super().__init__(entity_id)
        
        if not name or len(name) < 3:
            raise ValidationException("Camera name must have at least 3 characters")
        if rtsp_url is None:
            raise ValidationException("RTSP URL is required")
        if stream_path is None:
            raise ValidationException("Stream path is required")

        self.name = name
        self.rtsp_url = rtsp_url
        self.stream_path = stream_path
        self.location = location
        self.status = status

    @staticmethod
    def create(
        name: str,
        rtsp_url: RtspUrl,
        stream_path: StreamPath,
        location: str = "",
    ) -> "Camera":
        """Create new camera."""
        return Camera(
            name=name,
            rtsp_url=rtsp_url,
            stream_path=stream_path,
            location=location,
            status=CameraStatus.OFFLINE,
        )

    def activate(self) -> None:
        """Activate camera."""
        self.status = CameraStatus.ONLINE
        self._touch()

    def deactivate(self) -> None:
        """Deactivate camera."""
        self.status = CameraStatus.OFFLINE
        self._touch()

    def set_error(self) -> None:
        """Set camera to error state."""
        self.status = CameraStatus.ERROR
        self._touch()

    def set_connecting(self) -> None:
        """Set camera to connecting state."""
        self.status = CameraStatus.CONNECTING
        self._touch()

    @property
    def is_online(self) -> bool:
        """Check if camera is online."""
        return self.status == CameraStatus.ONLINE
