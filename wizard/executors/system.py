import time
import subprocess
import pyautogui


def mute() -> dict:
    """Mute system volume."""
    try:
        pyautogui.press("volumemute")
        time.sleep(0.2)
        return {"ok": True, "message": "System muted"}
    except Exception as e:
        return {"ok": False, "message": f"Failed to mute: {str(e)}"}


def volume_up() -> dict:
    """Increase system volume."""
    try:
        pyautogui.press("volumeup")
        time.sleep(0.2)
        return {"ok": True, "message": "Volume increased"}
    except Exception as e:
        return {"ok": False, "message": f"Failed to increase volume: {str(e)}"}


def volume_down() -> dict:
    """Decrease system volume."""
    try:
        pyautogui.press("volumedown")
        time.sleep(0.2)
        return {"ok": True, "message": "Volume decreased"}
    except Exception as e:
        return {"ok": False, "message": f"Failed to decrease volume: {str(e)}"}


def lock_computer() -> dict:
    """Lock the Windows computer."""
    try:
        subprocess.run(
            ["rundll32.exe", "user32.dll,LockWorkStation"],
            check=False,
        )
        return {"ok": True, "message": "Computer locked"}
    except Exception as e:
        return {"ok": False, "message": f"Failed to lock computer: {str(e)}"}
