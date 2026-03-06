import webbrowser
from urllib.parse import urlparse


def open_url(url: str) -> dict:
    """
    Open URL in default browser.

    Normalizes plain domains to https://.

    Args:
        url: URL string.

    Returns:
        Dict with "ok" (bool) and "message" (str).
    """
    try:
        # Normalize URL
        if not _has_scheme(url):
            url = f"https://{url}"

        # Open in browser
        webbrowser.open(url)
        return {"ok": True, "message": f"Opened {url}"}

    except Exception as e:
        return {"ok": False, "message": f"Failed to open URL: {str(e)}"}


def _has_scheme(url: str) -> bool:
    """Check if URL has a scheme (http://, https://, etc)."""
    parsed = urlparse(url)
    return bool(parsed.scheme)
