---
name: review-loop
description: "Deep, iterative, evidence-based review of existing repository artifacts such as code, architecture, plans, specifications, prompts, skills, rules, configuration, documentation, tests, and release output. Use when asked to review, audit, harden, verify, or refine completed work; after productive changes covered by .claude/rules/loop-policy.md; or when reviewing the current session delta, an explicit target, or all session work. Produces an authority-aware local disposition for every real finding: persist it only when repository writes are authorized, otherwise name its exact proposed SSOT or task target as PENDING-AUTH."
---

<!--
CODEX-CLAUDE-SKILL-PROXY
canonical_claude_skill: .claude/skills/review-loop/SKILL.md
contract_sha256: 83b3175e25d0c17db04853b86be85058c1811a12c95f1610a72904e9d80b7413
source_kind: repo
proxy_schema_version: 1
generated_by: .claude/skills/claude-skill-proxy-sync/scripts/sync_claude_skill_proxies.py
-->

# Claude Skill Proxy: Review Loop

This is a generated thin Codex proxy. The canonical implementation remains in
`.claude/skills/review-loop/SKILL.md` inside this repository.

## Runtime Instructions

1. Resolve the current Git repository root; do not use the proxy generator's
   machine or path.
2. Read `<repo>/.claude/skills/review-loop/SKILL.md` completely before taking task action.
3. Follow that canonical skill as the authoritative workflow.
4. Resolve its relative scripts, references, and assets from
   `<repo>/.claude/skills/review-loop/`.
5. Keep all kit skills repository-local. Never install, copy, or fall back to a
   user-global Claude or Codex skill directory.
6. If the canonical file is absent, stop and report the missing repo file.

Ordinary canonical body and resource changes are live. Regenerate this proxy only
after inventory, frontmatter trigger, or interface metadata changes.
