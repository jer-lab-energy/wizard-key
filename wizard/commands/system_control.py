import re

COMMAND = {
    "name": "system_control",
    "examples": [
        "mute",
        "unmute",
        "volume up",
        "volume down",
        "lock computer",
        "screenshot",
    ],
    "slots": ["action"],
}


def extract(text: str, memory: dict) -> dict:
    """
    Extract system control action from user input.

    Args:
        text: User input text.
        memory: Memory dict.

    Returns:
        Dict with "action" key if match found, else empty dict.
    """
    text_lower = text.lower()

    # Mute patterns
    if re.search(r"\bmute\b", text_lower):
        return {"action": "mute"}

    # Unmute patterns
    if re.search(r"\bunmute\b", text_lower):
        return {"action": "unmute"}

    # Volume up patterns
    if re.search(r"\bvolume\s*up\b|\bup\s*volume\b", text_lower):
        return {"action": "volume_up"}

    # Volume down patterns
    if re.search(r"\bvolume\s*down\b|\bdown\s*volume\b", text_lower):
        return {"action": "volume_down"}

    # Lock patterns
    if re.search(r"\block\b", text_lower):
        return {"action": "lock"}

    # Screenshot patterns
    if re.search(r"\bscreenshot\b|\bscreen\s*shot\b", text_lower):
        return {"action": "screenshot"}

    return {}
