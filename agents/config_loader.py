"""Loads config.yaml once and exposes it as a plain dict to the rest of the
system. Keeping this in one place means every agent reads the exact same
governance rules, model assignments, and integration settings.
"""
from __future__ import annotations

import functools
import os
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = REPO_ROOT / "config.yaml"


@functools.lru_cache(maxsize=1)
def load_config() -> dict:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def env(name: str, default: str | None = None) -> str | None:
    """Thin wrapper so agent modules don't import os directly everywhere."""
    return os.environ.get(name, default)
