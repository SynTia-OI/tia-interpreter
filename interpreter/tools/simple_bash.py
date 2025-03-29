import asyncio
import os
from typing import ClassVar, Literal, Any # Added Any

from anthropic.types.beta import BetaToolBash20241022Param

from .base import BaseAnthropicTool, CLIResult, ToolError, ToolResult

# print("Using simple bash tool")


class BashTool(BaseAnthropicTool):
    """A tool that executes bash commands and returns their output."""

    name: ClassVar[Literal["bash"]] = "bash"
    api_type: ClassVar[Literal["bash_20250124"]] = "bash_20250124" # Updated identifier
    interpreter: Any # Add interpreter reference

    def __init__(self, interpreter: Any): # Accept interpreter instance
        self.interpreter = interpreter
        super().__init__()

    async def __call__(
        self, command: str | None = None, restart: bool = False, **kwargs
    ):
        if restart: # Simple bash doesn't maintain session, so restart is a no-op conceptually
             return ToolResult(system="Simple bash tool does not maintain state; restart ignored.")

        if not command:
            raise ToolError("no command provided")

        # Check if command is allowed
        if command not in self.interpreter.allowed_commands:
            return ToolResult(error=f"Command '{command}' is not in allowed_commands.")

        try:
            # Set up non-interactive environment
            env = os.environ.copy()
            env.update(
                {
                    "DEBIAN_FRONTEND": "noninteractive",  # Prevents apt from prompting
                    "NONINTERACTIVE": "1",  # Generic non-interactive flag
                }
            )

            # Create process with shell=True and stdin set to DEVNULL
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                stdin=asyncio.subprocess.DEVNULL,  # Explicitly disable stdin
                env=env,
            )

            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(), timeout=300
                )

                # Decode and combine output
                output = stdout.decode() + stderr.decode()

                # Print output
                print(output, end="", flush=True)

                # Return combined output
                return CLIResult(output=output if output else "<No output>")

            except asyncio.TimeoutError:
                process.kill()
                msg = "Command timed out after 5 minutes"
                print(msg)
                return ToolResult(error=msg)

        except Exception as e:
            msg = f"Failed to run command: {str(e)}"
            print(msg)
            return ToolResult(error=msg)

    def to_params(self) -> BetaToolBash20241022Param:
        return {
            "type": self.api_type,
            "name": self.name,
        }
