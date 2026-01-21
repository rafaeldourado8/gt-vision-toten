"""Register camera use case."""
from uuid import uuid4
from src.core.application.base import UseCase, Result
from src.streaming.domain import (
    Camera,
    RtspUrl,
    StreamPath,
    CameraRepository,
    DuplicateStreamPathError,
)
from ..dtos.camera_dtos import RegisterCameraDTO, CameraDTO
from ..mappers.camera_mapper import CameraMapper


class RegisterCameraUseCase(UseCase[RegisterCameraDTO, Result[CameraDTO]]):
    """Register camera use case."""

    def __init__(self, camera_repository: CameraRepository) -> None:
        self._repository = camera_repository

    async def execute(self, input_dto: RegisterCameraDTO) -> Result[CameraDTO]:
        """Execute use case."""
        try:
            # Generate unique stream path
            stream_path_value = self._generate_stream_path(input_dto.name)
            
            # Check if stream path already exists
            existing = await self._repository.find_by_stream_path(stream_path_value)
            if existing:
                return Result.fail(f"Stream path already exists: {stream_path_value}")

            # Create value objects
            rtsp_url = RtspUrl(input_dto.rtsp_url)
            stream_path = StreamPath(stream_path_value)

            # Create camera
            camera = Camera.create(
                name=input_dto.name,
                rtsp_url=rtsp_url,
                stream_path=stream_path,
                location=input_dto.location,
            )

            # Save
            await self._repository.save(camera)

            return Result.ok(CameraMapper.to_dto(camera))

        except Exception as e:
            return Result.fail(str(e))

    def _generate_stream_path(self, name: str) -> str:
        """Generate unique stream path from name."""
        # Simple: lowercase, replace spaces with hyphens, add uuid suffix
        base = name.lower().replace(" ", "-")[:20]
        suffix = str(uuid4())[:8]
        return f"{base}-{suffix}"
