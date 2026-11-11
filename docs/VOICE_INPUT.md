# ARIA Voice Input Prototype

This is a **single-utterance microphone prototype**, not always-on listening.

## Install optional dependencies
```powershell
python -m pip install sounddevice numpy faster-whisper
```
Faster-Whisper downloads the selected model on first use. A GPU is optional; CPU inference may be slower.

## Use from Python
```python
from aria.voice import listen_and_route
text, result = listen_and_route(model_size="small")
print("Heard:", text)
print("Action:", result)
```

## Notes
- Capture stops after a silence interval or a maximum duration.
- Language is auto-detected by default. Set `language="te"` for Telugu or `language="en"` for English.
- This does not implement a wake word or background microphone monitoring.
- Only the existing safe command router receives the transcription. Unknown phrases are not executed.
- First-time model download and CPU transcription can take time.
