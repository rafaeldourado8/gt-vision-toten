"""Get camera status use case."""
from uuid import UUID
from src.core.application.base import UseCase, Result
from src.streaming.domain import CameraRepository
from ..dtos.camera_dtos import CameraStatusDTO
from ..mappers.camera_mapper import CameraMapper


class GetCameraStatusUseCase(UseCase[str, Result[CameraStatusDTO]]):
    """Get camera status use case."""

    def __init__(self, camera_repository: CameraRepository) -> None:
        self._repository = camera_repository

    async def execute(self, camera_id: str) -> Result[CameraStatusDTO]:
        """Execute use case."""
        try:
            camera_uuid = UUID(camera_id)
            
            camera = await self._repository.find_by_id(camera_uuid)
            if not camera:
                return Result.fail(f"Camera not found: {camera_id}")

            return Result.ok(CameraMapper.to_status_dto(camera))

        except ValueError:
            return Result.fail(f"Invalid camera ID: {camera_id}")
        except Exception as e:
            return Result.fail(str(e))
