"""Face detection mapper."""
from src.detection.domain import Face, FaceDetection
from ..dtos.detection_dtos import FaceDTO, FaceDetectionDTO, BoundingBoxDTO


class FaceDetectionMapper:
    """Face detection mapper."""

    @staticmethod
    def face_to_dto(face: Face) -> FaceDTO:
        """Convert face entity to DTO."""
        return FaceDTO(
            id=str(face.id),
            bounding_box=BoundingBoxDTO(
                x=face.bounding_box.x,
                y=face.bounding_box.y,
                width=face.bounding_box.width,
                height=face.bounding_box.height,
            ) if face.bounding_box else None,
            confidence=face.confidence.value if face.confidence else 0.0,
            has_encoding=face.has_encoding,
        )

    @staticmethod
    def to_dto(detection: FaceDetection) -> FaceDetectionDTO:
        """Convert detection to DTO."""
        return FaceDetectionDTO(
            id=str(detection.id),
            camera_id=str(detection.camera_id),
            timestamp=detection.timestamp.isoformat(),
            faces=[FaceDetectionMapper.face_to_dto(f) for f in detection.faces],
            face_count=detection.face_count,
        )
