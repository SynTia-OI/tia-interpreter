import os

from .base import CLIResult, ToolResult
from .collection import ToolCollection
from .computer import ComputerTool
from .edit import EditTool

# Use environment variable to choose bash tool, default to the more featured one
if os.environ.get("INTERPRETER_SIMPLE_BASH", "false").lower() == "true":
    from .simple_bash import BashTool
else:
    from .bash import BashTool # This is the one we modified

__ALL__ = [
    BashTool,
    CLIResult,
    ComputerTool,
    EditTool,
    ToolCollection,
    ToolResult,
]
