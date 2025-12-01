# Lyzr Kit Specifications

Design specifications for the Lyzr Kit SDK.

## Structure

```
specs/
├── concepts/                    # Core entity definitions
│   ├── agent.md                # Agent entity + schema
│   ├── tool.md                 # Tool entity + schema
│   └── feature.md              # Feature entity + schema
│
├── implementation/             # Technical details
│   ├── commands.md             # CLI commands
│   ├── storage.md              # Storage structure
│   └── schema.md               # Schema evolution
│
└── phases/                     # Implementation roadmap
    ├── phase-1-foundation.md   # Agents, CLI, storage
    ├── phase-2-agents.md       # Schema evolution
    ├── phase-3-tools.md        # Tools system
    └── phase-4-features.md     # Features system
```

## Reading Order

**For Product Understanding:**
1. [concepts/agent.md](concepts/agent.md)
2. [concepts/tool.md](concepts/tool.md)
3. [concepts/feature.md](concepts/feature.md)

**For Implementation:**
1. [implementation/commands.md](implementation/commands.md)
2. [implementation/storage.md](implementation/storage.md)
3. [implementation/schema.md](implementation/schema.md)
4. [phases/](phases/)

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
| 1 | Agents (basic), CLI, storage |
| 2 | Schema evolution |
| 3 | Tools |
| 4 | Features |
