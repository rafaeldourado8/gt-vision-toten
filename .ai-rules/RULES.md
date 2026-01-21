# 🤖 AI Code Assistant Rules

> **INSTRUÇÃO OBRIGATÓRIA**: Leia este arquivo COMPLETAMENTE antes de executar qualquer tarefa.
> Este diretório mantém contexto e regras para QUALQUER code assistant (Cursor, Copilot, Claude, etc).

## 📋 Índice de Regras

| Arquivo | Descrição | Prioridade |
|---------|-----------|------------|
| [rules/BOILERPLATE-USAGE.md](rules/BOILERPLATE-USAGE.md) | Uso correto do boilerplate | 🔴 CRÍTICA |
| [rules/ARCHITECTURE.md](rules/ARCHITECTURE.md) | SOLID, Clean Code, DDD | 🔴 CRÍTICA |
| [rules/TESTING.md](rules/TESTING.md) | TDD, Testes, Cobertura | 🔴 CRÍTICA |
| [rules/DOCKER.md](rules/DOCKER.md) | Containers, Docker Compose | 🟡 ALTA |
| [rules/CODE-QUALITY.md](rules/CODE-QUALITY.md) | Complexidade, Linting | 🟡 ALTA |
| [rules/FOLDER-STRUCTURE.md](rules/FOLDER-STRUCTURE.md) | Padrão de Pastas | 🟡 ALTA |
| [rules/GIT-WORKFLOW.md](rules/GIT-WORKFLOW.md) | Commits, Branches | 🟢 MÉDIA |

## ⚠️ REGRAS ABSOLUTAS (NUNCA VIOLAR)

```
1. NUNCA copiar código diretamente dos projetos de origem (vms-v2, StudyFlow-IA, Focus-AI)
2. SEMPRE adaptar e generalizar padrões antes de adicionar ao boilerplate
3. NUNCA criar arquivos .md fora de .ai-rules/ ou docs/
4. NUNCA fazer merge sem testes passando
5. NUNCA commitar código sem rodar linter
6. NUNCA ignorar erros de complexidade ciclomática
7. SEMPRE seguir estrutura de pastas definida
8. SEMPRE testar com docker-compose exec antes de PR
```

## 🚀 Fluxo de Trabalho Obrigatório

### Antes de Codar
```bash
# 1. Ler contexto do projeto
cat .ai-rules/context/PROJECT.md

# 2. Verificar bounded contexts existentes
ls -la src/

# 3. Entender a task atual
cat .ai-rules/context/CURRENT_SPRINT.md
```

### Durante o Código
```bash
# 1. Criar feature branch
git checkout -b feature/nome-descritivo

# 2. Seguir TDD
# - Escrever teste primeiro
# - Rodar teste (deve falhar)
# - Implementar código mínimo
# - Rodar teste (deve passar)
# - Refatorar

# 3. Validar complexidade
npm run lint  # ou equivalente
```

### Antes de Commitar
```bash
# 1. Rodar TODOS os testes
docker-compose exec app npm test

# 2. Verificar cobertura
docker-compose exec app npm run test:coverage

# 3. Lint check
docker-compose exec app npm run lint

# 4. Build check
docker-compose exec app npm run build
```

## 📁 Estrutura Esperada do Projeto

```
projeto/
├── .ai-rules/              # 🤖 ESTE DIRETÓRIO (regras AI)
├── docs/                   # 📚 Documentação do projeto
├── docker/                 # 🐳 Dockerfiles por bounded context
│   ├── api/
│   ├── worker/
│   └── web/
├── src/                    # 💻 Código fonte
│   ├── @core/              # Kernel compartilhado
│   ├── bounded-context-1/  # Contexto delimitado 1
│   └── bounded-context-2/  # Contexto delimitado 2
├── tests/                  # 🧪 Testes (espelha src/)
├── docker-compose.yml
├── docker-compose.test.yml
└── docker-compose.dev.yml
```

## 🔄 Comandos Rápidos

| Ação | Comando |
|------|---------|
| Subir ambiente | `docker-compose up -d` |
| Rodar testes | `docker-compose exec app npm test` |
| Testes + watch | `docker-compose exec app npm run test:watch` |
| Lint | `docker-compose exec app npm run lint` |
| Lint fix | `docker-compose exec app npm run lint:fix` |
| Build | `docker-compose exec app npm run build` |
| Shell no container | `docker-compose exec app sh` |

## 📖 Como Usar Este Diretório

### Para AI Assistants (Cursor, Copilot, Claude, etc)

1. **Início de Sessão**: Sempre ler `RULES.md` primeiro
2. **Nova Feature**: Consultar `rules/ARCHITECTURE.md`
3. **Escrevendo Testes**: Consultar `rules/TESTING.md`
4. **Criando Container**: Consultar `rules/DOCKER.md`
5. **Dúvida de Pasta**: Consultar `rules/FOLDER-STRUCTURE.md`

### Para Desenvolvedores

1. Clone este diretório para novos projetos
2. Personalize `context/PROJECT.md` com detalhes do projeto
3. Atualize `context/CURRENT_SPRINT.md` a cada sprint
4. Adicione regras específicas em `rules/`

---

**Versão**: 1.0.0  
**Última Atualização**: 2025-01-18
