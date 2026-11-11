import json
from aria.settings import AssistantSettings, SettingsStore


def test_defaults_and_prompt():
    settings = AssistantSettings()
    assert settings.name == "ARIA"
    assert "ARIA" in settings.prompt()
    assert "concise" in settings.prompt()


def test_save_load_roundtrip(tmp_path):
    store = SettingsStore(tmp_path / "settings.json")
    custom = AssistantSettings(name="ARIA", personality="witty but respectful",
                               response_style="brief", language="English")
    store.save(custom)
    assert store.load() == custom


def test_invalid_file_falls_back_to_defaults(tmp_path):
    path = tmp_path / "settings.json"
    path.write_text("{bad", encoding="utf-8")
    assert SettingsStore(path).load() == AssistantSettings()
