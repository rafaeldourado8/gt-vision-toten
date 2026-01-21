"""Detection SQLAlchemy models."""
from datetime import datetime
from uuid import UUID
from sqlalchemy import String, DateTime, Integer, JSON, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List


class Base(DeclarativeBase):
    """Base model."""
    pass


class FaceDetectionModel(Base):
    """Face detection model."""

    __tablename__ = "face_detections"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    camera_id: Mapped[UUID] = mapped_column(nullable=False, index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    frame_id: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # Relationship
    faces: Mapped[List["FaceModel"]] = relationship(
        "FaceModel", back_populates="detection", cascade="all, delete-orphan"
    )


class FaceModel(Base):
    """Face model."""

    __tablename__ = "faces"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    detection_id: Mapped[UUID] = mapped_column(
        ForeignKey("face_detections.id"), nullable=False, index=True
    )
    x: Mapped[int] = mapped_column(Integer, nullable=False)
    y: Mapped[int] = mapped_column(Integer, nullable=False)
    width: Mapped[int] = mapped_column(Integer, nullable=False)
    height: Mapped[int] = mapped_column(Integer, nullable=False)
    confidence: Mapped[float] = mapped_column(nullable=False)
    encoding: Mapped[dict] = mapped_column(JSON, nullable=True)

    # Relationship
    detection: Mapped["FaceDetectionModel"] = relationship(
        "FaceDetectionModel", back_populates="faces"
    )
