"""DeepFace adapter for face detection."""
import cv2
import numpy as np
from typing import List
from deepface import DeepFace
from src.detection.domain import Face, Confidence, BoundingBox, FaceEncoding


class DeepFaceAdapter:
    """DeepFace adapter."""

    def __init__(
        self,
        detector_backend: str = "opencv",
        model_name: str = "Facenet512",
    ) -> None:
        self._detector_backend = detector_backend
        self._model_name = model_name

    async def detect(self, frame_bytes: bytes) -> List[Face]:
        """Detect faces in frame."""
        try:
            # Convert bytes to numpy array
            nparr = np.frombuffer(frame_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if img is None:
                return []

            # Detect faces with DeepFace
            results = DeepFace.extract_faces(
                img_path=img,
                detector_backend=self._detector_backend,
                enforce_detection=False,
            )

            faces = []
            for result in results:
                # Get bounding box
                facial_area = result.get("facial_area", {})
                x = facial_area.get("x", 0)
                y = facial_area.get("y", 0)
                w = facial_area.get("w", 0)
                h = facial_area.get("h", 0)

                # Get confidence
                confidence_value = result.get("confidence", 0.0)

                # Create face entity
                face = Face.create(
                    bounding_box=BoundingBox(x=x, y=y, width=w, height=h),
                    confidence=Confidence(min(1.0, max(0.0, confidence_value))),
                )

                faces.append(face)

            return faces

        except Exception as e:
            print(f"Error detecting faces: {e}")
            return []

    async def extract_embedding(self, frame_bytes: bytes) -> FaceEncoding | None:
        """Extract face embedding from frame."""
        try:
            # Convert bytes to numpy array
            nparr = np.frombuffer(frame_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if img is None:
                return None

            # Extract embedding
            embedding_objs = DeepFace.represent(
                img_path=img,
                model_name=self._model_name,
                detector_backend=self._detector_backend,
                enforce_detection=False,
            )

            if not embedding_objs:
                return None

            # Get first face embedding
            embedding = embedding_objs[0].get("embedding", [])
            
            if not embedding:
                return None

            return FaceEncoding(embedding)

        except Exception as e:
            print(f"Error extracting embedding: {e}")
            return None
