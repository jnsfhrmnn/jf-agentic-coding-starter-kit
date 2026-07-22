---
name: finish-branch
description: "Safely complete a feature, fix, or release branch after its work is verified. Use when productive work on a non-default Git branch is ready to be intentionally committed, pushed, reviewed, merged, and optionally cleaned up; when the user asks to finish, close, merge, publish, or wrap up a branch; or when a CSK skill exits with verified branch work. Handles dirty trees, detached HEAD, worktrees, base drift, checks, pull requests, partial failures, and task closure without force-pushing or silently deleting branches. Protected worker branches from .csk/worktrees.json are never deleted; they integrate through a real merge commit and are re-synced onto the new default branch instead."
---

<!--
CODEX-CLAUDE-SKILL-PROXY
canonical_claude_skill: .claude/skills/finish-branch/SKILL.md
contract_sha256: 0b449331000a3723ccd19b96132a18dd03bdd3c75bf96dbfb1c812a656741dec
source_kind: repo
proxy_schema_version: 1
generated_by: .claude/skills/claude-skill-proxy-sync/scripts/sync_claude_skill_proxies.py
-->

# Claude Skill Proxy: Finish Branch

This is a generated thin Codex proxy. The canonical implementation remains in
`.claude/skills/finish-branch/SKILL.md` inside this repository.

## Runtime Instructions

1. Resolve the current Git repository root; do not use the proxy generator's
   machine or path.
2. Read `<repo>/.claude/skills/finish-branch/SKILL.md` completely before taking task action.
3. Follow that canonical skill as the authoritative workflow.
4. Resolve its relative scripts, references, and assets from
   `<repo>/.claude/skills/finish-branch/`.
5. Keep all kit skills repository-local. Never install, copy, or fall back to a
   user-global Claude or Codex skill directory.
6. If the canonical file is absent, stop and report the missing repo file.

Ordinary canonical body and resource changes are live. Regenerate this proxy only
after inventory, frontmatter trigger, or interface metadata changes.
