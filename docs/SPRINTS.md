# 🚀 GT-Vision Toten - Sprints

## 📅 Cronograma Geral

**Total Estimado**: 28-39 dias (~6-8 semanas)

| Sprint | Foco | Duração | Prioridade | Status |
|--------|------|---------|------------|--------|
| 1 | Fundação + Streaming | 3-5 dias | 🔴 CRÍTICA | 📋 To Do |
| 2 | Detection Context | 5-7 dias | 🔴 CRÍTICA | 📋 To Do |
| 3 | Student Context | 3-4 dias | 🔴 CRÍTICA | 📋 To Do |
| 4 | Attendance Context | 5-7 dias | 🔴 CRÍTICA | 📋 To Do |
| 5 | Dashboard Web | 5-7 dias | 🟡 ALTA | 📋 To Do |
| 6 | Notifications + Mobile | 4-5 dias | 🟡 ALTA | 📋 To Do |
| 7 | Deploy + Otimização | 3-4 dias | 🟢 MÉDIA | 📋 To Do |

---

## 🎯 SPRINT 1: Fundação e Estrutura Base

**Duração**: 3-5 dias  
**Objetivo**: Estrutura DDD + Streaming Context funcionando  
**Prioridade**: 🔴 CRÍTICA

### 📋 Tasks

#### 1.1 - Estrutura de Pastas DDD
**Responsável**: Dev  
**Estimativa**: 1h

**Descrição**:
Criar estrutura completa de pastas seguindo DDD.

**Estrutura**:
```
src/
├── @core/                    # Kernel compartilhado
│   ├── domain/
│   │   ├── base/
│   │   ├── value_objects/
│   │   └── errors/
│   ├── application/
│   │   └── base/
│   └── infra/
│       ├── database/
│       └── messaging/
├── streaming/                # Bounded Context 1
│   ├── domain/
│   │   ├── entities/
│   │   ├── value_objects/
│   │   ├── repositories/
│   │   └── errors/
│   ├── application/
│   │   ├── use_cases/
│   │   ├── dtos/
│   │   └── mappers/
│   └── infra/
│       ├── repositories/
│       ├── controllers/
│       └── adapters/
├── detection/                # Bounded Context 2
├── attendance/               # Bounded Context 3
├── student/                  # Bounded Context 4
└── notification/             # Bounded Context 5
```

**Critérios de Aceite**:
- [ ] Todas as pastas criadas
- [ ] `__init__.py` em cada pasta
- [ ] Estrutura espelhada em `tests/`

---

#### 1.2 - Streaming Domain Layer
**Responsável**: Dev  
**Estimativa**: 4-6h

**Entidades**:
- `Camera` (Aggregate Root)
  - Propriedades: id, name, rtsp_url, stream_path, status, location
  - Métodos: activate(), deactivate(), update_status()

**Value Objects**:
- `RtspUrl` - Valida formato RTSP
- `StreamPath` - Path único no MediaMTX
- `CameraStatus` - Enum (ONLINE, OFFLINE, ERROR, CONNECTING)

**Repositories** (Interfaces):
- `CameraRepository`
  - save(camera: Camera) -> None
  - find_by_id(camera_id: UUID) -> Camera | None
  - find_all() -> List[Camera]
  - delete(camera_id: UUID) -> None

**Domain Errors**:
- `InvalidRtspUrlError`
- `CameraNotFoundError`
- `DuplicateStreamPathError`

**Critérios de Aceite**:
- [ ] Camera é Aggregate Root válido
- [ ] Value Objects são imutáveis
- [ ] RtspUrl valida formato `rtsp://user:pass@host:port/path`
- [ ] CameraStatus é Enum
- [ ] Repositories são interfaces (ABC)
- [ ] Complexidade ciclomática < 5
- [ ] Cobertura de testes > 90%
- [ ] Zero dependências externas no domain

**Testes**:
```python
# tests/unit/streaming/domain/entities/test_camera.py
def test_create_camera_with_valid_data()
def test_camera_activate()
def test_camera_deactivate()
def test_camera_equality_by_id()

# tests/unit/streaming/domain/value_objects/test_rtsp_url.py
def test_valid_rtsp_url()
def test_invalid_rtsp_url_raises_error()
def test_rtsp_url_immutability()
```

---

#### 1.3 - Streaming Application Layer
**Responsável**: Dev  
**Estimativa**: 4-6h

**Use Cases**:

1. `RegisterCameraUseCase`
   - Input: RegisterCameraDTO (name, rtsp_url, location)
   - Output: CameraDTO
   - Regras: Valida RTSP, cria stream_path único, registra no MediaMTX

2. `RemoveCameraUseCase`
   - Input: camera_id
   - Output: None
   - Regras: Remove do MediaMTX, deleta do banco

3. `GetCameraStatusUseCase`
   - Input: camera_id
   - Output: CameraStatusDTO
   - Regras: Consulta status no MediaMTX

4. `ListCamerasUseCase`
   - Input: None
   - Output: List[CameraDTO]
   - Regras: Lista todas as câmeras

**DTOs**:
```python
@dataclass
class RegisterCameraDTO:
    name: str
    rtsp_url: str
    location: str

@dataclass
class CameraDTO:
    id: str
    name: str
    rtsp_url: str
    stream_path: str
    status: str
    location: str
    created_at: str
```

**Mappers**:
- `CameraMapper.to_dto(camera: Camera) -> CameraDTO`
- `CameraMapper.to_entity(dto: RegisterCameraDTO) -> Camera`

**Critérios de Aceite**:
- [ ] Use Cases seguem padrão UseCase[InputDTO, OutputDTO]
- [ ] DTOs são dataclasses
- [ ] Mappers isolam conversões
- [ ] Complexidade < 5 por método
- [ ] Cobertura > 90%

---

#### 1.4 - Streaming Infrastructure Layer
**Responsável**: Dev  
**Estimativa**: 6-8h

**Implementações**:

1. `MediaMTXAdapter`
   - Métodos:
     - add_path(stream_path: str, rtsp_url: str) -> bool
     - remove_path(stream_path: str) -> bool
     - get_path_status(stream_path: str) -> dict
     - list_paths() -> List[dict]
   - HTTP Client para API MediaMTX (porta 9997)

2. `InMemoryCameraRepository`
   - Para testes
   - Dict em memória

3. `SQLiteCameraRepository`
   - Implementa CameraRepository
   - SQLAlchemy

**Controllers**:
```python
# streaming/infra/controllers/camera_controller.py
@router.post("/cameras")
async def register_camera(dto: RegisterCameraDTO)

@router.delete("/cameras/{camera_id}")
async def remove_camera(camera_id: str)

@router.get("/cameras/{camera_id}/status")
async def get_camera_status(camera_id: str)

@router.get("/cameras")
async def list_cameras()
```

**Database**:
```sql
CREATE TABLE cameras (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    rtsp_url TEXT NOT NULL,
    stream_path VARCHAR(255) UNIQUE NOT NULL,
    status VARCHAR(50) NOT NULL,
    location VARCHAR(255),
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);
```

**Critérios de Aceite**:
- [ ] MediaMTXAdapter se comunica com API
- [ ] Repositories implementam interfaces do domain
- [ ] Controllers retornam DTOs
- [ ] Migrations criadas
- [ ] Testes de integração passando
- [ ] Docker Compose com MediaMTX + API

---

### 🎯 Entregáveis Sprint 1

- ✅ Estrutura DDD completa
- ✅ Streaming Context funcionando
- ✅ API REST para gerenciar câmeras
- ✅ Integração com MediaMTX
- ✅ Testes unitários + integração
- ✅ Docker Compose funcional

---

## 🎯 SPRINT 2: Detection Context + Integração

**Duração**: 5-7 dias  
**Objetivo**: Detecção facial funcionando end-to-end  
**Prioridade**: 🔴 CRÍTICA

### 📋 Tasks

#### 2.1 - Clonar e Adaptar Repositório de Detecção
**Responsável**: Dev  
**Estimativa**: 2-3h

**Descrição**:
- Clonar repositório de detecção facial
- Extrair apenas código necessário
- Remover dependências desnecessárias
- Adaptar para arquitetura DDD

**Critérios de Aceite**:
- [ ] Código de detecção isolado
- [ ] Dependências mínimas
- [ ] Sem lógica de negócio misturada

---

#### 2.2 - Detection Domain Layer
**Responsável**: Dev  
**Estimativa**: 6-8h

**Entidades**:
- `FaceDetection` (Aggregate Root)
  - Propriedades: id, camera_id, timestamp, faces, frame_id
  - Métodos: add_face(), get_best_face()

- `Face`
  - Propriedades: bounding_box, confidence, encoding
  - Métodos: compare_with(other: Face) -> float

**Value Objects**:
- `Confidence` - Float 0.0-1.0 com validação
- `BoundingBox` - x, y, width, height
- `FaceEncoding` - Array de 128 floats

**Domain Services**:
- `FaceComparator`
  - compare(face1: Face, face2: Face) -> float
  - find_best_match(face: Face, candidates: List[Face]) -> Face | None

**Critérios de Aceite**:
- [ ] FaceDetection é Aggregate Root
- [ ] Face é Entity
- [ ] Value Objects imutáveis
- [ ] FaceComparator usa algoritmo de comparação
- [ ] Complexidade < 5
- [ ] Cobertura > 90%

---

#### 2.3 - Detection Application Layer
**Responsável**: Dev  
**Estimativa**: 6-8h

**Use Cases**:

1. `DetectFacesUseCase`
   - Input: frame (bytes), camera_id
   - Output: List[FaceDTO]
   - Regras: Detecta faces no frame

2. `CompareFacesUseCase`
   - Input: face_encoding, student_id
   - Output: MatchResultDTO (matched: bool, confidence: float)
   - Regras: Compara com encoding do aluno

3. `ProcessFrameUseCase`
   - Input: frame, camera_id
   - Output: DetectionResultDTO
   - Regras: Detecta + compara + registra presença

**Critérios de Aceite**:
- [ ] Use Cases orquestram domain
- [ ] Sem lógica de detecção nos use cases
- [ ] DTOs bem definidos
- [ ] Cobertura > 90%

---

#### 2.4 - Detection Infrastructure Layer
**Responsável**: Dev  
**Estimativa**: 8-10h

**Adaptadores**:

1. `OpenCVFaceDetector`
   - Implementa interface FaceDetector
   - Usa Haar Cascade ou DNN

2. `FaceRecognitionEncoder`
   - Implementa interface FaceEncoder
   - Usa face_recognition lib

**Workers**:

1. `StreamProcessorWorker`
   - Consome frames do MediaMTX (HLS)
   - Processa a cada 1s (não todos os frames)
   - Envia para DetectFacesUseCase
   - Publica eventos de detecção

**Critérios de Aceite**:
- [ ] Worker consome HLS do MediaMTX
- [ ] Processa 1 frame/segundo
- [ ] Publica eventos no EventBus
- [ ] Testes de integração
- [ ] Docker Compose atualizado

---

### 🎯 Entregáveis Sprint 2

- ✅ Detection Context completo
- ✅ Detecção facial funcionando
- ✅ Worker processando streams
- ✅ Eventos de detecção publicados
- ✅ Testes end-to-end

---

## 🎯 SPRINT 3: Student Context

**Duração**: 3-4 dias  
**Objetivo**: Cadastro de alunos com fotos  
**Prioridade**: 🔴 CRÍTICA

### 📋 Tasks

#### 3.1 - Student Domain Layer
**Responsável**: Dev  
**Estimativa**: 4-5h

**Entidades**:
- `Student` (Aggregate Root)
  - Propriedades: id, name, class_room, face_profile, is_active
  - Métodos: update_face_profile(), deactivate()

**Value Objects**:
- `StudentId` - UUID
- `StudentName` - Validação de nome
- `ClassRoom` - Turma + série
- `FaceProfile` - Contém FaceEncoding + foto

**Critérios de Aceite**:
- [ ] Student é Aggregate Root
- [ ] Value Objects imutáveis
- [ ] Validações no domain
- [ ] Cobertura > 90%

---

#### 3.2 - Student Application Layer
**Responsável**: Dev  
**Estimativa**: 5-6h

**Use Cases**:

1. `RegisterStudentUseCase`
   - Input: name, class_room, photo
   - Output: StudentDTO
   - Regras: Valida, extrai encoding, salva

2. `UpdateStudentPhotoUseCase`
   - Input: student_id, photo
   - Output: StudentDTO
   - Regras: Atualiza encoding

3. `ImportStudentsFromExcelUseCase`
   - Input: excel_file
   - Output: ImportResultDTO
   - Regras: Valida, importa em lote

4. `GetStudentByIdUseCase`
   - Input: student_id
   - Output: StudentDTO

**Critérios de Aceite**:
- [ ] Use Cases bem definidos
- [ ] Importação Excel funciona
- [ ] Validações robustas
- [ ] Cobertura > 90%

---

#### 3.3 - Student Infrastructure Layer
**Responsável**: Dev  
**Estimativa**: 6-8h

**Repositories**:
- `SQLiteStudentRepository`

**Controllers**:
```python
@router.post("/students")
async def register_student(dto: RegisterStudentDTO)

@router.put("/students/{student_id}/photo")
async def update_photo(student_id: str, photo: UploadFile)

@router.post("/students/import")
async def import_students(file: UploadFile)

@router.get("/students/{student_id}")
async def get_student(student_id: str)

@router.get("/students")
async def list_students()
```

**Storage**:
- Salvar fotos em `/storage/students/{student_id}.jpg`
- Encodings no banco

**Critérios de Aceite**:
- [ ] API REST completa
- [ ] Upload de fotos funciona
- [ ] Importação Excel funciona
- [ ] Testes de integração

---

### 🎯 Entregáveis Sprint 3

- ✅ Student Context completo
- ✅ Cadastro de alunos
- ✅ Upload de fotos
- ✅ Importação Excel
- ✅ API REST funcional

---

## 🎯 SPRINT 4: Attendance Context

**Duração**: 5-7 dias  
**Objetivo**: Sistema de presença completo  
**Prioridade**: 🔴 CRÍTICA

### 📋 Tasks

#### 4.1 - Attendance Domain Layer
**Responsável**: Dev  
**Estimativa**: 6-8h

**Entidades**:
- `AttendanceRecord` (Aggregate Root)
  - Propriedades: id, student_id, timestamp, status, camera_id, confidence
  - Métodos: mark_as_late(), cancel()

- `AttendanceSession`
  - Propriedades: id, date, start_time, end_time, class_room
  - Métodos: is_active(), is_late()

**Value Objects**:
- `AttendanceStatus` - Enum (PRESENTE, AUSENTE, ATRASADO)
- `TimeWindow` - start, end

**Domain Services**:
- `AttendanceValidator` - Valida regras de presença
- `DuplicateDetector` - Evita duplicatas em 60s

**Critérios de Aceite**:
- [ ] Aggregate Root bem definido
- [ ] Regras de negócio no domain
- [ ] Validações robustas
- [ ] Cobertura > 90%

---

#### 4.2 - Attendance Application Layer
**Responsável**: Dev  
**Estimativa**: 6-8h

**Use Cases**:

1. `RegisterAttendanceUseCase`
   - Input: student_id, camera_id, timestamp, confidence
   - Output: AttendanceRecordDTO
   - Regras: Valida, verifica duplicata, registra

2. `GetAttendanceReportUseCase`
   - Input: date, class_room
   - Output: AttendanceReportDTO
   - Regras: Gera relatório

3. `ExportAttendanceToExcelUseCase`
   - Input: date_range, class_room
   - Output: excel_file
   - Regras: Exporta para Excel

**Event Handlers**:
- `OnFaceDetectedHandler`
  - Escuta FaceDetectedEvent
  - Chama RegisterAttendanceUseCase

**Critérios de Aceite**:
- [ ] Use Cases orquestram domain
- [ ] Event Handler funciona
- [ ] Exportação Excel funciona
- [ ] Cobertura > 90%

---

#### 4.3 - Attendance Infrastructure Layer
**Responsável**: Dev  
**Estimativa**: 8-10h

**Repositories**:
- `SQLiteAttendanceRepository`

**Cache**:
- Redis para duplicatas (TTL 60s)

**Controllers**:
```python
@router.post("/attendance")
async def register_attendance(dto: RegisterAttendanceDTO)

@router.get("/attendance/report")
async def get_report(date: str, class_room: str)

@router.get("/attendance/export")
async def export_excel(date_from: str, date_to: str)
```

**Critérios de Aceite**:
- [ ] API REST completa
- [ ] Cache Redis funciona
- [ ] Event Handler integrado
- [ ] Testes end-to-end

---

### 🎯 Entregáveis Sprint 4

- ✅ Attendance Context completo
- ✅ Registro de presença automático
- ✅ Relatórios funcionando
- ✅ Exportação Excel
- ✅ Sistema end-to-end funcional

---

## 🎯 SPRINT 5: Dashboard Web

**Duração**: 5-7 dias  
**Objetivo**: Interface administrativa completa  
**Prioridade**: 🟡 ALTA

### 📋 Tasks

#### 5.1 - Frontend Base
**Responsável**: Dev  
**Estimativa**: 4-6h

**Stack**:
- React 18 + TypeScript
- Vite
- TailwindCSS
- React Query
- Zustand
- React Router

**Estrutura**:
```
frontend/
├── src/
│   ├── components/
│   ├── pages/
│   ├── hooks/
│   ├── services/
│   ├── stores/
│   └── types/
```

---

#### 5.2 - Páginas
**Responsável**: Dev  
**Estimativa**: 12-16h

**Páginas**:

1. **Dashboard** (`/`)
   - Estatísticas em tempo real
   - Gráficos de presença
   - Status de câmeras
   - Últimas detecções

2. **Alunos** (`/students`)
   - Lista de alunos
   - Cadastro
   - Upload de foto
   - Importação Excel

3. **Câmeras** (`/cameras`)
   - Lista de câmeras
   - Adicionar/remover
   - Visualização de streams (HLS)
   - Status

4. **Relatórios** (`/reports`)
   - Filtros (data, turma)
   - Tabela de presença
   - Exportação Excel
   - Gráficos

**Critérios de Aceite**:
- [ ] Todas as páginas funcionais
- [ ] Design responsivo
- [ ] Loading states
- [ ] Error handling

---

#### 5.3 - WebSocket
**Responsável**: Dev  
**Estimativa**: 6-8h

**Features**:
- Notificações em tempo real
- Status de câmeras ao vivo
- Detecções ao vivo
- Atualizações de presença

**Critérios de Aceite**:
- [ ] WebSocket conecta
- [ ] Eventos em tempo real
- [ ] Reconexão automática

---

### 🎯 Entregáveis Sprint 5

- ✅ Dashboard completo
- ✅ Todas as páginas funcionais
- ✅ WebSocket funcionando
- ✅ UI/UX polida

---

## 🎯 SPRINT 6: Notification Context + Mobile

**Duração**: 4-5 dias  
**Objetivo**: Notificações e app mobile  
**Prioridade**: 🟡 ALTA

### 📋 Tasks

#### 6.1 - Notification Domain Layer
**Responsável**: Dev  
**Estimativa**: 3-4h

**Entidades**:
- `Notification` (Aggregate Root)

**Value Objects**:
- `NotificationType` - Enum (EMAIL, WHATSAPP, PUSH)
- `Recipient` - Email ou telefone

---

#### 6.2 - Notification Infrastructure
**Responsável**: Dev  
**Estimativa**: 6-8h

**Providers**:
- `WhatsAppProvider` (via API)
- `EmailProvider` (SMTP)
- `PushNotificationProvider` (Firebase)

---

#### 6.3 - Mobile App
**Responsável**: Dev  
**Estimativa**: 10-12h

**Stack**: React Native + Expo

**Telas**:
- Login
- Dashboard
- Notificações
- Presença do filho

---

### 🎯 Entregáveis Sprint 6

- ✅ Notificações funcionando
- ✅ App mobile básico
- ✅ Push notifications

---

## 🎯 SPRINT 7: Deploy + Otimização

**Duração**: 3-4 dias  
**Objetivo**: Produção ready  
**Prioridade**: 🟢 MÉDIA

### 📋 Tasks

#### 7.1 - Performance
- Cache Redis
- Otimização de queries
- Compressão de imagens
- CDN para assets

#### 7.2 - Docker Compose
- Todos os serviços
- Volumes persistentes
- Networks isoladas
- Health checks

#### 7.3 - Monitoramento
- Prometheus + Grafana
- Logs centralizados
- Alertas

---

### 🎯 Entregáveis Sprint 7

- ✅ Sistema em produção
- ✅ Monitoramento ativo
- ✅ Performance otimizada

---

## 📊 Resumo

| Sprint | Duração | Prioridade | Entregável Principal |
|--------|---------|------------|---------------------|
| 1 | 3-5 dias | 🔴 CRÍTICA | Streaming Context |
| 2 | 5-7 dias | 🔴 CRÍTICA | Detection Context |
| 3 | 3-4 dias | 🔴 CRÍTICA | Student Context |
| 4 | 5-7 dias | 🔴 CRÍTICA | Attendance Context |
| 5 | 5-7 dias | 🟡 ALTA | Dashboard Web |
| 6 | 4-5 dias | 🟡 ALTA | Notifications + Mobile |
| 7 | 3-4 dias | 🟢 MÉDIA | Deploy + Otimização |

**Total**: 28-39 dias (~6-8 semanas)

---

**Versão**: 1.0.0  
**Data**: 2025-01-18  
**Status**: 📋 Planejamento
