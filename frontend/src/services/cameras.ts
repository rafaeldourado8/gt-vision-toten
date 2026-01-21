import api from "./api";

export interface Camera {
  id: string;
  name: string;
  rtsp_url?: string;
  stream_path: string;
  status: "ONLINE" | "OFFLINE";
  location: string;
  created_at?: string;
  updated_at?: string;
}

export interface CreateCameraRequest {
  name: string;
  rtsp_url: string;
  location: string;
}

export const camerasService = {
  getAll: async (): Promise<Camera[]> => {
    const { data } = await api.get("/cameras");
    return data;
  },

  create: async (camera: CreateCameraRequest): Promise<Camera> => {
    const { data } = await api.post("/cameras", camera);
    return data;
  },

  delete: async (id: string): Promise<void> => {
    await api.delete(`/cameras/${id}`);
  },

  getStreamUrl: async (id: string): Promise<{ hls_url: string }> => {
    const { data } = await api.get(`/cameras/${id}/stream`);
    return data;
  },

  getStatus: async (id: string): Promise<{ status: string; is_online: boolean }> => {
    const { data } = await api.get(`/cameras/${id}/status`);
    return data;
  },
};
