#!/usr/bin/env python3
"""Deterministic ARgentOS updater."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path

from check import classify
from common import paths, resolve_project_root
from install import SOURCE_URL, run_git, write_manifest


def prepare_source() -> tuple[Path, str]:
    temp = Path(tempfile.mkdtemp(prefix="argentos-update-"))
    checkout = temp / "source"
    try:
        run_git(["clone", "--depth", "1", "--branch", "dist", SOURCE_URL, str(checkout)])
        commit = run_git(["rev-parse", "HEAD"], checkout)
        return temp, commit
    except Exception:
        shutil.rmtree(temp, ignore_errors=True)
        raise


def update_submodule(root: Path, payload: Path, target_commit: str) -> str:
    status = run_git(["-C", str(payload), "status", "--porcelain"])
    if status:
        raise RuntimeError("UPDATE_LOCAL_CHANGES")
    run_git(["-C", str(payload), "fetch", "origin", "dist"])
    run_git(["-C", str(payload), "checkout", "--detach", target_commit])
    run_git(["add", str(payload.relative_to(root))], root)
    return run_git(["-C", str(payload), "rev-parse", "HEAD"])


def replace_payload(source: Path, payload: Path) -> None:
    next_payload = payload.parent / ".agents.next"
    old_payload = payload.parent / ".agents.previous"
    if next_payload.exists():
        shutil.rmtree(next_payload)
    if old_payload.exists():
        shutil.rmtree(old_payload)
    shutil.copytree(source / ".agents", next_payload)
    payload.rename(old_payload)
    try:
        next_payload.rename(payload)
    except Exception:
        old_payload.rename(payload)
        raise
    shutil.rmtree(old_payload)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root")
    args = parser.parse_args()

    root, error = resolve_project_root(args.root)
    if error:
        print(json.dumps({"result": "UPDATE_BLOCKED", "state": "UNKNOWN", "ERROR": error}, sort_keys=True))
        return 2

    before = classify(root)
    if before["state"] not in ("INSTALLED", "INSTALLED_WITH_DRIFT"):
        print(json.dumps({
            "result": "UPDATE_BLOCKED",
            "state": before["state"],
            "ERROR": "STATE_NOT_INSTALLED",
        }, sort_keys=True))
        return 3

    p = paths(root)
    temp = None
    try:
        manifest = json.loads(p["manifest"].read_text(encoding="utf-8"))
        method = manifest["method"]

        temp, target_commit = prepare_source()
        source = temp / "source"
        version = (source / ".agents" / "VERSION").read_text(encoding="utf-8").strip()

        already_current = (
            before["state"] == "INSTALLED"
            and manifest.get("source_commit") == target_commit
            and manifest.get("installed_version") == version
        )
        if already_current:
            print(json.dumps({
                "result": "UPDATE_NOT_NEEDED",
                "state": "INSTALLED",
                "METHOD": method,
                "VERSION": version,
            }, sort_keys=True))
            return 0

        if method == "submodule":
            resolved_commit = update_submodule(root, p["payload_root"], target_commit)
        elif method in ("git_tree", "copy"):
            replace_payload(source, p["payload_root"])
            if method == "git_tree":
                run_git(["add", str(p["payload_root"].relative_to(root))], root)
            resolved_commit = target_commit
        else:
            raise RuntimeError("UPDATE_METHOD_MISMATCH")

        shutil.copy2(source / "AGENTS.md", p["protocol_entry"])
        write_manifest(p, method, resolved_commit)

        after = classify(root)
        if after["state"] != "INSTALLED":
            print(json.dumps({
                "result": "UPDATE_FAILED",
                "state": after["state"],
                "ERROR": "VERIFICATION_FAILED",
            }, sort_keys=True))
            return 5

        print(json.dumps(after | {
            "result": "UPDATE_COMPLETE",
            "state": "INSTALLED",
            "METHOD": method,
            "VERSION": version,
        }, sort_keys=True))
        return 0
    except (OSError, KeyError, ValueError, RuntimeError) as exc:
        after = classify(root)
        error_id = str(exc) if str(exc) in {
            "UPDATE_LOCAL_CHANGES",
            "UPDATE_METHOD_MISMATCH",
        } else "UPDATE_FAILED"
        print(json.dumps({
            "result": "UPDATE_FAILED",
            "state": after["state"],
            "ERROR": error_id,
        }, sort_keys=True))
        return 4
    finally:
        if temp:
            shutil.rmtree(temp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
