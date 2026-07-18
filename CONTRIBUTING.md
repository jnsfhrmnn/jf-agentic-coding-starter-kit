# Contributing

Thank you for helping make agentic software development easier to enter and safer
to operate.

## Before opening a change

1. Search existing issues and pull requests.
2. Keep the kit technology-neutral and useful with Claude Code and Codex.
3. Keep canonical skill logic in `.claude/skills/`; generate thin Codex proxies
   with `claude-skill-proxy-sync`.
4. Do not add global user-folder installation, cross-repository task transport,
   product-stack dependencies, secrets, private plans, or internal audit reports.
5. Prefer a focused issue before proposing a large workflow change.

## Development

Create a branch and run the public checks before opening a pull request:

```bash
python .claude/skills/csk-start/scripts/test_csk_start.py
python .claude/skills/csk-start/scripts/test_workflow_contracts.py
python .claude/skills/claude-skill-proxy-sync/scripts/test_sync_claude_skill_proxies.py
python .claude/skills/claude-skill-proxy-sync/scripts/sync_claude_skill_proxies.py --repo . --json
python .claude/skills/csk-start/scripts/csk_start.py --repo . state check-template-distribution
```

Pull requests should explain:

- the user problem;
- the workflow behavior before and after the change;
- deterministic checks versus contextual agent judgment;
- compatibility impact for Claude Code and Codex;
- tests and evidence;
- migration or documentation impact.

## Documentation

Write for a beginner first, then add expert details. Use complete commands, state
what directory they run in, explain destructive or external actions, and never
assume that passing tests authorizes a commit, push, merge, deploy, tag, or delete.

## License

By contributing, you agree that your contribution is provided under the repository's
MIT terms and that required upstream notices remain intact.
