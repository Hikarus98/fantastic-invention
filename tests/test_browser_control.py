from unittest.mock import patch
from aria.browser_control import normalize_url, open_url, search_web

def test_url_normalization():
    assert normalize_url("example.com")=="https://example.com"
    assert normalize_url("https://example.com")== "https://example.com"
    assert normalize_url("not a url") is None

@patch("aria.browser_control.webbrowser.open",return_value=True)
def test_open_url_calls_browser(mock_open):
    assert open_url("https://example.com")
    mock_open.assert_called_once_with("https://example.com",new=2)

@patch("aria.browser_control.webbrowser.open",return_value=True)
def test_search_uses_encoded_query(mock_open):
    assert search_web("AI news today")
    assert "AI+news+today" in mock_open.call_args.args[0]
