"""Tests for StreamPath."""
import pytest
from src.streaming.domain.value_objects.stream_path import StreamPath
from src.core.domain.errors import ValidationException


def test_valid_stream_path():
    """Test valid stream path."""
    path = StreamPath("camera-01")
    assert path.value == "camera-01"


def test_stream_path_with_underscore():
    """Test stream path with underscore."""
    path = StreamPath("camera_01")
    assert path.value == "camera_01"


def test_invalid_stream_path_with_special_chars():
    """Test invalid stream path with special characters."""
    with pytest.raises(ValidationException):
        StreamPath("camera@01")


def test_invalid_stream_path_too_long():
    """Test invalid stream path too long."""
    with pytest.raises(ValidationException):
        StreamPath("a" * 51)


def test_invalid_stream_path_empty():
    """Test invalid empty stream path."""
    with pytest.raises(ValidationException):
        StreamPath("")


def test_stream_path_str():
    """Test stream path string representation."""
    path = StreamPath("camera-01")
    assert str(path) == "camera-01"
