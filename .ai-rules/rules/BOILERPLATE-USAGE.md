# ⚠️ Regras de Uso do Boilerplate

> **LEITURA OBRIGATÓRIA** antes de usar qualquer módulo deste toolkit.

## 🎯 Propósito

Este boilerplate é um **toolkit de aceleração**, não um framework ou projeto completo.

**Objetivo**: Fornecer building blocks testados e padrões arquiteturais para acelerar novos projetos.

---

## ✅ USO PERMITIDO

### Inspiração e Adaptação
- Estudar padrões arquiteturais implementados
- Entender como aplicar DDD, SOLID e Clean Code
- Usar como referência para decisões de design
- Adaptar conceitos para seu contexto específico

### Extração de Building Blocks
- Copiar classes base genéricas (Entity, ValueObject, etc)
- Reutilizar interfaces abstratas
- Adaptar value objects comuns (Email, CNPJ, URL)
- Usar helpers de infraestrutura (Metrics, Cache)

### Aceleração de Desenvolvimento
- Template inicial para novos bounded contexts
- Estrutura de pastas como referência
- Padrões de nomenclatura e organização
- Exemplos de testes unitários

---

## ❌ USO PROIBIDO

### Cópia Direta de Projetos de Origem
- **NUNCA** copie código dos projetos vms-v2, StudyFlow-IA ou Focus-AI
- **NUNCA** use lógica de negócio específica desses projetos
- **NUNCA** inclua implementações concretas sem adaptar

### Uso Como Projeto Completo
- Este **NÃO** é um projeto executável
- Este **NÃO** é um framework com CLI
- Este **NÃO** substitui arquitetura do seu projeto

### Violação de Propriedade Intelectual
- Não copie código proprietário
- Não exponha segredos ou credenciais
- Não compartilhe lógica de negócio específica

---

## 📋 Checklist de Uso Correto

Antes de usar qualquer módulo:

- [ ] Entendi o padrão implementado?
- [ ] Preciso adaptar para meu contexto?
- [ ] Estou copiando apenas building blocks genéricos?
- [ ] Removi qualquer lógica de negócio específica?
- [ ] Ajustei imports e namespaces?
- [ ] Adicionei testes para meu caso de uso?

---

## 🔄 Fluxo de Uso Recomendado

```bash
# 1. Identificar necessidade no novo projeto
# Ex: Preciso de autenticação com RBAC

# 2. Estudar implementação no boilerplate
cd boilerplate/packages/auth/
# Ler código, entender padrões

# 3. Copiar building blocks genéricos
cp -r packages/auth/ novo-projeto/src/modules/auth/

# 4. ADAPTAR para seu contexto
# - Ajustar imports
# - Adicionar regras de negócio específicas
# - Integrar com sua infraestrutura
# - Escrever testes específicos

# 5. Evoluir independentemente
# O código agora é seu, evolua conforme necessário
```

---

## 🎓 Filosofia

> "Aprenda com os padrões, não copie as implementações."

Este boilerplate ensina **COMO** estruturar código, não **O QUE** implementar.

Cada projeto tem seu contexto único. Use este toolkit como:
- 📚 Biblioteca de referência
- 🏗️ Template arquitetural
- ⚡ Acelerador de setup inicial
- 🎯 Guia de boas práticas

**Nunca** como solução pronta.

---

## ⚖️ Responsabilidade

Ao usar este boilerplate, você assume responsabilidade por:
- Adaptar código para seu contexto
- Garantir que não viola propriedade intelectual
- Manter qualidade e testes no seu projeto
- Seguir princípios SOLID e Clean Code

---

## 📞 Dúvidas

Se não tiver certeza se pode usar algo:
1. Pergunte: "Isso é um building block genérico ou lógica específica?"
2. Se for específico, **não use**
3. Se for genérico, **adapte** para seu contexto
