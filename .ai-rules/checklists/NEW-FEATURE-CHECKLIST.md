# ✅ Checklist: Nova Feature

> Use este checklist ao desenvolver uma nova feature.

## 📋 Antes de Começar

- [ ] Ler `.ai-rules/RULES.md`
- [ ] Ler `.ai-rules/context/PROJECT.md`
- [ ] Ler `.ai-rules/context/CURRENT_SPRINT.md`
- [ ] Entender requisitos da feature
- [ ] Identificar bounded context correto

## 🌳 Setup

```bash
# Atualizar develop
git checkout develop
git pull origin develop

# Criar branch
git checkout -b feature/[nome-descritivo]
```

## 🏗️ Desenvolvimento (TDD)

### 1. Domain Layer
- [ ] Identificar entidades necessárias
- [ ] Criar/atualizar Value Objects
- [ ] Definir Domain Events
- [ ] Criar interface do Repository

**Testes primeiro!**
```bash
# Escrever testes para domain
# tests/unit/[context]/domain/entities/[entity].spec.ts
# tests/unit/[context]/domain/value-objects/[vo].spec.ts

# Rodar (deve FALHAR - Red)
docker-compose exec app npm test -- [arquivo].spec.ts

# Implementar código mínimo
# Rodar (deve PASSAR - Green)
docker-compose exec app npm test -- [arquivo].spec.ts

# Refatorar (Blue)
```

### 2. Application Layer
- [ ] Criar Use Case
- [ ] Criar DTOs
- [ ] Criar Mappers

**Testes primeiro!**
```bash
# Escrever testes para use case
# tests/unit/[context]/application/use-cases/[use-case].spec.ts

# Ciclo Red-Green-Refactor
docker-compose exec app npm test -- [arquivo].spec.ts
```

### 3. Infrastructure Layer
- [ ] Implementar Repository
- [ ] Criar Controller
- [ ] Configurar rotas

**Testes de integração!**
```bash
# tests/integration/[context]/repositories/[repo].int.spec.ts
docker-compose exec app npm run test:integration
```

## ✅ Verificações Finais

```bash
# 1. Todos os testes
docker-compose exec app npm test

# 2. Lint
docker-compose exec app npm run lint

# 3. Build
docker-compose exec app npm run build

# 4. Cobertura
docker-compose exec app npm run test:coverage
```

## 📤 Finalização

- [ ] Verificar `.ai-rules/checklists/PR-CHECKLIST.md`
- [ ] Rebase com develop
- [ ] Push e abrir PR

```bash
git fetch origin
git rebase origin/develop
git push origin feature/[nome]
```

---

## 📁 Arquivos a Criar (Template)

```
src/[bounded-context]/
├── domain/
│   ├── entities/[entity].entity.ts
│   ├── value-objects/[vo].vo.ts
│   ├── repositories/[entity].repository.ts
│   └── events/[entity]-created.event.ts
├── application/
│   └── use-cases/[action]-[entity]/
│       ├── [action]-[entity].use-case.ts
│       ├── [action]-[entity].dto.ts
│       └── index.ts
└── infra/
    ├── repositories/[orm]/[entity].[orm].repository.ts
    └── controllers/[entity].controller.ts

tests/
├── unit/[bounded-context]/
│   ├── domain/entities/[entity].entity.spec.ts
│   └── application/use-cases/[action]-[entity].use-case.spec.ts
└── integration/[bounded-context]/
    └── repositories/[entity].repository.int.spec.ts
```
