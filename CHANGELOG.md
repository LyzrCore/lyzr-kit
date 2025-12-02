# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2024-12-02

### Added
- Initial release of lyzr-kit SDK
- CLI tool (`lk`) for managing agents, tools, and features
- Agent management commands: `lk agent ls`, `lk agent get`, `lk agent set`
- Tool commands (stub): `lk tool ls`, `lk tool get`, `lk tool set`
- Feature commands (stub): `lk feature ls`, `lk feature get`, `lk feature set`
- Authentication command: `lk auth`
- Built-in agent collection: `chat-agent`, `qa-agent`
- Pydantic schemas for agent validation
- Storage manager for local-kit resources
- Full test suite with pytest

### Technical
- Python 3.10+ support
- src-layout package structure
- Typer CLI framework with Rich formatting
- YAML-based resource definitions
- uv package manager support

[Unreleased]: https://github.com/LyzrCore/lyzr-kit/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/LyzrCore/lyzr-kit/releases/tag/v0.1.0
