---
name: claude-skill-proxy-sync
description: "Synchronize canonical repository-local Claude skills from .claude/skills into portable thin Codex proxies under .codex/skills. Use after adding, renaming, moving, or removing a local skill, or after changing its YAML trigger description or agents/openai.yaml interface metadata. Do not use for ordinary SKILL.md body edits because Codex reads the canonical Claude file at runtime."
---

<!--
CODEX-CLAUDE-SKILL-PROXY
canonical_claude_skill: .claude/skills/claude-skill-proxy-sync/SKILL.md
contract_sha256: 668c55f07c0b79aff073178a34af3f806806c3f5156b2ec9b7b5ce784155992d
source_kind: repo
proxy_schema_version: 1
generated_by: .claude/skills/claude-skill-proxy-sync/scripts/sync_claude_skill_proxies.py
-->

# Claude Skill Proxy: Claude Skill Proxy Sync

This is a generated thin Codex proxy. The canonical implementation remains in
`.claude/skills/claude-skill-proxy-sync/SKILL.md` inside this repository.

## Runtime Instructions

1. Resolve the current Git repository root; do not use the proxy generator's
   machine or path.
2. Read `<repo>/.claude/skills/claude-skill-proxy-sync/SKILL.md` completely before taking task action.
3. Follow that canonical skill as the authoritative workflow.
4. Resolve its relative scripts, references, and assets from
   `<repo>/.claude/skills/claude-skill-proxy-sync/`.
5. Keep all kit skills repository-local. Never install, copy, or fall back to a
   user-global Claude or Codex skill directory.
6. If the canonical file is absent, stop and report the missing repo file.

Ordinary canonical body and resource changes are live. Regenerate this proxy only
after inventory, frontmatter trigger, or interface metadata changes.
