@echo off
setlocal enabledelayedexpansion
title Campus LMS Launcher
cd /d "%~dp0"

echo ============================================
echo   Campus LMS - Starting up...
echo ============================================
echo.

REM ---- Check Python is installed --------------------------------------
where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python was not found on this computer.
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    echo During install, make sure to check "Add python.exe to PATH".
    echo.
    pause
    exit /b 1
)

REM ---- Create a virtual environment on first run -----------------------
if not exist "venv\Scripts\activate.bat" (
    echo Setting up the app for the first time, please wait...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Could not create the virtual environment.
        pause
        exit /b 1
    )
)

call venv\Scripts\activate.bat

REM ---- Install/upgrade dependencies (fast no-op if already installed) --
echo Checking required packages...
python -m pip install --quiet --disable-pip-version-check -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install required packages. Check your internet connection.
    pause
    exit /b 1
)

REM ---- Launch the Flask server in its own window ------------------------
echo.
echo Starting the server in a new window...
echo (A "Campus LMS Server" window will open - keep it running while you use the app. Closing it stops the server.)
echo.

start "Campus LMS Server" cmd /k "call venv\Scripts\activate.bat && python app.py"

echo Waiting for the server to start...
timeout /t 4 /nobreak >nul

start "" http://localhost:5000

echo.
echo Done! Your browser should now be open to the Campus LMS.
echo You can close this window - just keep the "Campus LMS Server" window open.
echo.
pause
