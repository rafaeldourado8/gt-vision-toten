"""Detection controllers."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from src.detection.application import (
    DetectFacesUseCase,
    CompareFacesUseCase,
    GetRecentDetectionsUseCase,
    DetectFacesDTO,
    CompareFacesDTO,
    FaceDetectionDTO,
    MatchResultDTO,
)

router = APIRouter(prefix="/detections", tags=["detections"])


# Dependency injection (será configurado no main.py)
def get_detect_faces_use_case() -> DetectFacesUseCase:
    """Get detect faces use case."""
    raise NotImplementedError


def get_compare_faces_use_case() -> CompareFacesUseCase:
    """Get compare faces use case."""
    raise NotImplementedError


def get_recent_detections_use_case() -> GetRecentDetectionsUseCase:
    """Get recent detections use case."""
    raise NotImplementedError


@router.post("/detect/{camera_id}", response_model=FaceDetectionDTO)
async def detect_faces(
    camera_id: str,
    frame: UploadFile = File(...),
    use_case: DetectFacesUseCase = Depends(get_detect_faces_use_case),
) -> FaceDetectionDTO:
    """Detect faces in frame."""
    frame_bytes = await frame.read()
    
    dto = DetectFacesDTO(
        frame_bytes=frame_bytes,
        camera_id=camera_id,
    )
    
    result = await use_case.execute(dto)
    
    if result.is_failure:
        raise HTTPException(status_code=400, detail=result.error)
    
    return result.value


@router.post("/compare", response_model=MatchResultDTO)
async def compare_faces(
    dto: CompareFacesDTO,
    use_case: CompareFacesUseCase = Depends(get_compare_faces_use_case),
) -> MatchResultDTO:
    """Compare two faces."""
    result = await use_case.execute(dto)
    
    if result.is_failure:
        raise HTTPException(status_code=400, detail=result.error)
    
    return result.value


@router.get("/recent/{camera_id}", response_model=List[FaceDetectionDTO])
async def get_recent_detections(
    camera_id: str,
    use_case: GetRecentDetectionsUseCase = Depends(get_recent_detections_use_case),
) -> List[FaceDetectionDTO]:
    """Get recent detections for camera."""
    result = await use_case.execute(camera_id)
    
    if result.is_failure:
        raise HTTPException(status_code=404, detail=result.error)
    
    return result.value
