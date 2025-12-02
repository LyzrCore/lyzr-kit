"""Agent commands for lyzr-kit."""

import typer
from rich.console import Console
from rich.table import Table

from lyzr_kit.modules.storage.manager import StorageManager
from lyzr_kit.utils.auth import STUDIO_BASE_URL, AuthConfig, AuthError, load_auth, validate_auth
from lyzr_kit.utils.platform import PlatformClient, PlatformError

app = typer.Typer(no_args_is_help=True)
console = Console()


def _require_auth() -> AuthConfig:
    """Check authentication before running commands.

    Returns:
        AuthConfig if authentication is valid.

    Raises:
        typer.Exit: If authentication fails.
    """
    try:
        auth = load_auth()
        validate_auth(auth)
        return auth
    except AuthError as e:
        console.print(f"[red]Authentication Error:[/red]\n{e}")
        raise typer.Exit(1) from None


@app.command("ls")
@app.command("list", hidden=True)
def list_agents() -> None:
    """List all agents (built-in + cloned)."""
    storage = StorageManager()
    agents = storage.list_agents()

    if not agents:
        console.print("[yellow]No agents found[/yellow]")
        return

    table = Table(title="Agents")
    table.add_column("ID", style="cyan")
    table.add_column("NAME", style="white")
    table.add_column("CATEGORY", style="magenta")
    table.add_column("ACTIVE", style="green")
    table.add_column("ENDPOINT", style="dim")

    for agent in agents:
        endpoint_display = "-"
        if agent.endpoint:
            endpoint_display = (
                agent.endpoint[:40] + "..." if len(agent.endpoint) > 40 else agent.endpoint
            )
        table.add_row(
            agent.id,
            agent.name,
            agent.category,
            "Yes" if agent.is_active else "No",
            endpoint_display,
        )

    console.print(table)


@app.command("get")
def get_agent(agent_id: str) -> None:
    """Clone agent to local-kit/agents/<id>.yaml and create on platform."""
    # Require authentication for get command
    auth = _require_auth()

    storage = StorageManager()

    # Check if already exists in local
    if storage.agent_exists_local(agent_id):
        console.print(f"[red]Error: Agent '{agent_id}' already exists in local-kit[/red]")
        console.print("[dim]Use 'lk agent set' to update[/dim]")
        raise typer.Exit(1)

    # Get agent from built-in or error
    agent = storage.get_agent(agent_id)
    if not agent:
        console.print(f"[red]Error: Agent '{agent_id}' not found[/red]")
        console.print("[dim]Run 'lk agent ls' to see available agents[/dim]")
        raise typer.Exit(1)

    # Create agent on platform
    console.print("[dim]Creating agent on platform...[/dim]")
    try:
        platform = PlatformClient(auth)
        response = platform.create_agent(agent)

        # Update agent with platform details
        agent.is_active = True
        agent.endpoint = response.endpoint
        agent.platform_agent_id = response.agent_id
        agent.platform_env_id = response.env_id
        agent.marketplace_app_id = response.app_id

    except PlatformError as e:
        console.print(f"[red]Platform Error:[/red] {e}")
        raise typer.Exit(1) from None

    # Save to local
    path = storage.save_agent(agent)

    console.print(f"[green]Agent '{agent_id}' created successfully![/green]")
    console.print(f"[dim]Agent ID:[/dim] {response.agent_id}")
    console.print(f"[dim]Platform URL:[/dim] {response.platform_url}")
    if response.chat_url:
        console.print(f"[dim]Chat URL:[/dim] {response.chat_url}")
    console.print(f"[dim]API Endpoint:[/dim] {agent.endpoint}")
    console.print(f"[dim]Local config:[/dim] {path}")
    if response.app_id:
        console.print(f"[dim]Marketplace App:[/dim] {response.app_id}")


@app.command("set")
def set_agent(agent_id: str) -> None:
    """Update agent on platform from local-kit/agents/<id>.yaml."""
    # Require authentication for set command
    auth = _require_auth()

    storage = StorageManager()

    # Check if exists in local
    if not storage.agent_exists_local(agent_id):
        console.print(f"[red]Error: Agent '{agent_id}' not found in local-kit[/red]")
        console.print("[dim]Run 'lk agent get' first to clone the agent[/dim]")
        raise typer.Exit(1)

    # Load and validate
    agent = storage.get_agent(agent_id)
    if not agent:
        console.print(f"[red]Error: Failed to load agent '{agent_id}'[/red]")
        raise typer.Exit(1)

    # Check if agent has platform IDs
    if not agent.platform_agent_id or not agent.platform_env_id:
        console.print(f"[red]Error: Agent '{agent_id}' has no platform IDs[/red]")
        console.print("[dim]This agent may have been created before platform integration.[/dim]")
        console.print(
            "[dim]Delete local-kit/agents/{agent_id}.yaml and run 'lk agent get' again.[/dim]"
        )
        raise typer.Exit(1)

    # Update agent on platform
    console.print("[dim]Updating agent on platform...[/dim]")
    try:
        platform = PlatformClient(auth)
        response = platform.update_agent(
            agent=agent,
            agent_id=agent.platform_agent_id,
            env_id=agent.platform_env_id,
        )

        # Update endpoint (in case it changed)
        agent.endpoint = response.endpoint

    except PlatformError as e:
        console.print(f"[red]Platform Error:[/red] {e}")
        raise typer.Exit(1) from None

    # Save updated agent
    path = storage.save_agent(agent)

    console.print(f"[green]Agent '{agent_id}' updated successfully![/green]")
    console.print(f"[dim]Agent ID:[/dim] {response.agent_id}")
    console.print(f"[dim]Platform URL:[/dim] {response.platform_url}")
    # Use stored marketplace_app_id for chat URL
    if agent.marketplace_app_id:
        chat_url = f"{STUDIO_BASE_URL}/agent/{agent.marketplace_app_id}/"
        console.print(f"[dim]Chat URL:[/dim] {chat_url}")
    console.print(f"[dim]API Endpoint:[/dim] {agent.endpoint}")
    console.print(f"[dim]Local config:[/dim] {path}")
