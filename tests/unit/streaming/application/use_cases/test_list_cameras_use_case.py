"""Tests for ListCamerasUseCase."""
import pytest
from src.streaming.application import (
    ListCamerasUseCase,
    RegisterCameraUseCase,
    RegisterCameraDTO,
)
from tests.mocks.in_memory_camera_repository import InMemoryCameraRepository


@pytest.mark.asyncio
async def test_list_cameras_empty():
    """Test list cameras when empty."""
    repository = InMemoryCameraRepository()
    use_case = ListCamerasUseCase(repository)

    result = await use_case.execute()

    assert result.is_success
    assert len(result.value) == 0


@pytest.mark.asyncio
async def test_list_cameras_with_data():
    """Test list cameras with data."""
    repository = InMemoryCameraRepository()
    register_use_case = RegisterCameraUseCase(repository)
    list_use_case = ListCamerasUseCase(repository)

    # Register 2 cameras
    await register_use_case.execute(
        RegisterCameraDTO(name="Camera 01", rtsp_url="rtsp://192.168.1.100/stream")
    )
    await register_use_case.execute(
        RegisterCameraDTO(name="Camera 02", rtsp_url="rtsp://192.168.1.101/stream")
    )

    result = await list_use_case.execute()

    assert result.is_success
    assert len(result.value) == 2
    assert result.value[0].name == "Camera 01"
    assert result.value[1].name == "Camera 02"
