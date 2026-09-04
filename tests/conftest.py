"""Shared pytest fixtures. Puts the repo root on sys.path (matches the
sys.path.insert pattern every scripts/eliot_*.py already uses) so `import
agents...` works regardless of how pytest is invoked.
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
