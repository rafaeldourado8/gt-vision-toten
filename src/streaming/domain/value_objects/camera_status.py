"""Camera status value object."""
from enum import Enum


class CameraStatus(str, Enum):
    """Camera status."""

    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    ERROR = "ERROR"
    CONNECTING = "CONNECTING"
