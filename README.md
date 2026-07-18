# JF Agentic Coding Starter Kit

[![Validation](https://github.com/jnsfhrmnn/jf-agentic-coding-starter-kit/actions/workflows/validate.yml/badge.svg)](https://github.com/jnsfhrmnn/jf-agentic-coding-starter-kit/actions/workflows/validate.yml)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude_Code-compatible-6B4FBB)](https://docs.anthropic.com/en/docs/claude-code/getting-started)
[![OpenAI Codex](https://img.shields.io/badge/OpenAI_Codex-compatible-111111)](https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB)](https://www.python.org/downloads/)

> A beginner-friendly, technology-neutral workflow that helps Claude Code or
> Codex turn an idea—or an existing codebase—into an intentionally specified,
> reviewed, tested, and safely released software project.

**[English](#english) · [Deutsch](#deutsch) · [Requirements](REQUIREMENTS.md) · [Upstream](UPSTREAM.md) · [License](LICENSE)**

This repository is a **workflow starter kit, not an application boilerplate**.
It does not force React, Python, C++, a database, a cloud, or any other product
technology. The architecture workflow examines your actual requirements and
existing constraints before it proposes a stack.

---

<a id="english"></a>

## English

### What this kit gives you

AI coding becomes unreliable when decisions live only in chat, every new session
starts from memory, unfinished work is scattered, or an agent pushes before the
result has been reviewed. This kit adds a small, repository-local operating system
for software work:

- a guided product-to-release workflow;
- one source of truth for product, architecture, features, tasks, and status;
- a first-open decision that works across the whole Git repository, not only one
  local checkout;
- a safe adoption path for existing projects;
- ready-to-use local skills for both Claude Code and Codex;
- deterministic tools for mechanical checks and LLM judgment where context is
  genuinely required;
- review, QA, release-evidence, and branch-finish gates;
- no global skill installation and no hidden cross-repository task service.

It is designed for beginners who want a clear next step and for experienced
developers who want repeatable agentic engineering instead of prompt improvisation.

### Start here: the five-minute path

#### 1. Check the requirements

You need:

- a recent Git 2.x installation;
- Python 3.10 or newer;
- a GitHub account for creating and publishing your project;
- **either** Claude Code **or** OpenAI Codex, installed and authenticated;
- PowerShell on Windows or a POSIX-compatible shell on macOS/Linux;
- internet access for the coding agent and GitHub.

The kit itself uses only the Python standard library. There is no `pip install`
step. See [REQUIREMENTS.md](REQUIREMENTS.md) for installation links, version
checks, optional tools, and troubleshooting.

#### 2. Create your own repository from this template

The recommended beginner path is:

1. Click **Use this template** on GitHub.
2. Select **Create a new repository**.
3. Give the project its own name and choose public or private visibility.
4. Clone your new repository:

```bash
git clone https://github.com/YOUR-NAME/YOUR-PROJECT.git
cd YOUR-PROJECT
```

Using a GitHub template creates an independent project history. Do not develop
your product directly in the starter-kit repository.

If you only want to evaluate the kit by cloning it directly, keep the template as
`upstream` and reserve `origin` for your own project:

```bash
git clone https://github.com/jnsfhrmnn/jf-agentic-coding-starter-kit.git my-project
cd my-project
git remote rename origin upstream
git remote add origin https://github.com/YOUR-NAME/YOUR-PROJECT.git
gh repo set-default YOUR-NAME/YOUR-PROJECT
```

The last line matters if you use the GitHub CLI: with an `upstream` remote
present, `gh` otherwise resolves to the template repository and could open
pull requests there instead of in your project.

#### 3. Open the repository in your coding agent

For Claude Code:

```bash
claude
```

Then run:

```text
/csk-start
```

For Codex, open the folder in the Codex app/extension or run the Codex CLI, then
invoke:

```text
$csk-start
```

Claude commands use `/skill-name`; Codex uses `$skill-name`.

#### 4. Answer the one-time project question

`csk-start` inventories the repository before asking what kind of project this is:

- **Greenfield:** there is no meaningful product code yet. Store the greenfield
  decision and continue with `1-csk-init`.
- **Adopt existing work:** code, tests, configuration, or substantial product
  documentation already exists. Store the adoption decision and run
  `csk-adopt-plan-scaffold`.
- **Do not store yet:** inspect without changing the shared decision.

The decision lives in `.csk/project-state.json`. After its commit reaches your
project's default branch on `origin`, every clone reads the same answer. A new
laptop or teammate is not asked to reclassify the project.

The classification itself never authorizes a commit or push. The agent must show
the intended Git change and obtain approval for external actions.

#### 5. Start building

For a new idea:

```text
/1-csk-init I want to build a simple appointment planner for a small studio.
```

or in Codex:

```text
$1-csk-init I want to build a simple appointment planner for a small studio.
```

The assistant interviews you in plain language, writes the product contract,
creates a feature map, and recommends the next feature. You do not need to know
the right framework, database, or deployment platform in advance.

### The complete workflow

```text
Session start
    -> classify or resume the repository
    -> define the product and feature map
    -> write one feature specification
    -> choose/confirm architecture
    -> implement the required surface and/or core
    -> test and review against evidence
    -> finish and integrate the branch safely
    -> package, release, or deploy
```

| Step | Claude Code | Codex | Result |
|---|---|---|---|
| Start/resume | `/csk-start` | `$csk-start` | Valid state, open tasks, recommended next action |
| 1. Product | `/1-csk-init` | `$1-csk-init` | PRD, master product contract, feature map |
| 2. Feature | `/2-csk-write-spec` | `$2-csk-write-spec` | Testable specification for one feature |
| 3. Architecture | `/3-csk-architecture` | `$3-csk-architecture` | Approved, recorded technology and design |
| 4. Surface | `/4-csk-frontend` | `$4-csk-frontend` | User-facing implementation when required |
| 5. Core | `/5-csk-backend` | `$5-csk-backend` | Business logic, data, services, automation, or native core |
| 6. Quality | `/6-csk-qa` | `$6-csk-qa` | Test and review evidence; release decision |
| Branch finish | `/finish-branch` | `$finish-branch` | Verified commit/integration and optional approved cleanup |
| 7. Release | `/7-csk-deploy` | `$7-csk-deploy` | Package, release, deployment, and smoke-test evidence |

Supporting skills:

| Claude Code | Codex | Purpose |
|---|---|---|
| `/csk-adopt-plan-scaffold` | `$csk-adopt-plan-scaffold` | Inventory and model an existing project without rewriting it |
| `/csk-refine PROJ-X` | `$csk-refine PROJ-X` | Reopen, challenge, split, or improve a feature |
| `/csk-refine --master` | `$csk-refine --master` | Refine the whole-product goal and critical journeys |
| `/review-loop` | `$review-loop` | Deep-review artifacts and disposition findings |
| `/audit-plan-loop` | `$audit-plan-loop` | Audit and strengthen a non-trivial plan iteratively |
| `/claude-skill-proxy-sync` | `$claude-skill-proxy-sync` | Create/update Codex proxies for your own local Claude skills |
| `/csk-help` | `$csk-help` | Explain current state and the safest next step |

### Why this order? Classic software engineering, applied

The numbered steps follow the classic engineering cycle: capture requirements
first, specify features with acceptance criteria, then decide the architecture,
then build, then verify. Two proven reasons drive this order. First,
architecture is determined by the whole requirement set—deciding technology
against the complete feature list avoids expensive rework, because a change
that costs minutes during planning costs many times more after the technology
decision (Boehm's classic cost-of-change data: roughly 10–100x). That is why
the kit asks, before the architecture step, whether all currently known
features are captured. Second, QA at the end verifies the software against the
same acceptance criteria written in step 2—so "done" is an objective,
traceable check instead of a feeling. Every numbered workflow skill also opens
with one or two plain sentences explaining why its step happens now.

### Why this also professionalizes an existing project

You do **not** need to restart or rewrite a working codebase. The adoption path is
specifically for repositories where implementation came before consistent product
documentation or where AI coding accumulated context debt.

Structured adoption of an existing codebase is one of this kit's rarest
features: most spec-driven kits are greenfield-first. The closest the field
gets (as of July 2026) is codebase documentation (BMAD) or community
extensions (spec-kit) — without a verified feature mapping. Here it is a
built-in, tracked workflow (`csk-adopt-plan-scaffold`) with a machine-verified
coverage gate — the adoption cannot be marked complete while meaningful code
is left unmapped.

After the kit files have been added on a dedicated branch, the first inventory
detects implementation, tests, configuration, and project evidence. The adoption
skill then:

1. reads the repository as evidence instead of guessing from filenames;
2. maps relevant source material to real features;
3. records why unusual files are relevant instead of silently counting them;
4. preserves the current language, framework, and architecture as constraints;
5. builds a provisional feature index linked back to source evidence;
6. identifies missing product goals, unclear ownership, untested journeys, and
   architecture gaps;
7. blocks completion when meaningful code is not covered by the adoption record;
8. creates a clean handoff into specification, architecture review, QA, and normal
   delivery—without forcing a rewrite.

This is valuable for projects that have any of these symptoms:

- important decisions exist only in chat or in one developer's memory;
- nobody can quickly explain which features are complete;
- tests exist but are not connected to acceptance criteria;
- multiple AI agents produce inconsistent conventions;
- branches stay open, commits mix unrelated work, or releases lack evidence;
- a legacy stack is assumed to be wrong before requirements are examined;
- onboarding a new developer requires a long verbal handover.

The professionalization comes from adding explicit contracts around the code:

- `docs/PRD.md` owns product intent;
- `docs/master-feature.md` owns the whole-product goal, USP, journeys, and gaps;
- `docs/architecture.md` owns approved technology decisions;
- `features/INDEX.md` and feature specs own delivery state and acceptance evidence;
- `tasks/INDEX.md` owns only durable open or blocked continuation work;
- `.csk/project-state.json` owns the shared onboarding decision;
- `.claude/rules/workflow-state.md` owns allowed workflow transitions.

The code remains the implementation truth. The new documents make intent,
coverage, risk, and next actions reviewable.

#### Adding the kit to an existing repository

Work on a dedicated branch and make a backup first. Copy the workflow control
plane from this template into the repository:

- `.claude/`
- `.codex/`
- `.csk/project-state.json`
- `CLAUDE.md` and `AGENTS.md`
- `tasks/INDEX.md`
- the empty product/feature templates that do not overwrite existing evidence

If the existing project already has `CLAUDE.md`, `AGENTS.md`, `docs/`, or
`features/`, merge the content deliberately—do not overwrite it. Then open the
repository, run `csk-start`, choose adoption, and follow
`csk-adopt-plan-scaffold`. Review the resulting inventory before committing.

### How this kit compares to other agentic workflow kits

The core idea — guiding an AI agent from requirements to implementation with
repository-local commands — is well established. Excellent projects cover it,
including [github/spec-kit](https://github.com/github/spec-kit),
[OpenSpec](https://github.com/Fission-AI/OpenSpec),
[BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD),
[Agent OS](https://github.com/buildermethods/agent-os), and
[ccpm](https://github.com/automazeio/ccpm). If one of them fits your working
style, use it. This kit's contribution is the **governance layer** that most
of the field leaves open. To be transparent in both directions
(as of July 2026):

| Dimension | spec-kit and the large frameworks | This kit |
|---|---|---|
| Distribution and updates | ✅ Versioned CLI (`specify init`) with an upgrade path | GitHub template; no update mechanism yet — improvements do not reach existing projects automatically |
| Agent breadth | ✅ 30+ agents (Copilot, Cursor, Gemini CLI, Windsurf, …) | Exactly two: Claude Code and Codex |
| Greenfield speed | ✅ Productive in minutes; few concepts, little ceremony | Gates only pay off in projects you intend to keep |
| Ecosystem | ✅ Large communities, multiple maintainers, fast releases, many tutorials | One maintainer |
| Git safety | Mostly left to the agent's defaults | ✅ Core feature for people who do not know Git yet: branch gate, checkpoint commits, hard-gated `finish-branch`, no force push, explicit approval for every external action |
| Existing codebases | Partial at best: codebase documentation (BMAD) or community extensions (spec-kit) | ✅ Adoption workflow with feature mapping and a mechanical coverage gate |
| Delivery states | Quality gates without recorded proof | ✅ Evidence-gated: `Approved` and `Deployed` require verifiable proof |
| Team onboarding decision | Per machine or not modeled | ✅ One Git-tracked decision that every clone and teammate reads |
| Whole-product contract | Constitution/PRD level | ✅ `docs/master-feature.md` with system journeys and local/cloud boundaries |
| Technology choice | Stack-agnostic, but ordering is not enforced | ✅ Enforced gate: no stack before the architecture step approves it |

**This kit is for you if** you are a beginner who wants Git guardrails while
learning, you are taking over a codebase that already exists, or you need
delivery states backed by evidence. **Choose spec-kit or a similar framework
if** you want the fastest possible greenfield start, you work in Cursor or
Copilot, or you want a large ecosystem behind your tooling.

### Deterministic checks and contextual judgment

The opposite of deterministic is **non-deterministic**. In this kit, deterministic
means that identical input produces the same mechanically verifiable result:
JSON schema validation, task-table parsing, Git reachability, path existence,
state transitions, and evidence references.

Product meaning, architecture tradeoffs, UX quality, security risk, or whether a
test truly proves a requirement need contextual judgment. An LLM is useful there,
but its result must be made reviewable through written rationale and evidence.

The rule is simple:

- use scripts for facts a script can prove;
- use the agent for semantic decisions;
- never present an agent's confidence as deterministic proof.

### Repository-local skills: nothing is installed globally

Canonical skills live in `.claude/skills/`. Ready-made Codex proxy skills live in
`.codex/skills/` and reference the local canonical versions. They are versioned
with the project and do not modify `%USERPROFILE%/.claude`, `~/.claude`,
`$CODEX_HOME`, or `~/.codex`.

When you add your own Claude skill or change its trigger metadata, run
`claude-skill-proxy-sync`. The generated proxy stays in this repository. Ordinary
skill-body edits are read from the canonical file and do not require duplication.

### State survives chat resets

The kit treats repository files as source of truth. Every skill re-reads the
relevant files. This makes the project resilient when a conversation is compacted,
closed, or continued by another agent.

`tasks/INDEX.md` is intentionally not a transcript or a todo dump. A task is stored
only when it remains open across sessions, is blocked/deferred, or marks a verified
interruption point. Short-lived same-session activity does not create noise.

#### The task system in five lines

- `/csk-start` opens every session: it shows the board of open tasks and
  recommends exactly one next action; say `continue` to resume it.
- Store durable work in plain language or with `/csk-start --add "<task>"`;
  newly discovered follow-ups are shown as `PENDING-AUTH` and you are asked
  once before anything is stored.
- Record a blocker with `/csk-start --block TASK-001 --reason "<why>"`.
- Closing requires typed evidence, for example
  `/csk-start --close TASK-001 --evidence "commit:<sha>"` — claims without a
  locally verifiable proof are rejected.
- Completed rows are deleted, not archived; Git history is the audit trail.

### Safe Git and branch handling — built for people who do not know Git yet

Version control is where AI coding goes wrong most painfully: an agent commits
half-finished work, pushes to the wrong remote, force-overwrites history, or
deletes a branch whose work was never merged. Most agentic workflow kits treat
Git as a side detail. This kit treats it as a first-class safety system — and
that is exactly why beginners profit from it: **you do not need to know Git
commands to work safely.** The workflow asks before every durable action,
explains in one plain sentence what is about to happen, and verifies every
step instead of assuming it worked.

What the kit does for you:

- The workflow asks once, before implementation starts on the default branch,
  whether to create a feature branch — and explains why that protects you.
- After each verified increment, it proposes a checkpoint commit so progress
  survives a lost session. You approve; it never commits silently.
- Passing tests does not authorize commit, push, PR, merge, tag, deploy, or
  delete. Every external action needs your explicit yes.
- `finish-branch` performs the entire closing sequence for you — commit, push,
  pull request, waiting for green checks, merge, verified integration, and
  optional cleanup — with a hard stop at every failure. Nothing is ever deleted
  before the merge is proven to exist on your remote default branch.
- `origin` is your project repository; `upstream` is the starter-kit source and
  is never an implicit push target. The GitHub CLI resolution is pinned so a
  pull request cannot silently target the template repository.
- Force pushes are denied by default. Local and remote branch cleanup require
  separate, explicit approval.
- Closing a task requires typed, locally verifiable evidence — "done" is a
  checked fact, not a feeling.

Experienced developers get the same guarantees as review discipline; beginners
get them as guardrails they never have to configure.

### Project structure

```text
.
|-- README.md                         Beginner guide in English and German
|-- REQUIREMENTS.md                   Tools, versions, checks, troubleshooting
|-- CLAUDE.md                         Shared Claude workflow entry point
|-- AGENTS.md                         Codex entry point and compatibility rules
|-- .csk/
|   `-- project-state.json            Git-tracked project onboarding state
|-- .claude/
|   |-- rules/                        Security, workflow, frontend/core rules
|   |-- agents/                       Focused agent definitions
|   `-- skills/                       Canonical repository-local skills
|-- .codex/
|   `-- skills/                       Ready-to-use local Codex proxies
|-- docs/
|   |-- PRD.md                        Product intent
|   |-- master-feature.md             Whole-product contract
|   |-- architecture.md               Approved technical decisions
|   `-- engineering-principles.md     Quality and evidence principles
|-- features/
|   |-- INDEX.md                      Feature map and status
|   `-- PROJ-X-name.md                Feature specifications, created as needed
`-- tasks/
    `-- INDEX.md                      Durable open/blocked continuation work
```

No application source directory is included. The approved architecture decides
whether the project needs `src/`, `app/`, `Source/`, a workspace, a plugin, a
service layout, or something else.

### Public/private file boundary

The template publishes workflow code, empty SSOT templates, examples, and tests.
It excludes internal plans and audits, agent-local settings/sessions, caches,
environment files, keys, credentials, logs, and private notes through `.gitignore`.

Before every public push, still inspect:

```bash
git status --short
git diff --staged
git grep -n -I -E "(password|token|secret|api[_-]?key)"
```

Never assume `.gitignore` can remove a secret that was already committed. Rotate
exposed credentials and clean Git history before publication.

### Validation for maintainers

```bash
python .claude/skills/csk-start/scripts/test_csk_start.py
python .claude/skills/csk-start/scripts/test_workflow_contracts.py
python .claude/skills/claude-skill-proxy-sync/scripts/test_sync_claude_skill_proxies.py
python .claude/skills/claude-skill-proxy-sync/scripts/sync_claude_skill_proxies.py --repo . --json
```

The template distribution gate checks the committed Git snapshot, not an
untracked working-tree file:

```bash
python .claude/skills/csk-start/scripts/csk_start.py --repo . state check-template-distribution
```

GitHub Actions runs the same public-release checks on every push and pull request.

### Frequently asked questions

**Do I need to be a programmer?**

No. The workflow explains the next decision and asks focused questions. You still
need to review product decisions and should learn basic Git safety before release.

**Does it generate an app immediately?**

No. It first makes the goal and feature contract explicit. This avoids generating
a large but misaligned codebase.

**Which programming language does it use?**

Whichever language fits the approved requirements or already exists in an adopted
project. The kit itself does not select one.

**Can I use only Claude Code or only Codex?**

Yes. Both are first-class entry points; you do not need both.

**Can a team use it?**

Yes. Commit the workflow state and SSOT documents so every teammate and agent reads
the same decisions.

**Can I distribute or sell software built with it?**

Yes. The kit is provided under the MIT terms. Preserve the required license and
copyright notices. Your product's dependencies can have additional licenses.

### Upstream credit and how this edition differs

Special thanks to **Alex Sprogis**, original author of
[AlexPEClub/ai-coding-starter-kit](https://github.com/AlexPEClub/ai-coding-starter-kit).
Alex's work established the idea of guiding delivery through reusable Claude Code
skills. This edition exists because that foundation was shared publicly.

The projects now serve different use cases:

| Original kit by Alex Sprogis | This JF edition |
|---|---|
| Focused on production web apps | Technology-neutral: web, desktop, CLI, native, automation, services, plugins, and more |
| Claude Code workflow | Claude Code and OpenAI Codex compatibility |
| Preselected Next.js/TypeScript/Tailwind/shadcn/Supabase/Vercel direction | Architecture remains open until project evidence and requirements justify a choice |
| Starts from its bundled application stack | Supports greenfield work and evidence-based adoption of existing repositories |
| Feature workflow and specialized agents | Adds shared onboarding state, durable tasks, workflow-transition SSOT, review/audit loops, proxy sync, and safe branch completion |
| Web application code is included | No product implementation is imposed by the template |

This comparison is not a quality judgment. The original is useful when its web
stack is exactly what you want; this derivative is for teams that need broader
technology choices, existing-project adoption, or Claude/Codex portability.

See [UPSTREAM.md](UPSTREAM.md) for provenance and the license caveat.

### Maintainer

Maintained and extended by **Jens Fehrmann**
([@jnsfhrmnn](https://github.com/jnsfhrmnn)), an AI developer focused on
context engineering, repository-local agent workflows, deterministic safety
checks, and evidence-driven software delivery.

If the kit helps you, star the repository, open a well-scoped issue, or share what
you built. Contributions that preserve beginner clarity, technology neutrality,
and safe Git behavior are welcome.

---

<a id="deutsch"></a>

## Deutsch

### Was dir dieses Kit gibt

AI-Coding wird unzuverlässig, wenn Entscheidungen nur im Chat stehen, jede neue
Session aus Erinnerung beginnt, offene Arbeit verstreut ist oder ein Agent
ungeprüft pusht. Dieses Kit ergänzt deshalb ein kleines, repository-lokales
Betriebssystem für Softwareentwicklung:

- einen geführten Weg von der Produktidee bis zum Release;
- klare Single Sources of Truth für Produkt, Architektur, Features, Tasks und Status;
- eine einmalige Projektentscheidung, die über Git für alle Checkouts gilt;
- einen sicheren Übernahmepfad für bestehende Projekte;
- sofort nutzbare lokale Skills für Claude Code und Codex;
- deterministische Werkzeuge für mechanische Prüfungen und LLM-Bewertung dort, wo
  echter Kontext nötig ist;
- Review-, QA-, Release-Evidence- und Branch-Abschluss-Gates;
- keine globale Skill-Installation und keinen versteckten Cross-Repo-Taskdienst.

Das Kit richtet sich an Anfänger, die einen verständlichen nächsten Schritt
brauchen, und an erfahrene Entwickler, die reproduzierbare agentische Entwicklung
anstelle von Prompt-Improvisation wollen.

### Hier anfangen: der Fünf-Minuten-Einstieg

#### 1. Voraussetzungen prüfen

Du brauchst:

- eine aktuelle Git-2.x-Installation;
- Python 3.10 oder neuer;
- einen GitHub-Account zum Erstellen und Veröffentlichen deines Projekts;
- **entweder** Claude Code **oder** OpenAI Codex, installiert und angemeldet;
- PowerShell unter Windows oder eine POSIX-kompatible Shell unter macOS/Linux;
- Internetzugang für Coding-Agent und GitHub.

Das Kit verwendet ausschließlich die Python-Standardbibliothek. Es gibt keinen
`pip install`-Schritt. Installationslinks, Versionsprüfungen, optionale Werkzeuge
und Fehlerhilfe stehen in [REQUIREMENTS.md](REQUIREMENTS.md).

#### 2. Eigenes Repository aus dem Template erstellen

Der empfohlene Anfängerweg:

1. Auf GitHub **Use this template** anklicken.
2. **Create a new repository** wählen.
3. Eigenen Projektnamen und Sichtbarkeit festlegen.
4. Das neue Projekt klonen:

```bash
git clone https://github.com/DEIN-NAME/DEIN-PROJEKT.git
cd DEIN-PROJEKT
```

Ein GitHub-Template erzeugt eine unabhängige Projekthistorie. Entwickle dein
Produkt nicht direkt im Starter-Kit-Repository.

Wenn du das Kit nur durch direktes Klonen testen möchtest, benenne die Quelle in
`upstream` um und reserviere `origin` für dein eigenes Projekt:

```bash
git clone https://github.com/jnsfhrmnn/jf-agentic-coding-starter-kit.git mein-projekt
cd mein-projekt
git remote rename origin upstream
git remote add origin https://github.com/DEIN-NAME/DEIN-PROJEKT.git
gh repo set-default DEIN-NAME/DEIN-PROJEKT
```

Die letzte Zeile ist wichtig, wenn du die GitHub CLI nutzt: Mit vorhandenem
`upstream`-Remote löst `gh` sonst auf das Template-Repository auf und könnte
Pull Requests dort statt in deinem Projekt eröffnen.

#### 3. Repository im Coding-Agent öffnen

Claude Code im Projektordner starten:

```bash
claude
```

Danach:

```text
/csk-start
```

Für Codex den Ordner in App/Extension öffnen oder die CLI starten und ausführen:

```text
$csk-start
```

Claude verwendet `/skill-name`, Codex verwendet `$skill-name`.

#### 4. Einmalige Projektfrage beantworten

`csk-start` inventarisiert zuerst das Repository und bietet dann drei Wege:

- **Greenfield:** Es gibt noch keinen relevanten Produktcode. Greenfield speichern
  und mit `1-csk-init` fortfahren.
- **Bestehende Arbeit übernehmen:** Code, Tests, Konfiguration oder umfangreiche
  Produktdokumentation existieren bereits. Adoption speichern und
  `csk-adopt-plan-scaffold` starten.
- **Noch nicht speichern:** Nur prüfen, ohne die gemeinsame Entscheidung zu ändern.

Die Entscheidung steht in `.csk/project-state.json`. Sobald ihr Commit auf dem
Default-Branch deines Projekt-`origin` liegt, lesen alle Klone dieselbe Antwort.
Ein neuer Rechner oder Teamkollege klassifiziert das Projekt nicht erneut.

Die Antwort erlaubt noch keinen Commit oder Push. Externe Git-Aktionen müssen
separat und konkret freigegeben werden.

#### 5. Projekt beginnen

Für eine neue Idee:

```text
/1-csk-init Ich möchte einen einfachen Terminplaner für ein kleines Studio bauen.
```

oder in Codex:

```text
$1-csk-init Ich möchte einen einfachen Terminplaner für ein kleines Studio bauen.
```

Der Assistent führt ein verständliches Interview, schreibt den Produktvertrag,
erstellt die Feature-Map und empfiehlt den nächsten Schritt. Du musst Framework,
Datenbank oder Hosting nicht vorher kennen.

### Der vollständige Workflow

```text
Session starten
    -> Repository klassifizieren oder fortsetzen
    -> Produkt und Feature-Map definieren
    -> ein Feature vollständig spezifizieren
    -> Architektur wählen oder bestätigen
    -> Oberfläche und/oder Kern implementieren
    -> gegen Anforderungen testen und reviewen
    -> Branch sicher abschließen und integrieren
    -> paketieren, releasen oder deployen
```

Die Skill-Tabelle im englischen Abschnitt gilt identisch: Claude nutzt `/...`,
Codex `$...`. Mit `csk-help` erhältst du jederzeit Status und nächsten Schritt.

### Warum diese Reihenfolge? Klassische Softwaretechnik, angewendet

Die nummerierten Schritte folgen dem klassischen Entwicklungszyklus: erst
Anforderungen erfassen, dann Features mit Prüfkriterien spezifizieren, dann die
Architektur entscheiden, dann bauen, dann prüfen. Zwei bewährte Gründe tragen
diese Reihenfolge. Erstens: Die Architektur richtet sich nach der gesamten
Anforderungsmenge — wer die Technik gegen die vollständige Feature-Liste
entscheidet, vermeidet teure Umbauten, denn eine Änderung, die in der Planung
Minuten kostet, kostet nach der Technik-Entscheidung ein Vielfaches (Boehms
klassische Änderungskosten-Daten: grob 10–100x). Deshalb fragt das Kit vor dem
Architektur-Schritt, ob alle bekannten Features erfasst sind. Zweitens: Die
Qualitätsprüfung am Ende testet gegen genau die Prüfkriterien aus Schritt 2 —
„fertig" ist damit eine objektive, nachvollziehbare Prüfung statt eines
Gefühls. Jeder nummerierte Workflow-Skill beginnt zudem mit ein bis zwei
Sätzen, warum sein Schritt gerade jetzt kommt.

### Warum das Kit auch bestehende Projekte professionalisiert

Du musst funktionierenden Code **nicht** neu beginnen oder umschreiben. Der
Adoption-Pfad ist ausdrücklich für Repositories gedacht, in denen Implementierung
vor konsistenter Produktdokumentation entstanden ist oder AI-Coding bereits
Kontextschulden erzeugt hat.

Die strukturierte Übernahme einer bestehenden Codebasis ist eines der
seltensten Merkmale dieses Kits: Die meisten Spec-getriebenen Kits sind
Greenfield-first gedacht. Am nächsten kommt das Feld dem (Stand Juli 2026) mit
Codebasis-Dokumentation (BMAD) oder Community-Extensions (spec-kit) — ohne
verifizierte Feature-Zuordnung. Hier ist es ein eingebauter, getrackter
Workflow (`csk-adopt-plan-scaffold`) mit maschinell geprüftem Coverage-Gate:
Die Adoption kann nicht als abgeschlossen markiert werden, solange relevanter
Code unzugeordnet bleibt.

Nach dem Hinzufügen der Kit-Dateien auf einem eigenen Branch erkennt die erste
Inventur Implementierung, Tests, Konfiguration und Projektnachweise. Der
Adoption-Skill:

1. liest das Repository als Beleg, statt aus Dateinamen zu raten;
2. ordnet relevante Quellen echten Features zu;
3. verlangt für ungewöhnliche Quellen eine nachvollziehbare Relevanzbegründung;
4. behandelt vorhandene Sprache, Frameworks und Architektur als Constraints;
5. baut einen vorläufigen, quellverlinkten Feature-Index;
6. macht fehlende Produktziele, unklare Zuständigkeiten, ungetestete Journeys und
   Architekturlücken sichtbar;
7. blockiert einen falschen Abschluss, solange relevanter Code nicht abgedeckt ist;
8. übergibt sauber in Spezifikation, Architekturprüfung, QA und reguläre Lieferung,
   ohne einen Rewrite zu erzwingen.

Das hilft besonders, wenn:

- wichtige Entscheidungen nur im Chat oder im Kopf einer Person existieren;
- niemand schnell sagen kann, welche Features wirklich fertig sind;
- Tests nicht mit Akzeptanzkriterien verbunden sind;
- mehrere AI-Agenten unterschiedliche Konventionen erzeugen;
- Branches offen bleiben, Commits Themen vermischen oder Releases Belege vermissen;
- ein Legacy-Stack vorschnell verworfen wird;
- das Onboarding neuer Entwickler lange mündliche Übergaben braucht.

Professionalität entsteht durch überprüfbare Verträge rund um den Code:

- `docs/PRD.md` besitzt die Produktabsicht;
- `docs/master-feature.md` besitzt Gesamtziel, USP, Journeys und Lücken;
- `docs/architecture.md` besitzt bestätigte Technologieentscheidungen;
- `features/INDEX.md` und Feature-Spezifikationen besitzen Lieferstatus und Evidence;
- `tasks/INDEX.md` besitzt nur dauerhafte offene oder blockierte Fortsetzungsarbeit;
- `.csk/project-state.json` besitzt die gemeinsame Onboarding-Entscheidung;
- `.claude/rules/workflow-state.md` besitzt die erlaubten Workflow-Übergänge.

Der Code bleibt die Implementierungswahrheit. Die Dokumente machen Absicht,
Abdeckung, Risiko und nächste Aktionen überprüfbar.

#### Kit in ein bestehendes Repository einbauen

Lege vorher ein Backup und einen eigenen Integrationsbranch an. Übernimm die
Workflow-Steuerung aus diesem Template:

- `.claude/`
- `.codex/`
- `.csk/project-state.json`
- `CLAUDE.md` und `AGENTS.md`
- `tasks/INDEX.md`
- nur die leeren Produkt-/Feature-Vorlagen, die keine vorhandenen Quellen ersetzen

Existieren bereits `CLAUDE.md`, `AGENTS.md`, `docs/` oder `features/`, werden die
Inhalte bewusst zusammengeführt und nicht überschrieben. Danach Repository öffnen,
`csk-start` ausführen, Adoption wählen und `csk-adopt-plan-scaffold` folgen. Die
Inventur vor dem Commit prüfen.

### Wie sich das Kit von anderen agentischen Workflow-Kits unterscheidet

Die Kernidee — einen AI-Agenten mit repository-lokalen Kommandos von den
Anforderungen bis zur Implementierung zu führen — ist etabliert. Hervorragende
Projekte decken sie ab, darunter
[github/spec-kit](https://github.com/github/spec-kit),
[OpenSpec](https://github.com/Fission-AI/OpenSpec),
[BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD),
[Agent OS](https://github.com/buildermethods/agent-os) und
[ccpm](https://github.com/automazeio/ccpm). Wenn eines davon zu deinem
Arbeitsstil passt, nutze es. Der Beitrag dieses Kits ist die
**Governance-Schicht**, die das Feld überwiegend offenlässt. Transparenz in
beide Richtungen (Stand Juli 2026):

| Dimension | spec-kit und die großen Frameworks | Dieses Kit |
|---|---|---|
| Distribution und Updates | ✅ Versionierte CLI (`specify init`) mit Upgrade-Pfad | GitHub-Template; noch kein Update-Mechanismus — Verbesserungen erreichen bestehende Projekte nicht automatisch |
| Agenten-Breite | ✅ 30+ Agenten (Copilot, Cursor, Gemini CLI, Windsurf u. a.) | Genau zwei: Claude Code und Codex |
| Greenfield-Tempo | ✅ In Minuten produktiv; wenige Konzepte, wenig Zeremonie | Gates lohnen sich erst bei Projekten, die bleiben sollen |
| Ökosystem | ✅ Große Communities, mehrere Maintainer, hohe Release-Frequenz, viele Tutorials | Ein Maintainer |
| Git-Sicherheit | Bleibt meist den Agent-Defaults überlassen | ✅ Kernfeature für Menschen ohne Git-Vorwissen: Branch-Gate, Checkpoint-Commits, hart gegateter `finish-branch`, kein Force-Push, explizite Freigabe für jede externe Aktion |
| Bestehende Codebasen | Bestenfalls teilweise: Codebasis-Doku (BMAD) oder Community-Extensions (spec-kit) | ✅ Adoptions-Workflow mit Feature-Zuordnung und mechanischem Coverage-Gate |
| Lieferzustände | Quality-Gates ohne Beleg-Pflicht | ✅ Evidence-gekoppelt: `Approved` und `Deployed` verlangen prüfbare Belege |
| Team-Onboarding-Entscheidung | Pro Rechner oder nicht modelliert | ✅ Eine Git-getrackte Entscheidung, die jeder Klon und jedes Teammitglied liest |
| Ganzprodukt-Vertrag | Constitution-/PRD-Ebene | ✅ `docs/master-feature.md` mit System-Journeys und Local/Cloud-Grenzen |
| Technologie-Wahl | Stack-agnostisch, aber Reihenfolge nicht erzwungen | ✅ Erzwungenes Gate: kein Stack vor der Architektur-Freigabe |

**Dieses Kit ist für dich, wenn** du als Anfänger Git-Leitplanken willst,
während du nebenbei lernst, wenn du eine bestehende Codebasis übernimmst oder
wenn du Lieferzustände mit Belegen brauchst. **Wähle spec-kit oder ein
ähnliches Framework, wenn** du den schnellstmöglichen Greenfield-Start willst,
in Cursor oder Copilot arbeitest oder ein großes Ökosystem hinter deinem
Tooling haben möchtest.

### Deterministisch und nicht-deterministisch

Das Gegenteil von deterministisch heißt **nicht-deterministisch**.
Deterministisch bedeutet hier: Gleicher Input führt zu demselben mechanisch
prüfbaren Ergebnis—zum Beispiel bei JSON-Schema, Task-Tabelle, Git-Erreichbarkeit,
Pfadprüfung, Statusübergang oder Evidence-Referenz.

Produktbedeutung, Architekturabwägung, UX-Qualität, Sicherheitsrisiko oder die
Frage, ob ein Test eine Anforderung wirklich beweist, brauchen Kontext. Dort ist
LLM-Bewertung sinnvoll, muss aber durch Begründung und Evidence reviewbar werden.

Die Grundregel:

- Skripte für Fakten, die ein Skript beweisen kann;
- den Agenten für semantische Entscheidungen;
- LLM-Sicherheit niemals als deterministischen Beweis darstellen.

### Skills bleiben lokal im Repository

Kanonische Skills liegen in `.claude/skills/`, fertige Codex-Proxys in
`.codex/skills/`. Sie werden gemeinsam mit dem Projekt versioniert und nicht in
globale Benutzerordner kopiert. Eigene lokale Claude-Skills können mit
`claude-skill-proxy-sync` für Codex verfügbar gemacht werden.

### Zustand überlebt neue Chats

Die maßgeblichen Informationen stehen in Dateien, nicht im Chatgedächtnis. Jeder
Skill liest die relevanten Quellen neu. Deshalb funktionieren neue Sessions,
Kontextkomprimierung und Agentwechsel ohne mündliche Rekonstruktion.

`tasks/INDEX.md` ist kein Chatprotokoll und keine beliebige Todo-Liste. Ein Task
wird nur gespeichert, wenn er sessionsübergreifend offen, blockiert, verschoben
oder ein nachgewiesener Unterbrechungspunkt ist.

#### Das Task-System in fünf Zeilen

- `/csk-start` eröffnet jede Session: Es zeigt das Board der offenen Tasks und
  empfiehlt genau eine nächste Aktion; „weiter" setzt dort fort.
- Dauerhafte Arbeit speicherst du in Alltagssprache oder mit
  `/csk-start --add "<aufgabe>"`; neu entdeckte Folgearbeiten werden als
  `PENDING-AUTH` gezeigt, und du wirst einmal gefragt, bevor etwas gespeichert
  wird.
- Blocker erfasst `/csk-start --block TASK-001 --reason "<grund>"`.
- Schließen verlangt typisierte Evidence, zum Beispiel
  `/csk-start --close TASK-001 --evidence "commit:<sha>"` — Behauptungen ohne
  lokal prüfbaren Beleg werden abgelehnt.
- Erledigte Zeilen werden gelöscht, nicht archiviert; die Git-Historie ist der
  Nachweis.

### Sicheres Git- und Branch-Verhalten — gebaut für Menschen ohne Git-Vorwissen

Versionierung ist die Stelle, an der AI-Coding am schmerzhaftesten schiefgeht:
Ein Agent committet Halbfertiges, pusht zum falschen Remote, überschreibt
Historie per Force-Push oder löscht einen Branch, dessen Arbeit nie gemerged
wurde. Die meisten agentischen Workflow-Kits behandeln Git als Randnotiz.
Dieses Kit behandelt es als Sicherheitssystem erster Klasse — und genau davon
profitieren Anfänger: **Du musst keine Git-Kommandos kennen, um sicher zu
arbeiten.** Der Workflow fragt vor jeder dauerhaften Aktion, erklärt in einem
verständlichen Satz, was gleich passiert, und verifiziert jeden Schritt, statt
ihn anzunehmen.

Was das Kit für dich übernimmt:

- Vor Implementierungsbeginn auf dem Default-Branch fragt der Workflow einmal,
  ob ein Feature-Branch angelegt werden soll — und erklärt, warum dich das
  schützt.
- Nach jedem verifizierten Zwischenstand schlägt er einen Checkpoint-Commit
  vor, damit Fortschritt einen Session-Verlust überlebt. Du gibst frei;
  committet wird nie stillschweigend.
- Grüne Tests erlauben nicht automatisch Commit, Push, PR, Merge, Tag oder
  Deploy. Jede externe Aktion braucht dein ausdrückliches Ja.
- `finish-branch` erledigt die komplette Abschluss-Sequenz für dich —
  committen, pushen, Pull Request, Warten auf grüne Checks, Merge, verifizierte
  Integration und optionales Aufräumen — mit hartem Stopp bei jedem Fehler.
  Gelöscht wird erst, wenn der Merge nachweislich auf dem Remote-Default-Branch
  liegt.
- `origin` ist dein Projekt-Repository; `upstream` ist die Starter-Kit-Quelle
  und nie ein implizites Push-Ziel. Die GitHub-CLI-Auflösung wird gepinnt,
  damit ein Pull Request nicht still im Template-Repository landet.
- Force-Push ist standardmäßig gesperrt. Lokales und entferntes Branch-Löschen
  brauchen getrennte Freigaben.
- Ein Task wird nur mit typisierter, lokal prüfbarer Evidence geschlossen —
  „fertig" ist ein geprüfter Fakt, kein Gefühl.

Erfahrene Entwickler bekommen dieselben Garantien als Review-Disziplin;
Anfänger bekommen sie als Leitplanken, die sie nie konfigurieren müssen.

### Öffentlich und privat

Veröffentlicht werden Workflow-Code, leere SSOT-Vorlagen, Beispiele und Tests.
Ausgeschlossen sind interne Pläne und Audits, lokale Agent-Einstellungen und
Sessions, Caches, Umgebungsdateien, Schlüssel, Zugangsdaten, Logs und private
Notizen. Trotzdem vor jedem öffentlichen Push Status und Staged Diff prüfen.

Eine bereits committete Zugangsinformation wird durch `.gitignore` nicht entfernt.
In diesem Fall Zugang rotieren und die Git-Historie vor Veröffentlichung bereinigen.

### Häufige Fragen

**Muss ich programmieren können?**

Nein. Das Kit erklärt Entscheidungen und fragt fokussiert. Grundlegende Git-Sicherheit
und die fachliche Prüfung deiner Produktentscheidungen bleiben trotzdem wichtig.

**Generiert es sofort eine App?**

Nein. Zuerst werden Ziel und Feature-Vertrag eindeutig. Das verhindert viel Code,
der am eigentlichen Bedarf vorbeigeht.

**Welche Programmiersprache nutzt es?**

Die Sprache, die zu den bestätigten Anforderungen passt oder im bestehenden Projekt
bereits sinnvoll eingesetzt wird.

**Brauche ich Claude Code und Codex?**

Nein. Einer der beiden Agenten reicht; beide sind vollwertige Einstiegspunkte.

**Funktioniert es im Team?**

Ja. Committe Workflow-State und SSOT-Dokumente, damit Team und Agenten dieselben
Entscheidungen lesen.

### Dank an den Urheber und Unterschied zum Original

Ausdrücklicher Dank gilt **Alex Sprogis**, dem Urheber von
[AlexPEClub/ai-coding-starter-kit](https://github.com/AlexPEClub/ai-coding-starter-kit).
Sein Projekt hat die Grundlage geschaffen, Produktentwicklung durch wiederverwendbare
Claude-Code-Skills zu führen. Diese Edition ist möglich, weil Alex diese Idee
öffentlich mit der Community geteilt hat.

Das Original ist auf produktionsreife Web-Apps mit einem konkreten
Next.js-/TypeScript-/Tailwind-/shadcn-/Supabase-/Vercel-Weg ausgerichtet. Diese
JF-Edition verfolgt ergänzend einen anderen Schwerpunkt:

- technologieoffen statt festem App-Stack;
- Claude Code **und** Codex;
- Greenfield **und** strukturierte Übernahme bestehender Repositories;
- Git-geteiltes Onboarding, dauerhafte Tasks und Workflow-Status-SSOT;
- Review-Loop, Audit-Plan-Loop, Skill-Proxy-Sync und sicherer Branch-Abschluss;
- keine vorgegebene Produktimplementierung im Template.

Das ist kein Qualitätsurteil. Das Original ist ideal, wenn genau dieser Web-Stack
gewünscht ist. Diese Ableitung ist für breitere Technologieentscheidungen,
bestehende Projekte und Claude-/Codex-Portabilität gedacht.

Weitere Herkunfts- und Lizenzinformationen: [UPSTREAM.md](UPSTREAM.md).

### Maintainer

Weiterentwickelt und gepflegt von **Jens Fehrmann**
([@jnsfhrmnn](https://github.com/jnsfhrmnn)), AI Developer mit Fokus auf
Context Engineering, repository-lokale Agent-Workflows, deterministische
Sicherheitsprüfungen und evidenzbasierte Softwareauslieferung.

Wenn dir das Kit hilft, gib dem Repository einen Star, eröffne ein klar abgegrenztes
Issue oder zeige, was du damit gebaut hast.

---

## License / Lizenz

This derivative is distributed under the [MIT License](LICENSE) with explicit
upstream attribution. The upstream README declares MIT, but the upstream repository
did not contain a standalone license file when this edition was prepared. Preserve
the copyright and permission notices in redistributed copies. See
[UPSTREAM.md](UPSTREAM.md) for the complete provenance note and remaining caveat.

Diese Ableitung wird mit ausdrücklicher Upstream-Nennung unter der
[MIT-Lizenz](LICENSE) verteilt. Das Upstream-README nennt MIT, enthielt zum Zeitpunkt
der Prüfung aber keine separate Lizenzdatei. Copyright- und Erlaubnishinweise müssen
bei Weitergabe erhalten bleiben. Details stehen in [UPSTREAM.md](UPSTREAM.md).
