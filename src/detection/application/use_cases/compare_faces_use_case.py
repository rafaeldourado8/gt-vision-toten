"""Compare faces use case."""
from src.core.application.base import UseCase, Result
from src.detection.domain import Face, FaceComparator, FaceEncoding
from ..dtos.detection_dtos import CompareFacesDTO, MatchResultDTO


class CompareFacesUseCase(UseCase[CompareFacesDTO, Result[MatchResultDTO]]):
    """Compare two faces use case."""

    def __init__(self, similarity_threshold: float = 0.6) -> None:
        self._threshold = similarity_threshold

    async def execute(self, input_dto: CompareFacesDTO) -> Result[MatchResultDTO]:
        """Execute use case."""
        try:
            # Create face entities with encodings
            face1 = Face.create(
                bounding_box=None,
                confidence=None,
                encoding=FaceEncoding(input_dto.face1_encoding),
            )
            
            face2 = Face.create(
                bounding_box=None,
                confidence=None,
                encoding=FaceEncoding(input_dto.face2_encoding),
            )
            
            # Compare faces
            confidence = FaceComparator.compare(face1, face2)
            matched = confidence.value >= self._threshold
            
            return Result.ok(MatchResultDTO(
                matched=matched,
                confidence=confidence.value,
                similarity_percentage=confidence.percentage,
            ))
            
        except Exception as e:
            return Result.fail(str(e))
