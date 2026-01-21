# 🐳 Regras de Docker

> **OBRIGATÓRIO**: Cada bounded context DEVE ter seu próprio Dockerfile.
> **OBRIGATÓRIO**: Sempre testar via `docker-compose exec`.

## 📁 Estrutura de Diretórios Docker

```
docker/
├── [bounded-context-1]/
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   └── entrypoint.sh
│
├── [bounded-context-2]/
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   └── entrypoint.sh
│
├── nginx/
│   ├── Dockerfile
│   └── nginx.conf
│
└── postgres/
    ├── Dockerfile
    └── init.sql
```

---

## 📄 Dockerfile Padrão (Multi-stage)

```dockerfile
# docker/api/Dockerfile

# ============================================
# Stage 1: Dependencies
# ============================================
FROM node:20-alpine AS deps

WORKDIR /app

# Copiar apenas arquivos de dependência primeiro (cache)
COPY package*.json ./
COPY yarn.lock* ./

# Instalar dependências
RUN npm ci --only=production && npm cache clean --force

# ============================================
# Stage 2: Builder
# ============================================
FROM node:20-alpine AS builder

WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Build
RUN npm run build

# Remover devDependencies
RUN npm prune --production

# ============================================
# Stage 3: Runner (Produção)
# ============================================
FROM node:20-alpine AS runner

# Segurança: não rodar como root
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 appuser

WORKDIR /app

# Copiar apenas o necessário
COPY --from=builder --chown=appuser:nodejs /app/dist ./dist
COPY --from=builder --chown=appuser:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=appuser:nodejs /app/package.json ./

USER appuser

EXPOSE 3000

ENV NODE_ENV=production

CMD ["node", "dist/main.js"]
```

---

## 📄 Dockerfile.dev (Desenvolvimento)

```dockerfile
# docker/api/Dockerfile.dev

FROM node:20-alpine

WORKDIR /app

# Instalar ferramentas úteis para dev
RUN apk add --no-cache git curl

# Copiar arquivos de dependência
COPY package*.json ./

# Instalar TODAS as dependências (incluindo dev)
RUN npm install

# Não copiar código - usar volume
# COPY . .

EXPOSE 3000

# Hot reload
CMD ["npm", "run", "dev"]
```

---

## 🐙 Docker Compose

### docker-compose.yml (Base)
```yaml
version: '3.8'

services:
  api:
    build:
      context: .
      dockerfile: docker/api/Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgres://user:pass@db:5432/app
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  worker:
    build:
      context: .
      dockerfile: docker/worker/Dockerfile
    environment:
      - NODE_ENV=production
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis
      - db

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=app
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./docker/postgres/init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d app"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### docker-compose.dev.yml (Override para Dev)
```yaml
version: '3.8'

services:
  api:
    build:
      context: .
      dockerfile: docker/api/Dockerfile.dev
    volumes:
      - .:/app
      - /app/node_modules  # Preservar node_modules do container
    environment:
      - NODE_ENV=development
    command: npm run dev

  worker:
    build:
      context: .
      dockerfile: docker/worker/Dockerfile.dev
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
    command: npm run dev:worker
```

### docker-compose.test.yml (Para Testes)
```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: docker/api/Dockerfile.dev
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - NODE_ENV=test
      - DATABASE_URL=postgres://test:test@db-test:5432/test
    depends_on:
      db-test:
        condition: service_healthy

  db-test:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=test
      - POSTGRES_PASSWORD=test
      - POSTGRES_DB=test
    tmpfs:
      - /var/lib/postgresql/data  # RAM = velocidade
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U test -d test"]
      interval: 2s
      timeout: 2s
      retries: 10
```

---

## 🚀 Comandos Docker Obrigatórios

### Desenvolvimento
```bash
# Subir ambiente de desenvolvimento
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# Ver logs
docker-compose logs -f api

# Acessar shell do container
docker-compose exec api sh

# Instalar nova dependência
docker-compose exec api npm install package-name
```

### Testes (SEMPRE usar estes)
```bash
# Rodar testes unitários
docker-compose exec api npm test

# Rodar testes com watch
docker-compose exec api npm run test:watch

# Rodar testes de integração
docker-compose -f docker-compose.test.yml run --rm app npm run test:integration

# Rodar testes E2E
docker-compose -f docker-compose.test.yml run --rm app npm run test:e2e

# Cobertura
docker-compose exec api npm run test:coverage
```

### Build e Deploy
```bash
# Build de produção
docker-compose build --no-cache

# Build específico
docker-compose build api

# Push para registry
docker-compose push api
```

---

## 🔒 Boas Práticas de Segurança

### No Dockerfile
```dockerfile
# ✅ Usar usuário não-root
RUN addgroup --system app && adduser --system --ingroup app app
USER app

# ✅ Usar imagens específicas (não latest)
FROM node:20.10.0-alpine

# ✅ Não copiar arquivos sensíveis
# Use .dockerignore

# ✅ Usar multi-stage builds
# Reduz tamanho e superfície de ataque
```

### .dockerignore
```
node_modules
npm-debug.log
.git
.gitignore
.env
.env.*
*.md
docker-compose*.yml
.ai-rules
tests
coverage
.nyc_output
.vscode
.idea
```

---

## 📊 Health Checks Obrigatórios

```yaml
services:
  api:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### Endpoint de Health
```typescript
// src/infra/http/health.controller.ts
@Controller('health')
export class HealthController {
  @Get()
  check() {
    return {
      status: 'ok',
      timestamp: new Date().toISOString(),
      uptime: process.uptime(),
    };
  }
  
  @Get('ready')
  async readiness() {
    // Verificar conexões
    const dbOk = await this.checkDatabase();
    const redisOk = await this.checkRedis();
    
    if (!dbOk || !redisOk) {
      throw new ServiceUnavailableException();
    }
    
    return { status: 'ready' };
  }
}
```

---

## ✅ Checklist Docker

Antes de criar/modificar containers:

- [ ] Dockerfile usa multi-stage build?
- [ ] Usuário não-root configurado?
- [ ] .dockerignore atualizado?
- [ ] Health check configurado?
- [ ] Volumes para dados persistentes?
- [ ] Variáveis de ambiente documentadas?
- [ ] Bounded context tem seu próprio Dockerfile?
- [ ] docker-compose.test.yml funciona?

Antes de commit:

- [ ] `docker-compose build` funciona sem erros?
- [ ] `docker-compose exec app npm test` passa?
- [ ] `docker-compose exec app npm run lint` passa?
