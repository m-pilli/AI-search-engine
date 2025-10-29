@echo off
echo ========================================
echo AI Search Engine - Windows Setup
echo ========================================
echo.

:: Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not installed!
    echo.
    echo Please install Docker Desktop:
    echo 1. Go to: https://www.docker.com/products/docker-desktop/
    echo 2. Download and install Docker Desktop
    echo 3. Restart your computer
    echo 4. Run this script again
    echo.
    pause
    exit /b 1
)

echo [OK] Docker is installed
echo.

:: Check if Docker is running
docker ps >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not running!
    echo.
    echo Please start Docker Desktop:
    echo 1. Open Docker Desktop from Start Menu
    echo 2. Wait for Docker to start
    echo 3. Run this script again
    echo.
    pause
    exit /b 1
)

echo [OK] Docker is running
echo.

:: Navigate to project directory
cd /d "%~dp0"

echo Starting AI Search Engine...
echo This will take 2-3 minutes on first run.
echo.

:: Start Docker Compose
docker-compose up --build -d

echo.
echo ========================================
echo Services are starting...
echo ========================================
echo.
echo Waiting for services to be ready...
timeout /t 30 /nobreak >nul

:: Check if services are running
docker-compose ps

echo.
echo ========================================
echo AI Search Engine is Ready!
echo ========================================
echo.
echo Access the application:
echo   Frontend: http://localhost:3000
echo   Backend:  http://localhost:5000/api/health
echo.
echo To load sample data, run:
echo   load-sample-data.bat
echo.
echo To stop the application:
echo   stop.bat
echo.
echo To view logs:
echo   docker-compose logs -f
echo.
pause

