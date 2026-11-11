# ARIA personality and settings

Settings are stored in `data/aria_settings.json`. The file is created when you
save preferences; defaults are used if it is absent or invalid.

Example:

```json
{
  "name": "ARIA",
  "personality": "friendly, capable, calm, and proactive",
  "response_style": "clear and concise",
  "language": "match the user's language; support English and Telugu",
  "system_prompt": ""
}
```

Python API:

```python
from aria.settings import SettingsStore
store = SettingsStore()
settings = store.load()
settings.personality = "professional and warm"
settings.response_style = "short answers with practical steps"
store.save(settings)
```

The saved prompt shapes Ollama chat only; it does not change deterministic
computer-control routing or grant new permissions.
