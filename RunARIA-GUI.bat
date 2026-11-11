@echo off
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" (
  ".venv\Scripts\python.exe" -m aria.gui
) else (
  python -m aria.gui
)
pause
