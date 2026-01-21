# 📋 Contexto do Projeto

> **INSTRUÇÕES**: Atualize este arquivo com informações específicas do seu projeto.
> AI Assistants devem ler este arquivo para entender o contexto.

## 🎯 Visão Geral

**Nome do Projeto**: Boilerplate Toolkit

**Descrição**: 
Toolkit pessoal de módulos reutilizáveis seguindo DDD, SOLID e Clean Code.
Não é um framework, mas uma coleção de padrões extraídos de projetos reais.

**Stack Tecnológico**:
- **Linguagem**: Python
- **Padrões**: DDD, SOLID, Clean Code
- **Uso**: Biblioteca de módulos para copiar/adaptar em novos projetos

---

## ⚠️ REGRA CRÍTICA: USO DOS MÓDULOS

**NUNCA copie código diretamente dos projetos de origem (vms-v2, StudyFlow-IA, Focus-AI).**

✅ **PERMITIDO**:
- Inspiração em padrões e arquitetura
- Adaptação de conceitos para o boilerplate
- Extração de building blocks genéricos
- Simplificação e generalização

❌ **PROIBIDO**:
- Copiar código específico de negócio
- Usar como projeto completo
- Incluir lógica de domínio específica
- Copiar implementações concretas sem adaptar

**Objetivo**: Acelerar novos projetos com padrões testados, não substituir desenvolvimento.

---

## 📦 Packages Disponíveis

### 1. core/
- **Descrição**: Building blocks DDD
- **Componentes**: Entity, AggregateRoot, ValueObject, DomainEvent, UseCase, EventBus
- **Localização**: `packages/core/`

### 2. auth/
- **Descrição**: Sistema de autenticação com RBAC
- **Componentes**: User, Role, Permission, Email, Password
- **Localização**: `packages/auth/`

### 3. utils/
- **Descrição**: Value Objects reutilizáveis
- **Componentes**: CNPJ, URL, Status
- **Localização**: `packages/utils/`

### 4. observability/
- **Descrição**: Métricas e monitoramento
- **Componentes**: Metrics, prometheus_middleware
- **Localização**: `packages/observability/`

### 5. llm/
- **Descrição**: Serviços para LLMs
- **Componentes**: BaseLLMService, ModelRouter, CacheService, PromptBuilder
- **Localização**: `packages/llm/`

---

## 🚀 Como Usar

### Em Novo Projeto
```bash
# Copiar package desejado
cp -r boilerplate/packages/core novo-projeto/src/shared/

# Adaptar imports e namespaces
# Ajustar para necessidades específicas
```

### Desenvolvimento
```bash
# Este é um toolkit, não um projeto executável
# Use os módulos como referência/template
```

---

## 📝 Notas Importantes

- Este toolkit é para **inspiração e aceleração**, não uso direto
- Sempre adapte o código para o contexto do seu projeto
- Mantenha os princípios SOLID e DDD ao adaptar
- Siga as regras em `.ai-rules/` ao criar novos módulos
