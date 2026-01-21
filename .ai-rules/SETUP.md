# 🚀 Instalação do .ai-rules

## Método 1: Copiar Diretório

```bash
# Copiar para novo projeto
cp -r .ai-rules /caminho/do/novo/projeto/

# Ou usando rsync
rsync -av .ai-rules/ /caminho/do/novo/projeto/.ai-rules/
```

## Método 2: Git Subtree

```bash
# Adicionar como subtree
git subtree add --prefix=.ai-rules https://github.com/seu-user/ai-rules.git main --squash

# Atualizar posteriormente
git subtree pull --prefix=.ai-rules https://github.com/seu-user/ai-rules.git main --squash
```

## Método 3: Script de Inicialização

Crie um script `init-ai-rules.sh`:

```bash
#!/bin/bash

# Criar estrutura
mkdir -p .ai-rules/{rules,templates,checklists,context,scripts,docker}

# Baixar arquivos (se hospedado)
# curl -o .ai-rules/RULES.md https://raw.githubusercontent.com/.../RULES.md

echo "✅ .ai-rules inicializado!"
echo "📝 Não esqueça de:"
echo "   1. Editar context/PROJECT.md com info do projeto"
echo "   2. Editar context/CURRENT_SPRINT.md com sprint atual"
```

## Após Instalação

1. **Personalize o contexto:**
   ```bash
   # Editar informações do projeto
   nano .ai-rules/context/PROJECT.md
   
   # Editar sprint atual
   nano .ai-rules/context/CURRENT_SPRINT.md
   ```

2. **Configure seu AI assistant:**
   - Siga as instruções em `.ai-rules/AI-ASSISTANT-INSTRUCTIONS.md`

3. **Adicione ao .gitignore (opcional):**
   ```bash
   # Se não quiser versionar contexto específico
   echo ".ai-rules/context/CURRENT_SPRINT.md" >> .gitignore
   ```

## Estrutura Criada

```
.ai-rules/
├── RULES.md                      # 🎯 Ponto de entrada
├── AI-ASSISTANT-INSTRUCTIONS.md  # 🤖 Config para AIs
│
├── rules/                        # 📜 Regras detalhadas
│   ├── ARCHITECTURE.md           # SOLID, Clean Code, DDD
│   ├── TESTING.md                # TDD, Testes
│   ├── DOCKER.md                 # Containers
│   ├── CODE-QUALITY.md           # Complexidade, Lint
│   ├── FOLDER-STRUCTURE.md       # Estrutura de pastas
│   └── GIT-WORKFLOW.md           # Git flow
│
├── context/                      # 📋 Contexto do projeto
│   ├── PROJECT.md                # Info do projeto
│   └── CURRENT_SPRINT.md         # Sprint atual
│
├── checklists/                   # ✅ Checklists
│   ├── PR-CHECKLIST.md
│   └── NEW-FEATURE-CHECKLIST.md
│
├── templates/                    # 📝 Templates de código
│   ├── entity.template.ts
│   ├── value-object.template.ts
│   ├── use-case.template.ts
│   └── unit-test.template.ts
│
└── SETUP.md                      # Este arquivo
```
