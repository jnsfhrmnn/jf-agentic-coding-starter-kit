---
name: create-worker-worktree
description: "Create one permanent worker worktree so a second agent session can work in parallel without touching the main working copy. Use when a second session should open on the same repository, when the session guard reports another active session, when the user asks for parallel agents, a Codex/Claude worker, or a worktree, or when two sessions keep disturbing each other's files, index, or branch. Creates <repo>-<worker> on the protected branch <worker>-workbench from the default branch and registers it in .csk/worktrees.json."
---

<!--
CODEX-CLAUDE-SKILL-PROXY
canonical_claude_skill: .claude/skills/create-worker-worktree/SKILL.md
contract_sha256: 9017e50aea098b97940de03c25fc6ae7ba117114bd100cdc079cc8cf1dade6a2
source_kind: repo
proxy_schema_version: 1
generated_by: .claude/skills/claude-skill-proxy-sync/scripts/sync_claude_skill_proxies.py
-->

# Claude Skill Proxy: Create Worker Worktree

This is a generated thin Codex proxy. The canonical implementation remains in
`.claude/skills/create-worker-worktree/SKILL.md` inside this repository.

## Runtime Instructions

1. Resolve the current Git repository root; do not use the proxy generator's
   machine or path.
2. Read `<repo>/.claude/skills/create-worker-worktree/SKILL.md` completely before taking task action.
3. Follow that canonical skill as the authoritative workflow.
4. Resolve its relative scripts, references, and assets from
   `<repo>/.claude/skills/create-worker-worktree/`.
5. Keep all kit skills repository-local. Never install, copy, or fall back to a
   user-global Claude or Codex skill directory.
6. If the canonical file is absent, stop and report the missing repo file.

Ordinary canonical body and resource changes are live. Regenerate this proxy only
after inventory, frontmatter trigger, or interface metadata changes.
