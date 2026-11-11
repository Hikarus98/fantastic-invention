@echo off
setlocal
title ARIA - Update, Diagnose and Launch
cd /d "%~dp0"

echo ============================================
echo       ARIA UPDATE + DIAGNOSTICS
echo ============================================
echo.

REM Bootstrap when this BAT was downloaded into Downloads/Desktop.
if not exist ".git" (
  where git >nul 2>&1
  if errorlevel 1 (
    echo ERROR: Git is not installed or not on PATH.
    echo Install Git for Windows, then run this file again.
    pause
    exit /b 1
  )
  set "ARIA_HOME=%USERPROFILE%\ARIA"
  if exist "%ARIA_HOME%\.git" (
    echo Found existing ARIA repository at "%ARIA_HOME%".
  ) else (
    if exist "%ARIA_HOME%" (
      echo ERROR: "%ARIA_HOME%" exists but is not an ARIA Git repository.
      echo Rename that folder or choose another location before continuing.
      pause
      exit /b 1
    )
    echo This BAT is outside a Git repository.
    echo Cloning ARIA into "%ARIA_HOME%"...
    git clone https://github.com/Hikarus98/fantastic-invention "%ARIA_HOME%"
    if errorlevel 1 (
      echo ERROR: Clone failed. Check internet and GitHub access.
      pause
      exit /b 1
    )
  )
  echo.
  echo Running updater from the cloned ARIA folder...
  call "%ARIA_HOME%\Update-ARIA.bat"
  exit /b %ERRORLEVEL%
)

where git >nul 2>&1
if errorlevel 1 (
  echo ERROR: Git is not installed or not on PATH.
  pause
  exit /b 1
)

echo [1/4] Checking local changes...
git status --porcelain > "%TEMP%\aria_git_status.txt"
if errorlevel 1 goto :git_error
for %%F in ("%TEMP%\aria_git_status.txt") do if %%~zF GTR 0 (
  echo ERROR: Local files have changes. Save/commit them before updating.
  type "%TEMP%\aria_git_status.txt"
  del "%TEMP%\aria_git_status.txt"
  pause
  exit /b 1
)
del "%TEMP%\aria_git_status.txt" >nul 2>&1

echo.
echo [2/4] Downloading latest ARIA code...
git pull --ff-only origin main
if errorlevel 1 goto :git_error

echo.
echo [3/4] Installing/updating ARIA...
if exist ".venv\Scripts\python.exe" (
  set "PY=.venv\Scripts\python.exe"
) else (
  set "PY=python"
)
%PY% -m pip install --upgrade pip
if errorlevel 1 goto :pip_error
%PY% -m pip install -e .
if errorlevel 1 goto :pip_error

echo.
echo [4/4] Running ARIA diagnostics...
%PY% -m aria.main --check
if errorlevel 1 (
  echo.
  echo CHECK FAILED. Review the errors above; ARIA will not be launched.
  pause
  exit /b 1
)

echo.
echo Diagnostics passed. Launching ARIA...
if exist ".venv\Scripts\aria.exe" (
  ".venv\Scripts\aria.exe"
) else (
  %PY% -m aria.main
)
set "APP_EXIT=%ERRORLEVEL%"
echo.
echo ARIA process exited with code %APP_EXIT%.
echo Existing AREON folders/data are not migrated or deleted by this script.
pause
exit /b %APP_EXIT%

:git_error
echo ERROR: Git update failed. Check internet, branch, or repository state.
pause
exit /b 1

:pip_error
echo ERROR: Python dependency installation failed.
pause
exit /b 1
