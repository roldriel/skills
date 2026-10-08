"""Shared deterministic primitives for ARgentOS skill scripts."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

METHODS = ("submodule", "git_tree", "copy")
STATES = (
    "NOT_INSTALLED",
    "INSTALLED",
    "INSTALLED_WITH_DRIFT",
    "INCOMPLETE",
    "UNINSTALLED_WITH_SESSIONS",
    "BROKEN",
    "UNKNOWN",
)

ROOT_ENV = "ARGENTOS_PROJECT_ROOT"


def resolve_project_root(explicit: str | None) -> tuple[Path | None, str | None]:
    value = explicit or os.environ.get(ROOT_ENV)
    if not value:
        return None, "PROJECT_ROOT_UNRESOLVED"
    root = Path(value).expanduser()
    try:
        root = root.resolve(strict=True)
    except (FileNotFoundError, OSError):
        return None, "PROJECT_ROOT_INVALID"
    if not root.is_dir():
        return None, "PROJECT_ROOT_INVALID"
    return root, None


def paths(root: Path) -> dict[str, Path]:
    argentos = root / ".argentos"
    return {
        "project_root": root,
        "argentos_root": argentos,
        "payload_root": argentos / ".agents",
        "project_state_root": argentos / ".project",
        "backup_root": argentos / ".backup",
        "config_path": argentos / "features.toml",
        "protocol_entry": argentos / "AGENTS.md",
        "adapter": root / "AGENTS.md",
        "manifest": argentos / ".project" / "install.json",
        "version": argentos / ".agents" / "VERSION",
    }


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_tree(root: Path) -> str:
    digest = hashlib.sha256()
    if not root.is_dir():
        raise FileNotFoundError(root)
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        rel = path.relative_to(root).as_posix().encode("utf-8")
        digest.update(rel)
        digest.update(b"\0")
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        digest.update(b"\0")
    return digest.hexdigest()


def load_json(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None, "STATE_BROKEN"
    if not isinstance(value, dict):
        return None, "STATE_BROKEN"
    return value, None


def has_content(path: Path) -> bool:
    return path.exists() and any(path.iterdir()) if path.is_dir() else path.exists()
