import json
import subprocess
from pathlib import Path

# Common Windows app defaults
DEFAULT_APPS = {
    "zoom": "zoom.exe",
    "teams": "teams.exe",
    "outlook": "outlook.exe",
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "chrome": "chrome.exe",
    "firefox": "firefox.exe",
    "edge": "msedge.exe",
    "vscode": "code.exe",
    "discord": "discord.exe",
}


def _load_apps() -> dict:
    """Load apps configuration from apps.json."""
    apps_file = Path(__file__).parent.parent / "data" / "apps.json"

    if apps_file.exists():
        try:
            with open(apps_file) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass

    return {}


def open_app(app: str) -> dict:
    """
    Open an application by name.

    Args:
        app: Application name.

    Returns:
        Dict with "ok" (bool) and "message" (str).
    """
    app_lower = app.lower()

    # Try to load from apps.json
    apps_config = _load_apps()

    # Get target executable
    target = None

    if app_lower in apps_config:
        cfg = apps_config[app_lower]
        target = cfg.get("path") or cfg.get("executable")

    # Fall back to defaults
    if not target:
        target = DEFAULT_APPS.get(app_lower)

    if not target:
        return {"ok": False, "message": f"Unknown application: {app}"}

    try:
        subprocess.Popen(target, shell=False)
        return {"ok": True, "message": f"Launched {app}"}
    except FileNotFoundError:
        return {"ok": False, "message": f"Application not found: {target}"}
    except Exception as e:
        return {"ok": False, "message": f"Failed to launch {app}: {str(e)}"}
