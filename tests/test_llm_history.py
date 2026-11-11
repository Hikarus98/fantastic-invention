from aria.llm import OllamaClient


class FakeResponse:
    def raise_for_status(self):
        pass

    def json(self):
        return {"message": {"content": "reply"}}


def test_chat_includes_valid_history(monkeypatch):
    captured = {}

    def fake_post(url, json, timeout):
        captured.update(json)
        return FakeResponse()

    monkeypatch.setattr("aria.llm.requests.post", fake_post)
    client = OllamaClient()
    result = client.chat("new question", history=[
        {"role": "user", "content": "previous"},
        {"role": "assistant", "content": "answer"},
        {"role": "system", "content": "ignored"},
    ])
    assert result == "reply"
    assert [m["role"] for m in captured["messages"]] == [
        "system", "user", "assistant", "user"
    ]
    assert captured["messages"][-1]["content"] == "new question"
