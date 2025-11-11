@echo off
setlocal enabledelayedexpansion

echo [%date% %time%] Starting Life-Book bot...

:: Check if Python is installed
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

:: Activate virtual environment
if exist "venv\Scripts\activate" (
    call venv\Scripts\activate
) else (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate
    
    echo Installing requirements...
    pip install --upgrade pip
    if exist requirements.txt (
        pip install -r requirements.txt
    )
)

:: Set environment variables
set PYTHONUNBUFFERED=1
set PYTHONPATH=%~dp0

:: Run the bot with error handling
echo [%date% %time%] Starting bot...
python lifebook.py

if %ERRORLEVEL% neq 0 (
    echo [%date% %time%] Error: Bot crashed with code !ERRORLEVEL!
    pause
    exit /b !ERRORLEVEL!
) else (
    echo [%date% %time%] Bot stopped successfully
)
