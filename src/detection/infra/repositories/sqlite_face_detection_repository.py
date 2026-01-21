"""SQLite face detection repository."""
from typing import List
from uuid import UUID
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.detection.domain import (
    FaceDetection,
    Face,
    FaceDetectionRepository,
    Confidence,
    BoundingBox,
    FaceEncoding,
)
from .models import FaceDetectionModel, FaceModel


class SQLiteFaceDetectionRepository(FaceDetectionRepository):
    """SQLite face detection repository."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, detection: FaceDetection) -> None:
        """Save face detection."""
        model = await self._session.get(FaceDetectionModel, detection.id)

        if model:
            # Update
            model.camera_id = detection.camera_id
            model.timestamp = detection.timestamp
            model.frame_id = detection.frame_id
            model.updated_at = detection.updated_at
        else:
            # Insert
            model = FaceDetectionModel(
                id=detection.id,
                camera_id=detection.camera_id,
                timestamp=detection.timestamp,
                frame_id=detection.frame_id,
                created_at=detection.created_at,
                updated_at=detection.updated_at,
            )
            self._session.add(model)

            # Add faces
            for face in detection.faces:
                face_model = FaceModel(
                    id=face.id,
                    detection_id=detection.id,
                    x=face.bounding_box.x if face.bounding_box else 0,
                    y=face.bounding_box.y if face.bounding_box else 0,
                    width=face.bounding_box.width if face.bounding_box else 0,
                    height=face.bounding_box.height if face.bounding_box else 0,
                    confidence=face.confidence.value if face.confidence else 0.0,
                    encoding={"embedding": face.encoding.embedding} if face.encoding else None,
                )
                self._session.add(face_model)

        await self._session.commit()

    async def find_by_id(self, detection_id: UUID) -> FaceDetection | None:
        """Find detection by ID."""
        model = await self._session.get(FaceDetectionModel, detection_id)
        return self._to_entity(model) if model else None

    async def find_by_camera(
        self,
        camera_id: UUID,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> List[FaceDetection]:
        """Find detections by camera."""
        stmt = select(FaceDetectionModel).where(FaceDetectionModel.camera_id == camera_id)

        if start_date:
            stmt = stmt.where(FaceDetectionModel.timestamp >= start_date)
        if end_date:
            stmt = stmt.where(FaceDetectionModel.timestamp <= end_date)

        stmt = stmt.order_by(FaceDetectionModel.timestamp.desc())

        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]

    async def find_recent(self, camera_id: UUID, limit: int = 10) -> List[FaceDetection]:
        """Find recent detections."""
        stmt = (
            select(FaceDetectionModel)
            .where(FaceDetectionModel.camera_id == camera_id)
            .order_by(FaceDetectionModel.timestamp.desc())
            .limit(limit)
        )

        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]

    async def delete(self, detection_id: UUID) -> None:
        """Delete detection."""
        model = await self._session.get(FaceDetectionModel, detection_id)
        if model:
            await self._session.delete(model)
            await self._session.commit()

    def _to_entity(self, model: FaceDetectionModel) -> FaceDetection:
        """Convert model to entity."""
        faces = []
        for face_model in model.faces:
            encoding = None
            if face_model.encoding and "embedding" in face_model.encoding:
                encoding = FaceEncoding(face_model.encoding["embedding"])

            face = Face(
                entity_id=face_model.id,
                bounding_box=BoundingBox(
                    x=face_model.x,
                    y=face_model.y,
                    width=face_model.width,
                    height=face_model.height,
                ),
                confidence=Confidence(face_model.confidence),
                encoding=encoding,
            )
            faces.append(face)

        return FaceDetection(
            entity_id=model.id,
            camera_id=model.camera_id,
            timestamp=model.timestamp,
            faces=faces,
            frame_id=model.frame_id,
        )
