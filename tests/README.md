# 🧪 Testes E2E - GT-Vision

## 📋 Sobre

Testes end-to-end completos que validam todo o fluxo do sistema:

1. ✅ Login no sistema
2. ✅ Cadastro de aluno
3. ✅ Upload de foto do aluno
4. ✅ Cadastro de câmera
5. ✅ Início de streaming
6. ✅ Detecção facial
7. ✅ Registro de presença
8. ✅ Envio de notificação

---

## 🎯 Tipos de Teste

### 1. Teste Realista (RECOMENDADO)

Simula o fluxo real com cadastro de múltiplos alunos:
- Cadastra 3 alunos com fotos
- Usa webcam ou vídeo
- Monitora detecções em tempo real
- Valida presença e notificações

```bash
.\run-realistic-test.bat
```

### 2. Teste Rápido (Webcam)

Teste rápido de 30s com webcam:
```bash
.\run-webcam-test.bat
```

### 3. Teste Completo (Vídeo Simulado)

Teste automatizado com vídeo gerado:
```bash
.\run-e2e-test.bat
```

---

## 🚀 Como Executar

### Pré-requisitos

1. Sistema rodando:
```bash
docker-compose up -d
```

2. Dependências instaladas:
```bash
pip install -r requirements.txt
```

3. **(Opcional)** Adicione fotos reais em `tests/fixtures/faces/`:
   - `joao.jpg` - Foto do João Silva
   - `maria.jpg` - Foto da Maria Santos
   - `pedro.jpg` - Foto do Pedro Costa

   Se não adicionar, o sistema cria fotos simuladas automaticamente.

### Executar Teste Realista (Recomendado)

```bash
# Windows
.\run-realistic-test.bat

# Escolha:
# - Webcam: Usa sua câmera (60s de monitoramento)
# - Vídeo: Usa vídeo de teste (30s de monitoramento)
```

### Executar Outros Testes

```bash
# Windows
.\run-e2e-test.bat

# Linux/Mac
chmod +x run-e2e-test.sh
./run-e2e-test.sh
```

### Executar Manualmente

```bash
# 1. Gerar vídeo de teste
python tests/generate_test_video.py

# 2. Executar teste E2E
python tests/test_e2e_system.py
```

---

## 📹 Vídeo de Teste

O script `generate_test_video.py` cria um vídeo MP4 com:
- Duração: 30 segundos
- FPS: 30
- Resolução: 640x480
- Conteúdo: Pessoa simulada se movendo

O vídeo é salvo em: `tests/videos/test_video.mp4`

---

## 🔍 O Que é Testado

### 1. Streaming Context
- Cadastro de câmera
- Início/parada de streaming
- Integração com MediaMTX

### 2. Detection Context
- Detecção de faces no vídeo
- Reconhecimento facial
- Matching com alunos cadastrados

### 3. Student Context
- Cadastro de aluno
- Upload de fotos
- Armazenamento de embeddings

### 4. Attendance Context
- Registro automático de presença
- Validação de horários
- Prevenção de duplicatas

### 5. Notification Context
- Envio de notificações
- Integração com canais (SMS/Email/Push)

---

## 📊 Saída Esperada

```
========================================
🚀 TESTE E2E - GT-VISION SYSTEM
========================================

============================================================
🔹 STEP 1: Login
============================================================
✓ Login realizado com sucesso

============================================================
🔹 STEP 2: Cadastrar Aluno
============================================================
✓ Aluno criado: ID 1

============================================================
🔹 STEP 3: Upload Foto do Aluno
============================================================
✓ Foto do aluno enviada

============================================================
🔹 STEP 4: Cadastrar Câmera
============================================================
✓ Câmera criada: ID 1

============================================================
🔹 STEP 5: Iniciar Streaming
============================================================
✓ Streaming iniciado

============================================================
🔹 STEP 6: Aguardar Detecção
============================================================
Aguardando detecção (timeout: 60s)...
✓ Detecção encontrada

============================================================
🔹 STEP 7: Verificar Presença
============================================================
✓ Presença registrada

============================================================
🔹 STEP 8: Verificar Notificação
============================================================
✓ Notificação enviada

============================================================
🔹 RELATÓRIO FINAL
============================================================
✓ Login
✓ Cadastrar Aluno
✓ Upload Foto
✓ Cadastrar Câmera
✓ Iniciar Streaming
✓ Aguardar Detecção
✓ Verificar Presença
✓ Verificar Notificação

============================================================
Resultado: 8/8 testes passaram
============================================================
```

---

## 🐛 Troubleshooting

### Erro: "Connection refused"
- Verifique se os serviços estão rodando: `docker-compose ps`
- Inicie os serviços: `docker-compose up -d`

### Erro: "Timeout: Nenhuma detecção encontrada"
- Verifique logs do worker: `docker-compose logs worker`
- Verifique se o modelo de detecção está carregado
- Aumente o timeout no teste

### Erro: "Foto de teste não encontrada"
- O script cria automaticamente uma foto simulada
- Ou adicione uma foto real em: `tests/fixtures/test_face.jpg`

---

## 📝 Notas

- O teste usa vídeo simulado, não câmera real
- Dados de teste são criados e podem ser limpos após
- Timeout padrão de detecção: 60 segundos
- O teste valida todo o pipeline do sistema

---

## 🔄 Integração Contínua

Para CI/CD, adicione ao pipeline:

```yaml
- name: Run E2E Tests
  run: |
    docker-compose up -d
    sleep 10
    python tests/generate_test_video.py
    python tests/test_e2e_system.py
```
