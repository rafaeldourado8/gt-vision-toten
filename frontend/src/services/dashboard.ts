import api from "./api";

export interface DashboardStats {
  total_students: number;
  total_cameras: number;
  cameras_online: number;
  today_attendance: {
    present: number;
    late: number;
    absent: number;
  };
  last_detections: Array<{
    student_name: string;
    timestamp: string;
    camera: string;
    status: string;
  }>;
}

export interface AttendanceChartData {
  labels: string[];
  present: number[];
  late: number[];
  absent: number[];
}

export const dashboardService = {
  getStats: async (): Promise<DashboardStats> => {
    const { data } = await api.get("/dashboard/stats");
    return data;
  },

  getAttendanceChart: async (): Promise<AttendanceChartData> => {
    const { data } = await api.get("/dashboard/attendance-chart");
    return data;
  },
};
