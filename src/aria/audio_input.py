"""Microphone capture helpers for ARIA (optional sounddevice dependency)."""
from __future__ import annotations

import queue
import time
from dataclasses import dataclass


@dataclass(frozen=True)
class AudioConfig:
    sample_rate: int = 16000
    channels: int = 1
    silence_seconds: float = 1.2
    max_record_seconds: float = 12.0
    threshold: float = 0.012
    block_seconds: float = 0.25


def record_until_silence(config: AudioConfig | None = None):
    """Record float32 mono audio until silence or max duration.

    Returns a NumPy array. Requires optional packages: sounddevice and numpy.
    This is intentionally push-to-start (not always listening/wake-word).
    """
    try:
        import numpy as np
        import sounddevice as sd
    except ImportError as exc:
        raise RuntimeError("Mic support needs: pip install sounddevice numpy") from exc

    cfg = config or AudioConfig()
    chunks: queue.Queue = queue.Queue()
    started = time.monotonic()
    last_voice = started
    frames_per_block = max(1, int(cfg.sample_rate * cfg.block_seconds))

    def callback(indata, frames, time_info, status):
        if status:
            # Keep capture running; callers can inspect returned audio.
            pass
        chunks.put(indata[:, 0].copy())

    print("Listening... speak now (Ctrl+C to stop)")
    with sd.InputStream(samplerate=cfg.sample_rate, channels=cfg.channels,
                       dtype="float32", blocksize=frames_per_block,
                       callback=callback):
        collected = []
        while True:
            now = time.monotonic()
            if now - started >= cfg.max_record_seconds:
                break
            try:
                chunk = chunks.get(timeout=cfg.block_seconds + 0.5)
            except queue.Empty:
                continue
            collected.append(chunk)
            rms = float(np.sqrt(np.mean(np.square(chunk)))) if chunk.size else 0.0
            if rms >= cfg.threshold:
                last_voice = time.monotonic()
            elif collected and time.monotonic() - last_voice >= cfg.silence_seconds:
                break

    if not collected:
        return np.zeros(0, dtype=np.float32)
    return np.concatenate(collected).astype(np.float32, copy=False)
