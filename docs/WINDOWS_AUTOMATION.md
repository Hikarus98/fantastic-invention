# Windows automation primitives

`aria.windows_automation` adds narrow Windows-only helpers:

- `download_file(url, destination)`: HTTP(S) download to an explicit destination; checks nonempty output and removes partial files after errors.
- `launch_program(executable, args)`: launches a known executable path without a shell and checks whether it exits immediately.
- `process_running(image_name)`: checks the Windows task list by image basename.
- `installed_executable(paths)`: checks only explicit candidate paths.
- `run_installer(installer, approved=True)`: starts a known installer only after explicit approval. It does not silently elevate, click installer dialogs, or assert installation success.

All helpers return structured `AutomationResult` outcomes. They are Windows-only and cannot be verified in GitHub's Linux environment. The current CLI has not yet wired arbitrary natural-language plans into these functions. A safe product workflow must identify an official URL, show the destination and installer to the user, request approval, then verify the expected installation path and process separately.

## Security boundaries

No `shell=True`, no arbitrary command string execution, no silent UAC bypass, no auto-accepting license terms, and no automatic reboot. Use official vendor URLs and user-confirmed installer prompts.

## CLI commands

These explicit commands are wired into ARIA's slash-command handler:

- `/download https://vendor.example/installer.exe C:\\Users\\You\\Downloads\\installer.exe`
- `/install C:\\Users\\You\\Downloads\\installer.exe` (requires typing `YES` at the prompt)
- `/launch C:\\Program Files\\Vendor\\App.exe`
- `/check-process App.exe`

Paths containing spaces should be quoted, for example `/launch "C:\\Program Files\\Vendor\\App.exe"`. They are explicit path-based commands; natural-language planning and official URL discovery are not yet wired into the CLI.
