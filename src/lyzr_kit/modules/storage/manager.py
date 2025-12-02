"""Storage manager for lyzr-kit resources."""

from pathlib import Path

import yaml

from lyzr_kit.schemas.agent import Agent

# Built-in resources bundled with the package
COLLECTION_DIR = Path(__file__).parent.parent.parent / "collection"


class StorageManager:
    """Manages storage for agents, tools, and features."""

    def __init__(
        self,
        builtin_path: str | Path | None = None,
        local_path: str | Path = "local-kit",
    ) -> None:
        self.builtin_path = Path(builtin_path) if builtin_path else COLLECTION_DIR
        self.local_path = Path(local_path)

    def _ensure_local_dir(self, resource_type: str) -> Path:
        """Ensure local directory exists for resource type."""
        path = self.local_path / resource_type
        path.mkdir(parents=True, exist_ok=True)
        return path

    def _list_yaml_files(self, directory: Path) -> list[Path]:
        """List all YAML files in a directory."""
        if not directory.exists():
            return []
        return list(directory.glob("*.yaml"))

    # Agent operations

    def list_agents(self) -> list[Agent]:
        """List all agents from built-in and local directories."""
        agents = []

        # Built-in agents
        builtin_dir = self.builtin_path / "agents"
        for yaml_file in self._list_yaml_files(builtin_dir):
            agent = self._load_agent(yaml_file)
            if agent:
                agents.append(agent)

        # Local agents
        local_dir = self.local_path / "agents"
        for yaml_file in self._list_yaml_files(local_dir):
            agent = self._load_agent(yaml_file)
            if agent:
                agents.append(agent)

        return agents

    def get_agent(self, agent_id: str) -> Agent | None:
        """Get an agent by ID from local or built-in directory."""
        # Check local first
        local_file = self.local_path / "agents" / f"{agent_id}.yaml"
        if local_file.exists():
            return self._load_agent(local_file)

        # Check built-in
        builtin_file = self.builtin_path / "agents" / f"{agent_id}.yaml"
        if builtin_file.exists():
            return self._load_agent(builtin_file)

        return None

    def save_agent(self, agent: Agent) -> Path:
        """Save an agent to local directory."""
        self._ensure_local_dir("agents")
        path = self.local_path / "agents" / f"{agent.id}.yaml"

        data = agent.model_dump(exclude_none=True, exclude_unset=False)
        # Convert datetime to ISO format string
        for key in ["created_at", "updated_at"]:
            if key in data and data[key] is not None:
                data[key] = data[key].isoformat()

        with open(path, "w") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)

        return path

    def agent_exists_local(self, agent_id: str) -> bool:
        """Check if agent exists in local directory."""
        return (self.local_path / "agents" / f"{agent_id}.yaml").exists()

    def _load_agent(self, path: Path) -> Agent | None:
        """Load an agent from a YAML file."""
        try:
            with open(path) as f:
                data = yaml.safe_load(f)
            return Agent.model_validate(data)
        except Exception:
            return None
