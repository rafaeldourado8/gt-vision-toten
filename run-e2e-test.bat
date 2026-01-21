@echo off
echo ========================================
echo GT-VISION - TESTE E2E COMPLETO
echo ========================================
echo.

echo [1/3] Gerando video de teste...
python tests\generate_test_video.py
if %errorlevel% neq 0 (
    echo ERRO: Falha ao gerar video
    exit /b 1
)
echo.

echo [2/3] Verificando servicos...
docker-compose ps
echo.

echo [3/3] Executando teste E2E...
python tests\test_e2e_system.py
if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo TESTE FALHOU!
    echo ========================================
    exit /b 1
)

echo.
echo ========================================
echo TESTE PASSOU COM SUCESSO!
echo ========================================
