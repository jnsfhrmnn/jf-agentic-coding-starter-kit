#!/usr/bin/env python3
"""Repository-level contract tests for the CSK workflow."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[4]


def read(relative: str) -> str:
    return (REPO / relative).read_text(encoding="utf-8-sig")


class WorkflowContractTests(unittest.TestCase):
    def test_project_state_and_task_schema_are_tracked_contracts(self) -> None:
        state = json.loads(read(".csk/project-state.json"))
        self.assertEqual(1, state["schema_version"])
        role = state["repository_role"]
        mode = state["onboarding"]["mode"]
        adoption = state["onboarding"]["adoption_status"]
        self.assertIn(role, {"template", "project"})
        if role == "template":
            self.assertEqual(("pending", "not-assessed"), (mode, adoption))
        else:
            self.assertIn(
                (mode, adoption),
                {
                    ("pending", "not-assessed"),
                    ("greenfield", "not-applicable"),
                    ("adopt", "pending"),
                    ("adopt", "complete"),
                    ("adopt", "blocked"),
                },
            )
        tasks = read("tasks/INDEX.md")
        self.assertIn(
            "| ID | Status | Priority | Related | Expected branch | Resume skill | Task | Next action | Blocker | Updated |",
            tasks,
        )
        self.assertIn("live Git state is authoritative", tasks)
        self.assertTrue((REPO / ".claude/skills/csk-start/scripts/csk-start.ps1").is_file())
        self.assertTrue((REPO / ".claude/skills/csk-start/scripts/csk-start.sh").is_file())

    def test_all_workflow_consumers_reference_the_transition_ssot(self) -> None:
        consumers = [
            "CLAUDE.md",
            "AGENTS.md",
            ".claude/skills/csk-help/SKILL.md",
            *[f".claude/skills/{number}-csk-{name}/SKILL.md" for number, name in (
                (1, "init"),
                (2, "write-spec"),
                (3, "architecture"),
                (4, "frontend"),
                (5, "backend"),
                (6, "qa"),
                (7, "deploy"),
            )],
        ]
        for relative in consumers:
            with self.subTest(relative=relative):
                self.assertIn("workflow-state.md", read(relative))

        workflow = read(".claude/rules/workflow-state.md")
        for status in (
            "Roadmap", "Planned", "Architected", "In Progress",
            "In Review", "Approved", "Deployed", "Cancelled",
        ):
            self.assertIn(f"`{status}`", workflow)

    def test_branch_lifecycle_banners_and_feature_gate_are_present(self) -> None:
        workflow = read(".claude/rules/workflow-state.md")
        self.assertIn("## Branch lifecycle", workflow)
        for number, name in (
            (1, "init"), (2, "write-spec"), (3, "architecture"),
            (4, "frontend"), (5, "backend"), (6, "qa"), (7, "deploy"),
        ):
            with self.subTest(skill=f"{number}-csk-{name}"):
                skill = read(f".claude/skills/{number}-csk-{name}/SKILL.md")
                self.assertIn("## Step Banner", skill)
        architecture = read(".claude/skills/3-csk-architecture/SKILL.md")
        self.assertIn("## Feature Collection Gate", architecture)
        for name in ("4-csk-frontend", "5-csk-backend"):
            with self.subTest(skill=name):
                skill = read(f".claude/skills/{name}/SKILL.md")
                self.assertIn("branch gate", skill)
                self.assertIn("Checkpoint Commit", skill)

    def test_release_orders_both_reviews_around_external_action(self) -> None:
        deploy = read(".claude/skills/7-csk-deploy/SKILL.md")
        readiness = deploy.index("Phase 2: Readiness review")
        execute = deploy.index("Phase 3: Execute")
        final_review = deploy.index("Phase 5: Final review")
        bookkeeping = deploy.index("Phase 6: Bookkeeping")
        self.assertLess(readiness, execute)
        self.assertLess(execute, final_review)
        self.assertLess(final_review, bookkeeping)
        required_tag = deploy.index("If the approved release process requires a Git tag")
        deployed_update = deploy.index("Update the feature spec and feature index together to `Deployed`")
        self.assertLess(required_tag, deployed_update)

    def test_qa_remediation_routes_to_owners_without_advancing_status(self) -> None:
        qa = read(".claude/skills/6-csk-qa/SKILL.md")
        self.assertIn("Keep status `In Review`", qa)
        self.assertIn("`/4-csk-frontend`", qa)
        self.assertIn("`/5-csk-backend`", qa)
        self.assertIn("`/3-csk-architecture` or `/csk-refine`", qa)
        self.assertIn("do not create same-turn task churn", qa)

    def test_finish_branch_covers_critical_failure_states(self) -> None:
        finish = read(".claude/skills/finish-branch/SKILL.md").lower()
        for marker in (
            "detached", "multiple worktrees", "target advances", "merge conflict",
            "partially succeeds", "closed but unmerged", "checks fail or time out",
            "cleanup fails", "never force-push", "explicitly approved branch targets",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, finish)

    def test_settings_do_not_preapprove_git_mutations(self) -> None:
        settings = json.loads(read(".claude/settings.json"))
        allowed = settings["permissions"]["allow"]
        for fragment in ("git commit", "git push", "git tag", "git merge"):
            self.assertFalse(any(fragment in entry for entry in allowed), fragment)

    def test_every_canonical_skill_has_a_portable_codex_proxy(self) -> None:
        canonical_root = REPO / ".claude" / "skills"
        names = sorted(path.parent.name for path in canonical_root.glob("*/SKILL.md"))
        self.assertIn("finish-branch", names)
        for name in names:
            with self.subTest(name=name):
                proxy = read(f".codex/skills/{name}/SKILL.md")
                self.assertIn("CODEX-CLAUDE-SKILL-PROXY", proxy)
                self.assertIn(f".claude/skills/{name}/SKILL.md", proxy)
                self.assertNotIn(str(REPO), proxy)
                self.assertNotIn("C:\\Users\\", proxy)

    def test_removed_transport_concepts_have_no_active_references(self) -> None:
        forbidden = (
            "us" + "crx",
            "enve" + "lope",
            "in" + "box",
            "out" + "box",
            "im" + "ports",
        )
        excluded_roots = {
            (".git",),
            ("docs", "audits"),
            ("docs", "plans"),
        }
        excluded_files = {"CHANGELOG.md", Path(__file__).name}
        findings: list[str] = []
        for path in REPO.rglob("*"):
            if not path.is_file() or path.name in excluded_files or "__pycache__" in path.parts:
                continue
            relative = path.relative_to(REPO)
            if any(relative.parts[: len(prefix)] == prefix for prefix in excluded_roots):
                continue
            try:
                text = path.read_text(encoding="utf-8-sig").lower()
            except (UnicodeDecodeError, OSError):
                continue
            for term in forbidden:
                if term in text:
                    findings.append(f"{relative.as_posix()}: {term}")
        self.assertEqual([], findings)


if __name__ == "__main__":
    unittest.main()
