# ARIA roadmap

## Foundations
- [x] Ollama HTTP chat client
- [x] Environment configuration
- [x] Faster-Whisper transcription helper
- [x] Python package / CLI
- [x] Basic config tests and CI workflow

## Next milestones
- [ ] Audio capture with device selection and push-to-talk
- [ ] Continuous listening with robust silence detection
- [ ] Explicit Telugu / English language handling and transcription tests
- [ ] Intent router with typed, allow-listed actions
- [ ] Windows app launch and keyboard/mouse actions with user-visible confirmation for risky operations
- [ ] Action result verification and recovery
- [ ] Conversation memory controls
- [ ] UI, wake word, and packaged installer

## Safety principles
- Do not execute raw model-generated shell commands.
- Use a fixed registry of supported actions and validate all arguments.
- Ask before destructive, sensitive, or irreversible operations.
- Keep secrets, recordings, and local model weights out of Git.
