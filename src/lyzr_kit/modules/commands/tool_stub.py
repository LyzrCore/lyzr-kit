"""Tool CLI commands.

STUB: Tool commands will be fully implemented in Phase 3.
Currently, all commands return a placeholder message.
See specs/phases/phase-3.md for details.
"""

import typer
from rich.console import Console

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.command("ls")
def list_tools() -> None:
    """List all tools (built-in + cloned)."""
    console.print("[yellow]Not implemented (Phase 3)[/yellow]")


@app.command("get")
def get_tool(tool_id: str) -> None:
    """Clone tool to local-kit/tools/<id>.yaml."""
    console.print("[yellow]Not implemented (Phase 3)[/yellow]")


@app.command("set")
def set_tool(tool_id: str) -> None:
    """Update tool from local-kit/tools/<id>.yaml."""
    console.print("[yellow]Not implemented (Phase 3)[/yellow]")
