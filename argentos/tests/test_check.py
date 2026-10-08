import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from check import classify
from common import sha256_file, sha256_tree


class CheckContractTests(unittest.TestCase):
    def make_root(self) -> Path:
        return Path(tempfile.mkdtemp())

    def make_installed(self, root: Path) -> None:
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
        manifest = {
            "schema_version": 1,
            "method": "copy",
            "source_repository": "roldriel/argentos",
            "source_ref": "dist",
            "source_commit": "a" * 40,
            "installed_version": "11.7.0",
            "payload_digest": sha256_tree(payload),
            "protocol_entry_digest": sha256_file(argentos / "AGENTS.md"),
            "adapter_digest": sha256_file(root / "AGENTS.md"),
        }
        (state / "install.json").write_text(
            json.dumps(manifest), encoding="utf-8"
        )

    def test_not_installed(self):
        root = self.make_root()
        result = classify(root)
        self.assertEqual(result["state"], "NOT_INSTALLED")
        self.assertEqual(result["result"], "CHECK_PASS")

    def test_incomplete(self):
        root = self.make_root()
        (root / ".argentos").mkdir()
        result = classify(root)
        self.assertEqual(result["state"], "INCOMPLETE")
        self.assertEqual(result["result"], "CHECK_FAIL")

    def test_uninstalled_with_sessions(self):
        root = self.make_root()
        state = root / ".argentos" / ".project"
        state.mkdir(parents=True)
        (state / "session.json").write_text("{}", encoding="utf-8")
        result = classify(root)
        self.assertEqual(result["state"], "UNINSTALLED_WITH_SESSIONS")
        self.assertEqual(result["result"], "CHECK_WARN")

    def test_installed(self):
        root = self.make_root()
        self.make_installed(root)
        result = classify(root)
        self.assertEqual(result["state"], "INSTALLED")
        self.assertEqual(result["result"], "CHECK_PASS")
        self.assertEqual(result["METHOD"], "copy")

    def test_drift_is_not_healthy(self):
        root = self.make_root()
        self.make_installed(root)
        (root / ".argentos" / ".agents" / "changed.txt").write_text(
            "changed", encoding="utf-8"
        )
        result = classify(root)
        self.assertEqual(result["state"], "INSTALLED_WITH_DRIFT")
        self.assertEqual(result["result"], "CHECK_WARN")
        self.assertIn("payload_digest", result["DRIFT"])


if __name__ == "__main__":
    unittest.main()
