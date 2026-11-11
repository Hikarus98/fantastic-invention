# ARIA desktop GUI

A minimal Tkinter desktop chat interface is available.

## Run on Windows

Install the project in its environment (from repository root):

```powershell
python -m pip install -e .
python -m aria.gui
```

Or double-click `RunARIA-GUI.bat` after installation.

The UI routes supported explicit commands through ARIA's safe command router and sends other text to configured Ollama. Ollama must be running for chat. This is an initial UI—not a packaged installer, always-listening microphone interface, or full desktop automation console. Tkinter is included with most standard Windows Python installations.
