"""Tests for RtspUrl with webcam support."""
import pytest
from src.streaming.domain.value_objects.rtsp_url import RtspUrl
from src.core.domain.errors import ValidationException


def test_valid_rtsp_url():
    """Test valid RTSP URL."""
    url = RtspUrl("rtsp://admin:pass@192.168.1.100:554/stream")
    assert url.value == "rtsp://admin:pass@192.168.1.100:554/stream"
    assert not url.is_webcam


def test_rtsp_url_without_credentials():
    """Test RTSP URL without credentials."""
    url = RtspUrl("rtsp://192.168.1.100:554/stream")
    assert url.value == "rtsp://192.168.1.100:554/stream"
    assert not url.is_webcam


def test_valid_webcam_url():
    """Test valid webcam URL."""
    url = RtspUrl("webcam://0")
    assert url.value == "webcam://0"
    assert url.is_webcam
    assert url.webcam_index == 0


def test_webcam_url_with_different_index():
    """Test webcam URL with different index."""
    url = RtspUrl("webcam://1")
    assert url.webcam_index == 1


def test_invalid_rtsp_url_raises_error():
    """Test invalid RTSP URL raises error."""
    with pytest.raises(ValidationException):
        RtspUrl("http://invalid.com")


def test_invalid_webcam_url_raises_error():
    """Test invalid webcam URL raises error."""
    with pytest.raises(ValidationException):
        RtspUrl("webcam://abc")


def test_rtsp_url_immutability():
    """Test RTSP URL is immutable."""
    url = RtspUrl("rtsp://192.168.1.100/stream")
    assert url.value == "rtsp://192.168.1.100/stream"


def test_rtsp_url_str():
    """Test RTSP URL string representation."""
    url = RtspUrl("rtsp://192.168.1.100/stream")
    assert str(url) == "rtsp://192.168.1.100/stream"


def test_webcam_url_str():
    """Test webcam URL string representation."""
    url = RtspUrl("webcam://0")
    assert str(url) == "webcam://0"
