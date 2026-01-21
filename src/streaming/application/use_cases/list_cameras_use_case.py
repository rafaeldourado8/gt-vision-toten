"""List cameras use case."""
from typing import List
from src.core.application.base import UseCase, Result
from src.streaming.domain import CameraRepository
from ..dtos.camera_dtos import CameraDTO
from ..mappers.camera_mapper import CameraMapper


class ListCamerasUseCase(UseCase[None, Result[List[CameraDTO]]]):
    """List cameras use case."""

    def __init__(self, camera_repository: CameraRepository) -> None:
        self._repository = camera_repository

    async def execute(self, _: None = None) -> Result[List[CameraDTO]]:
        """Execute use case."""
        try:
            cameras = await self._repository.find_all()
            dtos = [CameraMapper.to_dto(camera) for camera in cameras]
            return Result.ok(dtos)

        except Exception as e:
            return Result.fail(str(e))
