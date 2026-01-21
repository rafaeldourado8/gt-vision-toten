"""Tests for CameraStatus."""
import pytest
from src.streaming.domain.value_objects.camera_status import CameraStatus


def test_camera_status_values():
    """Test camera status enum values."""
    assert CameraStatus.ONLINE == "ONLINE"
    assert CameraStatus.OFFLINE == "OFFLINE"
    assert CameraStatus.ERROR == "ERROR"
    assert CameraStatus.CONNECTING == "CONNECTING"


def test_camera_status_is_string_enum():
    """Test camera status is string enum."""
    assert isinstance(CameraStatus.ONLINE, str)
    assert isinstance(CameraStatus.OFFLINE, str)
