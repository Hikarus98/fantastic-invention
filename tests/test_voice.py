from unittest.mock import patch
import numpy as np

from aria.voice import listen_and_route, transcribe_audio


@patch("aria.voice.transcribe_audio", return_value="open Firefox")
@patch("aria.voice.record_until_silence", return_value=np.ones(100, dtype=np.float32))
@patch("aria.voice.route_command", return_value="routed")
def test_listen_bridge(mock_route, mock_record, mock_transcribe):
    text, result = listen_and_route()
    assert text == "open Firefox"
    assert result == "routed"
    mock_route.assert_called_once_with("open Firefox")


@patch("aria.voice.record_until_silence", return_value=np.zeros(0, dtype=np.float32))
def test_empty_audio_does_not_route(mock_record):
    text, result = listen_and_route()
    assert text == ""
    assert result is None
