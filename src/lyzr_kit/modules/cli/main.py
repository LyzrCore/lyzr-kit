"""Main CLI entry point for lyzr-kit."""

import typer

from lyzr_kit.modules.commands import agent, auth
from lyzr_kit.modules.commands import feature_stub as feature
from lyzr_kit.modules.commands import tool_stub as tool

app = typer.Typer(
    name="lk",
    help="Lyzr Kit - Manage AI agents, tools, and features",
    no_args_is_help=True,
)

# Register subcommands
app.add_typer(agent.app, name="agent", help="Manage agents")
app.add_typer(agent.app, name="a", hidden=True)  # Shorthand

app.add_typer(tool.app, name="tool", help="Manage tools")
app.add_typer(tool.app, name="t", hidden=True)  # Shorthand

app.add_typer(feature.app, name="feature", help="Manage features")
app.add_typer(feature.app, name="f", hidden=True)  # Shorthand

app.command(name="auth")(auth.auth)


if __name__ == "__main__":
    app()
