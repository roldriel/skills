import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from check import classify
from doctor import propose
from install import InstallError, validate_backup_destinations


class ScriptContractTests(unittest.TestCase):
    def test_root_must_be_explicit(self):
        from common import resolve_project_root
        root, error = resolve_project_root(None)
        self.assertIsNone(root)
        self.assertEqual(error, "PROJECT_ROOT_UNRESOLVED")

    def test_backup_conflict_is_detected_before_mutation(self):
        root = Path(tempfile.mkdtemp())
        backup = root / ".argentos" / ".backup"
        backup.mkdir(parents=True)
        (root / "AGENTS.md").write_text("original", encoding="utf-8")
        (backup / "_AGENTS.md").write_text("existing", encoding="utf-8")
        with self.assertRaises(InstallError) as ctx:
            validate_backup_destinations(root, backup)
        self.assertEqual(ctx.exception.error, "STATE_INCONSISTENT")

    def test_doctor_is_blocked_for_ambiguous_state(self):
        root = Path(tempfile.mkdtemp())
        (root / ".argentos").mkdir()
        result = propose(root)
        self.assertEqual(result["result"], "REPAIR_BLOCKED")
        self.assertEqual(result["ERROR"], "REPAIR_UNSAFE")

    def test_doctor_plan_for_adapter_drift_is_deterministic(self):
        root = Path(tempfile.mkdtemp())
        argentos = root / ".argentos"
        payload = argentos / ".agents"
        state = argentos / ".project"
        payload.mkdir(parents=True)
        state.mkdir()
        (argentos / ".backup").mkdir()
        (argentos / "features.toml").write_text("", encoding="utf-8")
        (root / "AGENTS.md").write_text("adapter", encoding="utf-8")
        (argentos / "AGENTS.md").write_text("protocol", encoding="utf-8")
        (payload / "VERSION").write_text("11.7.0", encoding="utf-8")

        from common import sha256_file, sha256_tree
        manifest = {
            "schema_version": 1,
            "method": "copy",
            "source_repository": "roldriel/argentos",
            "source_ref": "dist",
            "source_commit": "b" * 40,
            "installed_version": "11.7.0",
            "payload_digest": sha256_tree(payload),
            "protocol_entry_digest": sha256_file(argentos / "AGENTS.md"),
            "adapter_digest": "0" * 64,
        }
        (state / "install.json").write_text(json.dumps(manifest), encoding="utf-8")

        result = propose(root)
        self.assertEqual(result["result"], "REPAIR_PLAN_READY")
        self.assertEqual(result["plan"], ["refresh_adapter"])


if __name__ == "__main__":
    unittest.main()
