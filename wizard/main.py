import sys
import json

from .config import ensure_data_dir
from .router import Router
from .memory import load_memory, remember_alias
from .schema import ExecutionResult

# Import command modules
from .commands import open_app, open_url, switch_window, system_control, transform_text

# Import executors
from .executors import apps, browser, system, text_ops, windows


def build_command_defs() -> dict:
    """Build command definitions from all command modules."""
    return {
        open_app.COMMAND["name"]: open_app.COMMAND,
        open_url.COMMAND["name"]: open_url.COMMAND,
        switch_window.COMMAND["name"]: switch_window.COMMAND,
        system_control.COMMAND["name"]: system_control.COMMAND,
        transform_text.COMMAND["name"]: transform_text.COMMAND,
    }


def dispatch_executor(command: str, args: dict, memory: dict) -> dict:
    """Dispatch command to appropriate executor."""
    if command == "open_app":
        return apps.open_app(args.get("app", ""))

    elif command == "open_url":
        return browser.open_url(args.get("url", ""))

    elif command == "switch_window":
        return windows.switch_window()

    elif command == "transform_text":
        mode = args.get("mode", "")
        return text_ops.transform_selected_text(mode)

    elif command == "system_control":
        action = args.get("action", "")
        if action == "mute":
            return system.mute()
        elif action == "unmute":
            return {"ok": False, "message": "Unmute not yet implemented"}
        elif action == "volume_up":
            return system.volume_up()
        elif action == "volume_down":
            return system.volume_down()
        elif action == "lock":
            return system.lock_computer()
        elif action == "screenshot":
            return windows.take_screenshot()
        else:
            return {"ok": False, "message": f"Unknown action: {action}"}

    else:
        return {"ok": False, "message": f"Unknown command: {command}"}


def main():
    """Main entry point for wizard key."""
    try:
        # Setup
        ensure_data_dir()
        memory = load_memory()
        command_defs = build_command_defs()
        router = Router(command_defs)

        # Get input
        if len(sys.argv) < 2:
            result = {"ok": False, "message": "No command provided"}
            print(json.dumps(result, ensure_ascii=False))
            return

        text = " ".join(sys.argv[1:])

        # Route
        match = router.route(text)

        # Handle unknown command
        if match.command == "unknown":
            result = {
                "ok": False,
                "message": "Could not understand command",
                "match_score": float(match.score),
                "best_guess": match.example,
            }
            print(json.dumps(result, ensure_ascii=False))
            return

        # Extract parameters
        command_module = sys.modules[f"wizard.commands.{match.command}"]
        args = command_module.extract(text, memory)

        # Dispatch executor
        exec_result = dispatch_executor(match.command, args, memory)

        # Remember alias on success
        if exec_result.get("ok"):
            remember_alias(text, match.command, args)

        # Print result
        print(json.dumps(exec_result, ensure_ascii=False))

    except Exception as e:
        result = {"ok": False, "message": f"Internal error: {str(e)}"}
        print(json.dumps(result, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
