"""SQLite camera repository."""
from typing import List
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.streaming.domain import Camera, CameraRepository, RtspUrl, StreamPath, CameraStatus
from .models import CameraModel


class SQLiteCameraRepository(CameraRepository):
    """SQLite camera repository."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, camera: Camera) -> None:
        """Save camera."""
        model = await self._session.get(CameraModel, camera.id)
        
        if model:
            # Update
            model.name = camera.name
            model.rtsp_url = str(camera.rtsp_url)
            model.stream_path = str(camera.stream_path)
            model.status = camera.status.value
            model.location = camera.location
            model.updated_at = camera.updated_at
        else:
            # Insert
            model = CameraModel(
                id=camera.id,
                name=camera.name,
                rtsp_url=str(camera.rtsp_url),
                stream_path=str(camera.stream_path),
                status=camera.status.value,
                location=camera.location,
                created_at=camera.created_at,
                updated_at=camera.updated_at,
            )
            self._session.add(model)
        
        await self._session.commit()

    async def find_by_id(self, camera_id: UUID) -> Camera | None:
        """Find camera by ID."""
        model = await self._session.get(CameraModel, camera_id)
        return self._to_entity(model) if model else None

    async def find_by_stream_path(self, stream_path: str) -> Camera | None:
        """Find camera by stream path."""
        stmt = select(CameraModel).where(CameraModel.stream_path == stream_path)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def find_all(self) -> List[Camera]:
        """Find all cameras."""
        stmt = select(CameraModel)
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]

    async def delete(self, camera_id: UUID) -> None:
        """Delete camera."""
        model = await self._session.get(CameraModel, camera_id)
        if model:
            await self._session.delete(model)
            await self._session.commit()

    def _to_entity(self, model: CameraModel) -> Camera:
        """Convert model to entity."""
        return Camera(
            entity_id=model.id,
            name=model.name,
            rtsp_url=RtspUrl(model.rtsp_url),
            stream_path=StreamPath(model.stream_path),
            location=model.location,
            status=CameraStatus(model.status),
        )
