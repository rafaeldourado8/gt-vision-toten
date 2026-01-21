# 📁 Estrutura de Pastas

> **OBRIGATÓRIO**: Seguir esta estrutura em TODOS os projetos.
> **OBRIGATÓRIO**: Novos arquivos devem ser criados na pasta correta.

## 🗂️ Estrutura Raiz do Projeto

```
projeto/
│
├── 📁 .ai-rules/           # 🤖 Regras para AI assistants (ESTE DIRETÓRIO)
│   ├── RULES.md            # Ponto de entrada
│   ├── rules/              # Regras detalhadas
│   ├── context/            # Contexto do projeto
│   ├── checklists/         # Checklists reutilizáveis
│   └── templates/          # Templates de código
│
├── 📁 docs/                # 📚 Documentação do projeto
│   ├── architecture/       # Diagramas e decisões arquiteturais
│   ├── api/                # Documentação de API
│   └── guides/             # Guias de uso
│
├── 📁 docker/              # 🐳 Configurações Docker
│   ├── [bounded-context]/  # Dockerfile por contexto
│   ├── nginx/
│   └── postgres/
│
├── 📁 src/                 # 💻 Código fonte
│   ├── @core/              # Kernel compartilhado
│   └── [bounded-context]/  # Contextos delimitados
│
├── 📁 tests/               # 🧪 Testes (espelha src/)
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── 📁 scripts/             # 🔧 Scripts de automação
│
├── docker-compose.yml
├── docker-compose.dev.yml
├── docker-compose.test.yml
├── package.json
├── tsconfig.json
└── .env.example
```

---

## 📦 Estrutura de Bounded Context

Cada bounded context segue a mesma estrutura interna:

```
src/[bounded-context]/
│
├── 📁 domain/                    # 🎯 Camada de Domínio
│   │
│   ├── 📁 entities/              # Entidades com identidade
│   │   ├── order.entity.ts
│   │   └── index.ts
│   │
│   ├── 📁 value-objects/         # Objetos de valor (imutáveis)
│   │   ├── money.vo.ts
│   │   ├── order-id.vo.ts
│   │   └── index.ts
│   │
│   ├── 📁 aggregates/            # Raízes de agregados
│   │   ├── order.aggregate.ts
│   │   └── index.ts
│   │
│   ├── 📁 repositories/          # Interfaces de repositório
│   │   ├── order.repository.ts   # Interface apenas!
│   │   └── index.ts
│   │
│   ├── 📁 services/              # Domain Services
│   │   ├── pricing.service.ts
│   │   └── index.ts
│   │
│   ├── 📁 events/                # Domain Events
│   │   ├── order-created.event.ts
│   │   ├── order-cancelled.event.ts
│   │   └── index.ts
│   │
│   ├── 📁 errors/                # Erros de domínio
│   │   ├── invalid-order.error.ts
│   │   └── index.ts
│   │
│   └── index.ts                  # Barrel export
│
├── 📁 application/               # 🔄 Camada de Aplicação
│   │
│   ├── 📁 use-cases/             # Casos de uso
│   │   ├── create-order/
│   │   │   ├── create-order.use-case.ts
│   │   │   ├── create-order.dto.ts
│   │   │   └── index.ts
│   │   ├── cancel-order/
│   │   └── index.ts
│   │
│   ├── 📁 dtos/                  # DTOs compartilhados
│   │   ├── order.dto.ts
│   │   └── index.ts
│   │
│   ├── 📁 mappers/               # Conversões Entity <-> DTO
│   │   ├── order.mapper.ts
│   │   └── index.ts
│   │
│   ├── 📁 ports/                 # Interfaces para infra
│   │   ├── payment-gateway.port.ts
│   │   └── index.ts
│   │
│   └── index.ts
│
├── 📁 infra/                     # 🔌 Camada de Infraestrutura
│   │
│   ├── 📁 repositories/          # Implementações de repositório
│   │   ├── typeorm/
│   │   │   └── order.typeorm.repository.ts
│   │   ├── prisma/
│   │   │   └── order.prisma.repository.ts
│   │   └── index.ts
│   │
│   ├── 📁 controllers/           # Controllers HTTP
│   │   ├── order.controller.ts
│   │   └── index.ts
│   │
│   ├── 📁 providers/             # Serviços externos
│   │   ├── stripe.payment.provider.ts
│   │   └── index.ts
│   │
│   ├── 📁 database/              # Migrations, seeds
│   │   ├── migrations/
│   │   └── seeds/
│   │
│   └── index.ts
│
└── [bounded-context].module.ts   # Módulo principal
```

---

## 🔧 Estrutura do @core

O `@core` contém código compartilhado entre bounded contexts:

```
src/@core/
│
├── 📁 domain/
│   ├── 📁 base/                  # Classes base
│   │   ├── entity.base.ts
│   │   ├── aggregate-root.base.ts
│   │   ├── value-object.base.ts
│   │   └── domain-event.base.ts
│   │
│   ├── 📁 value-objects/         # VOs reutilizáveis
│   │   ├── uuid.vo.ts
│   │   ├── email.vo.ts
│   │   ├── money.vo.ts
│   │   └── index.ts
│   │
│   └── 📁 errors/                # Erros base
│       ├── domain.error.ts
│       └── index.ts
│
├── 📁 application/
│   ├── 📁 base/
│   │   ├── use-case.base.ts
│   │   └── result.ts
│   │
│   └── 📁 interfaces/
│       ├── logger.interface.ts
│       └── event-bus.interface.ts
│
├── 📁 infra/
│   ├── 📁 database/
│   │   ├── database.module.ts
│   │   └── connection.ts
│   │
│   ├── 📁 messaging/
│   │   ├── event-bus.ts
│   │   └── queue.ts
│   │
│   ├── 📁 logging/
│   │   └── logger.ts
│   │
│   └── 📁 config/
│       └── env.config.ts
│
└── index.ts
```

---

## 🧪 Estrutura de Testes

Os testes espelham a estrutura do `src/`:

```
tests/
│
├── 📁 unit/                      # Testes unitários
│   ├── [bounded-context]/
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   │   └── order.entity.spec.ts
│   │   │   └── value-objects/
│   │   │       └── money.vo.spec.ts
│   │   └── application/
│   │       └── use-cases/
│   │           └── create-order.use-case.spec.ts
│   └── @core/
│
├── 📁 integration/               # Testes de integração
│   ├── [bounded-context]/
│   │   └── repositories/
│   │       └── order.repository.int.spec.ts
│   └── @core/
│
├── 📁 e2e/                       # Testes end-to-end
│   └── [bounded-context]/
│       └── create-order.e2e.spec.ts
│
├── 📁 fixtures/                  # Dados de teste
│   └── orders.fixture.ts
│
├── 📁 mothers/                   # Object Mothers
│   └── order.mother.ts
│
├── 📁 builders/                  # Test Builders
│   └── order.builder.ts
│
├── 📁 fakes/                     # Fakes (implementações in-memory)
│   └── in-memory-order.repository.ts
│
└── 📁 mocks/                     # Mocks compartilhados
    └── payment-gateway.mock.ts
```

---

## 📝 Convenções de Nomenclatura

### Arquivos

| Tipo | Padrão | Exemplo |
|------|--------|---------|
| Entity | `[nome].entity.ts` | `order.entity.ts` |
| Value Object | `[nome].vo.ts` | `money.vo.ts` |
| Aggregate | `[nome].aggregate.ts` | `order.aggregate.ts` |
| Repository Interface | `[nome].repository.ts` | `order.repository.ts` |
| Repository Impl | `[nome].[orm].repository.ts` | `order.typeorm.repository.ts` |
| Use Case | `[ação]-[recurso].use-case.ts` | `create-order.use-case.ts` |
| DTO | `[nome].dto.ts` | `order.dto.ts` |
| Mapper | `[nome].mapper.ts` | `order.mapper.ts` |
| Controller | `[nome].controller.ts` | `order.controller.ts` |
| Module | `[nome].module.ts` | `order.module.ts` |
| Error | `[nome].error.ts` | `invalid-order.error.ts` |
| Event | `[nome]-[ação].event.ts` | `order-created.event.ts` |
| Test Unit | `[nome].spec.ts` | `order.entity.spec.ts` |
| Test Integration | `[nome].int.spec.ts` | `order.repository.int.spec.ts` |
| Test E2E | `[nome].e2e.spec.ts` | `create-order.e2e.spec.ts` |

### Pastas

```
✅ kebab-case para pastas
   bounded-context/
   use-cases/
   value-objects/

❌ Evite
   BoundedContext/
   useCases/
   valueObjects/
```

---

## 🚫 Regras de Localização

### Onde CRIAR arquivos

| Tipo de Arquivo | Localização |
|-----------------|-------------|
| Entidade | `src/[context]/domain/entities/` |
| Value Object | `src/[context]/domain/value-objects/` |
| Repository Interface | `src/[context]/domain/repositories/` |
| Repository Impl | `src/[context]/infra/repositories/` |
| Use Case | `src/[context]/application/use-cases/` |
| Controller | `src/[context]/infra/controllers/` |
| Dockerfile | `docker/[context]/` |
| Teste | `tests/[tipo]/[context]/[camada]/` |
| Documentação Markdown | `.ai-rules/` ou `docs/` |

### Onde NUNCA criar arquivos

```
❌ .md na raiz do projeto (exceto README.md)
❌ .md em src/
❌ Testes em src/
❌ Código em tests/
❌ Implementações em domain/
❌ Interfaces em infra/
❌ Lógica de negócio em infra/
```

---

## 📤 Barrel Exports (index.ts)

Cada pasta deve ter um `index.ts` exportando seus conteúdos:

```typescript
// src/orders/domain/entities/index.ts
export * from './order.entity';
export * from './order-item.entity';

// src/orders/domain/index.ts
export * from './entities';
export * from './value-objects';
export * from './repositories';
export * from './events';
export * from './errors';

// src/orders/index.ts
export * from './domain';
export * from './application';
// NÃO exportar infra para fora do módulo!
```

---

## ✅ Checklist de Estrutura

Ao criar novo código:

- [ ] Arquivo está na pasta correta da camada?
- [ ] Nome segue convenção?
- [ ] index.ts atualizado com export?
- [ ] Teste criado na pasta espelho?
- [ ] Sem imports cruzando camadas incorretamente?
- [ ] Sem .md fora de .ai-rules/ ou docs/?
