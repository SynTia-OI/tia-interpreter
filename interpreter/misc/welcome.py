import os
import random


def get_latest_model():
    """Detect the latest available model version."""
    # This function would connect to the API to determine the latest model
    # For demonstration purposes, we'll return a placeholder
    available_models = [
        "claude-3.7-sonnet-20250219"
    ]
    return available_models[-1]  # Return the latest model in the list


def welcome_message_1(args=None):
    latest_model = get_latest_model()
    model_name = latest_model.upper()
    
    print(
        f"""
\033[7m {model_name} \033[0m

This AI can modify files, install software, and execute commands.

By continuing, you accept all risks and responsibility.
"""
    )


def welcome_message_2(args=None):
    latest_model = get_latest_model()
    model_name = latest_model.upper()
    
    print(
        f'''
\033[7m {model_name} \033[0m

Tip: You can paste content by typing """ first.
'''
    )


def welcome_message_3(args=None):
    latest_model = get_latest_model()
    model_name = latest_model.lower()
    
    print(
        f"""
\033[94m {model_name}
> runs code, = edits files
@ requires approval\033[0m
"""
    )


def welcome_message_4(args=None):
    # Define color combinations
    COLORS = {
        "medium_blue": ("\033[48;5;27m", "\033[38;5;27m"),
        "dark_blue": ("\033[48;5;20m", "\033[38;5;20m"),
        "light_blue": ("\033[48;5;39m", "\033[38;5;39m"),
        "deep_sky_blue": ("\033[48;5;32m", "\033[38;5;32m"),
        "dodger_blue": ("\033[48;5;33m", "\033[38;5;33m"),
    }

    WHITE_FG = "\033[97m"
    BLACK_FG = "\033[30m"
    RESET = "\033[0m"
    
    latest_model = get_latest_model()
    model_name = latest_model.upper()

    # Different text layouts
    LAYOUTS = {
        "basic_background": lambda bg, fg: f"""
{bg} * {model_name} {RESET}

{fg}>{RESET} runs code
{fg}={RESET} edits files
{fg}@{RESET} requires approval
""",
        "compact": lambda bg, fg: f"""
{bg} * {model_name} {RESET} {fg}>{RESET} code {fg}={RESET} files {fg}@{RESET} approval
""",
        "white_on_color": lambda bg, fg: f"""
{bg}{WHITE_FG} * {model_name} {RESET}

{bg}{WHITE_FG}>{RESET} runs code
{bg}{WHITE_FG}={RESET} edits files
{bg}{WHITE_FG}@{RESET} requires approval
""",
        "white_on_color_2": lambda bg, fg: f"""
{bg}{WHITE_FG} * {model_name} {RESET}

{bg}{WHITE_FG}>{RESET} interpreter {bg}{WHITE_FG}={RESET} file editor
{bg}{WHITE_FG}@{RESET} actions require approval
""",
        "black_on_color": lambda bg, fg: f"""
{bg}{BLACK_FG} * {model_name} {RESET}

{bg}{BLACK_FG}>{RESET} runs code
{bg}{BLACK_FG}={RESET} edits files
{bg}{BLACK_FG}@{RESET} requires approval
""",
        "minimal": lambda bg, fg: f"""
* {model_name}

{fg}$ runs code
= edits files
! requires approval{RESET}
""",
        "double_line": lambda bg, fg: f"""
{bg} * {model_name} {RESET}

{fg}> runs code{RESET} {fg}= edits files{RESET}
{fg}@ requires approval{RESET}
""",
        "modern": lambda bg, fg: f"""
{bg} >> {model_name} << {RESET}

{fg}>{RESET} executes commands
{fg}□{RESET} manages files
{fg}^{RESET} needs approval
""",
        "technical": lambda bg, fg: f"""
{bg} {model_name} {RESET}

{fg}${RESET} runs code
{fg}#{RESET} edits files
{fg}@{RESET} needs ok
""",
        "technical_2": lambda bg, fg: f"""
{bg}{WHITE_FG} {model_name} {RESET}

# edits files
$ executes commands
@ actions require approval
""",
        "technical_3": lambda bg, fg: f"""
{bg}{WHITE_FG} {model_name} {RESET}

{fg}# file editor
$ bash executor
@ requires approval{RESET}
""",
        "brackets": lambda bg, fg: f"""
{bg} [ {model_name} ] {RESET}

{fg}[>]{RESET} run commands
{fg}[=]{RESET} file operations
{fg}[!]{RESET} elevated access
""",
        "ascii_art": lambda bg, fg: f"""
{bg} | {model_name}    | {RESET}

{fg}>>>{RESET} execute code
{fg}[=]{RESET} modify files
{fg}(!){RESET} request approval
""",
    }

    LAYOUTS = {
        k: v
        for k, v in LAYOUTS.items()
        if k
        in ["basic_background", "minimal", "technical", "technical_2", "technical_3"]
    }

    layout_items = list(LAYOUTS.items())
    color_items = list(COLORS.items())
    random.shuffle(layout_items)
    random.shuffle(color_items)

    for color_name, (BG, FG) in color_items:
        for layout_name, layout in layout_items:
            print(f"Style: {layout_name} with {color_name}\n\n\n")
            print("$: interpreter")
            print(layout(BG, FG))
            print("> make a react project")
            print("\n" * 10)


def welcome_message_5(args=None):
    WHITE_FG = "\033[97m"
    BLUE_BG = "\033[48;5;21m"  # Dark blue background
    BLUE_FG = "\033[38;5;21m"
    RESET = "\033[0m"
    
    latest_model = get_latest_model()
    model_name = latest_model.upper()

    tips = [
        'Use """ for multi-line input',
        "Try the wtf command to fix the last error",
        "Press Ctrl+C to cancel",
        "Messages starting with $ run in the shell",
    ]

    print(
        f"""
{BLUE_BG}{WHITE_FG} {model_name} {RESET}

# edits files
$ executes commands
@ actions require approval
"""
    )


def welcome_message_6():
    latest_model = get_latest_model()
    model_name = latest_model.split("-")[-1].capitalize()
    
    print(
        f"""
Tia Interpreter 0.1.0


A natural language interface for your computer.

Usage: i [prompt]
   or: interpreter [options]

Documentation: docs.openinterpreter.com
Run 'interpreter --help' for full options

"""
    )


def welcome_message_7():
    latest_model = get_latest_model()
    
    print(
        f"""
Tia Interpreter 0.1.0

A natural language interface for your computer.

Usage: interpreter [prompt] [-m model] [-t temp] [-k key] [options]
Execute natural language commands on your computer

    -m, --model <model>    Specify the language model to use
    -t, --temp <float>     Set temperature (0-1) for model responses
    -k, --key <key>        Set API key for the model provider
    -p, --profile <file>   Load settings from profile file
    --auto-run            Run commands without confirmation
    --no-tools            Disable tool/function calling
    --debug               Enable debug logging
    --serve               Start in server mode

example: interpreter "create a python script"
example: interpreter -m gpt-4 "analyze data.csv" 
example: interpreter --auto-run "install nodejs"
example: interpreter --profile work.json
"""
    )

def welcome_message_8():
    latest_model = get_latest_model()
    
    print(
        f"""
Tia Interpreter 0.1.0

A natural language interface for your computer.

Usage: interpreter [prompt] [-m model] [-t temp] [-k key] [options]
Execute natural language commands on your computer

    -m, --model <model>    Specify the language model to use
    -t, --temp <float>     Set temperature (0-1) for model responses
    -k, --key <key>        Set API key for the model provider
    -p, --profile <file>   Load settings from profile file
    --auto-run            Run commands without confirmation
    --no-tools            Disable tool/function calling
    --debug               Enable debug logging
    --serve               Start in server mode

example: interpreter "create a python script"
example: interpreter -m {latest_model} "analyze data.csv" 
example: interpreter --auto-run "install nodejs"
example: interpreter --profile work.json
"""
    )

def welcome_message_9():
    latest_model = get_latest_model()
    model_name = latest_model.split("-")[-1].capitalize()
    
    print(
        f"""
Tia Interpreter 0.1.0
A natural language interface for your computer.

A modern command-line assistant.

Usage: i [prompt]
   or: interpreter [options]

Documentation: docs.tiainterpreter.com
Run 'interpreter --help' for all options
"""
    )

# For backwards compatibility with original code
def welcome_message(args=None):
    """Default welcome message that uses the latest model and no emojis"""
    latest_model = get_latest_model()
    model_name = latest_model.upper()
    
    WHITE_FG = "\033[97m"
    BLUE_BG = "\033[48;5;21m"
    RESET = "\033[0m"
    
    print(
        f"""
{BLUE_BG}{WHITE_FG} {model_name} {RESET}

# edits files
$ executes commands
@ actions require approval
"""
    )