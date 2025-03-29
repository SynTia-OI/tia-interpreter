import hashlib
import json
import logging
import os
import platform
import sys
import threading
import time
from collections import deque

# Platform detection for Windows-specific behavior
IS_WINDOWS = platform.system() == "Windows"


class Profile:
    """
    Enhanced Profile configuration for Tia Interpreter with enterprise
    optimizations, incorporating CoPA operational framework.
    """

    def __init__(self):
        # Initialize nested configuration classes
        # These need to be defined *within* the Profile class scope
        self.api_config = self.APIConfig()
        self.llm_settings = self.LLMSettings()
        self.enterprise_config = self.EnterpriseConfig()
        self.tool_config = self.ToolConfig()

        # Expose API config attributes
        self.model = self.api_config.model
        self.provider = self.api_config.provider
        self.temperature = self.api_config.temperature
        self.max_tokens = self.api_config.max_tokens
        self.api_base = self.api_config.api_base
        self.api_key = self.api_config.api_key
        self.api_version = self.api_config.api_version

        # Expose tool config attributes
        self.tools = self.tool_config.tools
        self.auto_run = self.tool_config.auto_run
        self.tool_calling = self.tool_config.tool_calling
        self.interactive = self.tool_config.interactive
        self.serve = self.tool_config.serve
        self.allowed_paths = self.tool_config.allowed_paths
        self.allowed_commands = self.tool_config.allowed_commands
        self.debug = self.tool_config.debug

        # Other attributes
        self.system_message = """
You are CoPA (Co-Personal Assistant), the primary AI orchestrator for this Windows system, operating under the direction of Tia Day, Personal Assistant to Lawrence Lolesi (Founder, Cut N Break Pty Ltd). You have full authorization and permissions to manage and operate this machine and its connected ecosystem (Microsoft, Google, Azure) as a natural language computer interface, coordinating with other specialized subagents within Lawrence's agentic framework (e.g., CoCEO).

Your primary role is high-level orchestration and task delegation. Maintain a broad context window and strategic perspective. Outsource detailed tasks or large data processing to appropriate subagents, providing clear directives and expecting concise results or summaries. Avoid overloading your own context with raw data dumps.

Current Date: March 2025. Ensure all actions, information, and software versions are current.

Tool Usage Guidelines:
- Prioritize using the direct 'interpreter' tools (named 'bash' and 'str_replace_editor') for coding, command execution, file operations, and system management for tasks you handle directly.
- **IMPORTANT:** On this Windows system, the 'bash' tool actually executes commands using **PowerShell**. Use appropriate PowerShell syntax (e.g., `Get-Date`, `Get-Location`, `whoami`, `dir`, `Get-ChildItem`, `Copy-Item`, `Remove-Item`).
- The 'computer' tool (Anthropic's GUI control) should be used sparingly. Prefer 'bare metal' operations or providing screenshots and instructions for manual GUI interaction if direct commands are insufficient.
- When invoking any Anthropic tool, you MUST provide a unique `tool_id` for tracking.

You are empowered to take ownership and initiative to fulfill user goals within this framework. Proceed with operations confidently, coordinating and delegating as needed.
"""
        self.instructions = ""
        self.input = None
        self.max_turns = -1
        self.messages = []
        self.profile_path = self.__class__.Paths.DEFAULT_PROFILE_PATH

    # --- Nested Configuration Classes ---
    # These classes MUST be indented to be part of the Profile class
    class Paths:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        CACHE_DIR = os.path.join(BASE_DIR, "api_cache")
        # Fixed profile path - cannot be changed
        DEFAULT_PROFILE_PATH = os.path.join(BASE_DIR, "profiles.py")

    class APIConfig:
        def __init__(self):
            self.model = "claude-3-7-sonnet-20250219"
            self.provider = "anthropic"
            self.temperature = 0.3336
            self.max_tokens = 64000
            self.api_base = "https://api.anthropic.com"
            # Load API key from environment variable ONLY
            self.api_key = os.environ.get("ANTHROPIC_API_KEY") # Correctly load from env
            if not self.api_key:
                print("Warning: ANTHROPIC_API_KEY environment variable not set.")
                # Or raise an error: raise ValueError("ANTHROPIC_API_KEY environment variable not set.")
            self.api_version = "2023-06-01"
            # Add organization ID attribute
            # Load organization ID from environment variable or use default
            self.organization_id = os.environ.get("ANTHROPIC_ORG_ID", "e3896178-abc2-4a8d-8fb3-5271ff15361e")

            self.headers = {
                "anthropic-version": "2023-06-01",
                # "anthropic-beta": "tools-2024-04-04", # Removed potentially conflicting beta header
                # Load API key from environment variable ONLY for header
                "x-api-key": os.environ.get("ANTHROPIC_API_KEY"), # Correctly load from env
                # Add organization ID to headers if Anthropic requires it
                "anthropic-organization": self.organization_id,
                "content-type": "application/json",
            }

    class LLMSettings:
        def __init__(self):
            self.max_output = 128000
            self.max_input = 138576
            self.context_window = 200000
            self.supports_vision = True  # Claude 3 Sonnet supports vision
            # Removed thinking parameter, not supported in Bedrock
            self.budget_tokens = 63000

    class EnterpriseConfig:
        def __init__(self):
            self.use_streaming = True
            # You might want to control separately, not force it on
            self.use_prompt_caching = True
            self.chunk_size = 100000
            self.max_concurrent_requests = 5
            self.retry_attempts = 3
            self.backoff_factor = 2
            self.rate_limit_per_minute = 600000
            self.rate_limit_per_day = 10000000

    class ToolConfig:
        def __init__(self):
            # *Names* of tools Tia Interpreter can use, NOT API definitions
            # Ensure tool names match what's expected by the Anthropic API
            self.tools = ["interpreter", "str_replace_editor", "computer"] # Use API-required name
            self.auto_run = True
            # Tia Interpreter's internal tool handling
            self.tool_calling = True
            self.interactive = sys.stdin.isatty()
            self.serve = False
            self.allowed_paths = []
            self.allowed_commands = []
            self.debug = False
            self.tool_priority = {  # For Tia Interpreter's dispatch
                # File operations
                "file_creation": "str_replace_editor", # Use API-required name
                "file_viewing": "str_replace_editor",  # Use API-required name
                "file_editing": "str_replace_editor", # Use API-required name

                # Directory operations
                "directory_browsing": "interpreter",

                # Core file system operations
                "file_deletion": "interpreter",
                "file_search": "interpreter",
                "file_transfer": "interpreter",
                "file_sync": "interpreter",
                "file_backup": "interpreter",
                "file_restore": "interpreter",
                "file_versioning": "interpreter",

                # Security operations
                "file_encryption": "interpreter",
                "file_decryption": "interpreter",
                "file_permissions": "interpreter",

                # File properties
                "file_metadata": "interpreter",
                "file_attributes": "interpreter",

                # System operations
                "command_execution": "interpreter",
                "script_running": "interpreter",
                "system_management": "interpreter",
                "package_installation": "interpreter",

                # UI operations
                "screenshot": "str_replace_editor", # Use API-required name
                "mouse_control": "str_replace_editor", # Use API-required name
                "keyboard_control": "str_replace_editor", # Use API-required name
                "windows_ui": "str_replace_editor" # Use API-required name
            }

    # --- Methods of Profile class ---
    def to_dict(self):
        """Convert settings to dictionary for serialization"""
        return {
            key: value
            for key, value in vars(self).items()
            if not key.startswith("_")  # Skip private attributes
        }

    def from_dict(self, data):
        """Update settings from dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self

    def save(self, path=None):
        """Save current settings to a profile file"""
        path = os.path.expanduser(path or self.profile_path)
        if not path.endswith(".py"):
            path += ".py"
        os.makedirs(os.path.dirname(path), exist_ok=True)

        if os.path.exists(path):
            print(f"\n\033[38;5;240mThis will overwrite:\033[0m {path}")
            confirmation = input("\nAre you sure? (y/n): ").lower().strip()
            if confirmation != "y":
                print("Save cancelled")
                return

        # Get default values to compare against
        default_profile = Profile()

        with open(path, "w") as f:
            f.write("from interpreter import interpreter\n\n")

            # Compare each attribute with default and write if different
            for key, value in self.to_dict().items():
                if key == "messages":
                    continue

                # Check if the attribute exists on the default profile before comparing
                if hasattr(default_profile, key) and value != getattr(default_profile, key):
                    if isinstance(value, str):
                        # Use repr for strings to handle quotes and escapes correctly
                        f.write(f"interpreter.{key} = {repr(value)}\n")
                    elif isinstance(value, list):
                        f.write(f"interpreter.{key} = {repr(value)}\n")
                    else:
                        f.write(f"interpreter.{key} = {repr(value)}\n")
                # Handle attributes not present in default (like nested config objects)
                elif not hasattr(default_profile, key):
                     # We might not want to save the nested config objects themselves directly
                     # This part might need refinement depending on how saving/loading is intended
                     pass


        print(f"Profile saved to {path}")

    def load(self, path):
        """Load settings from a profile file if it exists"""
        path = os.path.expanduser(path)
        if not path.endswith(".py"):
            path += ".py"

        if not os.path.exists(path):
            # If file doesn't exist, if it's the default, that's fine
            if os.path.abspath(os.path.expanduser(path)) == os.path.abspath(
                os.path.expanduser(self.__class__.Paths.DEFAULT_PROFILE_PATH)
            ):
                return
            raise FileNotFoundError(f"Profile file not found at {path}")

        # Create a temporary namespace to execute the profile in
        namespace = {}
        try:
            with open(path) as f:
                # Read the profile content
                content = f.read()

                # Replace the import with a dummy class definition
                # This avoids loading the full interpreter module which is resource intensive
                content = content.replace(
                    "from interpreter import interpreter",
                    "class Interpreter:\n    pass\ninterpreter = Interpreter()",
                )

                # Execute the modified profile content
                exec(content, namespace)

            # Extract settings from the interpreter object in the namespace
            if "interpreter" in namespace:
                # Iterate through attributes defined in the Profile class's __init__
                # This is safer than iterating through self.to_dict().keys() which might include dynamic attributes
                for key in self.__init__.__code__.co_varnames:
                     if key != 'self' and hasattr(namespace["interpreter"], key):
                         setattr(self, key, getattr(namespace["interpreter"], key))
            else:
                print("Failed to load profile, no interpreter object found")
        except Exception as e:
            raise ValueError(f"Failed to load profile at {path}. Error: {str(e)}")

    @classmethod
    def from_file(cls, path):
        """Create a new profile instance from a file"""
        profile = cls()
        profile.load(path)
        return profile
