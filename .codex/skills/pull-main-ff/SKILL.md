---
name: pull-main-ff
description: "Safely update the local default branch (main/master) strictly by fast-forward from origin after a pull-request merge. Use after a worker or feature branch was merged, when the user says the local main is behind, or in the orchestrator step of the parallel-worktree cycle. Never switches branches, never creates a merge commit, blocks on uncommitted tracked changes, and stops with a MERGE-COMMIT-GATE when the incoming commits did not arrive through a pull-request merge."
---

<!--
CODEX-CLAUDE-SKILL-PROXY
canonical_claude_skill: .claude/skills/pull-main-ff/SKILL.md
contract_sha256: 016888ffccac522084dbe06ac1d2a20ff9526fc9ee99f1b757533d10f5ea24ed
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
