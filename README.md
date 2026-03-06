# Wizard Key

A Windows NLP automation tool that converts natural-language voice/text commands into system actions using semantic similarity. Integrates with AutoHotkey v2 for global hotkey support.

## What It Does

Wizard Key listens for user input (via AutoHotkey hotkey or command line) and routes commands to actions:

- **Open applications** (Zoom, Teams, Outlook, Notepad, etc.)
- **Transform text** (UPPERCASE, lowercase, Title Case)
- **Open URLs** (Gmail, YouTube, GitHub, arbitrary domains)
- **Control windows** (Switch window, Alt+Tab)
- **System control** (Mute, volume up/down, lock computer, screenshot)

Uses sentence-transformers for semantic matching, so commands like "open zoom", "launch zoom", "start zoom" all work.

## Architecture Overview

```
Router (semantic NLP)
  ↓
Memory (alias lookup)
  ↓
Command extraction (per-command logic)
  ↓
Executor (system action)
  ↓
Memory (remember alias for next time)
```

**Key components:**

- **Router**: Uses all-MiniLM-L6-v2 embeddings + cosine similarity to match user input to commands
- **Memory**: JSON-backed alias store (e.g., "open my email" → "open_url gmail")
- **Command modules**: Extract domain-specific parameters (app name, URL, text mode, etc.)
- **Executors**: Perform actual system actions (open apps, transform text, etc.)

## Folder Structure

```
wizard-key/
├── wizard/
│   ├── __init__.py
│   ├── main.py                    # Entry point
│   ├── config.py                  # Paths, constants
│   ├── schema.py                  # CommandMatch, ExecutionResult dataclasses
│   ├── router.py                  # Semantic routing
│   ├── memory.py                  # Alias persistence
│   ├── commands/
│   │   ├── open_app.py            # Open applications
│   │   ├── open_url.py            # Open URLs
│   │   ├── switch_window.py       # Window switching
│   │   ├── system_control.py      # Mute, volume, lock, screenshot
│   │   └── transform_text.py      # Text case transformation
│   ├── executors/
│   │   ├── apps.py                # App launching
│   │   ├── browser.py             # URL opening
│   │   ├── windows.py             # Window operations
│   │   ├── system.py              # Volume, lock, etc.
│   │   └── text_ops.py            # Clipboard text transform
│   └── data/
│       ├── apps.json              # App registry
│       └── memory.json            # Learned aliases
├── wizard_key.ahk                 # AutoHotkey v2 global hotkey
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## Installation

### Prerequisites

- **Python 3.9+** installed and in PATH (as `python` or `py`)
- **AutoHotkey v2** installed (for global hotkey support)

### Step 1: Clone and Install Dependencies

```powershell
cd wizard-key
pip install -r requirements.txt
```

Required packages:
- `sentence-transformers` — NLP semantic matching
- `pyautogui` — Keyboard/mouse control
- `pyperclip` — Clipboard access
- `numpy` — Numerical operations

### Step 2: Run AutoHotkey Script

```powershell
# In PowerShell or Windows Run (Win+R):
Start-Process "wizard_key.ahk"

# Or directly:
AutoHotkey.exe wizard_key.ahk
```

The v2 script will minimize to tray and wait for F13 press.

## Usage

### From Command Line

```powershell
py wizard/main.py "open zoom"
py wizard/main.py "make text uppercase"
py wizard/main.py "go to github"
py wizard/main.py "switch window"
py wizard/main.py "take a screenshot"
```

**Output** (JSON):
```json
{"ok": true, "message": "Launched zoom"}
{"ok": false, "message": "Could not understand command", "match_score": 0.35, "best_guess": "open zoom"}
```

### From AutoHotkey

1. **Press F13** (or modify hotkey in `wizard_key.ahk`)
2. **Type command** in InputBox (e.g., "open outlook")
3. **See result** in MsgBox (success ✓ or failure ✗)

## Supported Commands

### Open App

- "open zoom", "launch teams", "start outlook", "open notepad"
- More apps in `wizard/data/apps.json`

### Transform Text

- "make uppercase" — SELECTED TEXT
- "make lowercase" — selected text
- "title case" — Selected Text

**Note**: Requires text selected in active window (uses Ctrl+C, Ctrl+V)

### Open URL

- "open gmail", "go to youtube", "open reddit"
- "open example.com" (raw domains)
- "search google" → www.google.com

### Switch Window

- "switch window", "next app", "alt tab"

### System Control

- "mute" / "volume up" / "volume down" — Media keys
- "lock computer" — Windows lock screen
- "take a screenshot" — Saved to Pictures with timestamp

## Memory & Aliases

Wizard Key learns aliases to speed up future commands.

**First run:**
```
User: "open my zoom"
→ Fuzzy match to "open zoom" (app=zoom)
→ Execute
→ Save alias: "open my zoom" → open_app + {app: zoom}
```

**Next run:**
```
User: "open my zoom"
→ Exact match in memory
→ Execute instantly (score 1.0, no ML needed)
```

Aliases stored in `wizard/data/memory.json`:
```json
{
  "aliases": {
    "open my email": ["open_url", {"url": "https://mail.google.com"}]
  }
}
```

**Clear memory** (reset aliases):
```powershell
$null | Set-Content wizard/data/memory.json
```

## Configuring Apps

Edit `wizard/data/apps.json` to add or update applications:

```json
{
  "zoom": {
    "path": "C:\\Program Files\\Zoom\\bin\\Zoom.exe",
    "aliases": ["zoom app", "video call"]
  },
  "notion": {
    "path": "notion.exe",
    "aliases": ["my notes", "wiki"]
  },
  "custom_script": {
    "path": "C:\\Scripts\\myscript.bat"
  }
}
```

Fields:
- `path` or `executable` — Full path or command (default falls back to system PATH)
- `aliases` — Alternative names for memory learning

If app not found in JSON, falls back to built-in defaults (Zoom, Teams, Outlook, Notepad, Calculator, Chrome, Firefox, Edge, VS Code, Discord).

## Troubleshooting

### "Failed to load sentence-transformers model"

First run downloads model (~100MB). Make sure internet is available:

```powershell
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

Models cached in `~/.cache/huggingface/`.

### Text Transform Not Working

**Symptoms:** "No text selected" error

**Causes & fixes:**
- Text is not selected in active window → Select text first
- Clipboard permission denied → Run PowerShell as Administrator
- Another app has clipboard lock → Close clipboard managers (e.g., Ditto)

**Test:**
```powershell
py wizard/main.py "uppercase"  # Should fail with "no text selected"
```

### Volume/Lock Commands Fail

**Symptoms:** No sound change, computer won't lock

**Fixes:**
- Volume: Some systems don't support media keys via pyautogui → Use system volume mixer
- Lock: Run PowerShell as Administrator or check GPO (Group Policy)

### AutoHotkey Hotkey Not Triggering

**Symptoms:** F13 press does nothing

**Causes & fixes:**
1. Script not running → Double-click `wizard_key.ahk` or right-click → Run with AutoHotkey
2. F13 not programmable → Try F11, F12, or `Ctrl+Shift+W`
3. Another app claiming F13 → Disable in that app's settings

**Check if running:**
```powershell
Get-Process AutoHotkey
```

**Modify hotkey** (edit `wizard_key.ahk`):
```autohotkey
F11::  # Change F13 to F11
{ ... }
```

### JSON Parse Error in AutoHotkey

**Symptoms:** MsgBox shows garbled or empty message

**Likely cause:** Python exited with error, temp file corrupt

**Debug:**
```powershell
py wizard/main.py "test command"  # Check Python output directly
```

### "Unknown command" with High Match Score

Score < 0.42 threshold → Try more specific phrasing:

- ❌ "I want to open zoom" (0.38)
- ✓ "open zoom" (0.87)

Threshold configurable in `wizard/config.py` (`ROUTING_THRESHOLD`).

## Security Notes

- **Local only**: No data sent to external servers (embeddings computed locally)
- **Clipboard access**: pyautogui reads/writes clipboard for text transform (intentional)
- **No logging**: Command history not persisted (except aliases)

## Performance

- **Cold start**: ~2s (model load)
- **Warm start**: ~200ms per command
- **Latency**: Router + executor ≤500ms typical

For fastest performance with repeated commands, Wizard Key learns aliases (score 1.0 lookup, <10ms).

## License

MIT

## Contributing

Pull requests welcome! Suggested areas:
- More command types (email, calendar, todo)
- Confidence threshold tuning
- Platform support (Mac, Linux)
- Voice input integration
- Custom hotkey UI
