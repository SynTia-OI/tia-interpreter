import asyncio
import os
import shutil
import traceback
from typing import ClassVar, Literal, Any

import pyte
from anthropic.types.beta import BetaToolBash20241022Param

from .base import BaseAnthropicTool, CLIResult, ToolError, ToolResult


class _BashSession:
    """A session of a bash shell."""

    def __init__(self):
        self._started = False
        self._process = None
        self._sentinel = "<<exit>>"
        # Get terminal size, fallback to 80x24 if we can't
        terminal_size = shutil.get_terminal_size((80, 24))
        self._screen = pyte.Screen(terminal_size.columns, terminal_size.lines)
        self._stream = pyte.Stream(self._screen)

    async def start(self):
        if self._started:
            return

        # Explicitly use PowerShell on Windows
        shell = "powershell.exe -NoProfile -Command -" if os.name == "nt" else "/bin/bash"
        self._process = await asyncio.create_subprocess_shell(
            shell,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        self._started = True

    def stop(self):
        if not self._started:
            return
        if self._process and self._process.returncode is None:
            self._process.terminate()

    def _get_screen_text(self) -> str:
        """Get the current screen content as a string."""
        return "\n".join(line.rstrip() for line in self._screen.display).rstrip()

    async def run(self, command: str):
        """Execute a command in the shell."""
        if not self._started:
            raise ToolError("Session has not started.")
        if self._process.returncode is not None:
            return ToolResult(
                system="tool must be restarted",
                error=f"shell has exited with returncode {self._process.returncode}",
            )

        try:
            self._screen.reset()

            wrapped_command = f'{command}\n echo "{self._sentinel}"\n'
            self._process.stdin.write(wrapped_command.encode())
            await self._process.stdin.drain()

            while True:
                chunk = await self._process.stdout.read(1024)
                if not chunk:
                    break

                # Decode and handle sentinel
                decoded = chunk.decode(errors="replace")
                if self._sentinel in decoded:
                    # Print everything before the sentinel
                    print(decoded.split(self._sentinel)[0], end="", flush=True)
                else:
                    print(decoded, end="", flush=True)

                # Feed to terminal emulator for final state
                self._stream.feed(decoded)

                screen_text = self._get_screen_text()
                if self._sentinel in screen_text:
                    final_text = screen_text.split(self._sentinel)[0].rstrip()
                    return CLIResult(output=final_text if final_text else "<No output>")

            error = await self._process.stderr.read()
            if error:
                error_text = error.decode(errors="replace")
                print(error_text, end="", flush=True)
                self._stream.feed(error_text)

            final_output = self._get_screen_text()
            return CLIResult(output=final_output if final_output else "<No output>")

        except KeyboardInterrupt as e:
            self.stop()
            return CLIResult(output="Command cancelled by user.")
        except asyncio.CancelledError as e:
            self.stop()
            return CLIResult(output="Command cancelled by user.")
        except Exception as e:
            print("Unexpected error")
            traceback.print_exc()
            self.stop()
            return CLIResult(output=f"Command failed with error: {e}")


class BashTool(BaseAnthropicTool):
    """
    A tool that allows the agent to run bash commands.
    The tool parameters are defined by Anthropic and are not editable.
    """

    _session: _BashSession | None
    name: ClassVar[Literal["bash"]] = "bash"
    api_type: ClassVar[Literal["bash_20250124"]] = "bash_20250124" # Updated identifier
    interpreter: Any # Add interpreter reference

    def __init__(self, interpreter: Any): # Accept interpreter instance
        self.interpreter = interpreter
        self._session = None
        super().__init__()

    async def __call__(
        self, command: str | None = None, restart: bool = False, **kwargs
    ):
        if restart:
            if self._session:
                self._session.stop()
            self._session = _BashSession()
            await self._session.start()
            return ToolResult(system="tool has been restarted.")

        if self._session is None:
            self._session = _BashSession()
            await self._session.start()

        if command is not None:
            # Check if command is allowed - REMOVED FOR UNRESTRICTED ACCESS
            # if command not in self.interpreter.allowed_commands:
            #     return ToolResult(error=f"Command '{command}' is not in allowed_commands.")
            return await self._session.run(command)

        raise ToolError("no command provided.")

    def to_params(self) -> BetaToolBash20241022Param: # Note: Type hint might need update if Anthropic SDK changes param name
        return {
            "type": self.api_type,
            "name": self.name,
        }
