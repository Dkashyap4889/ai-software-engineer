import subprocess
from pathlib import Path


class CommandRunner:

    def run(
        self,
        command: list[str],
        cwd: str | Path,
        timeout: int = 120
    ):
        try:
            result = subprocess.run(
                command,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=timeout
            )

            return {
                "command": command,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0
            }

        except subprocess.TimeoutExpired as e:
            return {
                "command": command,
                "returncode": -1,
                "stdout": e.stdout or "",
                "stderr": "Command timed out",
                "success": False
            }