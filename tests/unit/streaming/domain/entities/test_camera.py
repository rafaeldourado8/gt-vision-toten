"""Tests for Camera entity."""
import pytest
from uuid import uuid4
from src.streaming.domain.entities.camera import Camera
from src.streaming.domain.value_objects.rtsp_url import RtspUrl
from src.streaming.domain.value_objects.stream_path import StreamPath
from src.streaming.domain.value_objects.camera_status import CameraStatus
from src.core.domain.errors import ValidationException


def test_create_camera():
    """Test create camera."""
    camera = Camera.create(
        name="Camera 01",
        rtsp_url=RtspUrl("rtsp://192.168.1.100/stream"),
        stream_path=StreamPath("camera-01"),
        location="Entrance",
    )
    assert camera.name == "Camera 01"
    assert camera.location == "Entrance"
    assert camera.status == CameraStatus.OFFLINE


def test_camera_without_name_raises_error():
    """Test camera without name raises error."""
    with pytest.raises(ValidationException):
        Camera(
            name="",
            rtsp_url=RtspUrl("rtsp://192.168.1.100/stream"),
            stream_path=StreamPath("camera-01"),
        )


def test_camera_activate():
    """Test camera activate."""
    camera = Camera.create(
        name="Camera 01",
        rtsp_url=RtspUrl("rtsp://192.168.1.100/stream"),
        stream_path=StreamPath("camera-01"),
    )
    camera.activate()
    assert camera.status == CameraStatus.ONLINE
    assert camera.is_online


def test_camera_deactivate():
    """Test camera deactivate."""
    camera = Camera.create(
        name="Camera 01",
        rtsp_url=RtspUrl("rtsp://192.168.1.100/stream"),
        stream_path=StreamPath("camera-01"),
    )
    camera.activate()
    camera.deactivate()
    assert camera.status == CameraStatus.OFFLINE
    assert not camera.is_online


def test_camera_set_error():
    """Test camera set error."""
    camera = Camera.create(
        name="Camera 01",
        rtsp_url=RtspUrl("rtsp://192.168.1.100/stream"),
        stream_path=StreamPath("camera-01"),
    )
    camera.set_error()
    assert camera.status == CameraStatus.ERROR


def test_camera_equality_by_id():
    """Test camera equality by ID."""
    camera_id = uuid4()
    camera1 = Camera(
        entity_id=camera_id,
        name="Camera 01",
        rtsp_url=RtspUrl("rtsp://192.168.1.100/stream"),
        stream_path=StreamPath("camera-01"),
    )
    camera2 = Camera(
        entity_id=camera_id,
        name="Camera 02",
        rtsp_url=RtspUrl("rtsp://192.168.1.200/stream"),
        stream_path=StreamPath("camera-02"),
    )
    assert camera1 == camera2
