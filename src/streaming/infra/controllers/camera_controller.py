"""Camera controllers."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from src.streaming.application import (
    RegisterCameraUseCase,
    RemoveCameraUseCase,
    GetCameraStatusUseCase,
    ListCamerasUseCase,
    RegisterCameraDTO,
    CameraDTO,
    CameraStatusDTO,
)

router = APIRouter(prefix="/cameras", tags=["cameras"])


# Dependency injection (será configurado no main.py)
def get_register_camera_use_case() -> RegisterCameraUseCase:
    """Get register camera use case."""
    raise NotImplementedError


def get_remove_camera_use_case() -> RemoveCameraUseCase:
    """Get remove camera use case."""
    raise NotImplementedError


def get_camera_status_use_case() -> GetCameraStatusUseCase:
    """Get camera status use case."""
    raise NotImplementedError


def get_list_cameras_use_case() -> ListCamerasUseCase:
    """Get list cameras use case."""
    raise NotImplementedError


@router.post("", response_model=CameraDTO, status_code=201)
async def register_camera(
    dto: RegisterCameraDTO,
    use_case: RegisterCameraUseCase = Depends(get_register_camera_use_case),
) -> CameraDTO:
    """Register new camera."""
    result = await use_case.execute(dto)
    
    if result.is_failure:
        raise HTTPException(status_code=400, detail=result.error)
    
    return result.value


@router.delete("/{camera_id}", status_code=204)
async def remove_camera(
    camera_id: str,
    use_case: RemoveCameraUseCase = Depends(get_remove_camera_use_case),
) -> None:
    """Remove camera."""
    result = await use_case.execute(camera_id)
    
    if result.is_failure:
        raise HTTPException(status_code=404, detail=result.error)


@router.get("/{camera_id}/status", response_model=CameraStatusDTO)
async def get_camera_status(
    camera_id: str,
    use_case: GetCameraStatusUseCase = Depends(get_camera_status_use_case),
) -> CameraStatusDTO:
    """Get camera status."""
    result = await use_case.execute(camera_id)
    
    if result.is_failure:
        raise HTTPException(status_code=404, detail=result.error)
    
    return result.value


@router.get("", response_model=List[CameraDTO])
async def list_cameras(
    use_case: ListCamerasUseCase = Depends(get_list_cameras_use_case),
) -> List[CameraDTO]:
    """List all cameras."""
    result = await use_case.execute()
    
    if result.is_failure:
        raise HTTPException(status_code=500, detail=result.error)
    
    return result.value
