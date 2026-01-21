@echo off
echo ========================================
echo GT-VISION - TESTE RAPIDO WEBCAM
echo ========================================
echo.
echo Este teste vai:
echo 1. Conectar na sua webcam
echo 2. Iniciar deteccao facial
echo 3. Mostrar resultados em tempo real
echo.
echo Pressione CTRL+C para cancelar
timeout /t 3
echo.

python tests\test_webcam_quick.py

if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo TESTE FALHOU!
    echo ========================================
    exit /b 1
)

echo.
echo ========================================
echo TESTE CONCLUIDO!
echo ========================================
