import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import call, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import install
import update
import uninstall
from check import classify


class LifecycleScriptTests(unittest.TestCase):
    def test_submodule_install_checks_out_pre_resolved_commit(self):
        root = Path(tempfile.mkdtemp())
        (root / ".git").mkdir()
        payload = root / ".argentos" / ".agents"
        payload.parent.mkdir(parents=True)
        target_commit = "d" * 40

        def run_git(args, cwd=None):
            if args[:3] == ["submodule", "add", "--branch"]:
                return ""
            if args[:4] == ["-C", str(payload), "checkout", "--detach"]:
                self.assertEqual(args[4], target_commit)
                return ""
            if args == ["-C", str(payload), "rev-parse", "HEAD"]:
                return target_commit
            self.fail(f"unexpected git invocation: {args!r}")

        with patch.object(install, "run_git", side_effect=run_git) as run_git_mock:
            result = install.materialize_submodule(payload, root, target_commit)

        self.assertEqual(result, target_commit)
        self.assertEqual(
            run_git_mock.call_args_list,
            [
                call(
                    [
                        "submodule",
                        "add",
                        "--branch",
                        "dist",
                        install.SOURCE_URL,
                        str(payload.relative_to(root)),
                    ],
                    root,
                ),
                call(["-C", str(payload), "checkout", "--detach", target_commit]),
                call(["-C", str(payload), "rev-parse", "HEAD"]),
            ],
        )

    def test_submodule_install_rejects_commit_mismatch(self):
        root = Path(tempfile.mkdtemp())
        (root / ".git").mkdir()
        payload = root / ".argentos" / ".agents"
        payload.parent.mkdir(parents=True)
        target_commit = "d" * 40
        actual_commit = "e" * 40

        def run_git(args, cwd=None):
            if args[:3] == ["submodule", "add", "--branch"]:
                return ""
            if args[:4] == ["-C", str(payload), "checkout", "--detach"]:
                self.assertEqual(args[4], target_commit)
                return ""
            if args == ["-C", str(payload), "rev-parse", "HEAD"]:
                return actual_commit
            self.fail(f"unexpected git invocation: {args!r}")

        with patch.object(install, "run_git", side_effect=run_git):
            with self.assertRaises(install.InstallError) as ctx:
                install.materialize_submodule(payload, root, target_commit)

        self.assertEqual(ctx.exception.error, "VERIFICATION_FAILED")
        self.assertIn(target_commit, str(ctx.exception))
        self.assertIn(actual_commit, str(ctx.exception))

    def test_submodule_update_checks_out_and_verifies_target_commit(self):
        root = Path(tempfile.mkdtemp())
        payload = root / ".argentos" / ".agents"
        payload.parent.mkdir(parents=True)
        target_commit = "f" * 40

        def run_git(args, cwd=None):
            if args[:4] == ["-C", str(payload), "status", "--porcelain"]:
                return ""
            if args == ["-C", str(payload), "fetch", "origin", "dist"]:
                return ""
            if args[:4] == ["-C", str(payload), "checkout", "--detach"]:
                self.assertEqual(args[4], target_commit)
                return ""
            if args == ["-C", str(payload), "rev-parse", "HEAD"]:
                return target_commit
            if args == ["add", str(payload.relative_to(root))]:
                return ""
            self.fail(f"unexpected git invocation: {args!r}")

        with patch.object(update, "run_git", side_effect=run_git) as run_git_mock:
            result = update.update_submodule(root, payload, target_commit)

        self.assertEqual(result, target_commit)
        self.assertEqual(
            run_git_mock.call_args_list,
            [
                call(["-C", str(payload), "status", "--porcelain"]),
                call(["-C", str(payload), "fetch", "origin", "dist"]),
                call(["-C", str(payload), "checkout", "--detach", target_commit]),
                call(["-C", str(payload), "rev-parse", "HEAD"]),
                call(["add", str(payload.relative_to(root))], root),
            ],
        )

    def test_submodule_update_rejects_commit_mismatch(self):
        root = Path(tempfile.mkdtemp())
        payload = root / ".argentos" / ".agents"
        payload.parent.mkdir(parents=True)
        target_commit = "f" * 40
        actual_commit = "e" * 40

        def run_git(args, cwd=None):
            if args[:4] == ["-C", str(payload), "status", "--porcelain"]:
                return ""
            if args[:4] == ["-C", str(payload), "fetch", "origin", "dist"]:
                return ""
            if args[:4] == ["-C", str(payload), "checkout", "--detach"]:
                self.assertEqual(args[4], target_commit)
                return ""
            if args == ["-C", str(payload), "rev-parse", "HEAD"]:
                return actual_commit
            self.fail(f"unexpected git invocation: {args!r}")

        with patch.object(update, "run_git", side_effect=run_git):
            with self.assertRaises(RuntimeError) as ctx:
                update.update_submodule(root, payload, target_commit)

        self.assertIn("VERIFICATION_FAILED", str(ctx.exception))
        self.assertIn(target_commit, str(ctx.exception))
        self.assertIn(actual_commit, str(ctx.exception))

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
