# Requirements / Voraussetzungen

This file describes the tools needed to use the workflow starter kit itself.
Dependencies for the product you build are selected later by the architecture
workflow and are not starter-kit requirements.

Diese Datei beschreibt die Werkzeuge für das Workflow-Starter-Kit. Abhängigkeiten
des eigentlichen Produkts werden später durch den Architektur-Workflow ausgewählt
und sind keine Voraussetzungen des Kits.

## Required / Erforderlich

| Tool | Requirement | Why |
|---|---|---|
| Git | Recent Git 2.x; 2.30+ recommended | Repository state, evidence, branches, and shared onboarding |
| Python | CPython 3.10 or newer | Deterministic `csk-start`, task, adoption, and release checks |
| GitHub | Account and repository access | Create a project from the template, collaborate, and publish |
| Coding agent | Claude Code **or** OpenAI Codex | Run the repository-local skills and perform contextual work |
| Shell | Windows PowerShell 5.1+ or POSIX shell | Launch the deterministic tools |
| Network | Internet access | Agent authentication/processing and GitHub operations |

The Python tools use only the standard library. There are no third-party Python
packages and no `pip install` step.

Die Python-Werkzeuge verwenden nur die Standardbibliothek. Es gibt keine externen
Python-Pakete und keinen `pip install`-Schritt.

## Official installation links / Offizielle Installationslinks

- [Git documentation and downloads](https://git-scm.com/docs/git)
- [Python downloads](https://www.python.org/downloads/)
- [GitHub: create a repository from a template](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template)
- [Claude Code setup](https://docs.anthropic.com/en/docs/claude-code/getting-started)
- [OpenAI Codex access and clients](https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan)
- [OpenAI Codex CLI getting started](https://help.openai.com/en/articles/11096431)

Node.js/npm is needed only when you choose an npm-based installation method for
Claude Code or the Codex CLI. It is not a runtime dependency of this kit. The
Codex desktop app or IDE extension may be used instead of the CLI.

Node.js/npm wird nur benötigt, wenn du Claude Code oder die Codex CLI über npm
installierst. Es ist keine Laufzeitabhängigkeit dieses Kits. Statt der CLI kann
auch die Codex Desktop-App oder IDE-Erweiterung verwendet werden.

## Verify your setup / Installation prüfen

Run in the repository root:

```bash
git --version
python --version
```

On systems where Python is exposed under another launcher, use one of:

```bash
python3 --version
py -3 --version
```

Check the agent you selected:

```bash
claude --version
```

or:

```bash
codex --version
```

You need only one of the two agent checks to succeed.

Nur einer der beiden Agent-Checks muss erfolgreich sein.

## Recommended but optional / Empfohlen, aber optional

| Tool/practice | Benefit |
|---|---|
| [GitHub CLI](https://cli.github.com/) | Convenient repository, issue, pull-request, and authentication commands |
| Code editor with Git diff support | Makes agent changes easier to inspect |
| Git credential manager or SSH key | Safer authentication than repeatedly entering credentials |
| Backup or protected default branch | Easier recovery before adopting the kit into existing code |
| GitHub branch protection and required checks | Prevents unreviewed changes from reaching the default branch |

## Operating-system notes / Hinweise zum Betriebssystem

### Windows

- Use PowerShell 5.1 or newer for `csk-start.ps1`.
- Claude Code supports Windows through WSL or Git for Windows according to its
  official setup guide.
- Codex support depends on the selected client. Follow the current OpenAI client
  documentation; WSL is a safe CLI option when native support is limited.
- The launcher detects `python`, `python3`, and `py -3`.

### macOS and Linux

- Use `csk-start.sh` with a POSIX-compatible shell.
- Ensure `python3` or `python` resolves to Python 3.10+.
- Make the launcher executable if your copied project lost the executable bit:

```bash
chmod +x .claude/skills/csk-start/scripts/csk-start.sh
```

## First health check / Erster Funktionstest

Windows:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .claude/skills/csk-start/scripts/csk-start.ps1 state check
powershell -NoProfile -ExecutionPolicy Bypass -File .claude/skills/csk-start/scripts/csk-start.ps1 tasks check
```

macOS/Linux:

```bash
.claude/skills/csk-start/scripts/csk-start.sh state check
.claude/skills/csk-start/scripts/csk-start.sh tasks check
```

Both commands should return machine-readable output with `"valid": true` for a
fresh, unchanged template.

Beide Befehle sollten bei einem frischen, unveränderten Template maschinenlesbare
Ausgabe mit `"valid": true` liefern.

## What you do not need yet / Was du noch nicht brauchst

The starter kit intentionally does not require:

- a JavaScript framework or Node.js product runtime;
- Docker or Kubernetes;
- a database;
- a cloud account or hosting provider;
- a package manager for the future product;
- a specific programming language beyond Python for the kit tooling.

`3-csk-architecture` recommends product technology only after it has read the
requirements, existing constraints, and feature specification.

## Troubleshooting / Fehlerhilfe

### No supported Python runtime

Install CPython 3.10+ and reopen the terminal. Confirm that `python`, `python3`, or
`py -3` works. The kit fails closed and does not modify state without a supported
runtime.

### Claude or Codex does not show local skills

1. Confirm that the repository root contains `.claude/skills/` and
   `.codex/skills/`.
2. Open the repository root, not a nested source folder.
3. Restart or reopen the coding-agent session.
4. Do not copy the skills into a global user directory.

### Git push goes to the starter kit

Inspect remotes:

```bash
git remote -v
```

Your project repository must be `origin`. The starter-kit source, if kept as a
remote, must be `upstream`.

### The first-use question appears in another clone

The decision becomes project-wide only after the changed
`.csk/project-state.json` commit is reachable from the default branch of the
confirmed project `origin`. Commit and push only after reviewing that exact change.

### Project-specific build tools are missing

Read `docs/architecture.md` and the relevant feature specification. Product
dependencies belong to the chosen project stack, not to this starter kit.
