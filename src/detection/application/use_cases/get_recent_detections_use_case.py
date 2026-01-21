"""Get recent detections use case."""
from uuid import UUID
from typing import List
from src.core.application.base import UseCase, Result
from src.detection.domain import FaceDetectionRepository
from ..dtos.detection_dtos import FaceDetectionDTO
from ..mappers.face_detection_mapper import FaceDetectionMapper


class GetRecentDetectionsUseCase(UseCase[str, Result[List[FaceDetectionDTO]]]):
    """Get recent detections use case."""

    def __init__(self, detection_repository: FaceDetectionRepository) -> None:
        self._repository = detection_repository

    async def execute(self, camera_id: str) -> Result[List[FaceDetectionDTO]]:
        """Execute use case."""
        try:
            camera_uuid = UUID(camera_id)
            
            detections = await self._repository.find_recent(camera_uuid, limit=10)
            dtos = [FaceDetectionMapper.to_dto(d) for d in detections]
            
            return Result.ok(dtos)
            
        except ValueError:
            return Result.fail(f"Invalid camera ID: {camera_id}")
        except Exception as e:
            return Result.fail(str(e))
