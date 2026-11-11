"""Faster-Whisper transcription helper."""
from pathlib import Path

class Transcriber:
    def __init__(self, model_size: str = "small", device: str = "auto", compute_type: str = "int8"):
        from faster_whisper import WhisperModel
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)

    def transcribe(self, audio_path: str | Path, language: str | None = None) -> str:
        segments, _info = self.model.transcribe(str(audio_path), language=language, vad_filter=True)
        return " ".join(segment.text.strip() for segment in segments).strip()
