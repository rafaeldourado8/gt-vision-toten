"""Detection DTOs."""
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class DetectFacesDTO:
    """Detect faces input DTO."""

    frame_bytes: bytes
    camera_id: str


@dataclass(frozen=True)
class BoundingBoxDTO:
    """Bounding box DTO."""

    x: int
    y: int
    width: int
    height: int


@dataclass(frozen=True)
class FaceDTO:
    """Face DTO."""

    id: str
    bounding_box: BoundingBoxDTO
    confidence: float
    has_encoding: bool


@dataclass(frozen=True)
class FaceDetectionDTO:
    """Face detection DTO."""

    id: str
    camera_id: str
    timestamp: str
    faces: List[FaceDTO]
    face_count: int


@dataclass(frozen=True)
class CompareFacesDTO:
    """Compare faces input DTO."""

    face1_encoding: List[float]
    face2_encoding: List[float]


@dataclass(frozen=True)
class MatchResultDTO:
    """Match result DTO."""

    matched: bool
    confidence: float
    similarity_percentage: float
