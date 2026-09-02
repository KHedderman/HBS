"""GitHub sync adapter for the Memory Curator and the Product Management
Director's PR sync duties.

Two modes:
  1. API mode — GITHUB_TOKEN + GITHUB_REPO set: pushes files via the
     GitHub REST API (works from anywhere, including outside this checkout).
  2. Local git mode (fallback) — no token: commits directly to the local
     working tree with `git`, since the Command Center already lives inside
     the HBS repo it's curating memory for. This never pushes automatically;
     it stages a commit so a human (or a subsequent `git push`) controls
     when memory actually reaches the remote.
"""
from __future__ import annotations

import base64
import subprocess
from pathlib import Path
from typing import Optional

import requests

from agents.config_loader import env

REPO_ROOT = Path(__file__).resolve().parent.parent
API_ROOT = "https://api.github.com"


def _api_mode_available() -> bool:
    return bool(env("GITHUB_TOKEN") and env("GITHUB_REPO"))


def push_memory_file(relative_path: str, content: str, commit_message: str) -> dict:
    """Writes `content` to `relative_path` (relative to repo root) and syncs
    it to GitHub. Returns a small status dict for logging.
    """
    full_path = REPO_ROOT / relative_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_text(content, encoding="utf-8")

    if _api_mode_available():
        return _push_via_api(relative_path, content, commit_message)
    return _commit_local(relative_path, commit_message)


def _push_via_api(relative_path: str, content: str, commit_message: str) -> dict:
    token = env("GITHUB_TOKEN")
    repo = env("GITHUB_REPO")
    url = f"{API_ROOT}/repos/{repo}/contents/{relative_path}"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}

    sha: Optional[str] = None
    existing = requests.get(url, headers=headers, timeout=15)
    if existing.status_code == 200:
        sha = existing.json().get("sha")

    payload = {
        "message": commit_message,
        "content": base64.b64encode(content.encode("utf-8")).decode("ascii"),
    }
    if sha:
        payload["sha"] = sha

    resp = requests.put(url, headers=headers, json=payload, timeout=15)
    if resp.status_code in (200, 201):
        return {"mode": "api", "status": "synced", "path": relative_path}
    return {"mode": "api", "status": "error", "detail": resp.text[:300]}


def _commit_local(relative_path: str, commit_message: str) -> dict:
    try:
        subprocess.run(["git", "add", relative_path], cwd=REPO_ROOT, check=True, capture_output=True)
        result = subprocess.run(
            ["git", "commit", "-m", commit_message],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return {"mode": "local_git", "status": "committed", "path": relative_path}
        # returncode != 0 commonly means "nothing to commit" — not an error.
        return {"mode": "local_git", "status": "no_change", "detail": result.stdout.strip()}
    except Exception as exc:  # pragma: no cover
        return {"mode": "local_git", "status": "error", "detail": str(exc)}
