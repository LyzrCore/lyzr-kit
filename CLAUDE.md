# CLAUDE.md

Guidance for Claude Code when working with this repository.

## Project Overview

lyzr-kit is a Python SDK for managing AI agents, tools, and features via the Lyzr platform.

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Agent** | AI entity (chat, qa) with model config |
| **Tool** | Capability agents can invoke |
| **Feature** | Behavioral modifier (context, guard, policy) |

## CLI Commands

```bash
lk auth                  # Save API key to .env
lk <resource> <action> [id]
```

| Resource | Short | Actions |
|----------|-------|---------|
| `agent` | `a` | `ls`, `get`, `set` |
| `tool` | `t` | `ls`, `get`, `set` |
| `feature` | `f` | `ls`, `get`, `set` |

## Storage

| Directory | Purpose |
|-----------|---------|
| `.lyzr-kit/` | Built-in resources (SDK-provided) |
| `local-kit/` | Cloned resources (via `lk get`) |

## File Paths

```
.lyzr-kit/agents/<id>.yaml      # Built-in agent
local-kit/agents/<id>.yaml      # Cloned agent
local-kit/tools/<id>.yaml       # Cloned tool
local-kit/features/<id>.yaml    # Cloned feature
```

## Project Structure (Target)

```
src/lyzr_kit/
├── __init__.py
├── cli/                 # Click commands
│   ├── main.py         # Entry point (lk)
│   ├── agent.py        # lk agent commands
│   ├── tool.py         # lk tool commands
│   └── feature.py      # lk feature commands
├── agents/
│   └── schema.py       # Agent Pydantic model
├── tools/
│   └── schema.py       # Tool Pydantic model
├── features/
│   └── schema.py       # Feature Pydantic model
└── core/
    ├── loader.py       # SchemaLoader with legacy patterns
    └── storage.py      # Storage path management
```

## Build Commands

```bash
pip install -e .        # Install in dev mode
pytest                  # Run tests
lk --help              # CLI help
```

## Implementation Phases

| Phase | Focus |
|-------|-------|
| 1 | Agents (basic), CLI, storage |
| 2 | Schema evolution |
| 3 | Tools |
| 4 | Features |

## Specs

See `specs/` for detailed specifications:
- `specs/concepts/` - Entity definitions (agent, tool, feature)
- `specs/implementation/` - Technical details (commands, storage, schema)
- `specs/phases/` - Implementation roadmap
