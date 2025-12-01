# Lyzr Kit

A Python SDK for managing AI agents, tools, and features via the Lyzr platform.

## Overview

Lyzr Kit (`lyzr-kit`) provides built-in definitions and lifecycle management for AI resources:

| Resource | Description |
|----------|-------------|
| **Agent** | AI entity that processes prompts and generates responses |
| **Tool** | Capability that agents can invoke (file_reader, calculator) |
| **Feature** | Behavioral modifier: context, guards, policies |

## Installation

```bash
pip install lyzr-kit
```

## CLI (`lk`)

### Auth

```bash
lk auth                    # Save API key to .env
```

### Commands

```bash
lk <resource> <action> [id]
```

| Resource | Short | Actions |
|----------|-------|---------|
| `agent` | `a` | `ls`, `get`, `set` |
| `tool` | `t` | `ls`, `get`, `set` |
| `feature` | `f` | `ls`, `get`, `set` |

### Examples

```bash
# List agents
lk a ls

# Clone and activate an agent
lk a get chat-agent

# Update agent from YAML
lk a set my-agent
```

## Storage

| Directory | Purpose |
|-----------|---------|
| `.lyzr-kit/` | Built-in resources (SDK-provided) |
| `local-kit/` | Cloned resources (via `lk get`) |

## Documentation

See [specs/](specs/) for detailed specifications.

## License

MIT
