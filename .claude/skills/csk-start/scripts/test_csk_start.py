#!/usr/bin/env python3
"""Tests for the deterministic repository-local CSK start tool."""

from __future__ import annotations

import argparse
import io
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock


MODULE_PATH = Path(__file__).with_name("csk_start.py")
SPEC = importlib.util.spec_from_file_location("csk_start", MODULE_PATH)
assert SPEC and SPEC.loader
CSK = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CSK
SPEC.loader.exec_module(CSK)


STATE = {
    "schema_version": 1,
    "repository_role": "template",
    "onboarding": {
        "mode": "pending",
        "adoption_status": "not-assessed",
        "decided_at": None,
        "scaffold_evidence": None,
    },
}

TASKS = """# Open Work Index

<!-- next-id: TASK-001 -->

| ID | Status | Priority | Related | Expected branch | Resume skill | Task | Next action | Blocker | Updated |
|---|---|---|---|---|---|---|---|---|---|

Completed rows are removed after evidence is recorded.
"""


def ns(**values):
    return argparse.Namespace(**values)


class CskStartTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name).resolve()
        subprocess.run(["git", "init", "-q", "-b", "main", str(self.repo)], check=True)
        (self.repo / ".claude" / "skills" / "csk-start").mkdir(parents=True)
        (self.repo / ".claude" / "skills" / "csk-start" / "SKILL.md").write_text(
            "---\nname: csk-start\ndescription: test\n---\n", encoding="utf-8"
        )
        (self.repo / ".codex" / "skills" / "csk-start").mkdir(parents=True)
        (self.repo / ".codex" / "skills" / "csk-start" / "SKILL.md").write_text(
            "---\nname: csk-start\ndescription: test proxy\n---\n", encoding="utf-8"
        )
        (self.repo / ".csk").mkdir()
        (self.repo / ".csk" / "project-state.json").write_text(
            json.dumps(STATE, indent=2) + "\n", encoding="utf-8"
        )
        (self.repo / "tasks").mkdir()
        (self.repo / "tasks" / "INDEX.md").write_text(TASKS, encoding="utf-8")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def state(self):
        return json.loads((self.repo / ".csk" / "project-state.json").read_text(encoding="utf-8"))

    def task_args(self, **overrides):
        values = {
            "operation": "add",
            "status": "open",
            "priority": "high",
            "related": "PROJ-1",
            "expected_branch": "feature/proj-1",
            "resume_skill": "csk-start",
            "task": "Finish core behavior",
            "next_action": "Run the focused test",
            "blocker": None,
        }
        values.update(overrides)
        return ns(**values)

    def write_adoption_fixture(self, *, include_source: bool = True, feature_row: bool = True) -> Path:
        (self.repo / "features").mkdir(exist_ok=True)
        feature_text = "# Adopt scaffold\n"
        if feature_row:
            feature_text += "\n| PROJ-1 | Adopted capability | Roadmap | - | 2026-07-18 |\n"
        (self.repo / "features" / "INDEX.md").write_text(feature_text, encoding="utf-8")
        (self.repo / "legacy-plan.md").write_text("# Legacy plan\n", encoding="utf-8")
        sources = []
        if include_source:
            sources.append({
                "path": "legacy-plan.md",
                "feature_ids": ["PROJ-1"],
                "non_feature_reason": None,
            })
        report = {
            "schema_version": 1,
            "feature_index": "features/INDEX.md",
            "sources": sources,
        }
        path = self.repo / ".csk" / "adoption-coverage.json"
        path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        return path

    def test_pending_state_is_valid(self) -> None:
        state, _ = CSK.load_state(self.repo)
        self.assertEqual("pending", state["onboarding"]["mode"])

    def test_template_distribution_guard_is_explicit_and_strict(self) -> None:
        with self.assertRaises(CSK.CskError):
            CSK.command_state(self.repo, ns(operation="check-template-distribution", snapshot="HEAD"))
        subprocess.run(["git", "-C", str(self.repo), "config", "user.name", "CSK Test"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "config", "user.email", "csk@example.invalid"], check=True)
        subprocess.run(
            ["git", "-C", str(self.repo), "add", ".csk/project-state.json"], check=True
        )
        index_result = CSK.command_state(
            self.repo,
            ns(operation="check-template-distribution", snapshot="index"),
        )
        self.assertEqual("index", index_result["snapshot"])
        subprocess.run(
            ["git", "-C", str(self.repo), "commit", "-q", "-m", "template state"], check=True
        )
        result = CSK.command_state(
            self.repo,
            ns(operation="check-template-distribution", snapshot="HEAD"),
        )
        self.assertTrue(result["distribution_template"])
        CSK.command_state(self.repo, ns(operation="decide", mode="greenfield"))
        subprocess.run(
            ["git", "-C", str(self.repo), "add", ".csk/project-state.json"], check=True
        )
        subprocess.run(
            ["git", "-C", str(self.repo), "commit", "-q", "-m", "project state"], check=True
        )
        (self.repo / ".csk" / "project-state.json").write_text(
            json.dumps(STATE, indent=2) + "\n",
            encoding="utf-8",
        )
        with self.assertRaises(CSK.CskError):
            CSK.command_state(self.repo, ns(operation="check-template-distribution", snapshot="HEAD"))

    def test_python_runtime_gate_is_fail_closed(self) -> None:
        CSK.validate_runtime((3, 10))
        with self.assertRaises(CSK.CskError):
            CSK.validate_runtime((3, 9))

    def test_missing_or_malformed_state_fails_closed(self) -> None:
        path = self.repo / ".csk" / "project-state.json"
        path.unlink()
        with self.assertRaises(CSK.CskError):
            CSK.load_state(self.repo)
        path.write_text("{broken", encoding="utf-8")
        with self.assertRaises(CSK.CskError):
            CSK.load_state(self.repo)

    def test_blocked_state_requires_reason_and_valid_timestamp(self) -> None:
        invalid = json.loads(json.dumps(STATE))
        invalid["repository_role"] = "project"
        invalid["onboarding"].update({
            "mode": "adopt",
            "adoption_status": "blocked",
            "decided_at": "2026-07-18T10:00:00Z",
            "scaffold_evidence": None,
        })
        path = self.repo / ".csk" / "project-state.json"
        path.write_text(json.dumps(invalid), encoding="utf-8")
        with self.assertRaises(CSK.CskError):
            CSK.load_state(self.repo)
        invalid["onboarding"]["scaffold_evidence"] = {
            "reason": "Missing source",
            "blocked_at": "not-a-time",
        }
        path.write_text(json.dumps(invalid), encoding="utf-8")
        with self.assertRaises(CSK.CskError):
            CSK.load_state(self.repo)
    def test_first_decision_changes_role_and_is_not_repeatable(self) -> None:
        result = CSK.command_state(self.repo, ns(operation="decide", mode="greenfield"))
        self.assertEqual("project", result["state"]["repository_role"])
        self.assertEqual("not-applicable", result["state"]["onboarding"]["adoption_status"])
        with self.assertRaises(CSK.CskError):
            CSK.command_state(self.repo, ns(operation="decide", mode="adopt"))

    def test_state_distribution_requires_reachability_from_origin_default(self) -> None:
        CSK.command_state(self.repo, ns(operation="decide", mode="greenfield"))
        subprocess.run(["git", "-C", str(self.repo), "config", "user.name", "CSK Test"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "config", "user.email", "csk@example.invalid"], check=True)
        subprocess.run(
            ["git", "-C", str(self.repo), "add", ".csk/project-state.json"], check=True
        )
        subprocess.run(
            ["git", "-C", str(self.repo), "commit", "-q", "-m", "state"], check=True
        )
        self.assertEqual("committed-local-no-origin", CSK.state_distribution(self.repo)["status"])

        with tempfile.TemporaryDirectory() as remote_dir:
            subprocess.run(["git", "init", "-q", "--bare", remote_dir], check=True)
            subprocess.run(
                ["git", "-C", str(self.repo), "remote", "add", "origin", remote_dir], check=True
            )
            subprocess.run(
                ["git", "-C", str(self.repo), "push", "-q", "-u", "origin", "main"], check=True
            )
            shared = CSK.state_distribution(self.repo)
            self.assertEqual("origin-default", shared["status"])
            self.assertEqual("project", shared["origin_role"])
            self.assertTrue(shared["projectwide"])

            subprocess.run(
                ["git", "-C", str(self.repo), "switch", "-q", "-c", "feature/state"], check=True
            )
            state_path = self.repo / ".csk" / "project-state.json"
            state_path.write_text(state_path.read_text(encoding="utf-8") + "\n", encoding="utf-8")
            subprocess.run(
                ["git", "-C", str(self.repo), "add", ".csk/project-state.json"], check=True
            )
            subprocess.run(
                ["git", "-C", str(self.repo), "commit", "-q", "-m", "branch state"], check=True
            )
            branch_only = CSK.state_distribution(self.repo)
            self.assertEqual("committed-not-on-origin-default", branch_only["status"])
            self.assertFalse(branch_only["projectwide"])

    def test_known_source_origin_is_never_projectwide(self) -> None:
        subprocess.run(
            [
                "git", "-C", str(self.repo), "remote", "add", "origin",
                "https://secret-token@github.com/AlexPEClub/ai-coding-starter-kit.git?token=hidden",
            ],
            check=True,
        )
        distribution = CSK.state_distribution(self.repo)
        self.assertEqual("source-template", distribution["origin_role"])
        self.assertFalse(distribution["projectwide"])
        self.assertNotIn("secret-token", distribution["origin_url"])
        self.assertNotIn("hidden", distribution["origin_url"])

    def test_explicit_recheck_returns_project_to_pending(self) -> None:
        CSK.command_state(self.repo, ns(operation="decide", mode="greenfield"))
        result = CSK.command_state(self.repo, ns(operation="recheck"))
        self.assertEqual("project", result["state"]["repository_role"])
        self.assertEqual("pending", result["state"]["onboarding"]["mode"])

    def test_adoption_requires_positive_complete_coverage(self) -> None:
        CSK.command_state(self.repo, ns(operation="decide", mode="adopt"))
        self.write_adoption_fixture(include_source=False)
        with self.assertRaises(CSK.CskError):
            CSK.command_state(
                self.repo,
                ns(operation="adoption-complete", coverage_report=".csk/adoption-coverage.json"),
            )
        self.write_adoption_fixture()
        result = CSK.command_state(
            self.repo,
            ns(operation="adoption-complete", coverage_report=".csk/adoption-coverage.json"),
        )
        self.assertEqual("complete", result["state"]["onboarding"]["adoption_status"])

    def test_adoption_rejects_empty_scaffold_despite_claimed_mapping(self) -> None:
        CSK.command_state(self.repo, ns(operation="decide", mode="adopt"))
        self.write_adoption_fixture(feature_row=False)
        with self.assertRaises(CSK.CskError):
            CSK.command_state(
                self.repo,
                ns(operation="adoption-complete", coverage_report=".csk/adoption-coverage.json"),
            )

    def test_non_inventory_coverage_source_requires_manual_relevance(self) -> None:
        CSK.command_state(self.repo, ns(operation="decide", mode="adopt"))
        (self.repo / "features").mkdir()
        (self.repo / "features" / "INDEX.md").write_text(
            "# Adopt scaffold\n\n| PROJ-1 | Product | Roadmap | - | 2026-07-18 |\n",
            encoding="utf-8",
        )
        (self.repo / "context-notes.txt").write_text("Product context notes\n", encoding="utf-8")
        report = {
            "schema_version": 1,
            "feature_index": "features/INDEX.md",
            "sources": [{
                "path": "context-notes.txt",
                "feature_ids": ["PROJ-1"],
                "non_feature_reason": None,
            }],
        }
        coverage_path = self.repo / ".csk" / "adoption-coverage.json"
        coverage_path.write_text(json.dumps(report), encoding="utf-8")
        with self.assertRaises(CSK.CskError):
            CSK.command_state(
                self.repo,
                ns(operation="adoption-complete", coverage_report=".csk/adoption-coverage.json"),
            )
        report["sources"][0]["manual_relevance_reason"] = "Notes hold the only recorded product decisions"
        coverage_path.write_text(json.dumps(report), encoding="utf-8")
        result = CSK.command_state(
            self.repo,
            ns(operation="adoption-complete", coverage_report=".csk/adoption-coverage.json"),
        )
        self.assertEqual("complete", result["state"]["onboarding"]["adoption_status"])

    def test_project_readme_is_an_inventory_candidate(self) -> None:
        (self.repo / "README.md").write_text("# Existing product\n", encoding="utf-8")
        candidates = {item["path"] for item in CSK.inventory(self.repo)["candidates"]}
        self.assertIn("README.md", candidates)

    def test_blanket_non_feature_reason_is_rejected(self) -> None:
        CSK.command_state(self.repo, ns(operation="decide", mode="adopt"))
        report_path = self.write_adoption_fixture()
        report = json.loads(report_path.read_text(encoding="utf-8"))
        report["sources"][0] = {
            "path": "legacy-plan.md",
            "feature_ids": None,
            "non_feature_reason": "x",
        }
        report_path.write_text(json.dumps(report), encoding="utf-8")
        with self.assertRaises(CSK.CskError):
            CSK.command_state(
                self.repo,
                ns(operation="adoption-complete", coverage_report=".csk/adoption-coverage.json"),
            )
        report["sources"][0]["non_feature_reason"] = (
            "historical: superseded by the 2026 roadmap rewrite"
        )
        report_path.write_text(json.dumps(report), encoding="utf-8")
        result = CSK.command_state(
            self.repo,
            ns(operation="adoption-complete", coverage_report=".csk/adoption-coverage.json"),
        )
        self.assertEqual("complete", result["state"]["onboarding"]["adoption_status"])

    def test_unmapped_inventory_candidate_blocks_completion(self) -> None:
        CSK.command_state(self.repo, ns(operation="decide", mode="adopt"))
        self.write_adoption_fixture()
        (self.repo / "src").mkdir()
        (self.repo / "src" / "engine.py").write_text("print('x')\n", encoding="utf-8")
        with self.assertRaises(CSK.CskError) as blocked:
            CSK.command_state(
                self.repo,
                ns(operation="adoption-complete", coverage_report=".csk/adoption-coverage.json"),
            )
        self.assertIn("unmapped inventory candidates", str(blocked.exception))
        self.assertIn("src/engine.py", str(blocked.exception))

    def test_inventory_covers_infrastructure_and_decision_files(self) -> None:
        (self.repo / "schema.sql").write_text("CREATE TABLE t (id INT);\n", encoding="utf-8")
        (self.repo / "deploy.yml").write_text("jobs: {}\n", encoding="utf-8")
        (self.repo / "Dockerfile").write_text("FROM scratch\n", encoding="utf-8")
        (self.repo / "docs").mkdir(exist_ok=True)
        (self.repo / "docs" / "adr-001-storage.md").write_text("# ADR\n", encoding="utf-8")
        candidates = {item["path"] for item in CSK.inventory(self.repo)["candidates"]}
        for expected in ("schema.sql", "deploy.yml", "Dockerfile", "docs/adr-001-storage.md"):
            self.assertIn(expected, candidates)

    def test_missing_completed_scaffold_can_transition_to_blocked(self) -> None:
        CSK.command_state(self.repo, ns(operation="decide", mode="adopt"))
        self.write_adoption_fixture()
        feature_index = self.repo / "features" / "INDEX.md"
        CSK.command_state(
            self.repo,
            ns(operation="adoption-complete", coverage_report=".csk/adoption-coverage.json"),
        )
        feature_index.unlink()
        checked = CSK.command_state(self.repo, ns(operation="check"))
        self.assertFalse(checked["valid"])
        self.assertEqual(1, len(checked["drift"]))
        with redirect_stdout(io.StringIO()):
            exit_code = CSK.main(["--repo", str(self.repo), "state", "check"])
        self.assertEqual(3, exit_code)
        blocked = CSK.command_state(
            self.repo,
            ns(operation="adoption-block", reason="Scaffold evidence disappeared"),
        )
        self.assertEqual("blocked", blocked["state"]["onboarding"]["adoption_status"])

    def test_changed_coverage_report_is_detected_as_drift(self) -> None:
        CSK.command_state(self.repo, ns(operation="decide", mode="adopt"))
        report = self.write_adoption_fixture()
        CSK.command_state(
            self.repo,
            ns(operation="adoption-complete", coverage_report=".csk/adoption-coverage.json"),
        )
        report.write_text(report.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        checked = CSK.command_state(self.repo, ns(operation="check"))
        self.assertFalse(checked["valid"])
        self.assertIn("coverage report changed", checked["drift"][0])

    def test_inventory_excludes_kit_templates_and_finds_code_and_plans(self) -> None:
        (self.repo / "docs").mkdir()
        (self.repo / "docs" / "architecture.md").write_text("# Architecture\n_Not chosen yet._\n", encoding="utf-8")
        (self.repo / "src").mkdir()
        (self.repo / "src" / "main.py").write_text("print('ok')\n", encoding="utf-8")
        (self.repo / "product-roadmap.md").write_text("# Existing roadmap\n", encoding="utf-8")
        (self.repo / "features").mkdir()
        (self.repo / "features" / "INDEX.md").write_text("# Existing features\n", encoding="utf-8")
        result = CSK.inventory(self.repo)
        self.assertEqual(3, result["candidate_count"])
        self.assertEqual({"implementation": 1, "project-evidence": 2}, result["counts"])

    def test_task_lifecycle_and_evidence_gate(self) -> None:
        created = CSK.mutate_tasks(self.repo, "add", self.task_args())
        self.assertEqual("TASK-001", created["created"])
        parsed, _ = CSK.load_tasks(self.repo)
        self.assertEqual("TASK-002", f"TASK-{parsed['next_id']:03d}")
        CSK.mutate_tasks(
            self.repo,
            "block",
            ns(operation="block", id="TASK-001", reason="Endpoint unavailable", next_action="Restore access"),
        )
        with self.assertRaises(CSK.CskError):
            CSK.mutate_tasks(
                self.repo,
                "close",
                ns(operation="close", id="TASK-001", evidence="commit:not-a-real-sha", evidence_record=None),
            )
        with self.assertRaises(CSK.CskError):
            CSK.mutate_tasks(
                self.repo,
                "close",
                ns(operation="close", id="TASK-001", evidence="test:integration-smoke", evidence_record=None),
            )
        (self.repo / "qa-evidence.md").write_text("Passed: integration-smoke\n", encoding="utf-8")
        CSK.mutate_tasks(
            self.repo,
            "close",
            ns(
                operation="close", id="TASK-001", evidence="test:integration-smoke",
                evidence_record="qa-evidence.md",
            ),
        )
        parsed, _ = CSK.load_tasks(self.repo)
        self.assertEqual([], parsed["rows"])

    def test_invalid_update_is_rejected_before_file_write(self) -> None:
        CSK.mutate_tasks(self.repo, "add", self.task_args(expected_branch="main"))
        before = (self.repo / "tasks" / "INDEX.md").read_bytes()
        with self.assertRaises(CSK.CskError):
            CSK.mutate_tasks(
                self.repo,
                "update",
                ns(
                    operation="update", id="TASK-001", status="blocked", priority=None,
                    related=None, expected_branch=None, resume_skill=None, task=None,
                    next_action=None, blocker=None,
                ),
            )
        self.assertEqual(before, (self.repo / "tasks" / "INDEX.md").read_bytes())

    def test_invalid_branch_missing_related_path_and_calendar_date_fail_closed(self) -> None:
        before = (self.repo / "tasks" / "INDEX.md").read_bytes()
        with self.assertRaises(CSK.CskError):
            CSK.mutate_tasks(self.repo, "add", self.task_args(expected_branch="bad branch"))
        with self.assertRaises(CSK.CskError):
            CSK.mutate_tasks(self.repo, "add", self.task_args(related="docs/missing.md"))
        with self.assertRaises(CSK.CskError):
            CSK.mutate_tasks(self.repo, "add", self.task_args(resume_skill="missing-skill"))
        self.assertEqual(before, (self.repo / "tasks" / "INDEX.md").read_bytes())

        invalid_date = TASKS.replace(
            "<!-- next-id: TASK-001 -->",
            "<!-- next-id: TASK-002 -->",
        ).replace(
            "|---|---|---|---|---|---|---|---|---|---|",
            "|---|---|---|---|---|---|---|---|---|---|\n"
            "| TASK-001 | open | high | PROJ-1 | main | direct | Work | Continue | - | 2026-02-31 |",
        )
        with self.assertRaises(CSK.CskError):
            CSK.parse_tasks(invalid_date.encode("utf-8"))

    def test_task_like_row_outside_table_fails_closed(self) -> None:
        misplaced = TASKS.replace(
            "<!-- next-id: TASK-001 -->",
            "<!-- next-id: TASK-002 -->",
        ) + "\n| TASK-001 | open | high | PROJ-1 | main | direct | Hidden | Continue | - | 2026-07-18 |\n"
        with self.assertRaises(CSK.CskError):
            CSK.parse_tasks(misplaced.encode("utf-8"))

    def test_branch_context_is_advisory_warning(self) -> None:
        CSK.mutate_tasks(self.repo, "add", self.task_args())
        parsed, _ = CSK.load_tasks(self.repo)
        warnings = CSK.branch_warnings(self.repo, parsed["rows"])
        self.assertEqual(1, len(warnings))

    def test_lock_and_digest_cas_refuse_lost_updates(self) -> None:
        lock = self.repo / ".csk" / "csk-start.lock"
        lock.write_text("busy", encoding="utf-8")
        with self.assertRaises(CSK.CskError):
            with CSK.repository_lock(self.repo):
                pass
        lock.unlink()
        target = self.repo / "tasks" / "INDEX.md"
        original = target.read_bytes()
        target.write_text(TASKS + "external\n", encoding="utf-8")
        with self.assertRaises(CSK.CskError):
            CSK.durable_replace(self.repo, target, original, CSK._sha256(original))

    def test_interrupted_replace_preserves_target_and_cleans_temp_file(self) -> None:
        target = self.repo / "tasks" / "INDEX.md"
        original = target.read_bytes()
        with mock.patch.object(CSK.os, "replace", side_effect=OSError("interrupted")):
            with self.assertRaises(OSError):
                CSK.durable_replace(
                    self.repo,
                    target,
                    original + b"new\n",
                    CSK._sha256(original),
                )
        self.assertEqual(original, target.read_bytes())
        self.assertEqual([], list((self.repo / ".csk").glob("csk-start-*.tmp")))

    def test_utf8_bom_state_and_tasks_are_accepted(self) -> None:
        state_path = self.repo / ".csk" / "project-state.json"
        state_path.write_bytes(b"\xef\xbb\xbf" + json.dumps(STATE).encode("utf-8"))
        state, _ = CSK.load_state(self.repo)
        self.assertEqual("template", state["repository_role"])
        tasks_path = self.repo / "tasks" / "INDEX.md"
        tasks_path.write_bytes(b"\xef\xbb\xbf" + TASKS.encode("utf-8"))
        parsed, _ = CSK.load_tasks(self.repo)
        self.assertEqual([], parsed["rows"])

    @unittest.skipIf(not hasattr(os, "symlink"), "symlinks unavailable")
    def test_symlink_escape_is_rejected(self) -> None:
        outside = Path(self.temp.name).parent / f"outside-{os.getpid()}"
        outside.mkdir(exist_ok=True)
        link = self.repo / "outside-link"
        try:
            os.symlink(outside, link, target_is_directory=True)
        except OSError:
            self.skipTest("symlink creation is not permitted")
        try:
            with self.assertRaises(CSK.CskError):
                CSK.safe_path(self.repo, Path("outside-link/file.txt"))
        finally:
            link.unlink(missing_ok=True)
            outside.rmdir()


if __name__ == "__main__":
    unittest.main()
