import api from "./api";

export interface Student {
  id: string;
  name: string;
  grade: string;
  section: string;
  class_room: string;
  has_face_profile: boolean;
  has_face_encoding: boolean;
  is_active: boolean;
  created_at?: string;
  updated_at?: string;
}

export interface CreateStudentRequest {
  name: string;
  grade: string;
  section: string;
}

export const studentsService = {
  getAll: async (): Promise<Student[]> => {
    const { data } = await api.get("/students");
    return data;
  },

  getById: async (id: string): Promise<Student> => {
    const { data } = await api.get(`/students/${id}`);
    return data;
  },

  create: async (student: CreateStudentRequest): Promise<Student> => {
    const { data } = await api.post("/students", student);
    return data;
  },

  delete: async (id: string): Promise<void> => {
    await api.delete(`/students/${id}`);
  },

  uploadPhoto: async (id: string, photo: File): Promise<Student> => {
    const formData = new FormData();
    formData.append("photo", photo);
    const { data } = await api.put(`/students/${id}/photo`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return data;
  },

  importExcel: async (file: File): Promise<{ imported: number; failed: number; errors: any[] }> => {
    const formData = new FormData();
    formData.append("file", file);
    const { data } = await api.post("/students/import", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return data;
  },
};
