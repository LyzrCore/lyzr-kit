"""Unit tests for storage manager."""

from pathlib import Path

from lyzr_kit.modules.storage.manager import StorageManager
from lyzr_kit.schemas.agent import Agent


class TestStorageManagerLoadAgent:
    """Tests for StorageManager._load_agent method."""

    def test_load_agent_returns_none_for_invalid_yaml(self):
        """_load_agent should return None for invalid YAML."""
        storage = StorageManager()

        # Create invalid YAML file
        agents_dir = Path.cwd() / "local-kit" / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)
        invalid_file = agents_dir / "invalid-agent.yaml"
        invalid_file.write_text("invalid: yaml: content: [")

        # Should return None, not raise
        result = storage._load_agent(invalid_file)
        assert result is None

    def test_load_agent_returns_none_for_invalid_schema(self):
        """_load_agent should return None for valid YAML but invalid schema."""
        storage = StorageManager()

        # Create YAML with missing required fields
        agents_dir = Path.cwd() / "local-kit" / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)
        invalid_file = agents_dir / "bad-schema.yaml"
        invalid_file.write_text("some_field: value\n")

        # Should return None (validation fails)
        result = storage._load_agent(invalid_file)
        assert result is None


class TestStorageManagerSaveAgent:
    """Tests for StorageManager.save_agent method."""

    def test_save_agent_converts_datetime_to_iso(self):
        """save_agent should convert datetime fields to ISO format."""
        from datetime import datetime

        from lyzr_kit.schemas.agent import ModelConfig

        storage = StorageManager()

        agent = Agent(
            id="test-agent",
            name="Test Agent",
            category="chat",
            created_at=datetime(2024, 1, 15, 10, 30, 0),
            model=ModelConfig(provider="openai", name="gpt-4", credential_id="cred-1"),
        )

        path = storage.save_agent(agent)
        content = path.read_text()

        # Should contain ISO format datetime
        assert "2024-01-15" in content
        assert "10:30:00" in content
