@echo off
echo ========================================
echo GT-VISION - TESTE REALISTA E2E
echo ========================================
echo.
echo Este teste simula o fluxo completo:
echo 1. Cadastro de 3 alunos com fotos
echo 2. Configuracao de camera
echo 3. Monitoramento em tempo real
echo 4. Deteccao facial automatica
echo 5. Registro de presenca
echo 6. Envio de notificacoes
echo.
echo ========================================
echo.

set /p USE_WEBCAM="Usar webcam? (S/N) [S]: "
if /i "%USE_WEBCAM%"=="N" (
    echo Usando video de teste...
    python tests\test_realistic_e2e.py --video --duration 30
) else (
    echo Usando webcam...
    echo.
    echo IMPORTANTE: Posicione seu rosto na frente da camera!
    echo.
    timeout /t 3
    python tests\test_realistic_e2e.py --duration 60
)

if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo TESTE FALHOU!
    echo ========================================
    pause
    exit /b 1
)

echo.
echo ========================================
echo TESTE CONCLUIDO COM SUCESSO!
echo ========================================
pause
