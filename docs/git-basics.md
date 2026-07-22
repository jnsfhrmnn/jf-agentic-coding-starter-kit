# Git Basics for Beginners / Git-Grundlagen für Anfänger

**[English](#english) · [Deutsch](#deutsch)**

This kit promises that you can work safely without knowing Git commands. That
promise holds because the workflow proposes every Git action, explains it, and
asks first. What you still need are a few **concepts**, so the questions the
workflow asks you actually make sense. This page is that missing piece. The
agent references it whenever a Git decision is yours to make.

---

<a id="english"></a>

## English

### The ten terms you actually need

| Term | Plain meaning |
|---|---|
| **Repository** | Your project folder plus its complete change history. |
| **Commit** | A named save point of your work - like a snapshot you can always return to. |
| **`main`** | The main line of your project - the one version that counts. (Older repositories call it `master`.) |
| **Branch** | A parallel lane next to `main` where work happens without touching the main line. |
| **Remote / `origin`** | The copy of your repository on a server (usually GitHub). `origin` is *your* project there; `upstream` is the template this kit came from - never a place to push your work. |
| **Push** | Upload your local commits to `origin`. Until you push, your save points exist only on your machine. |
| **Pull** | Download the newest commits from `origin` into your local copy. |
| **Pull request (PR)** | The controlled door through which a branch's work enters `main`: it shows the changes, runs the checks, and merges only when everything is green. |
| **Merge / merge commit** | Bringing one branch's work into another. A PR merge leaves a visible "these two lines joined here" save point - the merge commit. |
| **Worktree** | A second working folder attached to the same repository, with its own branch. Two sessions can work at the same time without touching each other. |

### Commit is not push

The most common beginner mix-up: a **commit** saves locally, a **push**
uploads. After a commit your work survives a lost session, but it is not on
GitHub yet. The workflow therefore treats them as two separate questions and
will never push just because you approved a commit.

### The three levels of parallel work

Before opening a second agent session, answer one question: *how many
sessions are working on this repository right now?*

```text
LEVEL 1 - One session at a time
  -> Work on main. No branches, no worktrees.
     Extra structure here is complexity without benefit.

LEVEL 2 - A second session on the SAME working copy
  -> Risk mode, not a permanent setup. Both sessions share files,
     index, and HEAD. If you must: never touch the same files, and
     never run Git actions (commit/pull) at the same moment.
     The kit warns you and points to level 3.

LEVEL 3 - Real parallel work (the actual workflow)
  -> The second agent gets its OWN PERMANENT worktree with its own
     branch (skill: create-worker-worktree) and opens its session
     DIRECTLY in that folder. Parallel, isolated, fast, safe.
```

Level 2 is not theoretical: two sessions on one working copy have produced,
within two days, a detached HEAD in the middle of a commit chain, foreign
unpushed commits inside the own push, a branch switch during a command
sequence, twice-discarded edits, and an index blocked by someone else's lint
error. The worktree makes all of that impossible.

### The orchestrator + worker cycle

One agent is the **orchestrator** (conductor) and keeps the main checkout on
`main`. Every additional agent is a **worker** with its own permanent
worktree and branch. Integration back into `main` goes exclusively through a
pull-request merge; afterwards the orchestrator fast-forwards its local
`main`.

```text
1. Create the worktree            (once - it is permanent)
2. Work in parallel               (orchestrator on main, worker in its folder)
3. Worker: merge the PR           (green checks, real merge commit,
                                   branch is KEPT)
4. Sync both sides                (one command everywhere: /pull-main-ff -
                                   on main it pulls fast-forward; on the
                                   worker branch it re-syncs and updates
                                   the remote ref)
5. main is current again          -> continue at 2
```

`/pull-main-ff` is deliberately **one** command for both sides: wherever you
stand, it brings you safely up to date - and when it stops, it tells you why
and what to do next. If your worker branch still carries commits that never
went through a pull request, it refuses and points you to `finish-branch`
first; nothing is merged silently.

Why step 3 keeps and re-syncs the branch: after every PR merge, `main` is
ahead of the worker branch. Because the PR used a real merge commit, the
worker branch is an ancestor of the new `main`, so the re-sync is a clean
fast-forward - no force ever needed. Skipping the re-sync lets the branch
drift further behind with every cycle until every new PR is conflict-prone.

### Memory hooks

- **Alone? Stay on `main`.** Parallel? Take a worktree.
- **One conductor, many musicians:** one agent holds `main` - every other
  agent plays in its own folder.
- **A worktree is not disposable:** create once, use permanently, re-sync
  after every merge.
- **Work returns to `main` only through the door (PR)** - never through the
  window (direct push).
- **When a tool stops, that is protection, not a defect:** read, understand,
  then decide deliberately.

### When something stops: what it means and what to do

The kit's tools fail closed: on any doubt they change nothing and stop. Every
stop below is safe - nothing has been lost when you see it.

| You see | What it means | Your next safe step |
|---|---|---|
| "uncommitted tracked changes" | There is unsaved work in the folder. The tool refuses to mix it with incoming changes. | Let the agent show the changes; commit what belongs to your task, then rerun. |
| `MERGE-COMMIT-GATE` | New commits reached `main` without going through a pull request. | Answer the agent's question: do you know where these commits came from? Confirm only if yes. |
| "main and origin/main have diverged" | Your local main line and the server version both moved - they no longer agree. | Do not force anything. Let the agent show both sides; usually your local extra commits belong on a branch. |
| Push rejected ("non-fast-forward") | The server has newer commits than you. Overwriting them would destroy someone's work. | Pull first (the agent proposes the safe way), then push again. |
| Merge conflict | Two lines changed the same spot; Git cannot decide which version is right. | Nothing is broken. The agent shows both versions; you pick, it resolves. |
| Red checks on a PR | Automated tests found a problem in the branch. | The merge stays blocked on purpose. Fix the finding on the branch; merge when green. |
| "worker branch has local commits not on origin" | Your worktree carries finished work that never went through a pull request; syncing now would silently mix it. | Integrate the work through `finish-branch` (pull request, checks, merge), then run the sync again. |
| "detached HEAD" | The session is standing on a specific save point instead of a branch - new commits would dangle. | Do not commit. The agent proposes returning to a branch or naming a rescue branch. |
| Protected-branch notice in `finish-branch` | The branch is permanent worker infrastructure. It gets re-synced, never deleted. | Nothing to do - that is the intended behaviour. |

### Practice without risk

Everything above can be rehearsed in a throwaway repository in ten minutes:
create an empty repo on GitHub, clone it, ask the agent to run one full cycle
(worktree, small change, PR, merge, re-sync, fast-forward). Nothing there is
precious, so every stop and every question can be explored calmly - the same
way this kit's own Git tooling was verified.

### What the kit never does

You will never see the workflow use force pushes, history rewrites on shared
branches, `--no-verify`, blind `git add -A` staging, or deleting branches
whose work is not proven to be on `origin/main`. These are not "advanced
techniques you learn later" - inside this workflow they simply do not exist.

---

<a id="deutsch"></a>

## Deutsch

### Die zehn Begriffe, die du wirklich brauchst

| Begriff | Klartext |
|---|---|
| **Repository** | Dein Projektordner samt vollständiger Änderungshistorie. |
| **Commit** | Ein benannter Speicherpunkt deiner Arbeit — wie ein Spielstand, zu dem du jederzeit zurück kannst. |
| **`main`** | Die Hauptlinie deines Projekts — die eine Version, die zählt. (Ältere Repositories nennen sie `master`.) |
| **Branch** | Eine Parallelspur neben `main`, auf der gearbeitet wird, ohne die Hauptlinie anzufassen. |
| **Remote / `origin`** | Die Kopie deines Repositories auf einem Server (meist GitHub). `origin` ist *dein* Projekt dort; `upstream` ist die Vorlage, aus der dieses Kit kam — dorthin wird nie gepusht. |
| **Push** | Lädt deine lokalen Commits zu `origin` hoch. Vor dem Push existieren deine Speicherpunkte nur auf deinem Rechner. |
| **Pull** | Holt die neuesten Commits von `origin` in deine lokale Kopie. |
| **Pull Request (PR)** | Die kontrollierte Tür, durch die Branch-Arbeit nach `main` kommt: zeigt die Änderungen, lässt die Prüfungen laufen und merged erst, wenn alles grün ist. |
| **Merge / Merge-Commit** | Führt die Arbeit eines Branches in einen anderen über. Ein PR-Merge hinterlässt einen sichtbaren „hier wurden zwei Spuren vereint"-Speicherpunkt — den Merge-Commit. |
| **Worktree** | Ein zweiter Arbeitsordner am selben Repository, mit eigenem Branch. Zwei Sessions können gleichzeitig arbeiten, ohne sich zu berühren. |

### Commit ist nicht Push

Die häufigste Anfänger-Verwechslung: Ein **Commit** speichert lokal, ein
**Push** lädt hoch. Nach einem Commit überlebt deine Arbeit einen
Session-Verlust — auf GitHub ist sie damit aber noch nicht. Der Workflow
behandelt beides deshalb als zwei getrennte Fragen und pusht nie, nur weil du
einen Commit freigegeben hast.

### Die drei Stufen paralleler Arbeit

Bevor eine zweite Agenten-Session aufgeht, beantworte eine Frage: *Wie viele
Sessions arbeiten gerade an diesem Repository?*

```text
STUFE 1 — Eine Session, nacheinander
  -> Einfach auf main arbeiten. Keine Branches, keine Worktrees.
     Zusätzliche Struktur wäre hier Komplexität ohne Nutzen.

STUFE 2 — Eine zweite Session auf DERSELBEN Working-Copy
  -> Risiko-Modus, kein Dauerzustand. Beide Sessions teilen sich
     Dateien, Index und HEAD. Wenn es sein muss: nie an denselben
     Dateien arbeiten, und Git-Aktionen (Commit/Pull) nie zeitgleich.
     Das Kit warnt dich und führt zu Stufe 3.

STUFE 3 — Echtes paralleles Arbeiten (der eigentliche Workflow)
  -> Der zweite Agent bekommt einen EIGENEN, DAUERHAFTEN Worktree
     mit eigenem Branch (Skill: create-worker-worktree) und öffnet
     seine Session DIREKT in diesem Ordner.
     Parallel, isoliert, schnell, sicher.
```

Stufe 2 ist nicht theoretisch: Zwei Sessions auf einer Working-Copy haben in
zwei Tagen einen detached HEAD mitten in einer Commit-Kette, fremde ungepushte
Commits im eigenen Push, einen Branch-Wechsel während einer Befehlsfolge,
zweimal verworfene Änderungen und einen durch fremden Lint-Fehler blockierten
Index erzeugt. Der Worktree macht all das unmöglich.

### Der Orchestrator-und-Worker-Zyklus

Ein Agent ist der **Orchestrator** (Dirigent) und hält den Haupt-Checkout auf
`main`. Jeder weitere Agent ist ein **Worker** mit eigenem, dauerhaftem
Worktree und Branch. Zurück nach `main` geht es ausschließlich über einen
Pull-Request-Merge; danach zieht der Orchestrator seinen lokalen `main` per
Fast-Forward nach.

```text
1. Worktree anlegen               (einmal — er ist dauerhaft)
2. Parallel arbeiten              (Orchestrator auf main, Worker im eigenen Ordner)
3. Worker: PR mergen              (grüne Checks, echter Merge-Commit,
                                   Branch BLEIBT)
4. Beide Seiten nachziehen        (überall dasselbe Kommando: /pull-main-ff —
                                   auf main pullt es per Fast-Forward; auf dem
                                   Worker-Branch re-synct es und zieht die
                                   Remote-Ref nach)
5. main ist wieder aktuell        -> weiter bei 2
```

`/pull-main-ff` ist bewusst **ein** Kommando für beide Seiten: Egal wo du
stehst — es bringt dich sicher auf den neuesten Stand, und wenn es stoppt,
sagt es dir warum und was als Nächstes zu tun ist. Trägt dein Worker-Branch
noch Commits, die nie durch einen Pull Request gegangen sind, verweigert es
und verweist zuerst auf `finish-branch` — nichts wird still gemergt.

Warum Schritt 3 den Branch behält und nachzieht: Nach jedem PR-Merge liegt
`main` vor dem Worker-Branch. Weil mit echtem Merge-Commit gemergt wurde, ist
der Worker-Branch ein Vorfahr des neuen `main` — der Re-Sync ist ein sauberer
Fast-Forward, nie ist Force nötig. Ohne Re-Sync fällt der Branch mit jedem
Zyklus weiter zurück, bis jeder neue PR konfliktträchtig wird.

### Merksätze

- **Allein? Bleib auf `main`.** Parallel? Nimm einen Worktree.
- **Ein Dirigent, viele Musiker:** Einer hält `main` — jeder andere spielt in
  seinem eigenen Ordner.
- **Der Worktree ist kein Wegwerf-Artikel:** einmal anlegen, dauerhaft
  nutzen, nach jedem Merge nachziehen.
- **Zurück auf `main` geht es nur durch die Tür (PR)** — nie durchs Fenster
  (Direkt-Push).
- **Wenn ein Werkzeug stoppt, ist das Schutz, kein Defekt:** lesen,
  verstehen, dann bewusst entscheiden.

### Wenn etwas stoppt: was es heißt und was du tust

Die Werkzeuge des Kits sind fail-closed: Im Zweifel ändern sie nichts und
halten an. Jeder Stopp unten ist sicher — wenn du ihn siehst, ist nichts
verloren gegangen.

| Du siehst | Was es bedeutet | Dein nächster sicherer Schritt |
|---|---|---|
| „uncommitted tracked changes" | Im Ordner liegt ungesicherte Arbeit. Das Werkzeug weigert sich, sie mit eingehenden Änderungen zu vermischen. | Lass dir die Änderungen zeigen; committe, was zu deiner Aufgabe gehört, dann erneut ausführen. |
| `MERGE-COMMIT-GATE` | Neue Commits sind ohne Pull Request auf `main` gelandet. | Beantworte die Frage des Agenten: Weißt du, woher diese Commits kommen? Nur bestätigen, wenn ja. |
| „main and origin/main have diverged" | Deine lokale Hauptlinie und die Server-Version haben sich beide bewegt — sie stimmen nicht mehr überein. | Nichts erzwingen. Lass dir beide Seiten zeigen; meist gehören deine lokalen Extra-Commits auf einen Branch. |
| Push abgelehnt („non-fast-forward") | Der Server hat neuere Commits als du. Überschreiben würde fremde Arbeit zerstören. | Erst pullen (der Agent schlägt den sicheren Weg vor), dann erneut pushen. |
| Merge-Konflikt | Zwei Spuren haben dieselbe Stelle geändert; Git kann nicht entscheiden, welche Version richtig ist. | Nichts ist kaputt. Der Agent zeigt beide Versionen; du wählst, er löst auf. |
| Rote Checks am PR | Automatische Tests haben ein Problem im Branch gefunden. | Der Merge bleibt absichtlich blockiert. Befund auf dem Branch beheben; mergen, wenn grün. |
| „worker branch has local commits not on origin" | Dein Worktree trägt fertige Arbeit, die nie durch einen Pull Request gegangen ist; jetzt zu syncen würde sie still vermischen. | Arbeit erst über `finish-branch` integrieren (Pull Request, Checks, Merge), dann den Sync erneut ausführen. |
| „detached HEAD" | Die Session steht auf einem einzelnen Speicherpunkt statt auf einem Branch — neue Commits würden in der Luft hängen. | Nicht committen. Der Agent schlägt vor, auf einen Branch zurückzukehren oder einen Rettungs-Branch zu benennen. |
| Schutz-Hinweis in `finish-branch` | Der Branch ist dauerhafte Worker-Infrastruktur. Er wird nachgezogen, nie gelöscht. | Nichts zu tun — genau das ist das gewollte Verhalten. |

### Gefahrlos üben

Alles oben lässt sich in zehn Minuten in einem Wegwerf-Repository
durchspielen: leeres Repo auf GitHub anlegen, klonen, den Agenten einen
vollen Zyklus fahren lassen (Worktree, kleine Änderung, PR, Merge, Re-Sync,
Fast-Forward). Dort ist nichts wertvoll — jeder Stopp und jede Frage kann in
Ruhe erkundet werden. Genau so wurde auch das Git-Tooling dieses Kits
verifiziert.

### Was das Kit niemals tut

Du wirst im Workflow nie Force-Pushes, Historien-Umschreibungen auf geteilten
Branches, `--no-verify`, blindes `git add -A` oder das Löschen von Branches
sehen, deren Arbeit nicht nachweislich auf `origin/main` liegt. Das sind
keine „Fortgeschrittenen-Techniken für später" — innerhalb dieses Workflows
existieren sie schlicht nicht.
