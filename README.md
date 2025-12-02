# Lyzr Kit

A Python SDK for managing AI agents via the Lyzr platform.

## Installation

```bash
pip install lyzr-kit
```

## Quick Start

### 1. Authenticate

```bash
lk auth
```

Enter your Lyzr API key when prompted. Get your API key from [Lyzr Studio](https://studio.lyzr.ai).

### 2. List Available Agents

```bash
lk agent ls
```

### 3. Deploy an Agent

```bash
lk agent get chat-agent
```

This will:
- Create the agent on the Lyzr platform
- Save the configuration to `local-kit/agents/chat-agent.yaml`
- Output URLs for the Platform, Chat interface, and API endpoint

### 4. Modify and Update

Edit `local-kit/agents/chat-agent.yaml`, then:

```bash
lk agent set chat-agent
```

## CLI Reference

```bash
lk auth                    # Save API key to .env
lk agent ls                # List all agents
lk agent get <id>          # Deploy agent to platform
lk agent set <id>          # Update agent on platform
```

Shorthand: `lk a ls`, `lk a get <id>`, `lk a set <id>`

## Built-in Agents

| ID | Name | Category |
|----|------|----------|
| `chat-agent` | Chat Assistant | chat |
| `qa-agent` | Q&A Agent | qa |
| `email-composer` | Email Composer | chat |
| `code-reviewer` | Code Reviewer | qa |
| `summarizer` | Text Summarizer | qa |
| `translator` | Language Translator | qa |
| `task-planner` | Task Planner | chat |
| `data-analyst` | Data Analyst | qa |
| `sql-expert` | SQL Expert | qa |
| `research-assistant` | Research Assistant | chat |
| `content-writer` | Content Writer | chat |
| `customer-support` | Customer Support Agent | chat |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `LYZR_API_KEY` | Yes | API key for Lyzr platform |
| `LYZR_USER_ID` | No | User ID for marketplace features |
| `LYZR_MEMBERSTACK_TOKEN` | No | Token for marketplace app creation |

## Storage

| Directory | Purpose |
|-----------|---------|
| `local-kit/agents/` | Your deployed agent configurations |
| `.env` | API credentials (created by `lk auth`) |

## Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run linter
ruff check src/

# Type check
mypy src/
```

## License

MIT
