# Storage Specification

## Overview

Lyzr Kit uses a two-directory storage system:

| Directory | Purpose | Contents |
|-----------|---------|----------|
| `.lyzr-kit/` | Built-in resources | SDK-provided agents, tools, features |
| `local-kit/` | Cloned resources | User resources created via `lk get` |

## Directory Structure

```
.lyzr-kit/                   # Built-in resources (SDK-provided)
├── agents/
│   ├── chat-agent.yaml
│   └── qa-agent.yaml
├── tools/
│   ├── file_reader.yaml
│   └── calculator.yaml
└── features/
    ├── memory.yaml
    └── pii_detector.yaml

local-kit/                   # Cloned resources (via `lk get`)
├── agents/<id>.yaml
├── tools/<id>.yaml
└── features/<id>.yaml

.env                         # API keys and secrets
```

## Resource Paths

| Resource | Built-in Path | Cloned Path |
|----------|---------------|-------------|
| Agent | `.lyzr-kit/agents/<id>.yaml` | `local-kit/agents/<id>.yaml` |
| Tool | `.lyzr-kit/tools/<id>.yaml` | `local-kit/tools/<id>.yaml` |
| Feature | `.lyzr-kit/features/<id>.yaml` | `local-kit/features/<id>.yaml` |

## File Formats

| File | Format | Description |
|------|--------|-------------|
| `agent.yaml` | YAML | Agent definition |
| `tool.yaml` | YAML | Tool definition |
| `feature.yaml` | YAML | Feature definition |
| `.env` | dotenv | API keys and secrets |

## Security

| Aspect | Implementation |
|--------|----------------|
| Secrets | Loaded from `.env` file, never written to YAML |
| Directory permissions | `0700` (owner only) |
| File permissions | `0600` (owner only) |

## Design Principles

1. **Two-Directory Split**: Built-in (`.lyzr-kit/`) vs cloned (`local-kit/`)
2. **Human-Readable**: YAML config files are easy to edit
3. **Secure**: Sensitive data via env vars, restricted permissions
4. **Minimal**: Only store what's needed, use defaults
