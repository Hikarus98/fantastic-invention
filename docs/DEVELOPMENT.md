# Development guide

## Create an environment

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

## Run
- Text chat: `aria`
- Connection check: `aria --check`
- Tests: `pytest`

## Current limitations
- The CLI currently accepts typed text; microphone capture and wake-word listening are not wired into the entry point.
- Desktop actions are not implemented yet. Never execute arbitrary shell commands from model output.
- Telugu/English speech transcription is a helper; end-to-end audio UX remains in progress.
