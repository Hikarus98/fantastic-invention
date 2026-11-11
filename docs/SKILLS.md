# ARIA skills

ARIA's skill registry is an explicit extension point for modular capabilities.

## Register a skill

```python
from aria.skills import SkillRegistry

skills = SkillRegistry()
skills.register("greet", "Return a greeting", lambda name: f"Hello {name}")
print(skills.run("greet", name="Rishith"))
```

## Built-in skills

`build_default_registry()` exposes `open_app` and `check_app`, which call ARIA's
existing allowlisted action registry.

## Security model

- Skills are Python callables registered by trusted code.
- There is no directory auto-import, plugin download, or model-generated code.
- Unknown names and duplicate registrations fail closed.
- Add new skills only after reviewing their implementation and permissions.
- This is a registry foundation; no GUI skill manager or third-party plugins yet.
