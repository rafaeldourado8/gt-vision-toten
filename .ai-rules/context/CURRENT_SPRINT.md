# 🏃 Sprint Atual

> **INSTRUÇÕES**: Atualize este arquivo a cada sprint.
> AI Assistants devem consultar este arquivo para entender o trabalho atual.

## 📅 Informações da Sprint

**Sprint**: 1 - Fundação e Estrutura Base  
**Período**: 2025-01-18 - 2025-01-23  
**Objetivo**: Estrutura DDD completa + Streaming Context funcionando

---

## 📋 Tasks da Sprint

### ✅ Concluídas

| ID | Descrição | Responsável |
|----|-----------|-------------|
| #1.1 | Estrutura de Pastas DDD | AI Assistant |

### 🔴 Em Andamento

| ID | Descrição | Responsável | Status |
|----|-----------|-------------|--------|
| #1.2 | Streaming Domain Layer | AI Assistant | 🔴 To Do |

### 📝 A Fazer

| ID | Descrição | Prioridade |
|----|-----------|------------|
| #1.3 | Streaming Application Layer | Alta |
| #1.4 | Streaming Infrastructure Layer | Alta |

---

## 🎯 Foco Atual

**Task Ativa**: #1.2 - Streaming Domain Layer

**Descrição Detalhada**:
Criar camada de domínio do Streaming Context seguindo DDD:
- Entities: Camera (Aggregate Root)
- Value Objects: RtspUrl, StreamPath, CameraStatus
- Repositories: Interface CameraRepository
- Domain Errors: InvalidRtspUrlError, CameraNotFoundError

**Arquivos Envolvidos**:
- `src/streaming/domain/entities/camera.py`
- `src/streaming/domain/value_objects/rtsp_url.py`
- `src/streaming/domain/value_objects/stream_path.py`
- `src/streaming/domain/value_objects/camera_status.py`
- `src/streaming/domain/repositories/camera_repository.py`
- `src/streaming/domain/errors/camera_errors.py`
- `tests/unit/streaming/domain/...`

**Critérios de Aceite**:
- [ ] Camera é Aggregate Root válido
- [ ] Value Objects são imutáveis
- [ ] RtspUrl valida formato rtsp://user:pass@host:port/path
- [ ] CameraStatus é Enum (ONLINE, OFFLINE, ERROR, CONNECTING)
- [ ] CameraRepository é interface (ABC)
- [ ] Complexidade ciclomática < 5 por classe
- [ ] Cobertura de testes > 90%
- [ ] Zero dependências externas no domain

**Dependências**:
- Depende de: Estrutura de pastas criada ✅
- Bloqueia: #1.3 (Application Layer)

---

## 🐛 Bugs Conhecidos

Nenhum bug conhecido no momento.

---

## 📝 Decisões Técnicas da Sprint

### Decisão 1: Bounded Context Separado
**Contexto**: Detection é um domínio distinto de AI (que apenas detecta)  
**Decisão**: Criar `src/detection/` separado de `src/ai/`  
**Consequências**: 
- ✅ Melhor separação de responsabilidades
- ✅ Mais fácil manutenção e evolução independente
- ✅ Equipes podem trabalhar em paralelo
- ⚠️ Precisa de comunicação entre contexts (via eventos ou API)

### Decisão 2: Enriquecimento Assíncrono
**Contexto**: API FIPE pode ser lenta (>1s) e não deve bloquear ingestão  
**Decisão**: Salvar detecção primeiro, enriquecer depois via background job  
**Consequências**:
- ✅ Ingestão rápida (<200ms)
- ✅ Não perde detecções por timeout
- ⚠️ Dados de veículo aparecem com delay (aceitável)

### Decisão 3: Cache Redis para Enriquecimento
**Contexto**: Mesma placa pode aparecer múltiplas vezes no mesmo dia  
**Decisão**: Cache de 24h para dados de veículos por placa  
**Consequências**:
- ✅ Reduz 90% das chamadas à API FIPE
- ✅ Melhora performance
- ⚠️ Dados podem ficar desatualizados por 24h (aceitável)

---

## 🔄 Atualizações

| Data | Atualização |
|------|-------------|
| 2025-01-18 | Sprint 14 iniciada - Documentação criada |

---

## ⚠️ Avisos para AI Assistants

### CRÍTICO - NUNCA FAZER
- ❌ NUNCA modificar `src/ai/` - é contexto separado
- ❌ NUNCA colocar lógica de negócio em controllers
- ❌ NUNCA criar dependências do Domain para Infrastructure
- ❌ NUNCA commitar sem testes
- ❌ NUNCA ignorar complexidade ciclomática >10

### SEMPRE FAZER
- ✅ SEMPRE seguir DDD: Domain → Application → Infrastructure
- ✅ SEMPRE criar testes ANTES de implementar (TDD)
- ✅ SEMPRE usar injeção de dependência
- ✅ SEMPRE validar com `pytest --cov` antes de PR
- ✅ SEMPRE criar migrations para mudanças no DB
- ✅ SEMPRE usar Value Objects para validações
- ✅ SEMPRE fazer Entities imutáveis quando possível

### Padrões Específicos desta Sprint
1. **Naming**: `VehicleDetection` (não `Detection` genérico)
2. **Confidence**: Float 0.0-1.0 (não porcentagem)
3. **Plate Format**: Mercosul ABC1D23 (7 caracteres)
4. **Timestamps**: UTC sempre
5. **IDs**: UUID v4

---

## 📚 Referências Obrigatórias

- [Sprint 14 Completo](../sprints/sprint-14.md)
- [Detection Context Architecture](../docs/architecture/detection-context.md)
- [DDD Rules](.ai-rules/rules/ARCHITECTURE.md)
- [Testing Rules](.ai-rules/rules/TESTING.md)
- [Code Quality Rules](.ai-rules/rules/CODE-QUALITY.md)
