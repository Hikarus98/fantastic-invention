# ARIA — Local AI Voice Assistant

**ARIA** is a personal, local-first AI assistant being built with Python, Ollama, and Faster-Whisper. The project is actively under development; this repository contains its initial runnable foundation, not a finished voice-controlled desktop product.

## What works in this repository today

- Text chat with a locally running Ollama model
- Ollama connection check
- Faster-Whisper transcription helper for audio files
- Environment-based settings
- Python package, Windows setup/launch scripts, and basic tests

## Planned / in progress

- Telugu and English microphone interaction
- Continuous listening and silence detection
- Telugu and English microphone interaction
- Continuous listening and silence detection
- Action verification, wake word, and desktop UI

**Current limitation:** The CLI is text-based. A small, allowlisted Windows app launcher is available through slash commands; it confirms launch requests, not that a window fully opened. Speech transcription is still a helper.

## Architecture direction

```text
Microphone / typed input
        ↓
Speech-to-text (Faster-Whisper)
        ↓
Intent and command router
        ↓
Ollama local model OR approved action
        ↓
Response / action result
        ↓
Verification and feedback
```

## Stack

| Area | Technology |
|---|---|
| Language | Python 3.11+ |
| Local inference | Ollama |
| Development model | `llama3.2:latest` |
| Speech recognition | Faster-Whisper |
| Development OS | Windows |

## Quick start (Windows)

1. Install Python 3.11+ and [Ollama](https://ollama.com/).
2. Pull the model: `ollama pull llama3.2`
3. Clone this repository and run `Setup-ARIA.bat`.
4. Start Ollama, then run `RunARIA.bat --check`.
5. Launch `RunARIA.bat` for text chat.

Manual setup and troubleshooting: [Development guide](docs/DEVELOPMENT.md).

## CLI

```powershell
aria --check
aria
pytest
```

Use slash commands for the safe app launcher, for example `/open Firefox`, `/open Notepad`, `/open Calculator`, or `/open Explorer`. Type `help` after the slash to list supported commands. Type `exit` to close the chat.

## Project documents

- [Roadmap](docs/ROADMAP.md)
- [Computer control prototype](docs/COMPUTER_CONTROL.md)
- [Development guide](docs/DEVELOPMENT.md)
- [Contributing](CONTRIBUTING.md)

## Safety

ARIA will use a controlled action registry rather than executing arbitrary model-generated shell commands. Destructive or sensitive actions should require confirmation. Do not commit secrets, private audio, or model weights.

## Status

Personal project / learning build — **in development**, not production-ready.

## Author

**M Sai Rishith** · [@Hikarus98](https://github.com/Hikarus98)

Licensed under the [MIT License](LICENSE).
