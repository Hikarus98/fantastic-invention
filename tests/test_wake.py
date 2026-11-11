import numpy as np
import pytest

from aria.wake import WakeWordListener


def test_listener_validates_audio_settings():
    with pytest.raises(ValueError):
        WakeWordListener(lambda chunk: False, lambda: None, chunk_frames=0)


def test_stop_sets_event():
    listener = WakeWordListener(lambda chunk: False, lambda: None)
    listener.stop()
    assert listener._stop.is_set()


def test_detector_contract_accepts_float32_chunk():
    seen = []
    listener = WakeWordListener(
        lambda chunk: seen.append((chunk.dtype, chunk.ndim)) or False,
        lambda: None,
    )
    assert listener.detector(np.zeros(16, dtype=np.float32)) is False
    assert seen == [(np.dtype("float32"), 1)]
