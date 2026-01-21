# 🧪 Regras de Testes

> **OBRIGATÓRIO**: Todo código deve ser escrito seguindo TDD.
> **OBRIGATÓRIO**: Testes devem rodar via `docker-compose exec`.

## 🔴🟢🔵 Ciclo TDD (Red-Green-Refactor)

```
1. 🔴 RED    - Escrever teste que FALHA
2. 🟢 GREEN  - Escrever código MÍNIMO para passar
3. 🔵 BLUE   - Refatorar mantendo testes verdes
```

### Regra de Ouro
```
❌ NUNCA escrever código de produção sem teste falhando primeiro
❌ NUNCA escrever mais código que o necessário para passar o teste
✅ SEMPRE refatorar após o teste passar
```

---

## 📊 Pirâmide de Testes

```
         /\
        /  \        E2E (5-10%)
       /----\       - Fluxos críticos de negócio
      /      \      
     /--------\     Integration (20-30%)
    /          \    - Repositórios, APIs, Filas
   /------------\   
  /              \  Unit (60-70%)
 /________________\ - Entidades, Value Objects, Use Cases
```

### Cobertura Mínima Obrigatória
```
Domain Layer:     90%+ (entidades, value objects, domain services)
Application Layer: 80%+ (use cases)
Infrastructure:    70%+ (repositórios, controllers)
```

---

## 🏗️ Estrutura de Testes

### Organização de Arquivos
```
tests/
├── unit/
│   ├── [bounded-context]/
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   │   └── order.spec.ts
│   │   │   └── value-objects/
│   │   │       └── money.spec.ts
│   │   └── application/
│   │       └── use-cases/
│   │           └── create-order.spec.ts
│   └── @core/
│
├── integration/
│   ├── [bounded-context]/
│   │   └── repositories/
│   │       └── order-repository.spec.ts
│   └── @core/
│
└── e2e/
    └── [bounded-context]/
        └── create-order.e2e.spec.ts
```

### Nomenclatura de Arquivos
```
✅ [nome-do-arquivo].spec.ts     # Testes unitários
✅ [nome-do-arquivo].int.spec.ts # Testes de integração  
✅ [nome-do-arquivo].e2e.spec.ts # Testes E2E
```

---

## 📝 Padrão de Escrita de Testes

### Estrutura AAA (Arrange-Act-Assert)
```typescript
describe('Order', () => {
  describe('addItem', () => {
    it('should add item to order and update total', () => {
      // Arrange (Preparar)
      const order = Order.create();
      const product = ProductMother.aProduct().build();
      
      // Act (Agir)
      order.addItem(product.id, 2);
      
      // Assert (Verificar)
      expect(order.items).toHaveLength(1);
      expect(order.total.amount).toBe(product.price.amount * 2);
    });
  });
});
```

### Nomenclatura de Testes
```typescript
// ✅ Padrão: should [expected behavior] when [condition]
it('should throw InvalidQuantityError when quantity is zero')
it('should emit OrderCreatedEvent when order is created')
it('should return null when order is not found')

// ✅ Alternativa: given [context] when [action] then [result]
it('given an empty cart when adding first item then cart has one item')
```

### Describe Aninhados
```typescript
describe('OrderService', () => {
  describe('createOrder', () => {
    describe('with valid data', () => {
      it('should create order successfully')
      it('should emit domain event')
    });
    
    describe('with invalid data', () => {
      it('should throw validation error')
    });
    
    describe('when user has no credit', () => {
      it('should throw InsufficientFundsError')
    });
  });
});
```

---

## 🏭 Object Mother / Test Data Builders

### Object Mother Pattern
```typescript
// tests/mothers/order.mother.ts
export class OrderMother {
  static aOrder(): OrderBuilder {
    return new OrderBuilder();
  }
  
  static aCompletedOrder(): Order {
    return this.aOrder()
      .withStatus(OrderStatus.COMPLETED)
      .build();
  }
  
  static aCancelledOrder(): Order {
    return this.aOrder()
      .withStatus(OrderStatus.CANCELLED)
      .build();
  }
}

// tests/builders/order.builder.ts
export class OrderBuilder {
  private props = {
    id: OrderId.generate(),
    userId: UserId.generate(),
    items: [],
    status: OrderStatus.PENDING,
    createdAt: new Date(),
  };
  
  withId(id: OrderId): this {
    this.props.id = id;
    return this;
  }
  
  withItems(items: OrderItem[]): this {
    this.props.items = items;
    return this;
  }
  
  withStatus(status: OrderStatus): this {
    this.props.status = status;
    return this;
  }
  
  build(): Order {
    return Order.reconstitute(this.props);
  }
}
```

### Uso nos Testes
```typescript
// ✅ Limpo e legível
const order = OrderMother.aOrder()
  .withItems([ItemMother.aItem().withQuantity(2).build()])
  .build();

// ❌ Evite criar objetos inline complexos
const order = new Order(
  OrderId.generate(),
  UserId.generate(),
  [new OrderItem(...)],
  OrderStatus.PENDING,
  new Date()
);
```

---

## 🎭 Mocks, Stubs e Fakes

### Quando Usar Cada Um

| Tipo | Uso | Exemplo |
|------|-----|---------|
| **Stub** | Retorna valores predefinidos | Repository que retorna Order fake |
| **Mock** | Verifica interações | Verificar se email foi enviado |
| **Fake** | Implementação simplificada | InMemoryRepository |
| **Spy** | Wrapper que registra chamadas | Logger spy |

### Implementação de Fakes
```typescript
// tests/fakes/in-memory-order-repository.ts
export class InMemoryOrderRepository implements OrderRepository {
  private orders: Map<string, Order> = new Map();
  
  async save(order: Order): Promise<void> {
    this.orders.set(order.id.value, order);
  }
  
  async findById(id: OrderId): Promise<Order | null> {
    return this.orders.get(id.value) ?? null;
  }
  
  async findAll(): Promise<Order[]> {
    return Array.from(this.orders.values());
  }
  
  // Helper para testes
  clear(): void {
    this.orders.clear();
  }
}
```

### Uso de Mocks (Jest)
```typescript
describe('CreateOrderUseCase', () => {
  it('should send notification after order creation', async () => {
    // Arrange
    const notifier = {
      notify: jest.fn().mockResolvedValue(undefined),
    };
    const useCase = new CreateOrderUseCase(repository, notifier);
    
    // Act
    await useCase.execute(command);
    
    // Assert
    expect(notifier.notify).toHaveBeenCalledTimes(1);
    expect(notifier.notify).toHaveBeenCalledWith(
      expect.objectContaining({ type: 'ORDER_CREATED' })
    );
  });
});
```

---

## 🐳 Executando Testes com Docker

### Comandos Obrigatórios
```bash
# Testes unitários
docker-compose exec app npm test

# Testes com watch (desenvolvimento)
docker-compose exec app npm run test:watch

# Testes de integração
docker-compose exec app npm run test:integration

# Testes E2E
docker-compose -f docker-compose.test.yml run --rm e2e npm run test:e2e

# Cobertura
docker-compose exec app npm run test:coverage

# Testes de um arquivo específico
docker-compose exec app npm test -- order.spec.ts
```

### docker-compose.test.yml
```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: docker/app/Dockerfile
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - NODE_ENV=test
      - DATABASE_URL=postgres://test:test@db:5432/test
    depends_on:
      - db
      
  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=test
      - POSTGRES_PASSWORD=test
      - POSTGRES_DB=test
    tmpfs:
      - /var/lib/postgresql/data  # RAM para velocidade
```

---

## ✅ Checklist Antes de Commit

```bash
# 1. Rodar TODOS os testes
docker-compose exec app npm test

# 2. Verificar cobertura mínima
docker-compose exec app npm run test:coverage
# Domain: 90%+, Application: 80%+, Infra: 70%+

# 3. Sem testes pulados ou focados
grep -r "\.only\|\.skip\|xit\|xdescribe" tests/
# Deve retornar vazio!

# 4. Testes de integração
docker-compose exec app npm run test:integration
```

---

## 🚫 Anti-Patterns de Testes

```
❌ Testes que dependem de ordem de execução
❌ Testes que acessam banco real
❌ Testes que dependem de estado global
❌ Testes com sleep/setTimeout
❌ Testes sem assertions
❌ Múltiplos asserts não relacionados
❌ Testes que testam implementação, não comportamento
❌ Copiar/colar código entre testes (use helpers!)
```

---

## 📈 Métricas de Qualidade

| Métrica | Mínimo | Ideal |
|---------|--------|-------|
| Cobertura de Linhas | 70% | 85%+ |
| Cobertura de Branches | 60% | 80%+ |
| Cobertura de Funções | 75% | 90%+ |
| Tempo de Execução Unit | < 30s | < 10s |
| Tempo de Execução Integration | < 2min | < 1min |
