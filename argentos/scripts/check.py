#!/usr/bin/env python3
"""Deterministic, read-only ARgentOS state checker."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from common import (
    METHODS,
    STATES,
    has_content,
    load_json,
    paths,
    resolve_project_root,
    sha256_file,
    sha256_tree,
)

REQUIRED_MANIFEST = {
    "schema_version",
    "method",
    "source_repository",
    "source_ref",
    "source_commit",
    "installed_version",
    "payload_digest",
    "protocol_entry_digest",
    "adapter_digest",
}
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")


def classify(root: Path) -> dict:
    p = paths(root)
    result = {
        "result": "CHECK_UNKNOWN",
        "state": "UNKNOWN",
        "PROJECT_ROOT": str(root),
        "ARGENTOS_ROOT": str(p["argentos_root"]),
        "METHOD": None,
        "VERSION": None,
        "DRIFT": [],
        "BACKUP_ARTIFACTS": [],
        "PRESERVED_SESSIONS": False,
        "ERROR": None,
    }

    a = p["argentos_root"]
    if not a.exists():
        result["state"] = "NOT_INSTALLED"
        result["result"] = "CHECK_PASS"
        return result

    if not a.is_dir():
        result["state"] = "BROKEN"
        result["result"] = "CHECK_FAIL"
        result["ERROR"] = "STATE_BROKEN"
        return result

    payload = p["payload_root"]
    state_root = p["project_state_root"]
    manifest = p["manifest"]
    protocol_entry = p["protocol_entry"]
    adapter = p["adapter"]

    backup = p["backup_root"]
    if backup.exists():
        for child in sorted(backup.iterdir()):
            result["BACKUP_ARTIFACTS"].append(child.name)

    # A removed installation with retained project state has neither the
    # protocol entry nor payload, while .project still contains data.
    if not protocol_entry.exists() and not payload.exists():
        if has_content(state_root):
            result["state"] = "UNINSTALLED_WITH_SESSIONS"
            result["result"] = "CHECK_WARN"
            result["PRESERVED_SESSIONS"] = True
            return result
        result["state"] = "INCOMPLETE"
        result["result"] = "CHECK_FAIL"
        result["ERROR"] = "INSTALL_INCOMPLETE"
        return result

    if not payload.is_dir() or not protocol_entry.is_file() or not adapter.is_file():
        result["state"] = "INCOMPLETE"
        result["result"] = "CHECK_FAIL"
        result["ERROR"] = "INSTALL_INCOMPLETE"
        return result

    if not state_root.is_dir() or not p["config_path"].is_file() or not manifest.is_file():
        result["state"] = "INCOMPLETE"
        result["result"] = "CHECK_FAIL"
        result["ERROR"] = "INSTALL_INCOMPLETE"
        return result

    data, error = load_json(manifest)
    if error or data is None:
        result["state"] = "BROKEN"
        result["result"] = "CHECK_FAIL"
        result["ERROR"] = error or "STATE_BROKEN"
        return result

    missing = REQUIRED_MANIFEST - data.keys()
    if missing:
        result["state"] = "BROKEN"
        result["result"] = "CHECK_FAIL"
        result["ERROR"] = "STATE_INCONSISTENT"
        result["MISSING_MANIFEST_FIELDS"] = sorted(missing)
        return result

    method = data.get("method")
    if method not in METHODS:
        result["state"] = "BROKEN"
        result["result"] = "CHECK_FAIL"
        result["ERROR"] = "STATE_INCONSISTENT"
        return result

    if data.get("schema_version") != 1:
        result["state"] = "BROKEN"
        result["result"] = "CHECK_FAIL"
        result["ERROR"] = "STATE_INCONSISTENT"
        return result

    if data.get("source_repository") != "roldriel/argentos" or data.get("source_ref") != "dist":
        result["state"] = "BROKEN"
        result["result"] = "CHECK_FAIL"
        result["ERROR"] = "STATE_INCONSISTENT"
        return result

    source_commit = data.get("source_commit")
    if not isinstance(source_commit, str) or not COMMIT_RE.fullmatch(source_commit):
        result["state"] = "BROKEN"
        result["result"] = "CHECK_FAIL"
        result["ERROR"] = "STATE_INCONSISTENT"
        return result

    result["METHOD"] = method
    result["VERSION"] = data.get("installed_version")

    try:
        payload_digest = sha256_tree(payload)
        protocol_entry_digest = sha256_file(protocol_entry)
        adapter_digest = sha256_file(adapter)
        version = p["version"].read_text(encoding="utf-8").strip()
    except (OSError, UnicodeDecodeError):
        result["state"] = "BROKEN"
        result["result"] = "CHECK_FAIL"
        result["ERROR"] = "STATE_BROKEN"
        return result

    if not version:
        result["state"] = "BROKEN"
        result["result"] = "CHECK_FAIL"
        result["ERROR"] = "STATE_BROKEN"
        return result

    result["VERSION"] = version

    checks = (
        ("payload_digest", payload_digest),
        ("protocol_entry_digest", protocol_entry_digest),
        ("adapter_digest", adapter_digest),
    )
    for field, observed in checks:
        expected = data.get(field)
        if expected != observed:
            result["DRIFT"].append(field)

    if data.get("installed_version") != version:
        result["DRIFT"].append("installed_version")

    if result["DRIFT"]:
        result["state"] = "INSTALLED_WITH_DRIFT"
        result["result"] = "CHECK_WARN"
        return result

    result["state"] = "INSTALLED"
    result["result"] = "CHECK_PASS"
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root")
    args = parser.parse_args()

    root, error = resolve_project_root(args.root)
    if error:
        output = {
            "result": "CHECK_UNKNOWN",
            "state": "UNKNOWN",
            "ERROR": error,
        }
        print(json.dumps(output, sort_keys=True))
        return 2

    try:
        output = classify(root)
    except OSError:
        output = {
            "result": "CHECK_UNKNOWN",
            "state": "UNKNOWN",
            "PROJECT_ROOT": str(root),
            "ERROR": "OPERATION_FAILED",
        }
        print(json.dumps(output, sort_keys=True))
        return 5

    print(json.dumps(output, sort_keys=True))
    return 0 if output["result"] != "CHECK_UNKNOWN" else 5


if __name__ == "__main__":
    sys.exit(main())
