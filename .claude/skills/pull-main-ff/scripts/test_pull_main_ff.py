#!/usr/bin/env python3
"""Scenario tests for the context-sensitive origin sync (pull_main_ff.py).

Each test builds a throwaway bare origin plus clones in a temp directory and
drives the real script through the safety-relevant scenarios: mode-A
fast-forward, honest no-op/ahead reporting, the MERGE-COMMIT-GATE with
override, mode-B re-sync with remote-ref healing, the unmerged-commits
guard, and the foreign-branch block. Requires git on PATH; uses only the
standard library.
"""

from __future__ import annotations

import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "pull_main_ff.py"


def run(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        args,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def git(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    result = run(["git", *args], cwd)
    if result.returncode != 0:
        raise AssertionError(
            f"git {' '.join(args)} failed in {cwd}:\n{result.stdout}\n{result.stderr}"
        )
    return result


def _force_remove(func, path, _exc_info):  # Windows: git objects are read-only
    os.chmod(path, stat.S_IWRITE)
    func(path)


class PullMainFfScenarioTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp(prefix="csk-pull-"))
        self.origin = self.root / "o.git"
        self.work = self.root / "work"
        git(["init", "--bare", "-q", str(self.origin)], self.root)
        git(["-C", str(self.origin), "symbolic-ref", "HEAD", "refs/heads/main"], self.root)
        git(["clone", "-q", str(self.origin), str(self.work)], self.root)
        self._identity(self.work)
        git(["commit", "--allow-empty", "-qm", "init"], self.work)
        git(["branch", "-M", "main"], self.work)
        git(["push", "-qu", "origin", "main"], self.work)

    def tearDown(self) -> None:
        shutil.rmtree(self.root, onerror=_force_remove)

    @staticmethod
    def _identity(repo: Path) -> None:
        git(["config", "user.email", "t@test.local"], repo)
        git(["config", "user.name", "T"], repo)

    def pull(self, cwd: Path, *flags: str) -> subprocess.CompletedProcess:
        return run([sys.executable, str(SCRIPT), *flags], cwd)

    def merge_via_pr(self, branch: str) -> Path:
        """Simulate a pull-request merge (real merge commit) in a fresh clone."""
        merger = self.root / "merger"
        if not merger.exists():
            git(["clone", "-q", str(self.origin), str(merger)], self.root)
            self._identity(merger)
        else:
            git(["fetch", "-q", "origin"], merger)
            git(["pull", "-q", "origin", "main"], merger)
        git(
            ["merge", "-q", "--no-ff", "--no-edit", "-m",
             f"Merge pull request #1 from {branch}", f"origin/{branch}"],
            merger,
        )
        git(["push", "-q", "origin", "main"], merger)
        return merger

    def add_worker(self) -> Path:
        worker = self.root / "work-codex"
        git(
            ["-C", str(self.work), "worktree", "add", "-q", "-b",
             "codex-workbench", str(worker), "main"],
            self.root,
        )
        return worker

    # --- Mode A -----------------------------------------------------------

    def test_mode_a_noop_and_ahead_are_reported_honestly(self) -> None:
        result = self.pull(self.work)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("already up to date", result.stdout)

        git(["commit", "--allow-empty", "-qm", "local only"], self.work)
        result = self.pull(self.work)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("AHEAD", result.stdout)

    def test_mode_a_fast_forwards_pr_merge_and_gates_direct_push(self) -> None:
        worker = self.add_worker()
        self._identity(worker)
        (worker / "f.txt").write_text("x\n", encoding="utf-8")
        git(["add", "f.txt"], worker)
        git(["commit", "-qm", "feat: work"], worker)
        git(["push", "-qu", "origin", "codex-workbench"], worker)
        merger = self.merge_via_pr("codex-workbench")

        result = self.pull(self.work)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("merge commit(s) included", result.stdout)

        (merger / "d.txt").write_text("d\n", encoding="utf-8")
        git(["add", "d.txt"], merger)
        git(["commit", "-qm", "direct push"], merger)
        git(["push", "-q", "origin", "main"], merger)

        gated = self.pull(self.work)
        self.assertEqual(2, gated.returncode)
        self.assertIn("MERGE-COMMIT-GATE", gated.stdout)

        overridden = self.pull(self.work, "--allow-non-merge-ff")
        self.assertEqual(0, overridden.returncode, overridden.stderr)
        self.assertIn("--allow-non-merge-ff", overridden.stdout)

    # --- Mode B -----------------------------------------------------------

    def test_mode_b_blocks_unmerged_commits_then_resyncs_and_heals(self) -> None:
        worker = self.add_worker()
        self._identity(worker)
        (worker / "f.txt").write_text("x\n", encoding="utf-8")
        git(["add", "f.txt"], worker)
        git(["commit", "-qm", "feat: work"], worker)
        git(["push", "-qu", "origin", "codex-workbench"], worker)

        blocked = self.pull(worker)
        self.assertEqual(1, blocked.returncode)
        self.assertIn("pull request", blocked.stderr)

        self.merge_via_pr("codex-workbench")
        # Simulate the host's "automatically delete head branches" setting.
        git(["push", "-q", "origin", "--delete", "codex-workbench"], self.work)

        resynced = self.pull(worker)
        self.assertEqual(0, resynced.returncode, resynced.stderr)
        self.assertIn("re-synced", resynced.stdout)
        self.assertIn("restored", resynced.stdout)

        worker_tip = git(["rev-parse", "HEAD"], worker).stdout.strip()
        remote = git(["ls-remote", "--heads", "origin", "codex-workbench"], worker)
        self.assertIn(worker_tip, remote.stdout)

        noop = self.pull(worker)
        self.assertEqual(0, noop.returncode, noop.stderr)
        self.assertIn("already at", noop.stdout)

    # --- Shared guards ------------------------------------------------------

    def test_foreign_branch_and_dirty_tree_block(self) -> None:
        git(["switch", "-qc", "feature/x"], self.work)
        blocked = self.pull(self.work)
        self.assertEqual(1, blocked.returncode)
        self.assertIn("neither the default branch", blocked.stderr)
        git(["switch", "-q", "main"], self.work)

        tracked = self.work / "tracked.txt"
        tracked.write_text("v1\n", encoding="utf-8")
        git(["add", "tracked.txt"], self.work)
        git(["commit", "-qm", "chore: tracked"], self.work)
        tracked.write_text("v2\n", encoding="utf-8")
        dirty = self.pull(self.work)
        self.assertEqual(1, dirty.returncode)
        self.assertIn("uncommitted tracked changes", dirty.stderr)


if __name__ == "__main__":
    unittest.main()
