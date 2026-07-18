# Failure Visibility And Error Tracking

Use this guide after `/3-csk-architecture` chooses a runtime and `/7-csk-deploy` identifies a release target.

## Goal

Production failures should be visible, attributable, and actionable.

## Choose A Tool

Pick the smallest option that fits the architecture:

- Platform-native logs and alerts.
- Hosted error tracking.
- Self-hosted observability.
- Simple structured logs for local/internal tools.

Record the choice in `docs/architecture.md`.

## Minimum Setup

- Capture unhandled errors.
- Capture failed background jobs or scheduled work.
- Include release/version identifiers.
- Include environment identifiers.
- Redact secrets and sensitive payloads.
- Define who receives alerts.

## Verification

- Trigger a safe test failure in a non-production environment.
- Confirm the failure is visible.
- Confirm stack traces or diagnostics are useful.
- Confirm sensitive data is not captured.
- Confirm the alert route reaches the right person/team.

## Release Checklist

- [ ] Error visibility tool chosen.
- [ ] Setup documented in `docs/architecture.md`.
- [ ] Required config variables documented with dummy values only.
- [ ] Safe test error verified.
- [ ] Alert ownership documented.
