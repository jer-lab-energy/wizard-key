import re

COMMAND = {
    "name": "transform_text",
    "examples": [
        "uppercase text",
        "make it uppercase",
        "convert to uppercase",
        "all caps",
        "lowercase",
        "lowercase text",
        "title case",
        "capitalize",
    ],
    "slots": ["mode"],
}


def extract(text: str, memory: dict) -> dict:
    """
    Extract text transformation mode from user input.

    Args:
        text: User input text.
        memory: Memory dict (unused).

    Returns:
        Dict with "mode" key (uppercase/lowercase/title) if match found, else empty dict.
    """
    text_lower = text.lower()

    # Check uppercase patterns
    if re.search(r"\b(uppercase|upper|all\s*caps|capitals|allcaps)\b", text_lower):
        return {"mode": "uppercase"}

    # Check lowercase patterns
    if re.search(r"\b(lowercase|lower|lower\s*caps)\b", text_lower):
        return {"mode": "lowercase"}

    # Check title case patterns
    if re.search(r"\b(title|capitalize|title\s*case)\b", text_lower):
        return {"mode": "title"}

    return {}
