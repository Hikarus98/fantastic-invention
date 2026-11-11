# ARIA Computer Control (prototype)

## Current scope
The first command router supports a tiny allowlist: Firefox, Chrome, Notepad,
Calculator, and Explorer. It recognizes commands such as `open Firefox` and
`launch Notepad`, plus `help`.

## Safety
- No arbitrary PowerShell, CMD, shell, or Python commands are accepted.
- Unknown commands are returned without execution.
- App names must match the allowlist.
- Launching an app is not proof that its window is ready; the current result
  confirms only that Windows accepted a launch request.

## Use
From the repository root, install the project in editable mode and run:

```powershell
python -m pip install -e .
python -c "from aria.router import route_command; print(route_command('open Notepad'))"
```

## Next steps
Add verified process/window detection, conversational multi-step state, voice input,
user approval for higher-impact actions, and integration tests on Windows.
