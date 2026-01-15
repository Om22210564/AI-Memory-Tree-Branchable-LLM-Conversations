@echo off
REM React Frontend Setup Script for Windows

echo.
echo ========================================
echo AI Memory Tree Chat - React Frontend Setup
echo ========================================
echo.

REM Check if Node.js is installed
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Node.js is not installed!
    echo Please download and install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

echo ✓ Node.js found: 
node --version

echo.
echo Installing npm dependencies...
echo.

cd frontend-react
npm install

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: npm install failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Make sure backend is running: python backend/main.py
echo 2. Run: npm run dev
echo 3. Open browser: http://localhost:3000
echo.
pause
