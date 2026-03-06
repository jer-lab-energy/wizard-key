import time
import pyautogui
import pyperclip


def transform_selected_text(mode: str) -> dict:
    """
    Transform selected text by mode (uppercase/lowercase/title).

    Copies selection, applies transformation, and pastes back.
    Preserves previous clipboard contents.

    Args:
        mode: "uppercase", "lowercase", or "title".

    Returns:
        Dict with "ok" (bool) and "message" (str).
    """
    if mode not in ("uppercase", "lowercase", "title"):
        return {"ok": False, "message": f"Invalid mode: {mode}"}

    # Save current clipboard
    prev_clipboard = pyperclip.paste()

    try:
        # Copy selection
        pyautogui.hotkey("ctrl", "c")
        time.sleep(0.2)

        selected = pyperclip.paste()

        # Check if anything was selected
        if selected == prev_clipboard:
            return {"ok": False, "message": "No text selected"}

        # Apply transformation
        if mode == "uppercase":
            transformed = selected.upper()
        elif mode == "lowercase":
            transformed = selected.lower()
        elif mode == "title":
            transformed = selected.title()

        # Copy transformed text to clipboard
        pyperclip.copy(transformed)
        time.sleep(0.1)

        # Paste
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.2)

        return {"ok": True, "message": f"Transformed to {mode}"}

    except Exception as e:
        return {"ok": False, "message": f"Failed to transform text: {str(e)}"}

    finally:
        # Restore previous clipboard
        pyperclip.copy(prev_clipboard)
