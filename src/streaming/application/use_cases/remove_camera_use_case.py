"""Remove camera use case."""
from uuid import UUID
from src.core.application.base import UseCase, Result
from src.streaming.domain import CameraRepository, CameraNotFoundError


class RemoveCameraUseCase(UseCase[str, Result[None]]):
    """Remove camera use case."""

    def __init__(self, camera_repository: CameraRepository) -> None:
        self._repository = camera_repository

    async def execute(self, camera_id: str) -> Result[None]:
        """Execute use case."""
        try:
            camera_uuid = UUID(camera_id)
            
            # Check if camera exists
            camera = await self._repository.find_by_id(camera_uuid)
            if not camera:
                return Result.fail(f"Camera not found: {camera_id}")

            # Delete
            await self._repository.delete(camera_uuid)

            return Result.ok(None)

        except ValueError:
            return Result.fail(f"Invalid camera ID: {camera_id}")
        except Exception as e:
            return Result.fail(str(e))
