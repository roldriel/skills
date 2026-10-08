#!/usr/bin/env python3
"""Deterministic ARgentOS installer."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from common import METHODS, paths, resolve_project_root, sha256_file, sha256_tree
from check import classify

SOURCE_URL = "https://github.com/roldriel/argentos.git"


class InstallError(RuntimeError):
    def __init__(self, error: str, message: str):
        super().__init__(message)
        self.error = error


def run_git(args: list[str], cwd: Path | None = None) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        raise InstallError("INSTALL_FAILED", completed.stderr.strip() or "git failed")
    return completed.stdout.strip()


def load_template() -> str:
    path = Path(__file__).resolve().parents[1] / "references" / "project-adapter-template.md"
    return path.read_text(encoding="utf-8")


def validate_backup_destinations(root: Path, backup: Path) -> None:
    for source, destination in (
        (root / "AGENTS.md", backup / "_AGENTS.md"),
        (root / ".agents", backup / "_agents"),
    ):
        if source.exists() and destination.exists():
            raise InstallError("STATE_INCONSISTENT", f"backup destination exists: {destination}")


def backup_existing(root: Path, p: dict[str, Path]) -> None:
    backup = p["backup_root"]
    backup.mkdir(parents=True, exist_ok=True)

    sources = [
        (root / "AGENTS.md", backup / "_AGENTS.md"),
        (root / ".agents", backup / "_agents"),
    ]
    for source, destination in sources:
        if not source.exists():
            continue
        if destination.exists():
            raise InstallError("STATE_INCONSISTENT", f"backup destination exists: {destination}")
        shutil.move(str(source), str(destination))


def prepare_source() -> tuple[Path, str]:
    temp = Path(tempfile.mkdtemp(prefix="argentos-source-"))
    checkout = temp / "source"
    try:
        run_git(["clone", "--depth", "1", "--branch", "dist", SOURCE_URL, str(checkout)])
        commit = run_git(["rev-parse", "HEAD"], checkout)
        if len(commit) != 40:
            raise InstallError("UPDATE_SOURCE_UNAVAILABLE", "invalid source commit")
        return temp, commit
    except Exception:
        shutil.rmtree(temp, ignore_errors=True)
        raise


def materialize_copy(source: Path, payload: Path) -> None:
    if not (source / ".agents").is_dir() or not (source / "AGENTS.md").is_file():
        raise InstallError("UPDATE_SOURCE_UNAVAILABLE", "dist payload is incomplete")
    shutil.copytree(source / ".agents", payload)


def materialize_tree(source: Path, payload: Path, root: Path) -> None:
    materialize_copy(source, payload)
    run_git(["add", str(payload.relative_to(root)), str((root / ".argentos").relative_to(root))], root)


def materialize_submodule(payload: Path, root: Path) -> str:
    if not (root / ".git").exists():
        raise InstallError("INSTALL_METHOD_UNSUPPORTED", "git submodule requires a Git worktree")
    run_git(["submodule", "add", "--branch", "dist", SOURCE_URL, str(payload.relative_to(root))], root)
    return run_git(["-C", str(payload), "rev-parse", "HEAD"])


def write_manifest(p: dict[str, Path], method: str, commit: str) -> None:
    version = p["version"].read_text(encoding="utf-8").strip()
    manifest = {
        "schema_version": 1,
        "method": method,
        "source_repository": "roldriel/argentos",
        "source_ref": "dist",
        "source_commit": commit,
        "installed_version": version,
        "payload_digest": sha256_tree(p["payload_root"]),
        "protocol_entry_digest": sha256_file(p["protocol_entry"]),
        "adapter_digest": sha256_file(p["adapter"]),
    }
    p["manifest"].write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root")
    parser.add_argument("--method", choices=METHODS, required=True)
    args = parser.parse_args()

    root, error = resolve_project_root(args.root)
    if error:
        print(json.dumps({"result": "INSTALL_BLOCKED", "state": "UNKNOWN", "ERROR": error}, sort_keys=True))
        return 2

    before = classify(root)
    if before["state"] not in ("NOT_INSTALLED", "UNINSTALLED_WITH_SESSIONS"):
        error_id = "INSTALL_ALREADY_PRESENT" if before["state"] in ("INSTALLED", "INSTALLED_WITH_DRIFT") else "INSTALL_INCOMPLETE"
        print(json.dumps({"result": "INSTALL_BLOCKED", "state": before["state"], "ERROR": error_id}, sort_keys=True))
        return 3

    p = paths(root)
    temp = None
    try:
        # All source and capability checks happen before project mutation.
        temp, commit = prepare_source()
        source = temp / "source"
        if not (source / ".agents").is_dir() or not (source / "AGENTS.md").is_file():
            raise InstallError("UPDATE_SOURCE_UNAVAILABLE", "dist payload is incomplete")
        if args.method == "submodule" and not (root / ".git").exists():
            raise InstallError("INSTALL_METHOD_UNSUPPORTED", "git submodule requires a Git worktree")

        validate_backup_destinations(root, p["backup_root"])
        if p["payload_root"].exists():
            raise InstallError("STATE_INCONSISTENT", "payload destination already exists")

        p["argentos_root"].mkdir(parents=True, exist_ok=True)
        p["project_state_root"].mkdir(parents=True, exist_ok=True)
        p["backup_root"].mkdir(parents=True, exist_ok=True)
        backup_existing(root, p)

        payload = p["payload_root"]
        if args.method == "submodule":
            resolved_commit = materialize_submodule(payload, root)
        elif args.method == "git_tree":
            materialize_tree(source, payload, root)
            resolved_commit = commit
        else:
            materialize_copy(source, payload)
            resolved_commit = commit

        shutil.copy2(source / "AGENTS.md", p["protocol_entry"])
        p["adapter"].write_text(load_template(), encoding="utf-8")
        if not p["config_path"].exists():
            p["config_path"].write_text("", encoding="utf-8")
        write_manifest(p, args.method, resolved_commit)

        after = classify(root)
        if after["state"] != "INSTALLED":
            raise InstallError("VERIFICATION_FAILED", "post-install check did not return INSTALLED")

        print(json.dumps(after | {"result": "INSTALL_COMPLETE", "state": "INSTALLED"}, sort_keys=True))
        return 0
    except InstallError as exc:
        after = classify(root)
        print(json.dumps({
            "result": "INSTALL_FAILED",
            "state": after["state"],
            "ERROR": exc.error,
            "message": str(exc),
        }, sort_keys=True))
        return 5 if exc.error == "VERIFICATION_FAILED" else 4
    finally:
        if temp:
            shutil.rmtree(temp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
