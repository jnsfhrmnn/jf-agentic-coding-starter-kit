#!/usr/bin/env python3
"""Tests for the repository-local Claude-to-Codex proxy generator."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("sync_claude_skill_proxies.py")
SPEC = importlib.util.spec_from_file_location("sync_claude_skill_proxies", MODULE_PATH)
assert SPEC and SPEC.loader
SYNC = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = SYNC
SPEC.loader.exec_module(SYNC)


class ProxySyncTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name).resolve()
        (self.repo / ".claude" / "skills").mkdir(parents=True)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def add_skill(self, name: str = "example-skill", description: str = "Use this example skill for realistic repository work.", body: str = "First body.") -> Path:
        skill_dir = self.repo / ".claude" / "skills" / name
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: {description}\n---\n\n# Example\n\n{body}\n",
            encoding="utf-8",
        )
        return skill_dir

    def sync(self) -> list:
        plan, expected = SYNC.plan_sync(self.repo)
        SYNC.apply_plan(self.repo, plan, expected, prune=False)
        return plan

    def test_apply_creates_portable_repo_relative_proxy(self) -> None:
        self.add_skill()
        self.sync()
        proxy = (self.repo / ".codex" / "skills" / "example-skill" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("canonical_claude_skill: .claude/skills/example-skill/SKILL.md", proxy)
        self.assertNotIn(str(self.repo), proxy)
        self.assertIn("Never install, copy, or fall back", proxy)

    def test_body_only_change_is_live_and_does_not_require_sync(self) -> None:
        skill = self.add_skill()
        self.sync()
        source = skill / "SKILL.md"
        source.write_text(source.read_text(encoding="utf-8").replace("First body.", "Second body."), encoding="utf-8")
        plan, _ = SYNC.plan_sync(self.repo)
        self.assertEqual(["ok"], [item.action for item in plan])

    def test_description_change_requires_update(self) -> None:
        skill = self.add_skill()
        self.sync()
        source = skill / "SKILL.md"
        source.write_text(source.read_text(encoding="utf-8").replace("realistic repository work", "portable repository work"), encoding="utf-8")
        plan, _ = SYNC.plan_sync(self.repo)
        self.assertEqual(["update"], [item.action for item in plan])

    def test_interface_metadata_change_requires_update(self) -> None:
        skill = self.add_skill()
        agents = skill / "agents"
        agents.mkdir()
        metadata = agents / "openai.yaml"
        metadata.write_text(
            'interface:\n  display_name: "Example One"\n  short_description: "Run the example repository workflow"\n  default_prompt: "Use $example-skill for this task."\n',
            encoding="utf-8",
        )
        self.sync()
        metadata.write_text(metadata.read_text(encoding="utf-8").replace("Example One", "Example Two"), encoding="utf-8")
        plan, _ = SYNC.plan_sync(self.repo)
        self.assertEqual(["update"], [item.action for item in plan])

    def test_unmanaged_codex_skill_is_never_overwritten(self) -> None:
        self.add_skill()
        target = self.repo / ".codex" / "skills" / "example-skill"
        target.mkdir(parents=True)
        unmanaged = "---\nname: example-skill\ndescription: User owned.\n---\n"
        (target / "SKILL.md").write_text(unmanaged, encoding="utf-8")
        plan, expected = SYNC.plan_sync(self.repo)
        self.assertEqual("conflict", plan[0].action)
        SYNC.apply_plan(self.repo, plan, expected, prune=False)
        self.assertEqual(unmanaged, (target / "SKILL.md").read_text(encoding="utf-8"))

    def test_stale_proxy_requires_explicit_prune(self) -> None:
        skill = self.add_skill()
        self.sync()
        (skill / "SKILL.md").unlink()
        skill.rmdir()
        plan, expected = SYNC.plan_sync(self.repo)
        self.assertEqual("stale", plan[0].action)
        SYNC.apply_plan(self.repo, plan, expected, prune=False)
        target = self.repo / ".codex" / "skills" / "example-skill"
        self.assertTrue(target.exists())
        SYNC.apply_plan(self.repo, plan, expected, prune=True)
        self.assertFalse(target.exists())

    def test_prune_refuses_generated_target_with_unmanaged_file(self) -> None:
        skill = self.add_skill()
        self.sync()
        target = self.repo / ".codex" / "skills" / "example-skill"
        (target / "notes.txt").write_text("user-owned", encoding="utf-8")
        (skill / "SKILL.md").unlink()
        skill.rmdir()
        plan, _ = SYNC.plan_sync(self.repo)
        self.assertEqual("conflict", plan[0].action)
        self.assertTrue((target / "notes.txt").exists())

    def test_selected_unknown_skill_fails(self) -> None:
        self.add_skill()
        with self.assertRaises(SYNC.SyncError):
            SYNC.plan_sync(self.repo, {"missing-skill"})


if __name__ == "__main__":
    unittest.main()
