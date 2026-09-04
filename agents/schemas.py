"""Typed data contracts for everything this system reads or writes as JSON —
the JSONL logs and `config.yaml`.

Every schema here mirrors a shape that was already *documented* in prose
somewhere else (`memory/schema.md`, `metrics/README.md`, `agents/hitl.py`'s
docstrings) but never actually enforced. These models close that gap: a
malformed write now fails loudly, at write time, instead of silently
corrupting a log that `recall()` or `governance_digest()` reads later.

Deliberately scoped: these validate the fields the rest of the codebase
actually reads, not every optional field `config.yaml` happens to carry
(namesake prose, expansion notes, etc.) — `model_config = ConfigDict(extra="allow")`
on the config models means real, already-present extra fields pass through
untouched rather than getting rejected by an overfit schema.
"""
from __future__ import annotations

import re

from pydantic import BaseModel, ConfigDict, Field, field_validator

_MODEL_REF_RE = re.compile(r"^[a-z_]+\.[a-z_]+$")


# ---------------------------------------------------------------------------
# memory/session_logs/<date>.jsonl and memory/long_term/knowledge_base.jsonl
# (memory/schema.md — both files share one record shape)
# ---------------------------------------------------------------------------
class MemoryEntry(BaseModel):
    timestamp: str
    request: str = Field(min_length=1)
    response: str = Field(min_length=1)
    directors_invoked: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# qa_logs/hitl_decision_log.jsonl (agents/hitl.py — two record shapes)
# ---------------------------------------------------------------------------
class HITLCheckpointRecord(BaseModel):
    checkpoint: str = Field(min_length=1)
    description: str = Field(min_length=1)
    approved: bool
    mode: str
    timestamp: str


class CostChoiceRecord(BaseModel):
    checkpoint: str = "cost_bearing_action"
    requested_model: str = Field(min_length=1)
    reason: str = Field(min_length=1)
    choice: str
    timestamp: str

    @field_validator("choice")
    @classmethod
    def _valid_choice(cls, v: str) -> str:
        allowed = {"keep_free_path", "flag_for_manual_upgrade"}
        if v not in allowed:
            raise ValueError(f"choice must be one of {allowed}, got {v!r}")
        return v


# ---------------------------------------------------------------------------
# qa_logs/routing_log.jsonl (scripts/eliot_log_routing.py)
# ---------------------------------------------------------------------------
class RoutingLogEntry(BaseModel):
    timestamp: str
    request: str = Field(min_length=1)
    directors_invoked: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# metrics/learning_metrics.jsonl (metrics/README.md)
# ---------------------------------------------------------------------------
class MetricEntry(BaseModel):
    timestamp: str
    program: str = Field(min_length=1)
    metric: str = Field(min_length=1)
    value: float | str
    source: str = Field(min_length=1)
    notes: str | None = None


# ---------------------------------------------------------------------------
# config.yaml — structural validation of the fields the code actually reads.
# `extra="allow"` on every model here: config.yaml carries a lot of prose
# (namesake_note, expansion_note, register_note, ...) that's real and
# meaningful to a human reader but irrelevant to validate structurally.
# ---------------------------------------------------------------------------
class ChiefOfStaffConfig(BaseModel):
    model_config = ConfigDict(extra="allow")
    namesake: str
    role: str
    model: str

    @field_validator("model")
    @classmethod
    def _model_ref_shape(cls, v: str) -> str:
        if not _MODEL_REF_RE.match(v):
            raise ValueError(f"model ref {v!r} doesn't look like 'provider.tier'")
        return v


class MemoryCuratorConfig(BaseModel):
    model_config = ConfigDict(extra="allow")
    namesake: str
    role: str
    model: str

    @field_validator("model")
    @classmethod
    def _model_ref_shape(cls, v: str) -> str:
        if not _MODEL_REF_RE.match(v):
            raise ValueError(f"model ref {v!r} doesn't look like 'provider.tier'")
        return v


class DirectorConfig(BaseModel):
    model_config = ConfigDict(extra="allow")
    id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    model: str
    namesake: str | None = None
    domains: list[str] = Field(default_factory=list)

    @field_validator("model")
    @classmethod
    def _model_ref_shape(cls, v: str) -> str:
        if not _MODEL_REF_RE.match(v):
            raise ValueError(f"model ref {v!r} doesn't look like 'provider.tier'")
        return v


class AgentsConfig(BaseModel):
    model_config = ConfigDict(extra="allow")
    chief_of_staff: ChiefOfStaffConfig
    memory_curator: MemoryCuratorConfig
    directors: list[DirectorConfig]

    @field_validator("directors")
    @classmethod
    def _unique_ids(cls, v: list[DirectorConfig]) -> list[DirectorConfig]:
        ids = [d.id for d in v]
        dupes = {i for i in ids if ids.count(i) > 1}
        if dupes:
            raise ValueError(f"duplicate director id(s): {dupes}")
        return v


class LoggingConfig(BaseModel):
    model_config = ConfigDict(extra="allow")
    qa_logs_dir: str
    routing_log: str
    hitl_decision_log: str
    outputs_dir: str


class AppConfig(BaseModel):
    """Top-level shape of config.yaml. Sections not consumed by any
    Python module (system, operating_mode, integrations, hitl_checkpoints)
    are left as plain dicts/lists rather than modeled field-by-field —
    validating them adds no safety since nothing in the codebase reads
    them structurally today, only Eliot reading the file directly in chat.
    """

    model_config = ConfigDict(extra="allow")
    agents: AgentsConfig
    logging: LoggingConfig
