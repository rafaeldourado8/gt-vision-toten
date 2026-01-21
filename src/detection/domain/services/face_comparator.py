"""Face comparator domain service."""
import numpy as np
from .entities.face import Face
from .value_objects.confidence import Confidence


class FaceComparator:
    """Face comparator service."""

    SIMILARITY_THRESHOLD = 0.6  # DeepFace default

    @staticmethod
    def compare(face1: Face, face2: Face) -> Confidence:
        """Compare two faces and return similarity confidence."""
        if not face1.has_encoding or not face2.has_encoding:
            return Confidence(0.0)

        # Calculate cosine similarity
        embedding1 = np.array(face1.encoding.embedding)
        embedding2 = np.array(face2.encoding.embedding)

        # Normalize
        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)

        if norm1 == 0 or norm2 == 0:
            return Confidence(0.0)

        # Cosine similarity
        similarity = np.dot(embedding1, embedding2) / (norm1 * norm2)
        
        # Convert to confidence (0-1 range)
        confidence_value = float((similarity + 1) / 2)  # Map from [-1,1] to [0,1]
        
        return Confidence(max(0.0, min(1.0, confidence_value)))

    @staticmethod
    def is_match(face1: Face, face2: Face, threshold: float | None = None) -> bool:
        """Check if two faces match."""
        threshold = threshold or FaceComparator.SIMILARITY_THRESHOLD
        confidence = FaceComparator.compare(face1, face2)
        return confidence.value >= threshold

    @staticmethod
    def find_best_match(target_face: Face, candidate_faces: list[Face]) -> tuple[Face | None, Confidence]:
        """Find best matching face from candidates."""
        if not candidate_faces:
            return None, Confidence(0.0)

        best_face = None
        best_confidence = Confidence(0.0)

        for candidate in candidate_faces:
            confidence = FaceComparator.compare(target_face, candidate)
            if confidence.value > best_confidence.value:
                best_face = candidate
                best_confidence = confidence

        return best_face, best_confidence
