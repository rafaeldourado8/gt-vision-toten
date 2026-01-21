# 🏗️ GT-Vision Toten - Arquitetura

## 📐 Visão Geral

Sistema de monitoramento de alunos baseado em **Domain-Driven Design (DDD)** com arquitetura em camadas.

---

## 🎯 Bounded Contexts

```
┌─────────────────────────────────────────────────────────────┐
│                      GT-Vision Toten                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │  Streaming   │  │  Detection   │  │  Attendance  │    │
│  │   Context    │──│   Context    │──│   Context    │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
│         │                  │                  │            │
│         └──────────────────┴──────────────────┘            │
│                           │                                │
│         ┌─────────────────┴─────────────────┐             │
│         │                                   │             │
│  ┌──────────────┐                  ┌──────────────┐      │
│  │   Student    │                  │ Notification │      │
│  │   Context    │                  │   Context    │      │
│  └──────────────┘                  └──────────────┘      │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

### 1. Streaming Context
**Responsabilidade**: Gerenciamento de câmeras e streams RTSP/HLS

**Entidades**:
- Camera (Aggregate Root)
- StreamConfig

**Casos de Uso**:
- Registrar câmera
- Remover câmera
- Obter status
- Listar câmeras

**Integrações**:
- MediaMTX API (porta 9997)

---

### 2. Detection Context
**Responsabilidade**: Detecção e reconhecimento facial

**Entidades**:
- FaceDetection (Aggregate Root)
- Face

**Casos de Uso**:
- Detectar faces
- Comparar faces
- Processar frame

**Integrações**:
- OpenCV
- face_recognition
- MediaMTX (HLS)

---

### 3. Attendance Context
**Responsabilidade**: Registro e gestão de presença

**Entidades**:
- AttendanceRecord (Aggregate Root)
- AttendanceSession

**Casos de Uso**:
- Registrar presença
- Gerar relatório
- Exportar Excel

**Integrações**:
- Detection Context (eventos)
- Student Context (consulta)

---

### 4. Student Context
**Responsabilidade**: Cadastro de alunos

**Entidades**:
- Student (Aggregate Root)

**Casos de Uso**:
- Registrar aluno
- Atualizar foto
- Importar Excel

**Integrações**:
- Detection Context (encodings)

---

### 5. Notification Context
**Responsabilidade**: Notificações e alertas

**Entidades**:
- Notification (Aggregate Root)

**Casos de Uso**:
- Enviar notificação
- Listar notificações

**Integrações**:
- WhatsApp API
- Email SMTP
- Firebase Push

---

## 🧱 Arquitetura em Camadas

```
┌─────────────────────────────────────────────────────────┐
│                  Presentation Layer                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   FastAPI    │  │   WebSocket  │  │  React Web   │ │
│  │  Controllers │  │   Handlers   │  │  Dashboard   │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                 Application Layer                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  Use Cases   │  │     DTOs     │  │   Mappers    │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                   Domain Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  Entities    │  │    Value     │  │   Domain     │ │
│  │  Aggregates  │  │   Objects    │  │   Services   │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│               Infrastructure Layer                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ Repositories │  │   Adapters   │  │   External   │ │
│  │  (SQLite)    │  │  (MediaMTX)  │  │   Services   │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### Regras de Dependência

```
✅ Presentation → Application → Domain
✅ Infrastructure → Domain (implementa interfaces)
❌ Domain → Infrastructure (NUNCA!)
❌ Domain → Application (NUNCA!)
```

---

## 🔄 Fluxo de Dados

### Fluxo de Detecção de Presença

```
1. [RTSP Camera]
      ↓ stream RTSP
2. [MediaMTX Container]
      ↓ converte para HLS
3. [StreamProcessorWorker]
      ↓ consome HLS (1 frame/s)
4. [DetectFacesUseCase]
      ↓ detecta faces
5. [OpenCVFaceDetector]
      ↓ retorna faces + encodings
6. [CompareFacesUseCase]
      ↓ compara com alunos
7. [FaceComparator]
      ↓ encontra match
8. [FaceDetectedEvent]
      ↓ publica evento
9. [OnFaceDetectedHandler]
      ↓ escuta evento
10. [RegisterAttendanceUseCase]
      ↓ registra presença
11. [AttendanceRepository]
      ↓ salva no banco
12. [AttendanceRegisteredEvent]
      ↓ publica evento
13. [SendNotificationUseCase]
      ↓ envia notificação
14. [WhatsAppProvider / EmailProvider]
      ↓ notifica pais/professores
```

---

## 🐳 Arquitetura de Containers

```yaml
version: '3.8'

services:
  # Streaming
  mediamtx:
    image: bluenviron/mediamtx:latest
    ports:
      - "8554:8554"  # RTSP
      - "8888:8888"  # HLS
      - "9997:9997"  # API
    volumes:
      - ./mediamtx.yml:/mediamtx.yml

  # Backend API
  api:
    build: ./docker/api
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
      - mediamtx
    environment:
      - DATABASE_URL=sqlite:///data/gtvision.db
      - REDIS_URL=redis://redis:6379
      - MEDIAMTX_API_URL=http://mediamtx:9997

  # Worker de Processamento
  worker:
    build: ./docker/worker
    depends_on:
      - api
      - mediamtx
      - redis
    environment:
      - MEDIAMTX_HLS_URL=http://mediamtx:8888

  # Banco de Dados
  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=gtvision
      - POSTGRES_USER=gtvision
      - POSTGRES_PASSWORD=gtvision123

  # Cache
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  # Frontend
  web:
    build: ./docker/web
    ports:
      - "3000:3000"
    depends_on:
      - api

  # Monitoramento
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3001:3000"
    depends_on:
      - prometheus

volumes:
  postgres_data:
```

---

## 📊 Modelo de Dados

### Diagrama ER

```
┌─────────────────┐
│    students     │
├─────────────────┤
│ id (PK)         │
│ name            │
│ class_room      │
│ face_encoding   │◄────┐
│ photo_path      │     │
│ is_active       │     │
│ created_at      │     │
└─────────────────┘     │
                        │
┌─────────────────┐     │
│    cameras      │     │
├─────────────────┤     │
│ id (PK)         │     │
│ name            │     │
│ rtsp_url        │     │
│ stream_path     │     │
│ status          │     │
│ location        │     │
└─────────────────┘     │
        │               │
        │               │
        ▼               │
┌─────────────────┐     │
│ face_detections │     │
├─────────────────┤     │
│ id (PK)         │     │
│ camera_id (FK)  │─────┘
│ timestamp       │
│ faces (JSON)    │
└─────────────────┘
        │
        │
        ▼
┌─────────────────┐
│ attendance_     │
│    records      │
├─────────────────┤
│ id (PK)         │
│ student_id (FK) │
│ camera_id (FK)  │
│ timestamp       │
│ status          │
│ confidence      │
└─────────────────┘
```

---

## 🔐 Segurança

### Autenticação
- JWT tokens
- Refresh tokens
- RBAC (Role-Based Access Control)

### Autorização
- Admin: Acesso total
- Professor: Visualizar presença da turma
- Pais: Visualizar presença do filho

### Dados Sensíveis
- Face encodings criptografados
- Fotos armazenadas com permissões restritas
- Logs sem dados pessoais

---

## 📈 Escalabilidade

### Horizontal Scaling
- Workers podem ser escalados independentemente
- API stateless (pode ter múltiplas instâncias)
- Redis para cache distribuído

### Performance
- Cache de encodings (Redis, TTL 24h)
- Processamento assíncrono (Celery/RQ)
- CDN para assets estáticos

### Limites
- 500 alunos ativos
- 5 câmeras simultâneas
- 1 frame/segundo por câmera
- 58 RPS

---

## 🔧 Tecnologias

### Backend
- **Python 3.11+**
- **FastAPI** - API REST
- **SQLAlchemy** - ORM
- **Alembic** - Migrations
- **Pydantic** - Validação
- **pytest** - Testes

### Frontend
- **React 18** - UI
- **TypeScript** - Type safety
- **TailwindCSS** - Styling
- **React Query** - Data fetching
- **Zustand** - State management

### Streaming
- **MediaMTX** - Server RTSP/HLS/WebRTC
- **OpenCV** - Processamento de vídeo
- **FFmpeg** - Conversão de vídeo

### Detecção
- **DeepFace** - Detecção e reconhecimento
- **TensorFlow** - Backend ML
- **OpenCV DNN** - Detecção rápida

### Infraestrutura
- **Docker** - Containerização
- **Redis** - Cache + Queue
- **PostgreSQL** - Banco principal
- **Nginx** - Reverse proxy
- **Prometheus + Grafana** - Monitoramento

---

## 📝 Decisões Arquiteturais

### 1. Por que DDD?
- Sistema complexo com múltiplos domínios
- Regras de negócio ricas
- Facilita manutenção e evolução

### 2. Por que Bounded Contexts separados?
- Isolamento de responsabilidades
- Equipes podem trabalhar em paralelo
- Facilita testes e deploy independente

### 3. Por que MediaMTX?
- Open source
- Suporta RTSP, HLS, WebRTC
- API REST para gerenciamento
- Leve e performático

### 4. Por que processar 1 frame/segundo?
- Reduz carga de CPU
- Suficiente para detecção de presença
- Aluno fica ~5s em frente à câmera

### 5. Por que SQLite em dev?
- Zero configuração
- Fácil para testes
- Migração simples para PostgreSQL

### 6. Por que Redis?
- Cache de encodings (performance)
- Detecção de duplicatas (TTL 60s)
- Queue para processamento assíncrono

---

**Versão**: 1.0.0  
**Data**: 2025-01-18  
**Status**: 📋 Planejamento
