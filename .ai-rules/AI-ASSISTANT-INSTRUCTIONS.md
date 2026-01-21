# 🤖 Instruções para AI Assistants

> Este arquivo contém instruções específicas para diferentes code assistants.

## 📋 Instruções Universais

**ANTES DE QUALQUER AÇÃO, LEIA:**

1. `.ai-rules/RULES.md` - Ponto de entrada obrigatório
2. `.ai-rules/context/PROJECT.md` - Contexto do projeto
3. `.ai-rules/context/CURRENT_SPRINT.md` - Sprint atual

**NUNCA:**
- Crie arquivos `.md` fora de `.ai-rules/` ou `docs/`
- Ignore os princípios SOLID e Clean Code
- Escreva código sem testes
- Faça merge sem testes passando
- Ignore erros de lint ou complexidade

---

## 🔷 Cursor AI

### Configuração (.cursorrules)

Copie para `.cursorrules` na raiz do projeto:

```
# Cursor Rules

## Contexto Obrigatório
Sempre leia os arquivos em .ai-rules/ antes de responder.
Prioridade: RULES.md > context/PROJECT.md > context/CURRENT_SPRINT.md

## Regras de Código
- Siga SOLID, Clean Code e DDD conforme .ai-rules/rules/ARCHITECTURE.md
- Use TDD conforme .ai-rules/rules/TESTING.md
- Estrutura de pastas conforme .ai-rules/rules/FOLDER-STRUCTURE.md
- Complexidade ciclomática máxima: 10

## Antes de Gerar Código
1. Pergunte em qual bounded context o código deve ser criado
2. Confirme a estrutura de pastas
3. Gere teste PRIMEIRO, depois implementação

## Proibições
- Não crie arquivos .md fora de .ai-rules/ ou docs/
- Não use `any` em TypeScript
- Não ignore erros de lint
- Não faça funções com mais de 20 linhas
```

---

## 🟣 GitHub Copilot

### Configuração (.github/copilot-instructions.md)

```markdown
# Copilot Instructions

## Project Rules
This project follows strict architectural guidelines documented in `.ai-rules/`.

Before generating code:
1. Check `.ai-rules/rules/ARCHITECTURE.md` for SOLID and DDD patterns
2. Check `.ai-rules/rules/FOLDER-STRUCTURE.md` for file locations
3. Follow TDD - write tests first

## Code Standards
- Max cyclomatic complexity: 10
- Max function lines: 20
- Max parameters: 3
- Always use TypeScript strict mode
- Never use `any` type

## Testing
- All code must have tests
- Follow AAA pattern (Arrange-Act-Assert)
- Use Object Mothers for test data
- Run tests via: docker-compose exec app npm test
```

---

## 🟠 Claude (Anthropic)

### Instruções Diretas

Ao usar Claude para este projeto, inicie a conversa com:

```
Você está trabalhando em um projeto que segue regras estritas de arquitetura.
Antes de qualquer código, leia os arquivos em .ai-rules/:

1. RULES.md - Regras principais
2. rules/ARCHITECTURE.md - SOLID, Clean Code, DDD
3. rules/TESTING.md - TDD obrigatório
4. rules/FOLDER-STRUCTURE.md - Estrutura de pastas
5. context/PROJECT.md - Contexto do projeto
6. context/CURRENT_SPRINT.md - Sprint atual

Regras absolutas:
- NUNCA crie .md fora de .ai-rules/ ou docs/
- SEMPRE use TDD (teste primeiro)
- SEMPRE verifique complexidade ciclomática (max 10)
- SEMPRE siga estrutura DDD
- SEMPRE rode testes via docker-compose exec
```

---

## 🟢 Amazon CodeWhisperer / Q

### Configuração (devfile.yaml)

```yaml
schemaVersion: 2.2.0
metadata:
  name: project-rules
components:
  - name: code-standards
    attributes:
      ai-rules-path: .ai-rules/
      architecture: DDD
      testing: TDD
      max-complexity: 10
```

---

## 🔵 Tabnine

### Configuração (.tabnine.json)

```json
{
  "projectContext": {
    "rulesDirectory": ".ai-rules",
    "architecture": "DDD",
    "testing": "TDD",
    "language": "TypeScript"
  },
  "codeStandards": {
    "maxComplexity": 10,
    "maxFunctionLines": 20,
    "maxParameters": 3
  }
}
```

---

## 📝 Prompt Universal para Qualquer AI

Use este prompt ao iniciar uma sessão com qualquer AI assistant:

```
Contexto do Projeto:

Este projeto segue uma arquitetura rigorosa baseada em DDD (Domain-Driven Design).
As regras completas estão em .ai-rules/

REGRAS OBRIGATÓRIAS:
1. SOLID principles (todas as 5)
2. Clean Code (funções pequenas, nomes descritivos)
3. TDD (Test-Driven Development) - SEMPRE teste primeiro
4. Complexidade ciclomática máxima: 10
5. Estrutura de pastas DDD: domain/ → application/ → infra/

PROIBIÇÕES:
- Arquivos .md fora de .ai-rules/ ou docs/
- Código sem testes
- Funções > 20 linhas
- Parâmetros > 3 por função
- Uso de `any` em TypeScript

ANTES DE CADA TAREFA:
1. Leia .ai-rules/RULES.md
2. Leia .ai-rules/context/CURRENT_SPRINT.md
3. Identifique o bounded context correto
4. Siga o checklist em .ai-rules/checklists/

PARA TESTAR:
docker-compose exec app npm test
docker-compose exec app npm run lint
```

---

## 🔄 Atualização de Contexto

Ao iniciar nova sessão, sempre informe o AI:

```
Atualização de contexto:
- Sprint atual: [número]
- Task em andamento: #[número]
- Bounded context: [nome]
- Branch: [nome da branch]
- Último comando executado: [comando]
```
