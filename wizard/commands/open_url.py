import re

COMMAND = {
    "name": "open_url",
    "examples": [
        "open gmail",
        "go to youtube",
        "open reddit",
        "open github",
        "search google",
        "open website",
    ],
    "slots": ["url"],
}

# Service name to URL mapping
SERVICE_URLS = {
    "gmail": "https://mail.google.com",
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "reddit": "https://www.reddit.com",
    "github": "https://www.github.com",
    "twitter": "https://www.twitter.com",
    "facebook": "https://www.facebook.com",
    "linkedin": "https://www.linkedin.com",
    "slack": "https://www.slack.com",
    "github.com": "https://www.github.com",
}


def extract(text: str, memory: dict) -> dict:
    """
    Extract URL from user input.

    Args:
        text: User input text.
        memory: Memory dict.

    Returns:
        Dict with "url" key if match found, else empty dict.
    """
    text_lower = text.lower()

    # Check service names
    for service, url in SERVICE_URLS.items():
        if service in text_lower:
            return {"url": url}

    # Check for raw domain pattern (simple)
    domain_match = re.search(r"(?:www\.)?([a-z0-9]+(?:\.[a-z0-9]+)+)", text_lower)
    if domain_match:
        domain = domain_match.group(0)
        if not domain.startswith("www."):
            domain = "www." + domain
        return {"url": f"https://{domain}"}

    return {}
