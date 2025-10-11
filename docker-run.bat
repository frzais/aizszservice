@echo off
REM Aizsz Service - Docker Run Script for Windows
REM This script helps you run the Aizsz Service container easily

setlocal enabledelayedexpansion

echo [INFO] Aizsz Service Docker Runner
echo =================================

REM Check if .env file exists
if not exist .env (
    echo [ERROR] .env file not found!
    echo [INFO] Please create .env file from .env.example template
    echo [INFO] Copy .env.example to .env and edit with your actual values
    pause
    exit /b 1
)

REM Check if Docker is running
docker version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not running or not installed!
    echo [INFO] Please start Docker Desktop and try again
    pause
    exit /b 1
)

REM Create necessary directories
echo [INFO] Creating necessary directories...
if not exist logs mkdir logs
if not exist plugins_cache mkdir plugins_cache

REM Build the Docker image
echo [INFO] Building Docker image...
docker build -t aizsz-service .
if errorlevel 1 (
    echo [ERROR] Failed to build Docker image!
    pause
    exit /b 1
)
echo [SUCCESS] Docker image built successfully!

REM Stop existing container if running
docker ps -q -f name=aizsz-service >nul 2>&1
if not errorlevel 1 (
    echo [WARNING] Stopping existing container...
    docker stop aizsz-service
)

REM Remove existing container if exists
docker ps -aq -f name=aizsz-service >nul 2>&1
if not errorlevel 1 (
    echo [WARNING] Removing existing container...
    docker rm aizsz-service
)

REM Run the container
echo [INFO] Starting Aizsz Service container...
docker run -d ^
    --name aizsz-service ^
    --restart unless-stopped ^
    --env-file .env ^
    -v "%cd%\logs:/app/logs" ^
    -v "%cd%\plugins_cache:/app/plugins_cache" ^
    -v "%cd%\asst.session:/app/asst.session:ro" ^
    aizsz-service

if errorlevel 1 (
    echo [ERROR] Failed to start container!
    pause
    exit /b 1
)

echo [SUCCESS] Aizsz Service started successfully!
echo [INFO] Container name: aizsz-service
echo [INFO] To view logs: docker logs -f aizsz-service
echo [INFO] To stop: docker stop aizsz-service
echo [INFO] To restart: docker restart aizsz-service

REM Show container status
echo [INFO] Container status:
docker ps -f name=aizsz-service

pause
