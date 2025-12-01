# CLI Commands Specification

## Overview

The `lk` CLI provides a simple interface for managing agents, tools, and features.

## Command Structure

```
lk <resource> <action> [id]
```

### Resources

| Resource | Short | Description |
|----------|-------|-------------|
| `agent` | `a` | Manage agents |
| `tool` | `t` | Manage tools |
| `feature` | `f` | Manage features |

### Actions

| Action | Description |
|--------|-------------|
| `ls` | List entities |
| `get` | Create/activate entity (requires unique ID) |
| `set` | Update entity from YAML definition |

## Resource Commands

| Command | Description | Output |
|---------|-------------|--------|
| `lk a ls` | List all agents (built-in + cloned) | Table: ID, NAME, CATEGORY, ACTIVE, ENDPOINT |
| `lk a get <id>` | Clone agent to `local-kit/agents/<id>.yaml` | Validates refs, creates on platform, fetches endpoint |
| `lk a set <id>` | Update agent from YAML | Reads from `local-kit/agents/<id>.yaml`, updates platform |
| `lk t ls` | List all tools (built-in + cloned) | Table: ID, NAME, ACTIVE, ENDPOINT |
| `lk t get <id>` | Clone tool to `local-kit/tools/<id>.yaml` | Creates on platform, fetches endpoint |
| `lk t set <id>` | Update tool from YAML | Reads from `local-kit/tools/<id>.yaml`, updates platform |
| `lk f ls` | List all features (built-in + cloned) | Table: ID, NAME, CATEGORY, ACTIVE, ENDPOINT |
| `lk f get <id>` | Clone feature to `local-kit/features/<id>.yaml` | Creates on platform, fetches endpoint |
| `lk f set <id>` | Update feature from YAML | Reads from `local-kit/features/<id>.yaml`, updates platform |

## Auth Command

| Command | Description | Output |
|---------|-------------|--------|
| `lk auth` | Save API key to `.env` | Prompts for key, saves as `LYZR_API_KEY` |

## Resource Meta

All resources have these meta fields (set by `get`):

| Field | Description |
|-------|-------------|
| `is_active` | Set to `true` by `get` |
| `endpoint` | Inference URL populated by `get` |

## `get` Process

1. Find resource in `.lyzr-kit/` (built-in) or validate new ID is unique
2. Validate references (tools, sub-agents, features, vars)
3. Create resource on Lyzr platform
4. Fetch inference endpoint
5. Clone YAML to `local-kit/<resources>/<id>.yaml` with `is_active: true` and `endpoint`

## `set` Process

1. Read updated YAML from `local-kit/<resources>/<id>.yaml`
2. Validate references
3. Update resource on platform
4. Refresh endpoint if needed

## Error Handling

| Code | Description |
|------|-------------|
| 0 | Success |
| 1 | General error |
| 2 | Invalid arguments |
| 3 | Configuration error |
| 4 | Network error |
| 5 | Authentication error |

### Common Errors

| Error | Hint |
|-------|------|
| Agent already exists | Use `lk agent set <id>` to update |
| Agent not found | Run `lk agent ls` to see available |
| Not authenticated | Run `lk auth` to save API key |

## Design Principles

1. **Simple**: Only 3 actions per resource (`ls`, `get`, `set`)
2. **Unique IDs**: `get` enforces unique IDs, errors if exists
3. **Platform-First**: `get` creates on platform and fetches endpoint
4. **YAML-Driven**: `set` reads from local YAML definition
5. **Validation Built-in**: References validated on `get` and `set`
