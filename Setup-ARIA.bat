@echo off
setlocal
cd /d "%~dp0"
py -3.12 -m venv .venv
if errorlevel 1 py -3 -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -e ".[dev]"
if errorlevel 1 (
  echo Setup failed. Check Python and internet connection.
  pause
  exit /b 1
)
echo.
echo ARIA setup complete. Start Ollama, then run RunARIA.bat --check
pause
