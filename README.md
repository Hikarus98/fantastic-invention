# ARIA — Local AI Voice Assistant

> A personal, local-first AI voice assistant project built with Python, Ollama, and Faster-Whisper.

**Status: In development** — ARIA is an ongoing personal project. Features and reliability are actively being improved.

## Overview

ARIA is being developed to understand spoken commands and assist with everyday desktop workflows while keeping its language-model inference local. The project combines speech recognition, a local LLM, intent handling, and computer automation.

## Planned / In-progress capabilities

- 🎙️ Speech input using Faster-Whisper
- 🌐 Telugu and English speech support
- 🧠 Local language-model responses through Ollama
- 🖥️ Desktop and application automation (in progress)
- 🔀 Voice → transcription → intent → action → verification workflow (planned)
- 🧩 Modular architecture for adding tools and capabilities

> This list describes the project's current direction; it does not imply every feature is complete or reliable yet.

## Architecture

```text
Microphone
   ↓
Speech recognition (Faster-Whisper)
   ↓
Transcription
   ↓
Intent / command handling
   ↓
Local LLM (Ollama) or action router
   ↓
Response / desktop action
   ↓
Verification and feedback
```

## Technology stack

| Component | Technology |
|---|---|
| Language | Python |
| Local LLM runtime | Ollama |
| Model used during development | `llama3.2:latest` |
| Speech recognition | Faster-Whisper |
| Operating system | Windows (development) |

## Getting started

ARIA is still under active development, and setup instructions may change as the codebase is organized.

1. Install Python.
2. Install [Ollama](https://ollama.com/) and pull the development model:
   ```powershell
   ollama pull llama3.2
   ```
3. Install Faster-Whisper in your Python environment:
   ```powershell
   pip install faster-whisper
   ```
4. Configure and run the project using the entry point and instructions in the source code.

**Note:** A complete, tested one-command installation is not available yet.

## Roadmap

- [ ] Stabilize continuous listening and Telugu/English transcription
- [ ] Improve intent detection and command routing
- [ ] Add safer, more reliable desktop action execution
- [ ] Verify actions and report failures clearly
- [ ] Add configuration and setup documentation
- [ ] Publish a demonstration

## Project status

ARIA is a personal learning and development project. It is not yet a finished product or a production-ready assistant.

## Author

**M Sai Rishith** — [GitHub: Hikarus98](https://github.com/Hikarus98)

---

*Built as an ongoing exploration of local AI, speech interfaces, and desktop automation.*
