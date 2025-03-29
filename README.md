# Tia Interpreter - CoPA Project

Hello Tia,

This is your personal AI Interpreter featuring CoPA (Co-Personal Assistant), designed to function as a Natural Language Interface.

**Project Repository:** [https://github.com/SynTia-OI/tia-interpreter](https://github.com/SynTia-OI/tia-interpreter)
**Contact:** hyperion@cutnbreak.com.au

## Overview

This project provides CoPA, an AI assistant built using the Claude 3.7 Sonnet model (as of March 2025), equipped with tools to interact with your Windows environment, primarily through PowerShell commands executed via its 'bash' tool, and file manipulation via its 'str_replace_editor' tool.

The goal is to create a seamless Natural Language Computer Interface tailored to your workflow at Cut N Break Pty Ltd.

## CoPA Capabilities

Based on the current configuration and system message, CoPA can:

*   **Execute PowerShell Commands:** Use the `bash` tool to run commands directly in PowerShell on your Windows system. This allows for system management, script execution, software interaction, etc. (Remember to use PowerShell syntax!).
*   **File Operations:** Use the `str_replace_editor` tool to view, create, edit (replace/insert text), and undo edits in files across the system.
*   **Computer Interaction (GUI):** Use the `computer` tool to control the mouse, keyboard, take screenshots, and perform basic GUI automation tasks if needed, although direct command execution is preferred.
*   **Orchestration & Delegation:** Act as a high-level orchestrator, maintaining context and potentially delegating tasks to other specialized agents within the framework (as defined in the system message).
*   **Coding Assistance:** Leverage its underlying language model (Claude 3.7 Sonnet) for coding tasks like writing, debugging, explaining, and refactoring code in various languages.
*   **Natural Language Interaction:** Understand and respond to requests in natural language, acting as an interface to your computer.

*Note: Access is currently configured to be unrestricted. CoPA can execute any command and access any file path its tools allow.*

## Setup & Running (Windows)

Here's the refined process to set up the development environment and run the interpreter after cloning the repository:

1.  **Create Virtual Environment:**
    *   Open PowerShell or Command Prompt in the project directory (`C:\my_interpreter_ai_agent\tia-interpreter`).
    *   Run: `uv venv`
    *   Activate the environment: `.venv\Scripts\activate` (or `Activate.ps1` for PowerShell)

2.  **Install Dependencies (Editable Mode Recommended for Development):**
    *   Ensure the virtual environment is active.
    *   Run: `uv pip install -e .[dev]`
    *   *(This uses `uv` and the `hatchling` build backend defined in `pyproject.toml` to install the package and its development dependencies in editable mode, meaning changes to the source code are reflected immediately.)*

3.  **Synchronize Environment (Crucial Step):**
    *   Ensure the virtual environment is active.
    *   Run: `uv sync --extra dev`
    *   *(This command ensures the environment matches the `uv.lock` file precisely, including development dependencies. This was the key step that resolved previous execution issues.)*

4.  **Run the Interpreter:**
    *   Ensure the virtual environment is active.
    *   Run the command: `tia-interpreter`
    *   *(Alternatively, you can run `python -m interpreter.cli`)*

## Development Notes & Troubleshooting

*   **Build System:** This project uses `hatchling` as the build backend, managed via `pyproject.toml`. `uv` interacts with Hatchling during installation.
*   **Editable Installs (`-e`):** Using `uv pip install -e .[dev]` is recommended for development. This creates links so that when you edit the source code (e.g., files in the `interpreter` directory), the changes are automatically used the next time you run `tia-interpreter` or `python -m interpreter.cli` **without needing to reinstall**.
*   **Applying Code Changes (Editable Mode):** If you've used editable mode, simply saving your code changes is usually enough. Restart the `tia-interpreter` application if it's already running to pick up the changes.
*   **Applying Code Changes (Normal Install):** If you installed *without* the `-e` flag (e.g., `uv pip install .` or `uv pip install dist/*.whl`), you **must** reinstall the package for code changes to take effect:
    1.  `uv pip uninstall tia-interpreter`
    2.  `uv pip install .` (or install the specific wheel if you built one)
*   **Updating Dependencies:** If you change dependencies in `pyproject.toml`:
    1.  Update the lock file: `uv lock --upgrade`
    2.  Synchronize the environment: `uv sync --extra dev` (or just `uv sync` if not using dev dependencies).
*   **Installation Issues (`ModuleNotFoundError`):** If the `tia-interpreter` command fails (especially after changes), ensure the environment is correctly synchronized using `uv sync --extra dev`. This command aligns the installed packages precisely with the lock file and often fixes entry point issues.
*   **Cache Cleaning (If necessary):** Python creates `__pycache__` directories containing compiled bytecode (`.pyc` files). While usually handled automatically, if you suspect stale bytecode is causing issues, you can manually remove these directories.
    *   In PowerShell: `Get-ChildItem -Recurse -Include __pycache__ | Remove-Item -Recurse -Force`
    *   After cleaning cache, it's often best to reinstall: `uv pip uninstall tia-interpreter` followed by `uv pip install .[dev]` and `uv sync --extra dev`.
*   **Metadata Sanitization:** When sharing code or building distributions, be mindful of sensitive information (like API keys hardcoded in `profiles.py` during testing). Ensure these are removed or managed via environment variables in production/shared versions. Version control systems like Git also store history; be careful what you commit.

Let me know if you need further assistance, Tia!
