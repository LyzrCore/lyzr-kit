"""Pytest configuration and shared fixtures."""

import os
import shutil
from pathlib import Path

import pytest

SANDBOX_DIR = Path(__file__).parent / "sandbox"
ENV_EXAMPLE = SANDBOX_DIR / ".env.example"
ENV_FILE = SANDBOX_DIR / ".env"


def _clean_sandbox():
    """Remove all files from sandbox except .gitignore, .gitkeep, and .env.example."""
    if SANDBOX_DIR.exists():
        for item in SANDBOX_DIR.iterdir():
            if item.name not in (".gitignore", ".gitkeep", ".env.example"):
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()


def _ensure_env_file():
    """Create .env from .env.example if it doesn't exist."""
    if not ENV_FILE.exists() and ENV_EXAMPLE.exists():
        shutil.copy(ENV_EXAMPLE, ENV_FILE)


@pytest.fixture(autouse=True)
def setup_sandbox():
    """Clean sandbox, ensure .env exists, and cd into it before each test."""
    _clean_sandbox()
    SANDBOX_DIR.mkdir(exist_ok=True)
    _ensure_env_file()
    os.chdir(SANDBOX_DIR)
    yield
