"""Tests for RegisterCameraUseCase."""
import pytest
from src.streaming.application import RegisterCameraUseCase, RegisterCameraDTO
from tests.mocks.in_memory_camera_repository import InMemoryCameraRepository


@pytest.mark.asyncio
async def test_register_camera_success():
    """Test register camera success."""
    repository = InMemoryCameraRepository()
    use_case = RegisterCameraUseCase(repository)

    dto = RegisterCameraDTO(
        name="Camera 01",
        rtsp_url="rtsp://192.168.1.100/stream",
        location="Entrance",
    )

    result = await use_case.execute(dto)

    assert result.is_success
    assert result.value.name == "Camera 01"
    assert result.value.location == "Entrance"
    assert result.value.status == "OFFLINE"


@pytest.mark.asyncio
async def test_register_camera_with_invalid_rtsp_url():
    """Test register camera with invalid RTSP URL."""
    repository = InMemoryCameraRepository()
    use_case = RegisterCameraUseCase(repository)

    dto = RegisterCameraDTO(
        name="Camera 01",
        rtsp_url="http://invalid.com",
        location="Entrance",
    )

    result = await use_case.execute(dto)

    assert result.is_failure
    assert "Invalid RTSP URL" in result.error


@pytest.mark.asyncio
async def test_register_camera_generates_unique_stream_path():
    """Test register camera generates unique stream path."""
    repository = InMemoryCameraRepository()
    use_case = RegisterCameraUseCase(repository)

    dto1 = RegisterCameraDTO(name="Camera 01", rtsp_url="rtsp://192.168.1.100/stream")
    dto2 = RegisterCameraDTO(name="Camera 01", rtsp_url="rtsp://192.168.1.101/stream")

    result1 = await use_case.execute(dto1)
    result2 = await use_case.execute(dto2)

    assert result1.is_success
    assert result2.is_success
    assert result1.value.stream_path != result2.value.stream_path
