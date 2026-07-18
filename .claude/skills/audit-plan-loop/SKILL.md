---
name: audit-plan-loop
description: Iterative, evidence-based working mode for building or refining a non-trivial deliverable through visible AUDIT, PLAN, REFINE, and LOG cycles. Use for plans, specifications, architecture, migrations, policies, complex documents, or implementation approaches that need contextual LLM judgment, explicit assumptions, adversarial self-critique, and convergence instead of a one-pass answer. Repository-local and single-repository only.
---

# Audit Plan Loop

Build one non-trivial deliverable iteratively. Seek weaknesses in the current
work instead of defending it, refine only verified problems, and stop when the
result converges.

## Gate 0: Establish The Brief

Before producing the deliverable:

1. Inspect available skills and tools; read applicable repository-local skills.
2. Read `AGENTS.md`, `CLAUDE.md`, relevant rules, and `tasks/INDEX.md`.
3. Restate the objective, scope, success criteria, constraints, and known facts.
4. List assumptions, gaps, and ambiguities.
5. Ask only when a critical ambiguity would materially change the result or
   require new authority. Otherwise state a safe assumption and continue.

Show a compact `GATE 0` block. Do not use the loop to hide a missing decision.

## Determine Write Authority

Do not infer repository write authority from invoking this skill.

- **Conversation-only:** when the user asks for a plan, explanation, analysis,
  or other answer without requesting repository changes, keep the deliverable
  in the response and do not mutate repository state.
- **Repository work:** write only when the current request already authorizes
  creating or changing repository artifacts, and remain inside that scope.
- **Pending persistence:** when conversation-only work reveals a follow-up that
  belongs in repository state, identify its exact proposed SSOT or task target
  as `PENDING-AUTH` and request one consolidated authorization before writing.

## Choose Evidence Intelligently

Use deterministic tools for mechanical facts such as file existence, parsing,
schema checks, link resolution, tests, linting, builds, counts, and diffs. Use
LLM context judgment for semantic completeness, intent, trade-offs, coherence,
missing concepts, risk, and whether different evidence means the same thing.

Do not force a semantic problem into a deterministic rule. Do not use LLM
judgment where a reliable mechanical check can answer exactly.

Define the best available evidence before starting. If an assertion cannot be
verified, label it `unverified`; never convert plausibility into proof.

## Maintain A Finding Backlog

Track each real weakness with:

- stable ID;
- location or affected decision;
- severity: `critical`, `high`, `medium`, or `low`;
- confidence from 0 to 100;
- evidence or `unverified`;
- next refinement;
- status.

Severity measures impact if true. Confidence measures whether the diagnosis is
correct. Prioritize by both; never silently discard a high-impact suspicion.
Verify uncertain critical or high findings before changing the deliverable.

## Run AUDIT -> PLAN -> REFINE -> LOG

Use compact visible iterations. The maximum is 20, but early convergence is the
goal.

### AUDIT

- Inspect the current deliverable against Gate 0 and its source-of-truth files.
- Check correctness, completeness, contradictions, edge cases, failure paths,
  security/privacy implications, performance, compatibility, and maintenance.
- From iteration 2 onward, verify that the last refinement fixed the intended
  cause without creating a regression.
- Name concrete locations and evidence. Record clean dimensions without
  inventing findings.

### PLAN

- Select the smallest coherent set of next refinements.
- Address verified critical/high findings first.
- State what changes, why, and how it will be verified.
- Ask before large, structural, hard-to-reverse, externally visible, or
  authority-expanding changes.

### REFINE

- Apply only authorized, in-scope changes.
- Preserve existing user work and repository rules.
- Do not opportunistically change unrelated code or another repository.
- Verify the affected surface immediately after the change.

### LOG

Use this compact record:

```text
Iteration N — findings: C/H/M/L | changed: <delta> | evidence: <result> | open: <IDs>
```

Keep the backlog durable across context compaction. Do not reprint whole files;
reference paths, sections, and deltas.

## Independent Refutation

Before acting on a critical/high finding below 90 confidence, ask an independent
agent to try to disprove it when such an agent is available. Provide only the
artifact, claimed defect, applicable rules, and verification tooling. If no
independent agent is available, perform and log an explicit contrary
refutation pass in the current context.

Before declaring a large or high-risk deliverable complete, use an independent
convergence check against Gate 0. A reproducible proof at confidence 90 or above
may use a logged one-sentence cause/fix confirmation instead of fan-out.

## Convergence

Stop on the first condition that applies:

1. No critical/high finding remains and the latest audit found no substantial
   new weakness; required evidence is green.
2. An iteration produced no measurable improvement; report stagnation and a
   materially different approach.
3. Iteration 20 is reached.

Never claim completion only because the iteration limit was reached. Mark all
remaining critical/high items `UNRESOLVED`.

## Preserve Open Work Locally

When repository writes are authorized, no open finding may survive only in
chat. Keep state in its existing SSOT:

- feature scope/status/evidence in the relevant feature spec;
- product gaps in `docs/master-feature.md`;
- architecture decisions in `docs/architecture.md`;
- durable continuation work in `tasks/INDEX.md` through `/csk-start`, only when
  it remains open/blocked, spans the current session, is explicitly deferred, or
  is a verified interruption point. Do not create same-turn task churn.

Without write authority, do not mutate these files. Mark each proposed
continuation `PENDING-AUTH`, name its exact local target, and state that it is
not yet durably conserved. Once writes are authorized, keep all workflow state
inside the current repository, record each follow-up exactly once, and link to
its owning SSOT.

## Final Handoff

Report the iterations, final artifact paths, verification evidence, remaining
risks, and the exact local disposition of every unresolved item.
