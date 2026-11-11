from aria.config import Config

def test_ollama_url_has_chat_endpoint():
    assert Config().ollama_url.endswith("/api/chat")

def test_default_model_is_set():
    assert Config().ollama_model
