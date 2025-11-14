## Cursor Settings Backup

This folder holds a minimal backup of my Cursor configuration plus a helper script for restoring it on a new Windows machine.

### Contents
- `Cursor/settings.json` – Cursor user settings.
- `Cursor/keybindings.json` – Cursor keybindings.
- `install_cursor_settings.py` – copies the files into the active Cursor profile.

### Restoring Settings Guide:
1. Copy this folder onto the target machine.
2. Open a terminal in the folder and run:
   ```powershell
   py install_cursor_settings.py
   ```
   The script looks for the two files above, then copies them into `%APPDATA%\Cursor\User`. If that directory is missing, you will be asked for the Cursor installation path.

### Notes
- The script copies files and leaves your backup untouched.
- Requires Python 3.10+ (any recent Python for Windows is fine).

