"""Detection domain errors."""
from src.core.domain.errors import DomainException, NotFoundException


class DetectionNotFoundError(NotFoundException):
    """Detection not found error."""

    def __init__(self, detection_id: str) -> None:
        super().__init__(f"Detection not found: {detection_id}")


class NoFacesDetectedError(DomainException):
    """No faces detected error."""

    def __init__(self) -> None:
        super().__init__("No faces detected in frame")


class InvalidFrameError(DomainException):
    """Invalid frame error."""

    def __init__(self, reason: str = "") -> None:
        super().__init__(f"Invalid frame: {reason}" if reason else "Invalid frame")
