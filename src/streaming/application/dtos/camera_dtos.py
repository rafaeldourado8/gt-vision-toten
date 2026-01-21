"""Streaming DTOs."""
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class RegisterCameraDTO:
    """Register camera input DTO."""

    name: str
    rtsp_url: str
    location: str = ""


@dataclass(frozen=True)
class CameraDTO:
    """Camera output DTO."""

    id: str
    name: str
    rtsp_url: str
    stream_path: str
    status: str
    location: str
    created_at: str
    updated_at: str


@dataclass(frozen=True)
class CameraStatusDTO:
    """Camera status DTO."""

    id: str
    name: str
    status: str
    is_online: bool
