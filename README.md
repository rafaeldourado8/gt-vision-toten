# 🎯 GT-Vision Toten

Sistema de Monitoramento de Alunos com Reconhecimento Facial

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)](https://fastapi.tiangolo.com/)
[![DDD](https://img.shields.io/badge/Architecture-DDD-orange.svg)](https://en.wikipedia.org/wiki/Domain-driven_design)
[![Tests](https://img.shields.io/badge/Coverage-90%25-brightgreen.svg)](https://pytest.org/)

---

## 📋 Sobre

Sistema automatizado para registro de presença de alunos utilizando:
- 📹 Câmeras RTSP
- 🤖 Detecção facial em tempo real
- 📊 Dashboard administrativo
- 📱 App mobile para pais
- 🔔 Notificações automáticas

---

## 🏗️ Arquitetura

Baseado em **Domain-Driven Design (DDD)** com 5 bounded contexts:

```
1. Streaming Context   → Gerenciamento de câmeras
2. Detection Context   → Detecção facial
3. Attendance Context  → Registro de presença
4. Student Context     → Cadastro de alunos
5. Notification Context → Notificações
```

---

## 🚀 Quick Start

### Pré-requisitos
- Python 3.11+
- Docker & Docker Compose
- Git

### Instalação

```bash
# Clone o repositório
git clone <repo-url>
cd GT-Vision-Toten

# Copie o .env
cp .env.example .env

# Inicie com Docker (RECOMENDADO)
.\start-dev.bat

# OU manualmente:

# Instale dependências
pip install -r requirements.txt

# Suba os serviços
docker-compose up -d

# Inicie a API (se não usar Docker para API)
uvicorn src.main:app --reload
```

Acesse: 
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- MediaMTX HLS: http://localhost:8888

### Usando Webcam

Para usar webcam ao invés de câmera RTSP:

```json
{
  "name": "Webcam Laptop",
  "rtsp_url": "webcam://0",
  "location": "Development"
}
```

Índices de webcam:
- `webcam://0` - Webcam padrão
- `webcam://1` - Segunda webcam
- `webcam://2` - Terceira webcam

---

## 📁 Estrutura do Projeto

```
GT-Vision Toten/
├── .ai-rules/          # Regras para AI assistants
├── docs/               # Documentação completa
├── packages/           # Boilerplate reutilizável
├── src/                # Código fonte
│   ├── @core/          # Kernel compartilhado
│   ├── streaming/      # Bounded Context 1
│   ├── detection/      # Bounded Context 2
│   ├── attendance/     # Bounded Context 3
│   ├── student/        # Bounded Context 4
│   └── notification/   # Bounded Context 5
├── tests/              # Testes
├── docker/             # Dockerfiles
└── mediamtx.yml        # Config MediaMTX
```

---

## 📚 Documentação

- [📋 Plano do Projeto](./docs/PROJECT-PLAN.md)
- [🚀 Sprints](./docs/SPRINTS.md)
- [🏗️ Arquitetura](./docs/ARCHITECTURE.md)

---

## 🧪 Testes

### Testes Unitários e Integração

```bash
# Rodar todos os testes
pytest

# Com cobertura
pytest --cov=src --cov-report=html

# Apenas unitários
pytest -m unit

# Apenas integração
pytest -m integration
```

### Testes E2E - Sistema Completo

**Teste com vídeo simulado** (valida todo o pipeline):
```bash
.\run-e2e-test.bat
```

Testa:
- ✅ Login e autenticação
- ✅ Cadastro de aluno + foto
- ✅ Streaming de vídeo
- ✅ Detecção facial com IA
- ✅ Registro de presença
- ✅ Envio de notificações

**Teste rápido com webcam**:
```bash
.\run-webcam-test.bat
```

Usa sua webcam para testar detecção em tempo real (30s).

Veja [tests/README.md](./tests/README.md) para mais detalhes.

---

## 🛠️ Tecnologias

### Backend
- **Python 3.11+**
- **FastAPI** - API REST
- **SQLAlchemy** - ORM
- **Pydantic** - Validação

### Streaming
- **MediaMTX** - Server RTSP/HLS/WebRTC
- **OpenCV** - Processamento de vídeo

### Detecção
- **DeepFace** - Detecção e reconhecimento facial
- **TensorFlow** - Backend de ML
- **OpenCV** - Processamento de vídeo

### Infraestrutura
- **Docker** - Containerização
- **Redis** - Cache
- **PostgreSQL** - Banco de dados

---

## 📊 Status do Projeto

**Sprint Atual**: Sprint 1 - Fundação e Estrutura Base  
**Progresso**: 🟢 Task 1.1 Concluída

Veja [CURRENT_SPRINT.md](./.ai-rules/context/CURRENT_SPRINT.md) para detalhes.

---

## 🤝 Contribuindo

1. Leia as regras em `.ai-rules/`
2. Siga DDD, SOLID e Clean Code
3. Complexidade ciclomática < 10
4. Cobertura de testes > 90%
5. Todos os testes devem passar

---

## 📝 Licença

Proprietary - Todos os direitos reservados

---

## 👥 Time

Desenvolvido com ❤️ seguindo as melhores práticas de engenharia de software.

---

**Versão**: 1.0.0  
**Data**: 2025-01-18
