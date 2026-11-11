# ARIA — Local AI Voice Assistant

**ARIA** is a personal, local-first AI assistant being built with Python, Ollama, and Faster-Whisper. The project is actively under development; this repository contains its initial runnable foundation, not a finished voice-controlled desktop product.

## What works in this repository today

- Text chat with a locally running Ollama model
- Ollama connection check
- Faster-Whisper transcription helper for audio files
- Single-utterance microphone capture with silence timeout
- CLI voice modes (`/voice`, `/voice-te`, `/voice-en`) feeding the safe command router
- Plain typed commands are routed automatically before chat (no `/` prefix needed for recognized commands)
- Safe named action registry and basic process-presence verification
- Conversational browser phrases (`find`, `look up`, `search`, `visit`, `open a new tab`) routed to explicit safe helpers
- Explicit browser search and URL opening commands
- Environment-based settings\n- JSON personality/preferences settings applied to Ollama chat\n- Explicit, safe skill registry for modular capabilities
- Sequential task runner with execution + verification gates and approval checkpoints
- Windows-only download, executable launch, installer approval, and process verification primitives
- Python package, Windows setup/launch scripts, and basic tests

## Planned / in progress

- Wake word and background always-on listening
- Window-level verification, wake word, and desktop UI
- Action verification, wake word, and desktop UI

**Current limitation:** Voice is manually triggered for one utterance; there is no wake word or background always-on listening. The app launcher confirms a launch request, not that the window fully opened.

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

Use `/voice` to record one utterance (auto language), `/voice-te` for Telugu, or `/voice-en` for English. You can say `open Firefox` or another allowlisted app. Typed commands: `/open Firefox`, `/open Notepad`, `/open Calculator`, `/open Explorer`, `/search for AI news`, `/go to example.com`. Try `find ChatGPT`, `look up AI news`, `visit example.com`, or `open a new tab`. These open a search/URL/blank tab in the default browser; they don't control an existing webpage. You can enter `open Firefox`, `find ChatGPT`, or `visit example.com` directly without `/`; recognized safe commands are handled, and other text goes to Ollama chat. Type `/help` for help. Type `exit` to close the chat.

## Project documents

- [Roadmap](docs/ROADMAP.md)\n- [Personality and settings](docs/SETTINGS.md)\n- [Skills registry](docs/SKILLS.md)
- [Task execution and verification](docs/TASK_EXECUTION.md)
- [Windows automation](docs/WINDOWS_AUTOMATION.md)
- [Computer control prototype](docs/COMPUTER_CONTROL.md)
- [Voice input prototype](docs/VOICE_INPUT.md)
- [Action verification](docs/ACTION_VERIFICATION.md)
- [Browser actions](docs/BROWSER_ACTIONS.md)
- [Development guide](docs/DEVELOPMENT.md)
- [Contributing](CONTRIBUTING.md)

## Safety

ARIA will use a controlled action registry rather than executing arbitrary model-generated shell commands. Destructive or sensitive actions should require confirmation. Do not commit secrets, private audio, or model weights.

## Status

Personal project / learning build — **in development**, not production-ready.

## Author

**M Sai Rishith** · [@Hikarus98](https://github.com/Hikarus98)

Licensed under the [MIT License](LICENSE).
