---
name: 7-csk-deploy
description: Release, package, deploy, or hand off an Approved feature using the architecture-approved target. Use only after recorded QA evidence and branch integration, with a readiness review before external action and a final review of the actual result before Deployed bookkeeping or tagging.
argument-hint: feature-spec-path or release/package/deploy target
user-invocable: true
---

# Release / Packaging / Deployment

Release only what QA approved, through the target and process recorded in the
architecture. A plan, successful local build, or user request to "deploy" does
not by itself prove release readiness or authorize external actions.

## Entry contract

1. Run `/csk-start` and read `.claude/rules/workflow-state.md`.
2. Resolve repository-local adapter config and source-of-truth paths.
3. Read architecture, master feature, engineering principles, loop policy,
   feature index, owning feature spec, QA results, and release instructions.
4. Require authoritative feature status `Approved` plus recorded QA evidence and
   no unresolved Critical/High finding.
5. Require an architecture-approved release/package/deploy target and rollback,
   recovery, or rerun path.
6. Inspect live Git state. If verified feature work remains on a non-default
   branch, run `/finish-branch` before release. Do not release from an unmerged or
   ambiguous branch unless the documented release process explicitly requires it
   and the user approves that exception.

If any gate is missing, stop and route to the owning skill. Do not use a quick-fix
waiver to bypass `Approved` status or evidence.

If `deploySkill` is configured, complete readiness checks here, then hand release
execution to that named repository-local skill. Resume this skill only with
direct release-result evidence.

## Phase 1: Harden and verify the release plan

Apply the planning hardening policy for non-trivial releases. Verify:

- target and version fit the architecture and approved feature scope;
- exact build/package/deploy commands and artifact inputs;
- local/offline, online/cloud, privacy, data-egress, licensing, and secret rules;
- configuration, migration, compatibility, platform, performance, cost, and
  resource assumptions;
- backup, rollback, recovery, rerun, monitoring, and handoff paths;
- how partial success can be detected and recovered without duplicate effects.

Run project-native build, test, lint, type, package, security, artifact, and smoke
checks required by the release. Verify that environment examples contain dummy
values only and that no secret or local-only artifact is included.

## Phase 2: Readiness review before external action

Run `/review-loop` on the release plan and pre-release evidence before any
publish, upload, tag, store, cloud, production, or other external mutation.
Disposition every Critical/High finding. The review must cover target fit, QA
evidence, artifact contents, privacy/security, rollback, observability, and
partial-failure recovery.

Present the user with:

- exact target, version, artifact, and commands/actions;
- evidence and remaining risks;
- external systems affected;
- rollback/recovery path;
- whether a Git tag or release record is proposed.

Obtain explicit approval for the exact external release actions. Treat tagging,
pushing a tag, creating a hosted release, publishing an artifact, and deploying
as distinct actions unless the user explicitly approves the bundled plan.

## Phase 3: Execute and observe

1. Build or select the exact approved artifact and record its identity/checksum
   where the architecture calls for it.
2. Execute only approved release actions through the approved target or delegated
   skill.
3. Capture command output, job/build IDs, artifact/version identifiers, URLs, and
   timestamps as available.
4. After every external boundary, inspect actual state. Never infer completion
   from a submitted request alone.
5. On failure or timeout, stop automatic progression, determine whether any part
   succeeded, and preserve an exact recovery task through `/csk-start` when the
   issue will survive the session.

Never rerun a possibly non-idempotent release blindly. A partial upload, package
publication, tag, hosted release, or deployment is incomplete until reconciled.

## Phase 4: Post-release verification

- Verify that the released artifact installs, starts, loads, or runs on its
  actual target.
- Smoke-test the released feature and critical affected journeys.
- Check health, logs, errors, permissions, configuration, migrations, external
  integrations, and monitoring appropriate to the target.
- Confirm no secrets, local-only data, prompts, caches, raw model output,
  temporary files, or sensitive logs escaped into the artifact or environment.
- Exercise or prove the rollback/recovery/rerun path to the documented degree.

If release or smoke verification fails, keep feature status `Approved`, record
the observed external state and recovery evidence, and do not tag or claim
`Deployed`.

## Phase 5: Final review of the actual result

After the release attempt and smoke checks, run `/review-loop` again on the
actual artifact/environment and captured evidence. This is separate from the
readiness review. Confirm:

- intended target and version are really live or handed off;
- release evidence is direct and internally consistent;
- QA assumptions still hold in the target environment;
- security, privacy, processing-mode, performance, and observability promises
  remain true;
- rollback and partial-state risks are resolved or explicitly block completion.

Do not update `Deployed`, create a final release tag, or close release
bookkeeping while a Critical/High result finding remains unresolved.

## Phase 6: Bookkeeping and optional tag

Only after final review passes:

1. If the approved release process requires a Git tag, create and push it only
   with the explicit tag authority obtained for the release plan, then verify
   both local and remote tag targets. A required-tag failure keeps the feature
   `Approved` and creates one exact recovery task; do not advance status.
2. Record release details, date, target, version, artifact/URL, commit SHA,
   required tag, verification, rollback path, and both review results in the
   feature spec.
3. Update the feature spec and feature index together to `Deployed`; reread both.
4. Close the owning durable task through `/csk-start` only when its acceptance
   condition is met and typed evidence exists.

Release evidence may be an artifact path/hash, URL, version, verified tag,
commit, job ID, or handoff record. Missing evidence leaves status `Approved`.

## Completion report

Report readiness review, approved external actions, actual target/version,
artifact and commit identity, smoke/monitoring result, final review, rollback
state, feature/task bookkeeping, tag state, and remaining risks. Say
`incomplete` for partial external state.

Before ending, preserve only durable unfinished or blocked work through
`/csk-start`. If a release branch remains open after a verified release result,
route it to `/finish-branch`.
