import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import install
import update
import uninstall
from check import classify


class LifecycleScriptTests(unittest.TestCase):
    def make_source(self, version: str) -> tuple[Path, str]:
        temp = Path(tempfile.mkdtemp())
        source = temp / "source"
        payload = source / ".agents"
        payload.mkdir(parents=True)
        (source / "AGENTS.md").write_text("protocol-entry", encoding="utf-8")
        (payload / "VERSION").write_text(version, encoding="utf-8")
        (payload / "INDEX.md").write_text("index", encoding="utf-8")
        return temp, "c" * 40

    def test_copy_install_moves_existing_adopter_artifacts(self):
        root = Path(tempfile.mkdtemp())
        (root / "AGENTS.md").write_text("original agents", encoding="utf-8")
        (root / ".agents").mkdir()
        (root / ".agents" / "ORIGINAL").write_text("original", encoding="utf-8")

        temp, commit = self.make_source("11.7.0")
        with patch.object(install, "prepare_source", return_value=(temp, commit)):
            with patch.object(sys, "argv", ["install.py", "--root", str(root), "--method", "copy"]):
                self.assertEqual(install.main(), 0)

        self.assertEqual(classify(root)["state"], "INSTALLED")
        self.assertEqual(
            (root / ".argentos" / ".backup" / "_AGENTS.md").read_text(encoding="utf-8"),
            "original agents",
        )
        self.assertEqual(
            (root / ".argentos" / ".backup" / "_agents" / "ORIGINAL").read_text(encoding="utf-8"),
            "original",
        )

    def test_update_repairs_payload_drift(self):
        root = Path(tempfile.mkdtemp())
        temp1, commit1 = self.make_source("11.7.0")
        with patch.object(install, "prepare_source", return_value=(temp1, commit1)):
            with patch.object(sys, "argv", ["install.py", "--root", str(root), "--method", "copy"]):
                self.assertEqual(install.main(), 0)

        (root / ".argentos" / ".agents" / "INDEX.md").write_text("drift", encoding="utf-8")
        self.assertEqual(classify(root)["state"], "INSTALLED_WITH_DRIFT")

        temp2, commit2 = self.make_source("11.8.0")
        with patch.object(update, "prepare_source", return_value=(temp2, commit2)):
            with patch.object(sys, "argv", ["update.py", "--root", str(root)]):
                self.assertEqual(update.main(), 0)

        state = classify(root)
        self.assertEqual(state["state"], "INSTALLED")
        self.assertEqual(state["VERSION"], "11.8.0")
        manifest = json.loads(
            (root / ".argentos" / ".project" / "install.json").read_text(encoding="utf-8")
        )
        self.assertEqual(manifest["source_commit"], commit2)

    def test_uninstall_keep_sessions_restores_backups(self):
        root = Path(tempfile.mkdtemp())
        (root / "AGENTS.md").write_text("original agents", encoding="utf-8")
        (root / ".agents").mkdir()
        (root / ".agents" / "ORIGINAL").write_text("original", encoding="utf-8")

        temp, commit = self.make_source("11.7.0")
        with patch.object(install, "prepare_source", return_value=(temp, commit)):
            with patch.object(sys, "argv", ["install.py", "--root", str(root), "--method", "copy"]):
                self.assertEqual(install.main(), 0)

        state = root / ".argentos" / ".project"
        (state / "session.json").write_text("session", encoding="utf-8")

        with patch.object(sys, "argv", ["uninstall.py", "--root", str(root), "--sessions", "keep"]):
            self.assertEqual(uninstall.main(), 0)

        self.assertEqual(classify(root)["state"], "UNINSTALLED_WITH_SESSIONS")
        self.assertEqual((root / "AGENTS.md").read_text(encoding="utf-8"), "original agents")
        self.assertEqual((root / ".agents" / "ORIGINAL").read_text(encoding="utf-8"), "original")
        self.assertTrue((root / ".argentos" / ".project" / "session.json").exists())


if __name__ == "__main__":
    unittest.main()
