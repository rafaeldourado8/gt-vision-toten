"""Detect faces use case."""
from uuid import UUID
from src.core.application.base import UseCase, Result
from src.detection.domain import FaceDetection, FaceDetectionRepository
from ..dtos.detection_dtos import DetectFacesDTO, FaceDetectionDTO
from ..mappers.face_detection_mapper import FaceDetectionMapper


class DetectFacesUseCase(UseCase[DetectFacesDTO, Result[FaceDetectionDTO]]):
    """Detect faces in frame use case."""

    def __init__(
        self,
        detection_repository: FaceDetectionRepository,
        face_detector,  # Will be FaceDetector interface
    ) -> None:
        self._repository = detection_repository
        self._detector = face_detector

    async def execute(self, input_dto: DetectFacesDTO) -> Result[FaceDetectionDTO]:
        """Execute use case."""
        try:
            camera_id = UUID(input_dto.camera_id)
            
            # Detect faces using detector adapter
            faces = await self._detector.detect(input_dto.frame_bytes)
            
            # Create detection aggregate
            detection = FaceDetection.create(
                camera_id=camera_id,
                faces=faces,
            )
            
            # Save detection
            await self._repository.save(detection)
            
            return Result.ok(FaceDetectionMapper.to_dto(detection))
            
        except ValueError:
            return Result.fail(f"Invalid camera ID: {input_dto.camera_id}")
        except Exception as e:
            return Result.fail(str(e))
