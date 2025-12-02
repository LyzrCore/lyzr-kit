"""Unit tests for agent CLI commands.

These tests verify CLI behavior and argument parsing.
For actual API integration tests, see tests/integration/test_agent_api.py
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from lyzr_kit.modules.cli.main import app
from lyzr_kit.utils.auth import AuthError

runner = CliRunner()


class TestAgentLs:
    """Tests for 'lk agent ls' command."""

    def test_ls_shows_builtin_agents(self):
        """ls should list built-in agents from collection."""
        result = runner.invoke(app, ["agent", "ls"])
        assert result.exit_code == 0
        assert "chat-agent" in result.output
        assert "qa-agent" in result.output

    def test_ls_shorthand(self):
        """'lk a ls' should work as shorthand."""
        result = runner.invoke(app, ["a", "ls"])
        assert result.exit_code == 0
        assert "chat-agent" in result.output

    def test_ls_shows_table_columns(self):
        """ls should display table with correct columns."""
        result = runner.invoke(app, ["agent", "ls"])
        assert result.exit_code == 0
        assert "ID" in result.output
        assert "NAME" in result.output
        assert "CATEGORY" in result.output
        assert "ACTIVE" in result.output

    @patch("lyzr_kit.modules.commands.agent.StorageManager")
    def test_ls_shows_no_agents_message(self, mock_storage_class):
        """ls should show message when no agents found."""
        mock_storage = MagicMock()
        mock_storage.list_agents.return_value = []
        mock_storage_class.return_value = mock_storage

        result = runner.invoke(app, ["agent", "ls"])
        assert result.exit_code == 0
        assert "No agents found" in result.output


class TestAgentHelp:
    """Tests for agent command help."""

    def test_agent_help(self):
        """agent --help should show available subcommands."""
        result = runner.invoke(app, ["agent", "--help"])
        assert result.exit_code == 0
        assert "ls" in result.output
        assert "get" in result.output
        assert "set" in result.output

    def test_agent_ls_help(self):
        """agent ls --help should show command description."""
        result = runner.invoke(app, ["agent", "ls", "--help"])
        assert result.exit_code == 0
        assert "List" in result.output or "list" in result.output

    def test_agent_get_help(self):
        """agent get --help should show command description."""
        result = runner.invoke(app, ["agent", "get", "--help"])
        assert result.exit_code == 0
        assert "AGENT_ID" in result.output

    def test_agent_set_help(self):
        """agent set --help should show command description."""
        result = runner.invoke(app, ["agent", "set", "--help"])
        assert result.exit_code == 0
        assert "AGENT_ID" in result.output


class TestAgentGetErrors:
    """Tests for error handling in 'lk agent get' command."""

    @patch("lyzr_kit.modules.commands.agent.load_auth")
    def test_get_fails_without_auth(self, mock_load_auth):
        """get should fail with auth error when no .env file."""
        mock_load_auth.side_effect = AuthError("Authentication required")

        result = runner.invoke(app, ["agent", "get", "chat-agent"])
        assert result.exit_code == 1
        assert "Authentication Error" in result.output

    @patch("lyzr_kit.modules.commands.agent.validate_auth")
    @patch("lyzr_kit.modules.commands.agent.load_auth")
    @patch("lyzr_kit.modules.commands.agent.PlatformClient")
    def test_get_fails_on_platform_error(
        self, mock_platform_class, mock_load_auth, mock_validate
    ):
        """get should show platform error message on API failure."""
        from lyzr_kit.utils.auth import AuthConfig
        from lyzr_kit.utils.platform import PlatformError

        mock_load_auth.return_value = AuthConfig(api_key="test-key")
        mock_validate.return_value = True

        mock_platform = MagicMock()
        mock_platform.create_agent.side_effect = PlatformError("API error")
        mock_platform_class.return_value = mock_platform

        result = runner.invoke(app, ["agent", "get", "chat-agent"])
        assert result.exit_code == 1
        assert "Platform Error" in result.output

    @patch("lyzr_kit.modules.commands.agent.validate_auth")
    @patch("lyzr_kit.modules.commands.agent.load_auth")
    @patch("lyzr_kit.modules.commands.agent.PlatformClient")
    def test_get_shows_marketplace_app_id(
        self, mock_platform_class, mock_load_auth, mock_validate
    ):
        """get should show marketplace app ID when available."""
        from lyzr_kit.utils.auth import AuthConfig
        from lyzr_kit.utils.platform import AgentResponse

        mock_load_auth.return_value = AuthConfig(api_key="test-key")
        mock_validate.return_value = True

        mock_platform = MagicMock()
        mock_platform.create_agent.return_value = AgentResponse(
            agent_id="agent-123",
            env_id="env-456",
            endpoint="https://api.example.com/chat/agent-123",
            platform_url="https://studio.lyzr.ai/agent-create/agent-123",
            chat_url="https://studio.lyzr.ai/agent/agent-123/",
            app_id="app-789",
        )
        mock_platform_class.return_value = mock_platform

        result = runner.invoke(app, ["agent", "get", "chat-agent"])
        assert result.exit_code == 0
        assert "Marketplace App:" in result.output
        assert "app-789" in result.output


class TestAgentSetErrors:
    """Tests for error handling in 'lk agent set' command."""

    @patch("lyzr_kit.modules.commands.agent.load_auth")
    def test_set_fails_without_auth(self, mock_load_auth):
        """set should fail with auth error when no .env file."""
        mock_load_auth.side_effect = AuthError("Authentication required")

        result = runner.invoke(app, ["agent", "set", "chat-agent"])
        assert result.exit_code == 1
        assert "Authentication Error" in result.output

    @patch("lyzr_kit.modules.commands.agent.validate_auth")
    @patch("lyzr_kit.modules.commands.agent.load_auth")
    @patch("lyzr_kit.modules.commands.agent.StorageManager")
    def test_set_fails_when_agent_load_fails(
        self, mock_storage_class, mock_load_auth, mock_validate
    ):
        """set should fail when agent cannot be loaded from local-kit."""
        from lyzr_kit.utils.auth import AuthConfig

        mock_load_auth.return_value = AuthConfig(api_key="test-key")
        mock_validate.return_value = True

        mock_storage = MagicMock()
        mock_storage.agent_exists_local.return_value = True
        mock_storage.get_agent.return_value = None  # Failed to load
        mock_storage_class.return_value = mock_storage

        result = runner.invoke(app, ["agent", "set", "broken-agent"])
        assert result.exit_code == 1
        assert "Failed to load agent" in result.output

    @patch("lyzr_kit.modules.commands.agent.validate_auth")
    @patch("lyzr_kit.modules.commands.agent.load_auth")
    @patch("lyzr_kit.modules.commands.agent.StorageManager")
    def test_set_fails_when_missing_platform_ids(
        self, mock_storage_class, mock_load_auth, mock_validate
    ):
        """set should fail when agent has no platform IDs."""
        from lyzr_kit.utils.auth import AuthConfig

        mock_load_auth.return_value = AuthConfig(api_key="test-key")
        mock_validate.return_value = True

        # Create mock agent without platform IDs
        mock_agent = MagicMock()
        mock_agent.platform_agent_id = None
        mock_agent.platform_env_id = None

        mock_storage = MagicMock()
        mock_storage.agent_exists_local.return_value = True
        mock_storage.get_agent.return_value = mock_agent
        mock_storage_class.return_value = mock_storage

        result = runner.invoke(app, ["agent", "set", "old-agent"])
        assert result.exit_code == 1
        assert "no platform IDs" in result.output

    @patch("lyzr_kit.modules.commands.agent.validate_auth")
    @patch("lyzr_kit.modules.commands.agent.load_auth")
    @patch("lyzr_kit.modules.commands.agent.StorageManager")
    @patch("lyzr_kit.modules.commands.agent.PlatformClient")
    def test_set_fails_on_platform_error(
        self, mock_platform_class, mock_storage_class, mock_load_auth, mock_validate
    ):
        """set should show platform error message on API failure."""
        from lyzr_kit.utils.auth import AuthConfig
        from lyzr_kit.utils.platform import PlatformError

        mock_load_auth.return_value = AuthConfig(api_key="test-key")
        mock_validate.return_value = True

        # Create mock agent with platform IDs
        mock_agent = MagicMock()
        mock_agent.platform_agent_id = "agent-123"
        mock_agent.platform_env_id = "env-456"

        mock_storage = MagicMock()
        mock_storage.agent_exists_local.return_value = True
        mock_storage.get_agent.return_value = mock_agent
        mock_storage_class.return_value = mock_storage

        mock_platform = MagicMock()
        mock_platform.update_agent.side_effect = PlatformError("API error")
        mock_platform_class.return_value = mock_platform

        result = runner.invoke(app, ["agent", "set", "my-agent"])
        assert result.exit_code == 1
        assert "Platform Error" in result.output
