from unittest.mock import patch
from aria.router import route_command

@patch("aria.router.search_web", return_value=True)
def test_find_phrase_searches_web(mock_search):
    result=route_command("find ChatGPT")
    assert result.handled and result.success
    mock_search.assert_called_once_with("ChatGPT")

@patch("aria.router.search_web", return_value=True)
def test_look_up_phrase_searches_web(mock_search):
    route_command("look up Telugu AI jobs")
    mock_search.assert_called_once_with("Telugu AI jobs")

@patch("aria.router.open_url", return_value=True)
def test_new_tab_opens_blank_tab(mock_open):
    result=route_command("open a new tab")
    assert result.success
    mock_open.assert_called_once_with("about:blank")

def test_unknown_command_is_not_executed():
    result=route_command("delete all files")
    assert not result.handled and not result.success
