#!/usr/bin/env python3
"""Deterministic ARgentOS uninstaller."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from check import classify
from common import paths, resolve_project_root, sha256_file
from install import run_git


def restore_file(backup: Path, destination: Path) -> None:
    if not backup.exists():
        return
    if destination.exists():
        raise RuntimeError("BACKUP_CONFLICT")
    shutil.move(str(backup), str(destination))


def restore_dir(backup: Path, destination: Path) -> None:
    if not backup.exists():
        return
    if destination.exists():
        raise RuntimeError("BACKUP_CONFLICT")
    shutil.move(str(backup), str(destination))


def remove_submodule(root: Path, payload: Path) -> None:
    run_git(["submodule", "deinit", "-f", "--", str(payload.relative_to(root))], root)
    run_git(["rm", "-f", "--", str(payload.relative_to(root))], root)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root")
    parser.add_argument("--sessions", choices=("keep", "delete"), required=True)
    args = parser.parse_args()

    root, error = resolve_project_root(args.root)
    if error:
        print(json.dumps({"result": "UNINSTALL_BLOCKED", "state": "UNKNOWN", "ERROR": error}, sort_keys=True))
        return 2

    before = classify(root)
    if before["state"] not in (
        "INSTALLED",
        "INSTALLED_WITH_DRIFT",
        "INCOMPLETE",
        "BROKEN",
        "UNINSTALLED_WITH_SESSIONS",
    ):
        print(json.dumps({
            "result": "UNINSTALL_BLOCKED",
            "state": before["state"],
            "ERROR": "STATE_NOT_INSTALLED",
        }, sort_keys=True))
        return 3

    p = paths(root)

    try:
        manifest = None
        if p["manifest"].is_file():
            manifest = json.loads(p["manifest"].read_text(encoding="utf-8"))

        if manifest and p["adapter"].is_file():
            current_adapter = sha256_file(p["adapter"])
            expected_adapter = manifest.get("adapter_digest")
            if expected_adapter and current_adapter != expected_adapter:
                print(json.dumps({
                    "result": "UNINSTALL_BLOCKED",
                    "state": before["state"],
                    "ERROR": "ADAPTER_CONFLICT",
                }, sort_keys=True))
                return 3

        method = manifest.get("method") if manifest else None
        if method == "submodule" and p["payload_root"].exists():
            remove_submodule(root, p["payload_root"])
        elif p["payload_root"].exists():
            shutil.rmtree(p["payload_root"])

        if p["protocol_entry"].exists():
            p["protocol_entry"].unlink()
        if p["config_path"].exists():
            p["config_path"].unlink()

        if p["adapter"].exists():
            p["adapter"].unlink()

        # Restore displaced adopter artifacts only after managed ARgentOS files
        # have been removed and never over an existing destination.
        backup = p["backup_root"]
        if backup.exists():
            restore_file(backup / "_AGENTS.md", root / "AGENTS.md")
            restore_dir(backup / "_agents", root / ".agents")
            restore_file(backup / "_gitignore", root / ".gitignore")

        if p["manifest"].exists():
            p["manifest"].unlink()

        if args.sessions == "delete":
            if p["project_state_root"].exists():
                shutil.rmtree(p["project_state_root"])
        else:
            # Keep project state, but remove the installation manifest.
            p["project_state_root"].mkdir(parents=True, exist_ok=True)

        if p["backup_root"].exists() and not any(p["backup_root"].iterdir()):
            p["backup_root"].rmdir()

        if p["argentos_root"].exists():
            remaining = [child for child in p["argentos_root"].iterdir()]
            if not remaining:
                p["argentos_root"].rmdir()

        after = classify(root)
        expected_state = "UNINSTALLED_WITH_SESSIONS" if args.sessions == "keep" and p["project_state_root"].exists() and any(p["project_state_root"].iterdir()) else "NOT_INSTALLED"
        if after["state"] != expected_state:
            print(json.dumps({
                "result": "UNINSTALL_FAILED",
                "state": after["state"],
                "ERROR": "VERIFICATION_FAILED",
            }, sort_keys=True))
            return 5

        print(json.dumps(after | {
            "result": "UNINSTALL_COMPLETE",
            "state": after["state"],
            "PRESERVED_SESSIONS": expected_state == "UNINSTALLED_WITH_SESSIONS",
        }, sort_keys=True))
        return 0

    except RuntimeError as exc:
        print(json.dumps({
            "result": "UNINSTALL_FAILED",
            "state": classify(root)["state"],
            "ERROR": str(exc) if str(exc) in {"BACKUP_CONFLICT"} else "OPERATION_FAILED",
        }, sort_keys=True))
        return 4
    except (OSError, ValueError, json.JSONDecodeError):
        print(json.dumps({
            "result": "UNINSTALL_FAILED",
            "state": classify(root)["state"],
            "ERROR": "OPERATION_FAILED",
        }, sort_keys=True))
        return 4


if __name__ == "__main__":
    sys.exit(main())
