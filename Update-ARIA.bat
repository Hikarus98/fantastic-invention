@echo off
setlocal
title ARIA - Update and Launch

echo ========================================
echo      ARIA (formerly AREON) UPDATE
echo ========================================
echo.
echo This updater uses the ARIA name; old AREON data is not deleted.
echo.

REM Move to the folder containing this batch file
cd /d "%~dp0"

REM Verify this is a Git checkout
if not exist ".git" (
    echo ERROR: Git repository not found in "%CD%".
    echo Clone ARIA first from:
    echo https://github.com/Hikarus98/fantastic-invention
    pause
    exit /b 1
)

REM Preserve local changes; refuse to overwrite them
git status --short
if errorlevel 1 (
    echo ERROR: Git status failed.
    pause
    exit /b 1
)
for /f "delims=" %%A in ('git status --porcelain') do (
    echo.
    echo ERROR: Local changes detected. Back them up or commit/stash them before updating.
    pause
    exit /b 1
)

echo.
echo [1/3] Pulling latest ARIA code...
git pull --ff-only origin main
if errorlevel 1 (
    echo ERROR: Git update failed. Check network, branch, or local repository state.
    pause
    exit /b 1
)

echo.
echo [2/3] Updating Python package/dependencies...
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" -m pip install --upgrade pip
    if errorlevel 1 goto :pip_error
    ".venv\Scripts\python.exe" -m pip install -e .
    if errorlevel 1 goto :pip_error
    set "ARIA_CMD=.venv\Scripts\aria.exe"
) else (
    python -m pip install --upgrade pip
    if errorlevel 1 goto :pip_error
    python -m pip install -e .
    if errorlevel 1 goto :pip_error
    set "ARIA_CMD=aria"
)

echo.
echo [3/3] Starting ARIA...
%ARIA_CMD%
if errorlevel 1 (
    echo.
    echo ARIA exited with an error. See the output above.
    pause
    exit /b 1
)
exit /b 0

:pip_error
echo ERROR: Dependency installation failed.
pause
exit /b 1
