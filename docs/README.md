# 📚 GT-Vision Toten - Documentação

Documentação completa do projeto GT-Vision Toten.

---

## 📋 Índice

### 📖 Documentos Principais

| Documento | Descrição |
|-----------|-----------|
| [PROJECT-PLAN.md](./PROJECT-PLAN.md) | Plano geral do projeto, visão, requisitos e stack |
| [SPRINTS.md](./SPRINTS.md) | Detalhamento de todas as sprints (7 sprints) |
| [ARCHITECTURE.md](./ARCHITECTURE.md) | Arquitetura do sistema, bounded contexts, fluxos |

---

## 🎯 Visão Rápida

**GT-Vision Toten** é um sistema de monitoramento de alunos com reconhecimento facial para registro automático de presença.

### Principais Features
- ✅ Detecção facial em tempo real
- ✅ Registro automático de presença
- ✅ Dashboard administrativo
- ✅ Notificações para pais e professores
- ✅ Relatórios e exportação Excel
- ✅ App mobile

### Stack
- **Backend**: Python + FastAPI + DDD
- **Frontend**: React + TypeScript
- **Streaming**: MediaMTX
- **Detecção**: OpenCV + face_recognition
- **Infra**: Docker + Redis + PostgreSQL

---

## 🚀 Início Rápido

### 1. Leia o Plano
```bash
# Entenda o projeto
cat docs/PROJECT-PLAN.md
```

### 2. Veja as Sprints
```bash
# Veja o cronograma
cat docs/SPRINTS.md
```

### 3. Entenda a Arquitetura
```bash
# Arquitetura detalhada
cat docs/ARCHITECTURE.md
```

---

## 📊 Cronograma

| Sprint | Foco | Duração | Status |
|--------|------|---------|--------|
| 1 | Fundação + Streaming | 3-5 dias | 📋 To Do |
| 2 | Detection Context | 5-7 dias | 📋 To Do |
| 3 | Student Context | 3-4 dias | 📋 To Do |
| 4 | Attendance Context | 5-7 dias | 📋 To Do |
| 5 | Dashboard Web | 5-7 dias | 📋 To Do |
| 6 | Notifications + Mobile | 4-5 dias | 📋 To Do |
| 7 | Deploy + Otimização | 3-4 dias | 📋 To Do |

**Total**: 28-39 dias (~6-8 semanas)

---

## 🏗️ Bounded Contexts

```
1. Streaming Context   → Gerenciamento de câmeras
2. Detection Context   → Detecção facial
3. Attendance Context  → Registro de presença
4. Student Context     → Cadastro de alunos
5. Notification Context → Notificações
```

---

## 📁 Estrutura do Projeto

```
GT-Vision Toten/
├── .ai-rules/          # Regras para AI assistants
├── docs/               # 📚 VOCÊ ESTÁ AQUI
│   ├── README.md
│   ├── PROJECT-PLAN.md
│   ├── SPRINTS.md
│   └── ARCHITECTURE.md
├── packages/           # Boilerplate reutilizável
├── src/                # Código fonte
│   ├── @core/
│   ├── streaming/
│   ├── detection/
│   ├── attendance/
│   ├── student/
│   └── notification/
├── tests/              # Testes
├── docker/             # Dockerfiles
└── mediamtx.yml        # Config MediaMTX
```

---

## 🔗 Links Úteis

### Regras de Desenvolvimento
- [Arquitetura (SOLID, DDD)](../.ai-rules/rules/ARCHITECTURE.md)
- [Qualidade de Código](../.ai-rules/rules/CODE-QUALITY.md)
- [Estrutura de Pastas](../.ai-rules/rules/FOLDER-STRUCTURE.md)
- [Testes](../.ai-rules/rules/TESTING.md)
- [Docker](../.ai-rules/rules/DOCKER.md)

### Contexto do Projeto
- [Projeto](../.ai-rules/context/PROJECT.md)
- [Sprint Atual](../.ai-rules/context/CURRENT_SPRINT.md)

---

## 📝 Como Contribuir

1. Leia as regras em `.ai-rules/`
2. Siga DDD, SOLID e Clean Code
3. Complexidade ciclomática < 10
4. Cobertura de testes > 90%
5. Todos os testes devem passar

---

## 📞 Contato

Para dúvidas sobre a documentação, consulte os arquivos em `.ai-rules/`.

---

**Versão**: 1.0.0  
**Data**: 2025-01-18  
**Status**: 📋 Planejamento
