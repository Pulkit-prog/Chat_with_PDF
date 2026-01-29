@echo off
REM Assessment Chat RAG - Windows Startup Script
REM This script validates the environment and starts the Streamlit app

echo.
echo ============================================================
echo Assessment Chat RAG - Windows Launcher
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://www.python.org/
    pause
    exit /b 1
)

REM Run the startup script
python start.py

REM If the script exits with error, pause to show the message
if errorlevel 1 (
    echo.
    echo ============================================================
    echo An error occurred. Please check the messages above.
    echo ============================================================
    pause
)
