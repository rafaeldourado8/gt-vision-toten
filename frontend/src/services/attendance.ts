import api from "./api";

export interface AttendanceRecord {
  id: string;
  student_id: string;
  camera_id: string;
  timestamp: string;
  status: "PRESENT" | "LATE" | "ABSENT";
  confidence: number;
  is_high_confidence: boolean;
}

export interface AttendanceReport {
  date: string;
  total_students: number;
  present_count: number;
  absent_count: number;
  late_count: number;
  records: AttendanceRecord[];
}

export const attendanceService = {
  register: async (data: {
    student_id: string;
    camera_id: string;
    confidence: number;
  }) => {
    const response = await api.post("/attendance", data);
    return response.data;
  },

  getReport: async (date: string): Promise<AttendanceReport> => {
    const response = await api.get(`/attendance/report/${date}`);
    return response.data;
  },

  getStudentHistory: async (
    studentId: string,
    startDate?: string,
    endDate?: string
  ) => {
    const params = new URLSearchParams();
    if (startDate) params.append("start_date", startDate);
    if (endDate) params.append("end_date", endDate);

    const response = await api.get(
      `/attendance/student/${studentId}?${params.toString()}`
    );
    return response.data;
  },

  exportExcel: async (date: string) => {
    const response = await api.get(`/attendance/export/${date}`, {
      responseType: "blob",
    });
    
    // Download file
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", `attendance_${date}.xlsx`);
    document.body.appendChild(link);
    link.click();
    link.remove();
  },
};
