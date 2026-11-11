import pytest
from aria.skills import SkillRegistry, build_default_registry


def test_register_list_and_run_skill():
    registry = SkillRegistry()
    registry.register("echo", "Return text", lambda text: text)
    assert registry.run("ECHO", text="hello") == "hello"
    assert registry.list_skills() == [{"name": "echo", "description": "Return text"}]


def test_duplicate_and_unknown_skills_are_rejected():
    registry = SkillRegistry()
    registry.register("one", "test", lambda: 1)
    with pytest.raises(ValueError):
        registry.register("one", "duplicate", lambda: 2)
    with pytest.raises(KeyError):
        registry.run("missing")


def test_default_registry_only_exposes_safe_actions():
    registry = build_default_registry()
    assert {item["name"] for item in registry.list_skills()} == {"check_app", "open_app"}
