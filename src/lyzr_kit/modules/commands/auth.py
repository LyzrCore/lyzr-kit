"""Auth command for lyzr-kit."""

from pathlib import Path

import typer
from rich.console import Console

console = Console()

# Environment variable name for API key
ENV_VAR_NAME = "LYZR_API_KEY"


def auth() -> None:
    """Save Lyzr API key to .env file.

    The API key is used to authenticate with the Lyzr platform.
    Get your API key from https://agent.api.lyzr.app
    """
    console.print("\n[bold]Lyzr Authentication Setup[/bold]")
    console.print("[dim]Get your API key from https://agent.api.lyzr.app[/dim]\n")

    api_key = typer.prompt("Enter your Lyzr API key", hide_input=True)

    if not api_key or not api_key.strip():
        console.print("[red]Error: API key cannot be empty[/red]")
        raise typer.Exit(1)

    api_key = api_key.strip()

    env_path = Path(".env")

    # Read existing .env content
    existing_content = ""
    if env_path.exists():
        existing_content = env_path.read_text()

    # Update or add LYZR_API_KEY
    lines = existing_content.splitlines()
    updated = False
    new_lines = []

    for line in lines:
        if line.startswith(f"{ENV_VAR_NAME}="):
            new_lines.append(f"{ENV_VAR_NAME}={api_key}")
            updated = True
        else:
            new_lines.append(line)

    if not updated:
        new_lines.append(f"{ENV_VAR_NAME}={api_key}")

    env_path.write_text("\n".join(new_lines) + "\n")

    console.print(f"[green]✓ API key saved to .env as {ENV_VAR_NAME}[/green]")
    console.print("[dim]You can now use lk commands to manage agents.[/dim]")
