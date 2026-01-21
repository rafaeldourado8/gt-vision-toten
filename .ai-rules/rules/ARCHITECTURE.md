# 🏗️ Regras de Arquitetura

> **LEITURA OBRIGATÓRIA** antes de criar qualquer classe, módulo ou serviço.

## 📐 SOLID Principles

### S - Single Responsibility Principle (SRP)
```
✅ Uma classe = Uma responsabilidade = Um motivo para mudar
❌ Classes "God Object" que fazem tudo
```

**Exemplo Correto:**
```typescript
// ✅ Cada classe tem uma responsabilidade
class UserValidator {
  validate(user: User): ValidationResult { }
}

class UserRepository {
  save(user: User): Promise<void> { }
}

class UserNotificationService {
  sendWelcomeEmail(user: User): Promise<void> { }
}
```

**Exemplo Errado:**
```typescript
// ❌ Uma classe fazendo tudo
class UserService {
  validate(user: User) { }
  save(user: User) { }
  sendEmail(user: User) { }
  generateReport(user: User) { }
}
```

### O - Open/Closed Principle (OCP)
```
✅ Aberto para extensão, fechado para modificação
✅ Use interfaces e abstrações
❌ Modificar código existente para adicionar features
```

**Padrão Obrigatório:**
```typescript
// Interface base
interface PaymentProcessor {
  process(payment: Payment): Promise<PaymentResult>;
}

// Extensões (não modificam o original)
class CreditCardProcessor implements PaymentProcessor { }
class PixProcessor implements PaymentProcessor { }
class BoletoProcessor implements PaymentProcessor { }
```

### L - Liskov Substitution Principle (LSP)
```
✅ Subclasses devem ser substituíveis por suas classes base
✅ Não quebrar contratos de interface
❌ Override que muda comportamento esperado
```

### I - Interface Segregation Principle (ISP)
```
✅ Interfaces pequenas e específicas
✅ Clientes não dependem de métodos que não usam
❌ Interfaces "fat" com muitos métodos
```

**Exemplo:**
```typescript
// ✅ Interfaces segregadas
interface Readable {
  read(): Data;
}

interface Writable {
  write(data: Data): void;
}

interface Deletable {
  delete(): void;
}

// Composição conforme necessidade
class FileStorage implements Readable, Writable, Deletable { }
class ReadOnlyStorage implements Readable { }
```

### D - Dependency Inversion Principle (DIP)
```
✅ Dependa de abstrações, não de implementações
✅ Use injeção de dependência
❌ Instanciar dependências dentro de classes
```

**Obrigatório:**
```typescript
// ✅ Injeção de dependência
class OrderService {
  constructor(
    private readonly orderRepository: OrderRepository,  // Interface
    private readonly paymentGateway: PaymentGateway,    // Interface
    private readonly notifier: Notifier                 // Interface
  ) {}
}

// ❌ NUNCA fazer isso
class OrderService {
  private orderRepository = new MySQLOrderRepository(); // Concreto!
}
```

---

## 🧹 Clean Code

### Nomenclatura
```
✅ Nomes descritivos e pronunciáveis
✅ Verbos para funções: getUserById, calculateTotal
✅ Substantivos para classes: UserRepository, OrderValidator
✅ Booleanos com prefixo: isActive, hasPermission, canExecute
❌ Abreviações obscuras: usr, calc, proc
❌ Nomes genéricos: data, info, temp, aux
```

### Funções
```
✅ Máximo 20 linhas por função
✅ Máximo 3 parâmetros (use objeto se precisar mais)
✅ Uma função = Uma tarefa
✅ Evite efeitos colaterais
❌ Funções que fazem mais de uma coisa
```

### Comentários
```
✅ Código auto-explicativo > comentários
✅ Comentários para "por quê", não "o quê"
✅ JSDoc/TSDoc para APIs públicas
❌ Comentários óbvios: // incrementa contador
❌ Código comentado (delete!)
```

### Formatação
```
✅ Indentação consistente (2 ou 4 espaços)
✅ Linha máxima: 100-120 caracteres
✅ Arquivo máximo: 200-300 linhas
✅ Agrupar código relacionado
```

---

## 🎯 Domain-Driven Design (DDD)

### Estrutura de Bounded Context
```
src/
├── @core/                      # Kernel compartilhado
│   ├── domain/
│   │   ├── value-objects/      # VOs reutilizáveis
│   │   └── events/             # Eventos de domínio base
│   └── infra/
│       ├── database/
│       └── messaging/
│
├── [bounded-context]/          # Ex: orders, users, payments
│   ├── domain/
│   │   ├── entities/           # Entidades do domínio
│   │   ├── value-objects/      # Value Objects
│   │   ├── aggregates/         # Aggregates
│   │   ├── repositories/       # Interfaces de repositório
│   │   ├── services/           # Domain Services
│   │   └── events/             # Domain Events
│   │
│   ├── application/
│   │   ├── use-cases/          # Casos de uso
│   │   ├── dtos/               # Data Transfer Objects
│   │   └── mappers/            # Conversões Entity <-> DTO
│   │
│   └── infra/
│       ├── repositories/       # Implementações de repositório
│       ├── controllers/        # Controllers HTTP/GraphQL
│       └── providers/          # Serviços externos
```

### Regras de Camadas

**Domain Layer (Coração)**
```
✅ Zero dependências externas (nem framework)
✅ Entidades com comportamento (não apenas dados)
✅ Value Objects imutáveis
✅ Agregados protegem invariantes
❌ Imports de infra ou application
```

**Application Layer (Orquestração)**
```
✅ Use Cases orquestram o domínio
✅ Depende apenas de Domain
✅ Define interfaces para Infra
❌ Lógica de negócio aqui
```

**Infrastructure Layer (Adaptadores)**
```
✅ Implementa interfaces do Domain/Application
✅ Detalhes técnicos: DB, HTTP, Queues
✅ Pode usar frameworks
❌ Lógica de negócio
```

### Entidades vs Value Objects

**Entity:**
```typescript
// ✅ Tem identidade, pode mudar ao longo do tempo
class Order {
  constructor(
    private readonly id: OrderId,  // Identidade
    private items: OrderItem[],
    private status: OrderStatus
  ) {}
  
  addItem(item: OrderItem): void { }
  cancel(): void { }
}
```

**Value Object:**
```typescript
// ✅ Sem identidade, imutável, comparado por valor
class Money {
  private constructor(
    readonly amount: number,
    readonly currency: Currency
  ) {}
  
  static create(amount: number, currency: Currency): Money {
    // validações
    return new Money(amount, currency);
  }
  
  add(other: Money): Money {
    // retorna NOVO objeto
    return Money.create(this.amount + other.amount, this.currency);
  }
  
  equals(other: Money): boolean {
    return this.amount === other.amount && 
           this.currency === other.currency;
  }
}
```

### Aggregates

```
✅ Uma entidade raiz por agregado
✅ Acesso externo APENAS pela raiz
✅ Transação = 1 agregado
✅ Referência entre agregados por ID, não objeto
```

```typescript
// ✅ Order é a raiz do agregado
class Order {
  private items: OrderItem[];  // Interno ao agregado
  
  // Acesso controlado pela raiz
  addItem(product: ProductId, quantity: number): void {
    const item = OrderItem.create(product, quantity);
    this.items.push(item);
  }
}

// ❌ NUNCA expor internos
order.items.push(new OrderItem()); // ERRADO!
```

---

## ✅ Checklist de Revisão

Antes de finalizar qualquer código, verifique:

- [ ] Classe tem apenas UMA responsabilidade?
- [ ] Novas features foram por extensão (não modificação)?
- [ ] Dependências são injetadas via construtor?
- [ ] Nomes são claros e descritivos?
- [ ] Funções têm no máximo 20 linhas?
- [ ] Entidades estão no Domain layer?
- [ ] Value Objects são imutáveis?
- [ ] Agregados protegem seus invariantes?
- [ ] Não há import de infra no domain?
