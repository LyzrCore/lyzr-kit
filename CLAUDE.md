# CLAUDE.md

Guidance for Claude Code when working with this repository.

## Project Overview

lyzr-kit is a Python SDK for managing AI agents, tools, and features via the Lyzr platform.

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Agent** | AI entity (chat, qa) with model config |
| **Tool** | Capability agents can invoke (Phase 3) |
| **Feature** | Behavioral modifier (Phase 4) |

## CLI Commands

```bash
lk auth                  # Save API key to .env
lk <resource> <action> [id]
```

| Resource | Short | Actions |
|----------|-------|---------|
| `agent` | `a` | `ls`, `get`, `set` |
| `tool` | `t` | `ls`, `get`, `set` (stub) |
| `feature` | `f` | `ls`, `get`, `set` (stub) |

## Storage

| Location | Purpose |
|----------|---------|
| `src/lyzr_kit/collection/` | Built-in resources (bundled with package) |
| `local-kit/` | Cloned resources (via `lk get`) |

## File Paths

```
src/lyzr_kit/collection/agents/<id>.yaml   # Built-in agent
local-kit/agents/<id>.yaml                 # Cloned agent
local-kit/tools/<id>.yaml                  # Cloned tool
local-kit/features/<id>.yaml               # Cloned feature
```

## Project Structure

```
src/lyzr_kit/
├── __init__.py
├── schemas/             # Pydantic models
│   ├── agent.py        # Agent schema (full)
│   ├── tool.py         # Tool schema (stub)
│   └── feature.py      # Feature schema (stub)
├── collection/          # Built-in resources
│   ├── agents/         # chat-agent.yaml, qa-agent.yaml
│   ├── tools/          # (empty, Phase 3)
│   └── features/       # (empty, Phase 4)
├── modules/
│   ├── cli/
│   │   └── main.py     # Typer app entry point
│   ├── commands/       # CLI command implementations
│   │   ├── agent.py    # ls, get, set
│   │   ├── tool.py     # stub
│   │   ├── feature.py  # stub
│   │   └── auth.py     # API key management
│   └── storage/
│       └── manager.py  # StorageManager class
└── utils/              # Shared utilities

tests/
├── conftest.py         # Shared fixtures (temp_workdir)
└── unit/
    └── commands/       # CLI command unit tests
        ├── test_agent.py
        ├── test_tool.py
        ├── test_feature.py
        └── test_auth.py
```

## Build Commands

```bash
pip install -e .        # Install in dev mode
pytest tests/ -v        # Run tests
lk --help              # CLI help
```

## Implementation Phases

| Phase | Focus | Status |
|-------|-------|--------|
| 1 | Agents (basic), CLI, storage | ✅ Done |
| 2 | Schema evolution | Pending |
| 3 | Tools | Stub |
| 4 | Features | Stub |

## Specs

See `specs/` for detailed specifications:
- `specs/concepts/` - Entity definitions (agent, tool, feature)
- `specs/implementation/` - Technical details (commands, storage, schema)
- `specs/phases/` - Implementation roadmap
