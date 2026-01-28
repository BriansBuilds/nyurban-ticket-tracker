@echo off
echo Setting up NY Urban Ticket Tracker...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://www.python.org/
    pause
    exit /b 1
)

echo Python found!
echo.

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Setup complete!
echo.
echo Testing the script...
python check_availability.py

echo.
echo If you see output above, the script is working!
echo.
echo To set up the scheduler:
echo 1. Use Task Scheduler (see README.md)
echo 2. Or run: powershell -ExecutionPolicy Bypass -File run_scheduler.ps1
echo.
pause
