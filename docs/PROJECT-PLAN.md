# 📋 GT-Vision Toten - Plano do Projeto

## 🎯 Visão Geral

**Sistema de Monitoramento de Alunos com Reconhecimento Facial**

Sistema automatizado para registro de presença de alunos utilizando câmeras RTSP, detecção facial em tempo real e dashboard administrativo.

---

## 🏗️ Arquitetura

### Stack Tecnológica

- **Backend**: Python + FastAPI
- **Frontend**: React + TypeScript + TailwindCSS
- **Streaming**: MediaMTX (RTSP/HLS/WebRTC)
- **Detecção**: OpenCV + face_recognition / YOLO
- **Banco de Dados**: SQLite (dev) / PostgreSQL (prod)
- **Cache**: Redis
- **Containerização**: Docker + Docker Compose
- **Padrões**: DDD, SOLID, Clean Code

### Bounded Contexts (DDD)

```
1. Streaming Context   - Gerenciamento de câmeras e streams
2. Detection Context   - Processamento de detecção facial
3. Attendance Context  - Registro e gestão de presença
4. Student Context     - Cadastro de alunos
5. Notification Context - Alertas e notificações
```

---

## 📊 Requisitos Funcionais

### Core
- ✅ Importar alunos matriculados (Excel/CSV)
- ✅ Posicionar aluno em frente ao totem
- ✅ Escanear face em segundos
- ✅ Salvar mapeamento facial no banco
- ✅ Enviar presença para professores e pais

### Suporte
- ✅ Exportar relatório Excel/CSV de matrículas
- ✅ Split automático de cadastro
- ✅ Push de relatórios detalhados
- ✅ Registro de presença para professores (painel admin + webapp)
- ✅ Reuniões via chat webapp/pc (estilo Discord)
- ✅ Notificações de provas e atividades
- ✅ Calendário de provas

---

## 📐 Requisitos Não Funcionais

### Capacidade
- **DAU**: 500 alunos ativos
- **Requests**: 5 req/s (POST presença, GET relatórios)
- **RPS**: 5 * 10^6 / 10^5 = 58 RPS

### Performance
- **Bandwidth**: 500 rps * 100kb = 50mb
- **Storage**: 12 GB/dia

### Escalabilidade
- Baixa latência
- Alta disponibilidade
- Integridade de dados

---

## 🎨 Fluxo do Sistema

```
[RTSP Camera] 
    ↓
[MediaMTX Container]
    ↓
[Stream Processor Worker]
    ↓
[Face Detection Service]
    ↓
[Face Comparison]
    ↓
[Attendance Registration]
    ↓
[Dashboard + Notifications]
```

---

## 🔐 Regras de Desenvolvimento

### SOLID
- ✅ Single Responsibility
- ✅ Open/Closed
- ✅ Liskov Substitution
- ✅ Interface Segregation
- ✅ Dependency Inversion

### Clean Code
- ✅ Nomes descritivos
- ✅ Funções ≤ 20 linhas
- ✅ Parâmetros ≤ 3
- ✅ Código auto-explicativo

### Complexidade Ciclomática
- 🟢 1-4: Ideal
- 🟡 5-7: Considerar refatorar
- 🟠 8-10: Refatorar se possível
- 🔴 11+: **OBRIGATÓRIO refatorar**

---

## 📁 Estrutura de Pastas

```
GT-Vision Toten/
├── .ai-rules/              # Regras para AI assistants
├── docs/                   # Documentação
├── packages/               # Boilerplate reutilizável
│   ├── core/
│   ├── auth/
│   ├── utils/
│   ├── observability/
│   └── llm/
├── src/                    # Código fonte
│   ├── @core/              # Kernel compartilhado
│   ├── streaming/          # Bounded Context 1
│   ├── detection/          # Bounded Context 2
│   ├── attendance/         # Bounded Context 3
│   ├── student/            # Bounded Context 4
│   └── notification/       # Bounded Context 5
├── tests/                  # Testes (espelha src/)
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── docker/                 # Dockerfiles
├── mediamtx.yml            # Config MediaMTX
└── docker-compose.yml
```

---

## 🚀 Roadmap

Veja [SPRINTS.md](./SPRINTS.md) para detalhamento completo.

| Sprint | Foco | Duração | Status |
|--------|------|---------|--------|
| 1 | Fundação + Streaming | 3-5 dias | 📋 Planejado |
| 2 | Detection Context | 5-7 dias | 📋 Planejado |
| 3 | Student Context | 3-4 dias | 📋 Planejado |
| 4 | Attendance Context | 5-7 dias | 📋 Planejado |
| 5 | Dashboard Web | 5-7 dias | 📋 Planejado |
| 6 | Notifications + Mobile | 4-5 dias | 📋 Planejado |
| 7 | Deploy + Otimização | 3-4 dias | 📋 Planejado |

**Total Estimado**: 28-39 dias (~6-8 semanas)

---

## 🔧 Tecnologias Detalhadas

### Backend
- **FastAPI**: API REST
- **SQLAlchemy**: ORM
- **Alembic**: Migrations
- **Pydantic**: Validação
- **pytest**: Testes

### Frontend
- **React 18**: UI
- **TypeScript**: Type safety
- **TailwindCSS**: Styling
- **React Query**: Data fetching
- **Zustand**: State management

### Streaming
- **MediaMTX**: Server RTSP/HLS/WebRTC
- **OpenCV**: Captura de frames
- **FFmpeg**: Processamento de vídeo

### Detecção
- **face_recognition**: Detecção e encoding
- **dlib**: Face landmarks
- **YOLO** (opcional): Detecção rápida

### Infraestrutura
- **Docker**: Containerização
- **Redis**: Cache + Queue
- **PostgreSQL**: Banco principal
- **Nginx**: Reverse proxy
- **Prometheus + Grafana**: Monitoramento

---

## 📈 Métricas de Sucesso

- ✅ Cobertura de testes > 90%
- ✅ Complexidade ciclomática < 10
- ✅ Tempo de detecção < 2s
- ✅ Tempo de resposta API < 200ms
- ✅ Uptime > 99.5%
- ✅ Zero dependências circulares

---

## 🔗 Links Úteis

- [Sprints Detalhados](./SPRINTS.md)
- [Regras de Arquitetura](../.ai-rules/rules/ARCHITECTURE.md)
- [Regras de Qualidade](../.ai-rules/rules/CODE-QUALITY.md)
- [Estrutura de Pastas](../.ai-rules/rules/FOLDER-STRUCTURE.md)

---

**Versão**: 1.0.0  
**Data**: 2025-01-18  
**Status**: 📋 Planejamento
