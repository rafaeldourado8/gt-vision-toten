import api from "./api";

export interface FaceDetection {
  id: string;
  camera_id: string;
  timestamp: string;
  faces: Array<{
    id: string;
    bounding_box: {
      x: number;
      y: number;
      width: number;
      height: number;
    };
    confidence: number;
    has_encoding: boolean;
  }>;
  face_count: number;
}

export const detectionService = {
  detectFaces: async (cameraId: string, frame: File): Promise<FaceDetection> => {
    const formData = new FormData();
    formData.append("frame", frame);

    const response = await api.post(`/detections/detect/${cameraId}`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  },

  compareFaces: async (
    face1Encoding: number[],
    face2Encoding: number[]
  ) => {
    const response = await api.post("/detections/compare", {
      face1_encoding: face1Encoding,
      face2_encoding: face2Encoding,
    });
    return response.data;
  },

  getRecentDetections: async (cameraId: string): Promise<FaceDetection[]> => {
    const response = await api.get(`/detections/recent/${cameraId}`);
    return response.data;
  },
};
