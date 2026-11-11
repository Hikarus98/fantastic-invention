from aria.memory import MemoryStore


def test_messages_are_saved_and_returned_chronologically(tmp_path):
    memory = MemoryStore(tmp_path / "memory.sqlite3")
    memory.add_message("user", "Hi")
    memory.add_message("assistant", "Hello")
    assert [m["content"] for m in memory.recent_messages()] == ["Hi", "Hello"]


def test_fact_upsert_and_recall(tmp_path):
    memory = MemoryStore(tmp_path / "memory.sqlite3")
    memory.remember("assistant_name", "ARIA")
    memory.remember("assistant_name", "ARIA v2")
    assert memory.recall("assistant_name") == "ARIA v2"
    assert memory.all_facts() == {"assistant_name": "ARIA v2"}


def test_clear_removes_messages_and_facts(tmp_path):
    memory = MemoryStore(tmp_path / "memory.sqlite3")
    memory.add_message("user", "secret")
    memory.remember("x", "y")
    memory.clear()
    assert memory.recent_messages() == []
    assert memory.all_facts() == {}
