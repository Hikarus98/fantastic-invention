# ARIA Wake-word listening (experimental)

Wake listening is **not enabled on startup**. It must be explicitly launched and
stopped by the user. The core provides a microphone loop, cooldown, stop event,
and detector callback; it intentionally does not bundle a wake-word model or
assume a vendor/license.

## Detector adapter

Pass a callable detector to `WakeWordListener`. It receives a mono float32 chunk
(at 16 kHz by default) and returns `True` when the configured wake phrase is
detected. Integrate an approved local detector/model in your own adapter.

Example shape:

```python
from aria.wake import WakeWordListener
from aria.voice import listen_and_route

def detector(audio_chunk):
    # Feed chunk to your local wake-word model and return its detection result.
    return False

def on_wake():
    heard, result = listen_and_route(language=None)
    print("Heard:", heard)
    if result:
        print("ARIA:", result.message)

listener = WakeWordListener(detector, on_wake)
try:
    listener.run()  # blocking; Ctrl+C stops it
except KeyboardInterrupt:
    listener.stop()
```

The stream is paused while `on_wake` runs so the command microphone capture
does not compete with the wake stream. A cooldown avoids immediate retriggers.
Use headphones or test carefully to prevent speaker feedback.

## Safety and limitations

- No always-listening behavior unless a user explicitly starts this loop.
- No bundled wake model, wake phrase, or background service yet.
- The callback currently uses the existing one-utterance voice flow.
- This is an experimental architecture; verify microphone behavior on Windows.
