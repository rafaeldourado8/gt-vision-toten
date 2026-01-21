@echo off
echo Starting GT-Vision Toten Development Environment...
echo.

REM Check if .env exists
if not exist .env (
    echo Creating .env from .env.example...
    copy .env.example .env
)

REM Create data and storage directories
if not exist data mkdir data
if not exist storage mkdir storage

REM Start Docker Compose
echo Starting services...
docker-compose up -d

echo.
echo Services started!
echo.
echo API: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo MediaMTX HLS: http://localhost:8888
echo MediaMTX API: http://localhost:9997
echo.
echo To view logs: docker-compose logs -f
echo To stop: docker-compose down
