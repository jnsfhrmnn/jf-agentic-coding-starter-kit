---
name: audit-plan-loop
description: "Iterative, evidence-based working mode for building or refining a non-trivial deliverable through visible AUDIT, PLAN, REFINE, and LOG cycles. Use for plans, specifications, architecture, migrations, policies, complex documents, or implementation approaches that need contextual LLM judgment, explicit assumptions, adversarial self-critique, and convergence instead of a one-pass answer. Repository-local and single-repository only."
---

<!--
CODEX-CLAUDE-SKILL-PROXY
canonical_claude_skill: .claude/skills/audit-plan-loop/SKILL.md
contract_sha256: ec7139fc3a60c5b9f58d3c9b9129a25cfb53f4c31deded7298ae111fd4e11490
source_kind: repo
proxy_schema_version: 1
generated_by: .claude/skills/claude-skill-proxy-sync/scripts/sync_claude_skill_proxies.py
-->

# Claude Skill Proxy: Audit Plan Loop

This is a generated thin Codex proxy. The canonical implementation remains in
`.claude/skills/audit-plan-loop/SKILL.md` inside this repository.

## Runtime Instructions

1. Resolve the current Git repository root; do not use the proxy generator's
   machine or path.
2. Read `<repo>/.claude/skills/audit-plan-loop/SKILL.md` completely before taking task action.
3. Follow that canonical skill as the authoritative workflow.
4. Resolve its relative scripts, references, and assets from
   `<repo>/.claude/skills/audit-plan-loop/`.
5. Keep all kit skills repository-local. Never install, copy, or fall back to a
   user-global Claude or Codex skill directory.
6. If the canonical file is absent, stop and report the missing repo file.

Ordinary canonical body and resource changes are live. Regenerate this proxy only
after inventory, frontmatter trigger, or interface metadata changes.
