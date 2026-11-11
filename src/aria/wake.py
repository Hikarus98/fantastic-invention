"""Opt-in wake-word listening loop with an injectable detector.

The detector receives mono float32 audio chunks and returns True when its wake
word is detected. This keeps model choice/licensing separate from ARIA core.
"""
from __future__ import annotations

import threading
from collections.abc import Callable

import numpy as np

Detector = Callable[[np.ndarray], bool]
WakeCallback = Callable[[], None]


class WakeWordListener:
    """Read microphone chunks until stopped; trigger callback on wake detection."""

    def __init__(
        self,
        detector: Detector,
        on_wake: WakeCallback,
        *,
        sample_rate: int = 16000,
        chunk_frames: int = 1024,
        cooldown_seconds: float = 2.0,
    ) -> None:
        if sample_rate <= 0 or chunk_frames <= 0:
            raise ValueError("sample_rate and chunk_frames must be positive")
        self.detector = detector
        self.on_wake = on_wake
        self.sample_rate = sample_rate
        self.chunk_frames = chunk_frames
        self.cooldown_seconds = max(0.0, cooldown_seconds)
        self._stop = threading.Event()

    def stop(self) -> None:
        """Request a clean stop; safe to call from another thread."""
        self._stop.set()

    def run(self) -> None:
        """Blocking microphone loop. Requires sounddevice and a configured detector."""
        try:
            import sounddevice as sd
        except ImportError as exc:
            raise RuntimeError("Wake listening needs: pip install sounddevice") from exc

        self._stop.clear()
        last_trigger = 0.0
        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype="float32",
            blocksize=self.chunk_frames,
        ) as stream:
            while not self._stop.is_set():
                audio, overflowed = stream.read(self.chunk_frames)
                if overflowed:
                    # A dropped chunk is not fatal; continue with the next one.
                    continue
                chunk = np.asarray(audio, dtype=np.float32).reshape(-1)
                if self.detector(chunk):
                    now = threading time.monotonic()
                    if now - last_trigger >= self.cooldown_seconds:
                        last_trigger = now
                        stream.stop()
                        try:
                            self.on_wake()
                        finally:
                            if not self._stop.is_set():
                                stream.start()
