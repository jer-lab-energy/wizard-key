COMMAND = {
    "name": "switch_window",
    "examples": [
        "switch window",
        "next window",
        "alt tab",
        "next app",
        "change app",
        "cycle windows",
    ],
    "slots": [],
}


def extract(text: str, memory: dict) -> dict:
    """
    Extract parameters for switch_window command.

    Args:
        text: User input text.
        memory: Memory dict.

    Returns:
        Empty dict (no parameters needed).
    """
    return {}
