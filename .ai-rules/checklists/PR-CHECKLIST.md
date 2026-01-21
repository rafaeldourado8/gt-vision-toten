# ✅ Checklist de Pull Request

> Use este checklist antes de abrir qualquer PR.

## 📝 Pré-PR

### Código
- [ ] Código segue princípios SOLID
- [ ] Código segue Clean Code
- [ ] Estrutura DDD respeitada
- [ ] Arquivos na pasta correta
- [ ] Nomenclatura segue padrões

### Qualidade
- [ ] Complexidade ciclomática ≤ 10
- [ ] Funções com ≤ 20 linhas
- [ ] ≤ 3 parâmetros por função
- [ ] Sem código comentado
- [ ] Sem `console.log` ou `debugger`

### Testes
- [ ] Testes escritos (TDD)
- [ ] Todos os testes passando
- [ ] Cobertura mínima atingida:
  - [ ] Domain: 90%+
  - [ ] Application: 80%+
  - [ ] Infra: 70%+
- [ ] Sem `.only` ou `.skip`

### Verificações
- [ ] `docker-compose exec app npm run lint` ✅
- [ ] `docker-compose exec app npm test` ✅
- [ ] `docker-compose exec app npm run build` ✅

### Git
- [ ] Branch com nome correto (feature/bugfix/etc)
- [ ] Commits seguem Conventional Commits
- [ ] Rebase feito com branch alvo
- [ ] Sem commits de merge desnecessários

## 📋 PR

### Descrição
- [ ] Título claro e descritivo
- [ ] Descrição explica o "porquê"
- [ ] Issue relacionada linkada
- [ ] Screenshots (se UI)

### Tamanho
- [ ] PR tem < 400 linhas alteradas
- [ ] Se maior, justificativa no PR

---

## 🔄 Comandos Rápidos

```bash
# Verificação completa
docker-compose exec app npm run lint && \
docker-compose exec app npm test && \
docker-compose exec app npm run build

# Rebase
git fetch origin
git rebase origin/develop

# Push
git push origin [sua-branch]
```
