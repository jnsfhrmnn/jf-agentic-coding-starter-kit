---
name: claude-skill-proxy-sync
description: Synchronize canonical repository-local Claude skills from .claude/skills into portable thin Codex proxies under .codex/skills. Use after adding, renaming, moving, or removing a local skill, or after changing its YAML trigger description or agents/openai.yaml interface metadata. Do not use for ordinary SKILL.md body edits because Codex reads the canonical Claude file at runtime.
---

# Claude Skill Proxy Sync

Keep one canonical skill implementation for Claude and Codex without installing
anything into a user's global skill directories.

## Contract

- `.claude/skills/<name>/SKILL.md` is the canonical implementation.
- `.codex/skills/<name>/SKILL.md` is a generated thin proxy.
- Every proxy resolves the repository root at runtime and reads the canonical
  Claude skill through a repository-relative path.
- Never read from or write to `%USERPROFILE%\.claude\skills`,
  `%USERPROFILE%\.codex\skills`, `~/.claude/skills`, `~/.codex/skills`, or
  `$CODEX_HOME/skills`.
- Never embed the current machine's absolute repository path in a proxy.
- Preserve `csk-adopt-plan-scaffold`; it is a required bundled skill.

## Decide Whether Sync Is Needed

Run the sync after:

- adding, renaming, moving, or deleting a directory in `.claude/skills`;
- changing `name` or `description` in a canonical skill's YAML frontmatter;
- changing `display_name`, `short_description`, or `default_prompt` in a
  canonical skill's `agents/openai.yaml`.

Do not sync after an ordinary body, script, reference, or asset edit. The proxy
loads those canonical repo-local files at runtime, so those changes are live.

## Workflow

1. Resolve the current Git repository root. Stop if `.claude/skills` is missing.
2. Read `AGENTS.md`, `CLAUDE.md`, and repository rules before changing files.
3. Inspect the plan without writing:

   ```text
   python .claude/skills/claude-skill-proxy-sync/scripts/sync_claude_skill_proxies.py --repo .
   ```

4. Review every `create`, `update`, `stale`, or `conflict` result. Never
   overwrite an unmanaged Codex skill.
5. Apply safe creates and updates:

   ```text
   python .claude/skills/claude-skill-proxy-sync/scripts/sync_claude_skill_proxies.py --repo . --apply
   ```

6. If a canonical skill was deliberately removed, review the stale list and
   prune only generated proxies:

   ```text
   python .claude/skills/claude-skill-proxy-sync/scripts/sync_claude_skill_proxies.py --repo . --apply --prune
   ```

7. Run the script once more without `--apply`; it must report `ok` for every
   canonical skill and no stale proxies.
8. Run the bundled tests and skill validation.

Use `--name <skill-name>` to inspect or update one skill. Use `--json` for a
machine-readable plan. Read [references/proxy-plan.md](references/proxy-plan.md)
before changing the proxy schema or generator behavior.

## Safety

- `--prune` is valid only with `--apply` and removes only directories carrying
  this generator's marker.
- A target without the marker is a conflict and remains untouched.
- Generated paths must remain inside `.codex/skills` under the resolved repo.
- `AGENTS.md` and `CLAUDE.md` are maintained source files, not generated output.
  Change them only when the user authorized that exact change.

## Completion Evidence

Report the canonical skill count, created/updated/pruned proxies, conflicts, test
results, and confirmation that no generated file contains an absolute or global
user path.
