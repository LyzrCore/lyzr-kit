# Lyzr Kit Specifications

This directory contains the design specifications for the Lyzr Kit SDK.

## Structure

```
specs/
├── concepts/                 # Core entity definitions
│   ├── agent.md             # Agent entity + schema
│   ├── tool.md              # Tool entity + schema
│   └── feature.md           # Feature entity + schema
│
├── implementation/          # Technical implementation details
│   ├── commands.md          # CLI command specification
│   ├── storage.md           # Local storage structure
│   └── schema.md            # Schema evolution & migrations
│
└── phases/                  # Implementation roadmap
    ├── phase-1-foundation.md   # Agents (without tools/features), CLI, storage
    ├── phase-2-agents.md       # Schema evolution
    ├── phase-3-tools.md        # Tools system
    └── phase-4-features.md     # Features system
```

## Reading Order

### For Understanding the Product

1. Start with [concepts/agent.md](concepts/agent.md) - the core entity
2. Read [concepts/tool.md](concepts/tool.md) - agent capabilities
3. Read [concepts/feature.md](concepts/feature.md) - behavioral modifiers

### For Implementation

1. Review [implementation/commands.md](implementation/commands.md) - CLI commands
2. Review [implementation/storage.md](implementation/storage.md) - local storage
3. Review [implementation/schema.md](implementation/schema.md) - schema evolution
4. Follow [phases/](phases/) for implementation order

## Key Decisions

| Decision | Choice |
|----------|--------|
| Package name | `lyzr-kit` |
| CLI command | `lk` |
| Config format | YAML |
| Scope | Built-in definitions + lifecycle management |
| Schema validation | Pydantic models |
| Schema evolution | Structural detection, in-memory migration |

## Storage

| Directory | Purpose |
|-----------|---------|
| `.lyzr-kit/` | Built-in resources (SDK-provided) |
| `local-kit/` | Cloned resources (via `lk get`) |

## Phases

| Phase | Focus |
|-------|-------|
| Phase 1 | Agents (basic), CLI commands, storage |
| Phase 2 | Schema evolution |
| Phase 3 | Tools |
| Phase 4 | Features |
