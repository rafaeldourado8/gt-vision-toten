# 🔀 Git Workflow

> **OBRIGATÓRIO**: Seguir padrões de commit e branches.
> **OBRIGATÓRIO**: Nunca fazer push direto para main/master.

## 🌳 Estratégia de Branches

```
main (ou master)
│
├── develop
│   │
│   ├── feature/nome-da-feature
│   ├── feature/outra-feature
│   │
│   ├── bugfix/nome-do-bug
│   │
│   └── refactor/nome-da-refatoracao
│
├── release/v1.2.0
│
└── hotfix/bug-critico
```

### Tipos de Branch

| Prefixo | Uso | Base | Merge para |
|---------|-----|------|------------|
| `feature/` | Nova funcionalidade | develop | develop |
| `bugfix/` | Correção de bug | develop | develop |
| `refactor/` | Refatoração sem nova feature | develop | develop |
| `hotfix/` | Bug crítico em produção | main | main + develop |
| `release/` | Preparar release | develop | main + develop |

### Nomenclatura de Branches

```bash
# ✅ Correto
feature/add-user-authentication
feature/implement-order-checkout
bugfix/fix-payment-calculation
refactor/extract-email-service
hotfix/fix-critical-security-issue

# ❌ Incorreto
feature/auth           # Muito vago
Feature/UserAuth       # PascalCase
feature_user_auth      # Underscore
my-feature             # Sem prefixo
```

---

## 📝 Padrão de Commits (Conventional Commits)

### Formato

```
<tipo>(<escopo>): <descrição curta>

[corpo opcional]

[rodapé opcional]
```

### Tipos de Commit

| Tipo | Uso | Exemplo |
|------|-----|---------|
| `feat` | Nova feature | `feat(auth): add JWT authentication` |
| `fix` | Correção de bug | `fix(payment): correct tax calculation` |
| `refactor` | Refatoração | `refactor(orders): extract pricing logic` |
| `test` | Testes | `test(users): add unit tests for validation` |
| `docs` | Documentação | `docs(readme): update installation guide` |
| `style` | Formatação | `style(lint): fix eslint warnings` |
| `chore` | Tarefas | `chore(deps): update dependencies` |
| `perf` | Performance | `perf(query): optimize database queries` |
| `ci` | CI/CD | `ci(github): add test workflow` |

### Regras

```bash
# ✅ Correto
feat(orders): add order cancellation endpoint
fix(auth): handle expired token gracefully
refactor(users): extract email validation to value object
test(orders): add integration tests for checkout flow

# ❌ Incorreto
Add feature                    # Sem tipo
feat: add feature              # Sem escopo
feat(auth) add login          # Sem dois pontos
FEAT(auth): ADD LOGIN          # Maiúsculas
feat(auth): Added login        # Passado
feat(auth): Add login.         # Ponto final
```

### Breaking Changes

```bash
# Commit com breaking change
feat(api)!: change response format for orders endpoint

BREAKING CHANGE: The orders endpoint now returns items as an array 
instead of an object. Update all clients to handle the new format.
```

---

## 🔄 Fluxo de Trabalho

### Nova Feature

```bash
# 1. Atualizar develop
git checkout develop
git pull origin develop

# 2. Criar branch
git checkout -b feature/add-order-validation

# 3. Desenvolver com commits pequenos e frequentes
git add .
git commit -m "feat(orders): add order validation schema"
git commit -m "test(orders): add validation unit tests"
git commit -m "feat(orders): implement validation in use case"

# 4. Manter atualizado com develop
git fetch origin
git rebase origin/develop

# 5. Push
git push origin feature/add-order-validation

# 6. Abrir Pull Request para develop
```

### Correção de Bug

```bash
# 1. Criar branch do develop
git checkout develop
git pull origin develop
git checkout -b bugfix/fix-payment-rounding

# 2. Corrigir e testar
git commit -m "fix(payment): correct rounding in currency conversion"
git commit -m "test(payment): add tests for currency rounding"

# 3. Push e PR
git push origin bugfix/fix-payment-rounding
```

### Hotfix (Bug Crítico em Produção)

```bash
# 1. Criar branch do main
git checkout main
git pull origin main
git checkout -b hotfix/fix-security-vulnerability

# 2. Corrigir
git commit -m "fix(auth): patch XSS vulnerability"

# 3. Merge para main E develop
# Via PR para main (requer aprovação)
# Após merge, fazer backport para develop
git checkout develop
git merge hotfix/fix-security-vulnerability
```

---

## 🔍 Pull Request Checklist

### Antes de Abrir PR

```bash
# 1. Rebase com a branch alvo
git fetch origin
git rebase origin/develop  # ou main

# 2. Rodar todos os testes
docker-compose exec app npm test

# 3. Verificar lint
docker-compose exec app npm run lint

# 4. Verificar build
docker-compose exec app npm run build

# 5. Review próprio do diff
git diff origin/develop
```

### Template de PR

```markdown
## Descrição
[Breve descrição do que foi feito]

## Tipo de Mudança
- [ ] Nova feature
- [ ] Bug fix
- [ ] Refatoração
- [ ] Documentação
- [ ] Outro: ___

## Checklist
- [ ] Código segue padrões do projeto
- [ ] Testes escritos e passando
- [ ] Lint sem erros
- [ ] Build funcionando
- [ ] Documentação atualizada (se necessário)
- [ ] PR tem tamanho adequado (<400 linhas)

## Screenshots (se aplicável)
[Adicionar screenshots]

## Como Testar
1. Passo 1
2. Passo 2
3. Resultado esperado

## Issues Relacionadas
Closes #123
```

---

## 🏷️ Tags e Releases

### Versionamento Semântico

```
MAJOR.MINOR.PATCH

1.0.0 → 1.0.1  # Patch: bug fix
1.0.1 → 1.1.0  # Minor: nova feature (retrocompatível)
1.1.0 → 2.0.0  # Major: breaking change
```

### Criar Release

```bash
# 1. Criar branch de release
git checkout develop
git checkout -b release/v1.2.0

# 2. Bump version
npm version minor  # ou major/patch

# 3. Merge para main
# Via PR para main

# 4. Tag
git checkout main
git pull origin main
git tag -a v1.2.0 -m "Release v1.2.0"
git push origin v1.2.0

# 5. Merge de volta para develop
git checkout develop
git merge main
```

---

## 🛡️ Proteções de Branch

### main/master

```yaml
# GitHub Branch Protection Rules
- Require pull request before merging
- Require approvals: 1 (mínimo)
- Dismiss stale reviews
- Require status checks:
  - tests
  - lint
  - build
- Require branches to be up to date
- Include administrators
```

### develop

```yaml
- Require pull request before merging
- Require status checks:
  - tests
  - lint
```

---

## 📋 Git Hooks (Husky)

### Configuração

```json
// package.json
{
  "husky": {
    "hooks": {
      "pre-commit": "lint-staged",
      "commit-msg": "commitlint -E HUSKY_GIT_PARAMS",
      "pre-push": "npm test"
    }
  },
  "lint-staged": {
    "*.ts": [
      "eslint --fix",
      "prettier --write"
    ]
  }
}
```

### commitlint.config.js

```javascript
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      ['feat', 'fix', 'refactor', 'test', 'docs', 'style', 'chore', 'perf', 'ci']
    ],
    'scope-empty': [2, 'never'],
    'subject-case': [2, 'always', 'lower-case'],
    'subject-full-stop': [2, 'never', '.'],
  }
};
```

---

## ✅ Resumo de Regras

```
✅ Sempre criar branch para mudanças
✅ Commits pequenos e frequentes
✅ Seguir Conventional Commits
✅ Rebase antes de PR
✅ Rodar testes antes de push
✅ Code review obrigatório
✅ Squash merge para main

❌ Push direto para main/develop
❌ Commits gigantes
❌ Mensagens vagas como "fix" ou "update"
❌ Merge sem testes passando
❌ Force push em branches compartilhadas
```
