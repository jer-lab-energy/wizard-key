import json
import re
from pathlib import Path

COMMAND = {
    "name": "open_app",
    "examples": [
        "open zoom",
        "launch zoom",
        "open outlook",
        "start calculator",
        "open notepad",
        "open teams",
    ],
    "slots": ["app"],
}

# Common verbs to strip
VERBS = {"open", "launch", "start", "run", "bring up"}


def extract(text: str, memory: dict) -> dict:
    """
    Extract app name from user input.

    Args:
        text: User input text.
        memory: Memory dict with optional "preferred_apps" key.

    Returns:
        Dict with "app" key if match found, else empty dict.
    """
    cleaned = _clean_text(text)

    # Check preferred_apps in memory
    preferred_apps = memory.get("preferred_apps", {})
    for alias, app_name in preferred_apps.items():
        if alias.lower() in cleaned:
            return {"app": app_name}

    # Load apps from apps.json
    apps_file = Path(__file__).parent.parent / "data" / "apps.json"
    app_names = {}
    app_aliases = {}

    if apps_file.exists():
        try:
            with open(apps_file) as f:
                apps_data = json.load(f)
                for app_name, config in apps_data.items():
                    app_names[app_name.lower()] = app_name
                    for alias in config.get("aliases", []):
                        app_aliases[alias.lower()] = app_name
        except (json.JSONDecodeError, IOError):
            pass

    # Try exact app name match
    for app_lower, app_orig in app_names.items():
        if app_lower in cleaned:
            return {"app": app_orig}

    # Try alias match
    for alias_lower, app_name in app_aliases.items():
        if alias_lower in cleaned:
            return {"app": app_name}

    return {}


def _clean_text(text: str) -> str:
    """Clean text by lowercasing and removing common verbs."""
    text = text.lower()
    for verb in VERBS:
        text = re.sub(rf"\b{verb}\s+", "", text)
    return text.strip()
