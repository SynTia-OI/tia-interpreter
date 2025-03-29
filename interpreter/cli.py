import sys

# Help message
if "--help" in sys.argv:
    from .misc.help import help_message

    help_message()
    sys.exit(0)

# Version message
if "--version" in sys.argv:
    print("Tia Interpreter 0.1.0")
    sys.exit(0)

import argparse
import asyncio
import os
import subprocess
import threading
from typing import Any, Dict

from .misc.get_input import async_get_input
from .misc.spinner import SimpleSpinner
from .profiles import Profile

# Global interpreter object
global_interpreter = None


def _parse_list_arg(value: str) -> list:
    """Parse a comma-separated or JSON-formatted string into a list"""
    if not value:
        return []

    # Try parsing as JSON first
    if value.startswith("["):
        try:
            import json

            return json.loads(value)
        except json.JSONDecodeError:
            pass

    # Fall back to comma-separated parsing
    return [item.strip() for item in value.split(",") if item.strip()]


def _profile_to_arg_params(profile: Profile) -> Dict[str, Dict[str, Any]]:
    """Convert Profile attributes to argparse parameter definitions"""
    # Note: Defaults are taken from the loaded profile (profiles.py)
    return {
        "server": {
            "flags": ["--serve", "-s"],
            "action": "store_true",
            "default": profile.serve,
            "help": "Start the server",
        },
        "model": {
            "flags": ["--model", "-m"],
            "default": profile.model,
            "help": "Specify the model name (overrides profile)",
        },
        "provider": {
            "flags": ["--provider"],
            "default": profile.provider,
            "help": "Specify the API provider (overrides profile)",
        },
        "api_base": {
            "flags": ["--api-base", "-b"],
            "default": profile.api_base,
            "help": "Specify the API base URL (overrides profile)",
        },
        "api_key": {
            "flags": ["--api-key", "-k"],
            "default": profile.api_key,
            "help": "Specify the API key (overrides profile)",
        },
        "api_version": {
            "flags": ["--api-version"],
            "default": profile.api_version,
            "help": "Specify the API version (overrides profile)",
        },
        "temperature": {
            "flags": ["--temperature"],
            "default": profile.temperature,
            "help": "Specify the temperature (overrides profile)",
        },
        "max_tokens": {
            "flags": ["--max-tokens"],
            "default": profile.max_tokens,
            "help": "Specify the maximum number of tokens (overrides profile)",
        },
        "tools": {
            "flags": ["--tools"],
            "default": profile.tools,
            "help": "Specify enabled tools (overrides profile, comma-separated or JSON list)",
            "type": _parse_list_arg,
        },
        "allowed_commands": {
            "flags": ["--allowed-commands"],
            "default": profile.allowed_commands,
            "help": "Specify allowed commands (overrides profile, comma-separated or JSON list)",
            "type": _parse_list_arg,
        },
        "allowed_paths": {
            "flags": ["--allowed-paths"],
            "default": profile.allowed_paths,
            "help": "Specify allowed paths (overrides profile, comma-separated or JSON list)",
            "type": _parse_list_arg,
        },
        "auto_run": {
            "flags": ["--auto-run", "-y"],
            "action": "store_true",
            "default": profile.auto_run,
            "help": "Automatically run tools (overrides profile)",
        },
        "tool_calling": {
            "flags": ["--no-tool-calling"],
            "action": "store_false",
            "default": profile.tool_calling,
            "dest": "tool_calling",
            "help": "Disable tool calling (overrides profile)",
        },
        "interactive": {
            "flags": ["--interactive"],
            "action": "store_true",
            "default": profile.interactive,
            "help": "Enable interactive mode (overrides profile)",
        },
        "no_interactive": {
            "flags": ["--no-interactive"],
            "action": "store_false",
            "default": profile.interactive,
            "dest": "interactive",
            "help": "Disable interactive mode (overrides profile)",
        },
        "system_message": {
            "flags": ["--system-message"],
            "default": profile.system_message,
            "help": "Overwrite system message (overrides profile)",
        },
        "custom_instructions": {
            "flags": ["--instructions"],
            "default": profile.instructions,
            "help": "Appended to default system message (overrides profile)",
        },
        "input": {
            "flags": ["--input"],
            "default": profile.input,
            "help": "Pre-fill first user message",
        },
        "max_turns": {
            "flags": ["--max-turns"],
            "type": int,
            "default": profile.max_turns,
            "help": "Set maximum conversation turns (overrides profile, -1 for unlimited)",
        },
        "profile": {
            "flags": ["--profile"],
            "default": "profiles.py", # Default to local file
            "help": "Path to profile configuration (ignored, uses profiles.py in CWD)", # Updated help text
            "metavar": "PATH",
        },
        "debug": {
            "flags": ["--debug", "-d"],
            "action": "store_true",
            "default": profile.debug,
            "help": "Run in debug mode (overrides profile)",
        },
    }


def load_interpreter(args):
    from .interpreter import Interpreter

    # Initialize interpreter (which loads profiles.py by default now)
    interpreter = Interpreter()

    # Apply CLI arguments over the loaded profile settings
    for key, value in args.items():
        # Check if the argument was actually provided by the user (not the default)
        # This is a bit tricky with argparse, might need refinement
        # A simple check is if the value is different from the profile's default for that key
        profile_default = getattr(interpreter._profile, key, None)
        if hasattr(interpreter, key) and value is not None and value != profile_default:
             # Only override if CLI arg is different from profile default
            setattr(interpreter, key, value)
            if args.get("debug"):
                print(f"[CLI Override] Set {key} = {value}")

    return interpreter


async def async_load_interpreter(args):
    return load_interpreter(args)


async def async_main(args):
    global global_interpreter

    if args["serve"]:
        global_interpreter = await async_load_interpreter(args)
        print("Starting server...")
        global_interpreter.server()
        return

    if (
        args["input"] is None
        and sys.stdin.isatty()
        and sys.argv[0].endswith("interpreter")
    ):
        from .misc.welcome import welcome_message

        welcome_message()

    if args["input"] is None and (
        sys.stdin.isatty() and args.get("no_interactive") is not True
    ):
        # Load the interpreter in a separate thread
        def load_interpreter_thread(args):
            loop = asyncio.new_event_loop()
            global global_interpreter
            global_interpreter = loop.run_until_complete(async_load_interpreter(args))

        thread = threading.Thread(target=load_interpreter_thread, args=(args,))
        thread.start()

        # Get user input
        message = await async_get_input()

        # Wait for the thread to finish
        thread.join()
    else:
        spinner = SimpleSpinner()
        spinner.start()
        global_interpreter = await async_load_interpreter(args)
        message = args["input"] if args["input"] is not None else sys.stdin.read()
        spinner.stop()
    print()
    global_interpreter.messages = [{"role": "user", "content": message}]
    try:
        async for _ in global_interpreter.async_respond():
            pass
    except KeyboardInterrupt:
        global_interpreter._spinner.stop()
    except asyncio.CancelledError:
        global_interpreter._spinner.stop()
    print()

    if global_interpreter.interactive:
        await global_interpreter.async_chat()


def parse_args():
    profile = Profile()
    local_profile_path = "profiles.py"  # Always use profiles.py in CWD
    if os.path.exists(local_profile_path):
        profile.load(local_profile_path)
    # else:
    #     # If profiles.py doesn't exist, Profile() uses defaults
    #     print(f"No '{local_profile_path}' found in the current directory. Using default settings.")

    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument("--help", "-h", action="store_true", help="Show help")
    parser.add_argument("--version", action="store_true", help="Show version")
    parser.add_argument(
        "--profiles", action="store_true", help="Open profiles directory (shows CWD)" # Updated help
    )
    parser.add_argument(
        "--save", action="store", metavar="PATH", help="Save current settings to profiles.py (ignores PATH)" # Updated help
    )

    # Pass the loaded profile to generate args with correct defaults
    arg_params = _profile_to_arg_params(profile)
    for param in arg_params.values():
        flags = param.pop("flags")
        parser.add_argument(*flags, **param)

    if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
        # Handle direct input like `interpreter "do something"`
        # Parse with defaults first, then add the input
        default_args = vars(parser.parse_args([]))
        return {**default_args, "input": " ".join(sys.argv[1:])} # Simplified input handling

    args = vars(parser.parse_args())

    if args["profiles"]:
        # Show current working directory instead of default profile folder
        cwd = os.getcwd()
        print(f"Profile ('profiles.py') is loaded from the current directory: {cwd}")
        if sys.platform == "win32":
            os.startfile(cwd)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.run([opener, cwd])
        sys.exit(0)

    # Remove the logic for loading profile via --profile argument
    # if args["profile"] != profile.profile_path: # This check is no longer needed
    #     # We always load from profiles.py now
    #     pass

    if args["save"]:
        # Save current settings (potentially overridden by CLI args) to profiles.py
        # Create a temporary profile instance reflecting current args
        current_profile = Profile()
        for key, value in args.items():
             # Only save keys that are actual profile attributes
            if hasattr(current_profile, key) and value is not None:
                setattr(current_profile, key, value)

        # Always save to local profiles.py, ignore the provided path
        save_path = "profiles.py"
        current_profile.save(save_path)
        print(f"Settings saved to {save_path}")
        sys.exit(0)

    # Remove the --profile arg from the final dict as it's not used by load_interpreter
    args.pop("profile", None)
    args.pop("save", None) # Also remove save arg

    return args


def main():
    """Entry point for the CLI"""
    try:
        args = parse_args()

        if args["serve"]:
            print("Starting OpenAI-compatible server...")
            global_interpreter = load_interpreter(args)
            global_interpreter.server()
            return

        asyncio.run(async_main(args))
    except KeyboardInterrupt:
        sys.exit(0)
    except asyncio.CancelledError:
        sys.exit(0)


if __name__ == "__main__":
    main()
