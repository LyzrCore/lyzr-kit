# Lyzr Kit

A Python SDK for building and deploying AI agents locally, powered by the Lyzr platform.

## Overview

Lyzr Kit (`lyzr-kit`) is a unified SDK that provides:

- **Agent Management**: Create, configure, and run AI agents locally
- **Tool System**: Extensible tools that agents can use
- **Feature System**: Context, guards, and policies for agent behavior
- **CLI**: Command-line interface (`lk`) for all operations
- **Platform Integration**: Seamless connection to Lyzr's backend for LLM access

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Agent** | An AI entity that can process prompts and generate responses |
| **Tool** | A capability that agents can invoke (e.g., file_reader, calculator) |
| **Feature** | Behavioral modifiers: context (RAG), guards (validation), policies (rate limits) |
| **Schema** | YAML definitions for agents, tools, and features |

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      Lyzr Kit SDK                        │
│  ┌─────────────────────────────────────────────────┐    │
│  │     CLI (lk)          │      SDK (lyzr_kit)     │    │
│  │  Thin wrapper         │   Core business logic   │    │
│  └─────────────────────────────────────────────────┘    │
│                          │                               │
│                          ▼                               │
│  ┌─────────────────────────────────────────────────┐    │
│  │              Platform Client                     │    │
│  │   HTTP client for agent.api.lyzr.app            │    │
│  └─────────────────────────────────────────────────┘    │
│                          │                               │
└──────────────────────────┼───────────────────────────────┘
                           │ HTTPS
                           ▼
┌─────────────────────────────────────────────────────────┐
│              Lyzr Platform Backend                       │
│   Providers: OpenAI, Anthropic, Bedrock, HuggingFace    │
└─────────────────────────────────────────────────────────┘
```

## Quick Start

### Installation

```bash
pip install lyzr-kit
```

### CLI Usage

```bash
# Configure API key
lk config set api_key your-lyzr-api-key

# List agents
lk agent ls

# Run an agent
lk run my-agent "Hello, how are you?"

# List tools
lk tool ls
```

### SDK Usage

```python
from lyzr_kit import AgentManager
from lyzr_kit.platform import PlatformClient

# Initialize
client = PlatformClient(api_key="your-api-key")
manager = AgentManager(client=client)

# Create and run an agent
agent = await manager.create(
    agent_type="chat",
    name="my-assistant",
    config={
        "provider_id": "openai",
        "model": "gpt-4",
        "system_prompt": "You are a helpful assistant."
    }
)

response = await agent.run("Hello!")
print(response.content)
```

## Documentation

See the [specs/](specs/) directory for detailed specifications:

- [Concepts](specs/concepts/) - Core entity definitions
- [Implementation](specs/implementation/) - Technical design
- [Phases](specs/phases/) - Implementation roadmap

## License

MIT
