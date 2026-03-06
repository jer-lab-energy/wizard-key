import time
from datetime import datetime
from pathlib import Path
import pyautogui


def switch_window() -> dict:
    """
    Switch to next window using Alt+Tab.

    Returns:
        Dict with "ok" (bool) and "message" (str).
    """
    try:
        pyautogui.hotkey("alt", "tab")
        time.sleep(0.2)
        return {"ok": True, "message": "Switched window"}
    except Exception as e:
        return {"ok": False, "message": f"Failed to switch window: {str(e)}"}


def take_screenshot() -> dict:
    """
    Take a screenshot and save with timestamp.

    Saves to Pictures folder if available, falls back to project root.

    Returns:
        Dict with "ok" (bool), "message" (str), and "path" (str) on success.
    """
    try:
        # Determine save location
        pictures_dir = Path.home() / "Pictures"
        if pictures_dir.exists():
            save_dir = pictures_dir
        else:
            save_dir = Path(__file__).parent.parent.parent

        # Generate timestamped filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        filepath = save_dir / filename

        # Take and save screenshot
        screenshot = pyautogui.screenshot()
        screenshot.save(str(filepath))

        return {"ok": True, "message": f"Screenshot saved", "path": str(filepath)}

    except Exception as e:
        return {"ok": False, "message": f"Failed to take screenshot: {str(e)}"}
