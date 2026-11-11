@echo off
setlocal
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe (
  echo ARIA environment not found. Run Setup-ARIA.bat first.
  pause
  exit /b 1
)
.venv\Scripts\python.exe -m aria.main %*
