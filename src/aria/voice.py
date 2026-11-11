"""Voice bridge: microphone audio -> Faster-Whisper -> safe command router."""
from __future__ import annotations

from .audio_input import AudioConfig, record_until_silence
from .router import route_command


def transcribe_audio(audio, model_size: str = "small", language: str | None = None) -> str:
    """Transcribe a float32 waveform with Faster-Whisper."""
    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:
        raise RuntimeError("Speech support needs: pip install faster-whisper") from exc

    model = WhisperModel(model_size, device="auto", compute_type="auto")
    segments, _info = model.transcribe(audio, language=language, vad_filter=True)
    return " ".join(segment.text.strip() for segment in segments).strip()


def listen_and_route(*, model_size: str = "small", language: str | None = None,
                     audio_config: AudioConfig | None = None):
    """Capture one utterance, transcribe, then route only recognized safe commands."""
    audio = record_until_silence(audio_config)
    if audio.size == 0:
        return "", None
    text = transcribe_audio(audio, model_size=model_size, language=language)
    if not text:
        return "", None
    # Voice commands must be explicitly phrased as app-opening commands.
    return text, route_command(text)
