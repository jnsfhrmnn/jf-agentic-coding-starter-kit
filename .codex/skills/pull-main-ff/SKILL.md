---
name: pull-main-ff
description: "Context-sensitive safe sync with origin - one command for both sides of the worker-worktree cycle. On the default branch (main/master) it fast-forwards from origin; on a protected worker branch (*-workbench or .csk/worktrees.json) it re-syncs the branch onto the new default and fast-forward-pushes the remote ref, restoring it after host auto-delete. Use after a pull-request merge, when the user says their branch or main is behind, or as the sync step of the parallel-worktree cycle (both sides). Never switches branches, never creates a merge commit, blocks on uncommitted tracked changes and on unmerged worker commits, and stops with a MERGE-COMMIT-GATE when incoming commits bypassed the pull-request door."
---

<!--
CODEX-CLAUDE-SKILL-PROXY
canonical_claude_skill: .claude/skills/pull-main-ff/SKILL.md
contract_sha256: ea5f7a916db792d5405dacf7fdd0e370637b9e8b79e97ecad96059cda88ae488
source_kind: repo
proxy_schema_version: 1
generated_by: .claude/skills/claude-skill-proxy-sync/scripts/sync_claude_skill_proxies.py
-->

# Claude Skill Proxy: Pull Main Ff

This is a generated thin Codex proxy. The canonical implementation remains in
`.claude/skills/pull-main-ff/SKILL.md` inside this repository.

## Runtime Instructions

1. Resolve the current Git repository root; do not use the proxy generator's
   machine or path.
2. Read `<repo>/.claude/skills/pull-main-ff/SKILL.md` completely before taking task action.
3. Follow that canonical skill as the authoritative workflow.
4. Resolve its relative scripts, references, and assets from
   `<repo>/.claude/skills/pull-main-ff/`.
5. Keep all kit skills repository-local. Never install, copy, or fall back to a
   user-global Claude or Codex skill directory.
6. If the canonical file is absent, stop and report the missing repo file.

Ordinary canonical body and resource changes are live. Regenerate this proxy only
after inventory, frontmatter trigger, or interface metadata changes.
