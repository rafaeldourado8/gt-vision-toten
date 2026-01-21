# 📊 Regras de Qualidade de Código

> **OBRIGATÓRIO**: Código deve passar em TODAS as verificações antes de commit.
> **OBRIGATÓRIO**: Complexidade ciclomática máxima: 10.

## 🔄 Complexidade Ciclomática

### O que é?
Mede o número de caminhos independentes através do código. Cada `if`, `for`, `while`, `case`, `&&`, `||`, `?:` adiciona +1.

### Limites Obrigatórios

| Nível | Complexidade | Ação |
|-------|--------------|------|
| 🟢 Simples | 1-4 | ✅ Ideal |
| 🟡 Moderado | 5-7 | ⚠️ Considerar refatorar |
| 🟠 Complexo | 8-10 | 🔶 Refatorar se possível |
| 🔴 Muito Complexo | 11+ | ❌ OBRIGATÓRIO refatorar |

### Exemplo de Refatoração

**❌ Antes (Complexidade: 12)**
```typescript
function processOrder(order: Order): Result {
  if (!order) return Result.fail('No order');           // +1
  if (!order.items) return Result.fail('No items');     // +1
  
  let total = 0;
  for (const item of order.items) {                     // +1
    if (item.quantity <= 0) continue;                   // +1
    if (item.price < 0) return Result.fail('Invalid');  // +1
    
    if (item.discount) {                                // +1
      if (item.discount.type === 'percent') {           // +1
        total += item.price * (1 - item.discount.value / 100);
      } else if (item.discount.type === 'fixed') {      // +1
        total += Math.max(0, item.price - item.discount.value);
      } else {                                          // +1
        total += item.price;
      }
    } else {
      total += item.price;
    }
  }
  
  if (order.coupon && order.coupon.isValid()) {        // +2
    total = order.coupon.apply(total);
  }
  
  return Result.ok(total);
}
```

**✅ Depois (Complexidade: 3 por função)**
```typescript
function processOrder(order: Order): Result<number> {
  const validation = this.validateOrder(order);
  if (validation.isFailure) return validation;
  
  const total = this.calculateTotal(order.items);
  const finalTotal = this.applyCoupon(total, order.coupon);
  
  return Result.ok(finalTotal);
}

private validateOrder(order: Order): Result<void> {
  if (!order) return Result.fail('No order');
  if (!order.items?.length) return Result.fail('No items');
  return Result.ok();
}

private calculateTotal(items: OrderItem[]): number {
  return items
    .filter(item => item.quantity > 0)
    .reduce((sum, item) => sum + this.calculateItemPrice(item), 0);
}

private calculateItemPrice(item: OrderItem): number {
  if (!item.discount) return item.price;
  return item.discount.apply(item.price);
}

private applyCoupon(total: number, coupon?: Coupon): number {
  if (!coupon?.isValid()) return total;
  return coupon.apply(total);
}
```

---

## 📏 Métricas de Código

### Limites por Arquivo/Função

| Métrica | Limite | Ação se Exceder |
|---------|--------|-----------------|
| Linhas por função | 20 | Extrair funções |
| Parâmetros por função | 3 | Usar objeto/DTO |
| Linhas por arquivo | 300 | Dividir responsabilidades |
| Profundidade de aninhamento | 3 | Extrair ou early return |
| Complexidade ciclomática | 10 | Refatorar obrigatório |

### Configuração ESLint
```javascript
// .eslintrc.js
module.exports = {
  rules: {
    'complexity': ['error', { max: 10 }],
    'max-lines-per-function': ['error', { max: 20, skipBlankLines: true, skipComments: true }],
    'max-params': ['error', 3],
    'max-depth': ['error', 3],
    'max-lines': ['error', { max: 300, skipBlankLines: true, skipComments: true }],
    'max-nested-callbacks': ['error', 3],
  }
};
```

### Configuração SonarQube (se usar)
```yaml
# sonar-project.properties
sonar.javascript.lcov.reportPaths=coverage/lcov.info

# Limites
sonar.issue.ignore.multicriteria=e1
sonar.issue.ignore.multicriteria.e1.ruleKey=typescript:S3776
sonar.issue.ignore.multicriteria.e1.resourceKey=**/*.spec.ts
```

---

## 🧹 Linting Obrigatório

### Configuração Base (.eslintrc.js)
```javascript
module.exports = {
  parser: '@typescript-eslint/parser',
  parserOptions: {
    project: 'tsconfig.json',
    sourceType: 'module',
  },
  plugins: ['@typescript-eslint/eslint-plugin', 'import'],
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:@typescript-eslint/recommended-requiring-type-checking',
    'plugin:import/errors',
    'plugin:import/warnings',
    'plugin:import/typescript',
  ],
  root: true,
  env: {
    node: true,
    jest: true,
  },
  ignorePatterns: ['.eslintrc.js', 'dist/', 'node_modules/'],
  rules: {
    // Complexidade
    'complexity': ['error', { max: 10 }],
    'max-lines-per-function': ['error', { max: 20, skipBlankLines: true, skipComments: true }],
    'max-params': ['error', 3],
    'max-depth': ['error', 3],
    
    // TypeScript
    '@typescript-eslint/explicit-function-return-type': 'error',
    '@typescript-eslint/explicit-module-boundary-types': 'error',
    '@typescript-eslint/no-explicit-any': 'error',
    '@typescript-eslint/no-unused-vars': 'error',
    '@typescript-eslint/no-floating-promises': 'error',
    
    // Imports
    'import/order': ['error', {
      'groups': [
        'builtin',
        'external',
        'internal',
        ['parent', 'sibling'],
        'index'
      ],
      'newlines-between': 'always',
      'alphabetize': { order: 'asc' }
    }],
    'import/no-cycle': 'error',
    
    // Geral
    'no-console': 'error',
    'no-debugger': 'error',
    'eqeqeq': ['error', 'always'],
    'curly': ['error', 'all'],
  },
};
```

### Prettier (.prettierrc)
```json
{
  "semi": true,
  "trailingComma": "all",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false,
  "bracketSpacing": true,
  "arrowParens": "avoid"
}
```

---

## 🔍 Code Review Checklist

### Antes de Abrir PR

```bash
# 1. Lint
docker-compose exec app npm run lint
# Zero erros!

# 2. Testes
docker-compose exec app npm test
# Todos passando!

# 3. Build
docker-compose exec app npm run build
# Sem erros de compilação!

# 4. Cobertura
docker-compose exec app npm run test:coverage
# Mínimo atingido!
```

### Durante Code Review

**Arquitetura**
- [ ] Segue SOLID?
- [ ] Segue padrão de camadas DDD?
- [ ] Não há dependências circulares?
- [ ] Novos arquivos estão na pasta correta?

**Código**
- [ ] Complexidade ciclomática ≤ 10?
- [ ] Funções ≤ 20 linhas?
- [ ] Parâmetros ≤ 3?
- [ ] Nomes são descritivos?
- [ ] Sem código morto/comentado?
- [ ] Sem `any` explícito?

**Testes**
- [ ] Cobertura mínima atingida?
- [ ] Testes seguem AAA?
- [ ] Sem `.only` ou `.skip`?
- [ ] Testes são independentes?

**Segurança**
- [ ] Sem dados sensíveis hardcoded?
- [ ] Inputs são validados?
- [ ] Sem SQL/NoSQL injection?
- [ ] Logs não expõem dados sensíveis?

---

## 📈 Scripts package.json

```json
{
  "scripts": {
    "lint": "eslint \"{src,tests}/**/*.ts\" --max-warnings 0",
    "lint:fix": "eslint \"{src,tests}/**/*.ts\" --fix",
    "format": "prettier --write \"src/**/*.ts\" \"tests/**/*.ts\"",
    "format:check": "prettier --check \"src/**/*.ts\" \"tests/**/*.ts\"",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "test:integration": "jest --config jest.integration.config.js",
    "test:e2e": "jest --config jest.e2e.config.js",
    "build": "tsc -p tsconfig.build.json",
    "check": "npm run lint && npm run format:check && npm run test && npm run build"
  }
}
```

---

## 🚫 Código Proibido

```typescript
// ❌ NUNCA fazer isso

// 1. any explícito
const data: any = fetchData();

// 2. Console em produção
console.log('debug:', data);

// 3. Código comentado
// const oldImplementation = ...

// 4. Magic numbers
if (status === 1) { }  // O que é 1?

// 5. Strings mágicas
if (role === 'admin') { }  // Usar enum!

// 6. Nested callbacks hell
getData(data => {
  process(data, result => {
    save(result, response => {
      // ...
    });
  });
});

// 7. Mutação de parâmetros
function update(user) {
  user.name = 'changed';  // ❌ Muta o original
}

// 8. Catch vazio
try { } catch (e) { }  // Engole erro!

// 9. == ao invés de ===
if (value == null) { }  // Use ===
```

---

## ✅ Checklist Final

Antes de cada commit:

```bash
# Executar verificação completa
docker-compose exec app npm run check

# Ou individualmente:
docker-compose exec app npm run lint
docker-compose exec app npm run format:check
docker-compose exec app npm test
docker-compose exec app npm run build
```

Todos devem passar com **ZERO erros** e **ZERO warnings**.
