"""RTSP URL value object."""
import re
from src.core.domain.base import ValueObject
from src.core.domain.errors import ValidationException


class RtspUrl(ValueObject):
    """RTSP URL value object."""

    RTSP_PATTERN = re.compile(
        r"^rtsp://(?:([^:@]+):([^@]+)@)?([^:/]+)(?::(\d+))?(/.*)?$"
    )
    WEBCAM_PATTERN = re.compile(r"^webcam://(\d+)$")

    def __init__(self, value: str) -> None:
        if not self._is_valid(value):
            raise ValidationException(
                f"Invalid URL format: {value}. "
                "Expected: rtsp://[user:pass@]host[:port][/path] or webcam://0"
            )
        self._value = value

    @property
    def value(self) -> str:
        return self._value

    @property
    def is_webcam(self) -> bool:
        """Check if URL is webcam."""
        return self._value.startswith("webcam://")

    @property
    def webcam_index(self) -> int | None:
        """Get webcam index if URL is webcam."""
        if not self.is_webcam:
            return None
        match = self.WEBCAM_PATTERN.match(self._value)
        return int(match.group(1)) if match else None

    def _is_valid(self, value: str) -> bool:
        return bool(self.RTSP_PATTERN.match(value) or self.WEBCAM_PATTERN.match(value))

    def __str__(self) -> str:
        return self._value
