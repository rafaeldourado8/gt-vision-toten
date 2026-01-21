"""Streaming domain errors."""
from src.core.domain.errors import DomainException, NotFoundException


class CameraNotFoundError(NotFoundException):
    """Camera not found error."""

    def __init__(self, camera_id: str) -> None:
        super().__init__(f"Camera not found: {camera_id}")


class DuplicateStreamPathError(DomainException):
    """Duplicate stream path error."""

    def __init__(self, stream_path: str) -> None:
        super().__init__(f"Stream path already exists: {stream_path}")
