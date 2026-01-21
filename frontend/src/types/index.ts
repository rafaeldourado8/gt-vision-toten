export interface User {
  id: string;
  email: string;
  name: string;
  role: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface Camera {
  id: string;
  name: string;
  stream_path: string;
  status: "ONLINE" | "OFFLINE";
  location: string;
  rtsp_url?: string;
  created_at?: string;
  updated_at?: string;
}

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

export interface AttendanceRecord {
  id: string;
  student_id: string;
  camera_id: string;
  timestamp: string;
  status: "PRESENT" | "LATE" | "ABSENT";
  confidence: number;
  is_high_confidence: boolean;
}

export interface Notification {
  id: string;
  type: "attendance" | "camera" | "student" | "system";
  title: string;
  message: string;
  read: boolean;
  created_at: string;
}

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
  }>;
}
