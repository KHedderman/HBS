"""Loads config.yaml once and exposes it as a plain dict to the rest of the
system. Keeping this in one place means every agent reads the exact same
governance rules, model assignments, and integration settings.
"""
from __future__ import annotations

import functools
import os
from pathlib import Path

import yaml
from pydantic import ValidationError

from agents.schemas import AppConfig

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = REPO_ROOT / "config.yaml"


@functools.lru_cache(maxsize=1)
def load_config() -> dict:
    """Parses config.yaml and validates its structure against AppConfig
    before returning it. Still returns the plain dict (not the validated
    model) so every existing `cfg["agents"]["directors"]`-style call site
    keeps working unchanged — validation is a fail-fast gate, not a new
    access pattern to migrate to.
    """
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    try:
        AppConfig.model_validate(raw)
    except ValidationError as exc:
        raise ValueError(
            f"config.yaml failed schema validation — see agents/schemas.py:AppConfig:\n{exc}"
        ) from exc

    return raw


def env(name: str, default: str | None = None) -> str | None:
    """Thin wrapper so agent modules don't import os directly everywhere."""
    return os.environ.get(name, default)
