# ARIA Action Registry & Verification

The named action registry rejects unknown actions, including arbitrary shell execution.

## Registered actions
- `open_application(name=...)`: launches an allowlisted app and checks whether its process appears.
- `check_application(name=...)`: checks for an allowlisted app process.

## Verification limits
- `success`: request accepted or process detected.
- `verified`: process presence detected.
- Process presence does not prove a window is visible, responsive, or ready for input.

Example:
```python
from aria.actions import execute_action
print(execute_action("open_application", name="notepad"))
print(execute_action("check_application", name="firefox"))
```
No arbitrary shell command, deletion, or unrestricted keyboard/mouse action is exposed.
