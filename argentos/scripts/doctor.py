#!/usr/bin/env python3
"""Deterministic ARgentOS repair planner/executor."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path

from check import classify
from common import load_json, paths, resolve_project_root, sha256_file, sha256_tree
from install import SOURCE_URL, load_template, run_git


SAFE_ACTIONS = {
    "refresh_payload",
    "refresh_adapter",
}


def propose(root: Path) -> dict:
    state = classify(root)
    if state["state"] == "INSTALLED":
        return {"result": "REPAIR_NOT_NEEDED", "state": "INSTALLED", "plan": []}
    if state["state"] != "INSTALLED_WITH_DRIFT":
        return {
            "result": "REPAIR_BLOCKED",
            "state": state["state"],
            "ERROR": "REPAIR_UNSAFE",
            "plan": [],
        }

    drift = set(state.get("DRIFT", []))
    actions = []
    if {"payload_digest", "installed_version", "protocol_entry_digest"} & drift:
        actions.append("refresh_payload")
    if "adapter_digest" in drift:
        actions.append("refresh_adapter")

    return {
        "result": "REPAIR_PLAN_READY",
        "state": state["state"],
        "plan": actions,
    }


def prepare_source() -> tuple[Path, str]:
    temp = Path(tempfile.mkdtemp(prefix="argentos-doctor-"))
    checkout = temp / "source"
    try:
        run_git(["clone", "--depth", "1", "--branch", "dist", SOURCE_URL, str(checkout)])
        commit = run_git(["rev-parse", "HEAD"], checkout)
        return temp, commit
    except Exception:
        shutil.rmtree(temp, ignore_errors=True)
        raise


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


def execute(root: Path, actions: list[str]) -> dict:
    if any(action not in SAFE_ACTIONS for action in actions):
        return {
            "result": "REPAIR_BLOCKED",
            "state": classify(root)["state"],
            "ERROR": "REPAIR_UNSAFE",
        }

    before = classify(root)
    if before["state"] != "INSTALLED_WITH_DRIFT":
        return {
            "result": "REPAIR_BLOCKED",
            "state": before["state"],
            "ERROR": "REPAIR_UNSAFE",
        }

    p = paths(root)
    manifest, error = load_json(p["manifest"])
    if error or manifest is None:
        return {
            "result": "REPAIR_BLOCKED",
            "state": before["state"],
            "ERROR": "REPAIR_UNSAFE",
        }

    if "refresh_payload" not in actions and "protocol_entry_digest" in set(before.get("DRIFT", [])):
        return {
            "result": "REPAIR_BLOCKED",
            "state": before["state"],
            "ERROR": "REPAIR_UNSAFE",
        }

    temp = None
    try:
        if "refresh_payload" in actions:
            temp, commit = prepare_source()
            source = temp / "source"
            method = before["METHOD"]

            if method == "submodule":
                status = run_git(["-C", str(p["payload_root"]), "status", "--porcelain"])
                if status:
                    raise RuntimeError("UPDATE_LOCAL_CHANGES")
                run_git(["-C", str(p["payload_root"]), "fetch", "origin", "dist"])
                run_git(["-C", str(p["payload_root"]), "checkout", "--detach", commit])
            else:
                replace_payload(source, p["payload_root"])

            shutil.copy2(source / "AGENTS.md", p["protocol_entry"])

            manifest["source_commit"] = commit
            manifest["installed_version"] = p["version"].read_text(encoding="utf-8").strip()
            manifest["payload_digest"] = sha256_tree(p["payload_root"])
            manifest["protocol_entry_digest"] = sha256_file(p["protocol_entry"])

        if "refresh_adapter" in actions:
            p["adapter"].write_text(load_template(), encoding="utf-8")

        manifest["adapter_digest"] = sha256_file(p["adapter"])
        p["manifest"].write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        after = classify(root)
        if after["state"] != "INSTALLED":
            return {
                "result": "REPAIR_FAILED",
                "state": after["state"],
                "ERROR": "VERIFICATION_FAILED",
            }

        return after | {
            "result": "REPAIR_COMPLETE",
            "state": "INSTALLED",
            "REPAIRED": actions,
        }
    finally:
        if temp:
            shutil.rmtree(temp, ignore_errors=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root")
    parser.add_argument("--plan", help="JSON file containing an actions array")
    parser.add_argument("--propose", action="store_true")
    args = parser.parse_args()

    root, error = resolve_project_root(args.root)
    if error:
        print(json.dumps({"result": "REPAIR_BLOCKED", "state": "UNKNOWN", "ERROR": error}, sort_keys=True))
        return 2

    if args.propose:
        output = propose(root)
        print(json.dumps(output, sort_keys=True))
        return 0 if output["result"] != "REPAIR_BLOCKED" else 3

    if not args.plan:
        print(json.dumps({
            "result": "REPAIR_BLOCKED",
            "state": classify(root)["state"],
            "ERROR": "REPAIR_UNSAFE",
        }, sort_keys=True))
        return 2

    try:
        plan = json.loads(Path(args.plan).read_text(encoding="utf-8"))
        actions = plan["actions"]
        if not isinstance(actions, list):
            raise ValueError
    except (OSError, json.JSONDecodeError, KeyError, ValueError):
        print(json.dumps({
            "result": "REPAIR_BLOCKED",
            "state": classify(root)["state"],
            "ERROR": "REPAIR_UNSAFE",
        }, sort_keys=True))
        return 2

    try:
        output = execute(root, actions)
    except RuntimeError as exc:
        output = {
            "result": "REPAIR_FAILED",
            "state": classify(root)["state"],
            "ERROR": str(exc) if str(exc) == "UPDATE_LOCAL_CHANGES" else "REPAIR_FAILED",
        }

    print(json.dumps(output, sort_keys=True))
    return 0 if output["result"] in ("REPAIR_COMPLETE", "REPAIR_NOT_NEEDED") else 4


if __name__ == "__main__":
    sys.exit(main())
