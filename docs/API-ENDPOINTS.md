# 📡 GT-Vision Toten - API Endpoints

**Base URL**: `http://localhost:8000`

---

## 🔐 Authentication

### POST /auth/login
Login de usuário

**Request:**
```json
{
  "email": "admin@gtvision.com",
  "password": "senha123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "email": "admin@gtvision.com",
    "name": "Admin",
    "role": "admin"
  }
}
```

---

## 📹 Cameras (Streaming)

### POST /cameras
Registrar nova câmera

**Request:**
```json
{
  "name": "Câmera Entrada",
  "rtsp_url": "rtsp://192.168.1.100/stream",
  "location": "Portaria Principal"
}
```

**Response:**
```json
{
  "id": "uuid",
  "name": "Câmera Entrada",
  "rtsp_url": "rtsp://192.168.1.100/stream",
  "stream_path": "camera-entrada-abc123",
  "status": "OFFLINE",
  "location": "Portaria Principal",
  "created_at": "2025-01-18T10:00:00Z",
  "updated_at": "2025-01-18T10:00:00Z"
}
```

### GET /cameras
Listar todas as câmeras

**Response:**
```json
[
  {
    "id": "uuid",
    "name": "Câmera Entrada",
    "stream_path": "camera-entrada-abc123",
    "status": "ONLINE",
    "location": "Portaria Principal"
  }
]
```

### GET /cameras/{camera_id}/status
Status da câmera

**Response:**
```json
{
  "id": "uuid",
  "name": "Câmera Entrada",
  "status": "ONLINE",
  "is_online": true
}
```

### DELETE /cameras/{camera_id}
Remover câmera

**Response:** `204 No Content`

### GET /cameras/{camera_id}/stream
URL do stream HLS

**Response:**
```json
{
  "hls_url": "http://localhost:8888/camera-entrada-abc123/index.m3u8"
}
```

---

## 🎓 Students (Alunos)

### POST /students
Cadastrar novo aluno

**Request:**
```json
{
  "name": "João Silva",
  "grade": "5º Ano",
  "section": "A"
}
```

**Response:**
```json
{
  "id": "uuid",
  "name": "João Silva",
  "grade": "5º Ano",
  "section": "A",
  "class_room": "5º Ano - A",
  "has_face_profile": false,
  "has_face_encoding": false,
  "is_active": true,
  "created_at": "2025-01-18T10:00:00Z",
  "updated_at": "2025-01-18T10:00:00Z"
}
```

### GET /students
Listar todos os alunos

**Response:**
```json
[
  {
    "id": "uuid",
    "name": "João Silva",
    "class_room": "5º Ano - A",
    "has_face_profile": true,
    "is_active": true
  }
]
```

### GET /students/{student_id}
Detalhes do aluno

**Response:**
```json
{
  "id": "uuid",
  "name": "João Silva",
  "grade": "5º Ano",
  "section": "A",
  "class_room": "5º Ano - A",
  "has_face_profile": true,
  "has_face_encoding": true,
  "is_active": true
}
```

### PUT /students/{student_id}/photo
Upload de foto do aluno

**Request:** `multipart/form-data`
- `photo`: arquivo de imagem (JPG/PNG)

**Response:**
```json
{
  "id": "uuid",
  "name": "João Silva",
  "has_face_profile": true,
  "has_face_encoding": true
}
```

### DELETE /students/{student_id}
Remover aluno

**Response:** `204 No Content`

### POST /students/import
Importar alunos via Excel/CSV

**Request:** `multipart/form-data`
- `file`: arquivo Excel/CSV

**Response:**
```json
{
  "imported": 50,
  "failed": 2,
  "errors": [
    {"row": 3, "error": "Nome inválido"},
    {"row": 7, "error": "Turma não encontrada"}
  ]
}
```

---

## 🤖 Detection (Detecção Facial)

### POST /detections/detect/{camera_id}
Detectar faces em frame

**Request:** `multipart/form-data`
- `frame`: imagem do frame

**Response:**
```json
{
  "id": "uuid",
  "camera_id": "uuid",
  "timestamp": "2025-01-18T10:00:00Z",
  "faces": [
    {
      "id": "uuid",
      "bounding_box": {
        "x": 100,
        "y": 150,
        "width": 200,
        "height": 250
      },
      "confidence": 0.95,
      "has_encoding": true
    }
  ],
  "face_count": 1
}
```

### POST /detections/compare
Comparar duas faces

**Request:**
```json
{
  "face1_encoding": [0.1, 0.2, ...],
  "face2_encoding": [0.15, 0.22, ...]
}
```

**Response:**
```json
{
  "matched": true,
  "confidence": 0.87,
  "similarity_percentage": 87.5
}
```

### GET /detections/recent/{camera_id}
Detecções recentes da câmera

**Response:**
```json
[
  {
    "id": "uuid",
    "camera_id": "uuid",
    "timestamp": "2025-01-18T10:00:00Z",
    "face_count": 2
  }
]
```

---

## ✅ Attendance (Presença)

### POST /attendance
Registrar presença

**Request:**
```json
{
  "student_id": "uuid",
  "camera_id": "uuid",
  "confidence": 0.92
}
```

**Response:**
```json
{
  "id": "uuid",
  "student_id": "uuid",
  "camera_id": "uuid",
  "timestamp": "2025-01-18T08:15:00Z",
  "status": "PRESENT",
  "confidence": 0.92,
  "is_high_confidence": true
}
```

### GET /attendance/report/{date}
Relatório de presença por data

**Example:** `/attendance/report/2025-01-18`

**Response:**
```json
{
  "date": "2025-01-18",
  "total_students": 150,
  "present_count": 142,
  "absent_count": 5,
  "late_count": 3,
  "records": [
    {
      "id": "uuid",
      "student_id": "uuid",
      "timestamp": "2025-01-18T08:15:00Z",
      "status": "PRESENT",
      "confidence": 0.92
    }
  ]
}
```

### GET /attendance/student/{student_id}
Histórico de presença do aluno

**Query params:**
- `start_date`: data inicial (YYYY-MM-DD)
- `end_date`: data final (YYYY-MM-DD)

**Response:**
```json
[
  {
    "id": "uuid",
    "timestamp": "2025-01-18T08:15:00Z",
    "status": "PRESENT",
    "confidence": 0.92
  }
]
```

### GET /attendance/export/{date}
Exportar relatório em Excel

**Response:** Arquivo Excel para download

---

## 📊 Dashboard (Estatísticas)

### GET /dashboard/stats
Estatísticas gerais

**Response:**
```json
{
  "total_students": 150,
  "total_cameras": 5,
  "cameras_online": 4,
  "today_attendance": {
    "present": 142,
    "late": 3,
    "absent": 5
  },
  "last_detections": [
    {
      "student_name": "João Silva",
      "timestamp": "2025-01-18T08:15:00Z",
      "camera": "Câmera Entrada"
    }
  ]
}
```

### GET /dashboard/attendance-chart
Dados para gráfico de presença (últimos 7 dias)

**Response:**
```json
{
  "labels": ["12/01", "13/01", "14/01", "15/01", "16/01", "17/01", "18/01"],
  "present": [145, 148, 142, 150, 147, 143, 142],
  "late": [3, 2, 5, 0, 2, 4, 3],
  "absent": [2, 0, 3, 0, 1, 3, 5]
}
```

---

## 🔔 Notifications (Notificações)

### GET /notifications
Listar notificações do usuário

**Response:**
```json
[
  {
    "id": "uuid",
    "type": "attendance",
    "title": "Presença Registrada",
    "message": "João Silva registrou presença às 08:15",
    "read": false,
    "created_at": "2025-01-18T08:15:00Z"
  }
]
```

### PUT /notifications/{notification_id}/read
Marcar notificação como lida

**Response:** `204 No Content`

---

## 🏥 Health Check

### GET /health
Status da API

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "services": {
    "database": "connected",
    "redis": "connected",
    "rabbitmq": "connected",
    "mediamtx": "connected"
  }
}
```

---

## 📝 Total de Endpoints: 28

**Autenticação**: 1  
**Câmeras**: 6  
**Alunos**: 6  
**Detecção**: 3  
**Presença**: 4  
**Dashboard**: 2  
**Notificações**: 2  
**Health**: 1  
**WebSocket**: 3 (tempo real)
