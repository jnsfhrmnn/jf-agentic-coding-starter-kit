---
name: csk-adopt-plan-scaffold
description: "Exhaustive repository-local CSK adoption workflow for an existing codebase or project with implementation, plans, roadmaps, audits, backlogs, architecture, requirements, tests, handoffs, or product sources of truth. Use when .csk/project-state.json says adoption is pending or blocked, when a repository must be reverse-engineered before feature specification, or when existing evidence must become a provisional source-linked feature scaffold. Reads only the current repository and records completion or blockers through csk-start."
---

<!--
CODEX-CLAUDE-SKILL-PROXY
canonical_claude_skill: .claude/skills/csk-adopt-plan-scaffold/SKILL.md
contract_sha256: 23f0dc19224ce4ba32f6d26b4686b8ff4a39b55f5035014200d07588d22098ed
source_kind: repo
proxy_schema_version: 1
generated_by: .claude/skills/claude-skill-proxy-sync/scripts/sync_claude_skill_proxies.py
-->

# Claude Skill Proxy: CSK Adopt Plan Scaffold

This is a generated thin Codex proxy. The canonical implementation remains in
`.claude/skills/csk-adopt-plan-scaffold/SKILL.md` inside this repository.

## Runtime Instructions

1. Resolve the current Git repository root; do not use the proxy generator's
   machine or path.
2. Read `<repo>/.claude/skills/csk-adopt-plan-scaffold/SKILL.md` completely before taking task action.
3. Follow that canonical skill as the authoritative workflow.
4. Resolve its relative scripts, references, and assets from
   `<repo>/.claude/skills/csk-adopt-plan-scaffold/`.
5. Keep all kit skills repository-local. Never install, copy, or fall back to a
   user-global Claude or Codex skill directory.
6. If the canonical file is absent, stop and report the missing repo file.

Ordinary canonical body and resource changes are live. Regenerate this proxy only
after inventory, frontmatter trigger, or interface metadata changes.
