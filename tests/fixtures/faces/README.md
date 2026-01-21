# 📸 Fotos de Teste - Alunos

Este diretório contém fotos dos alunos para testes do sistema.

## 📋 Como Usar

### Opção 1: Fotos Reais (Recomendado)

Adicione fotos reais de rostos neste diretório:

```
tests/fixtures/faces/
├── joao.jpg      # Foto do João Silva
├── maria.jpg     # Foto da Maria Santos
└── pedro.jpg     # Foto do Pedro Costa
```

**Requisitos das fotos:**
- Formato: JPG ou PNG
- Tamanho: Mínimo 640x480
- Rosto visível e centralizado
- Boa iluminação
- Sem óculos escuros ou máscaras

### Opção 2: Fotos Simuladas (Automático)

Se não adicionar fotos, o sistema cria automaticamente fotos simuladas para teste.

## 🎯 Alunos de Teste

O teste cadastra 3 alunos:

1. **João Silva**
   - Matrícula: 2024001
   - Turma: 3º Ano A
   - Foto: `joao.jpg`

2. **Maria Santos**
   - Matrícula: 2024002
   - Turma: 3º Ano A
   - Foto: `maria.jpg`

3. **Pedro Costa**
   - Matrícula: 2024003
   - Turma: 2º Ano B
   - Foto: `pedro.jpg`

## 📝 Dicas

- Use fotos diferentes para cada aluno
- Tire fotos em condições similares às da câmera real
- Teste com diferentes ângulos e iluminações
- Fotos de alta qualidade melhoram a detecção

## 🔒 Privacidade

⚠️ **IMPORTANTE**: Não commite fotos reais no Git!

Este diretório está no `.gitignore` para proteger a privacidade.
