# Abuse Controls And Rate Limiting

Use this guide when the product exposes public endpoints, high-cost actions, authentication flows, file uploads, payments, AI calls, or other abuse-prone operations.

## Goal

Protect users, infrastructure, cost, and data integrity without blocking legitimate use.

## Decide What To Limit

Common candidates:

- Login or signup attempts.
- Password reset or invite flows.
- Public write endpoints.
- File uploads.
- Search or export actions.
- Expensive compute or external API calls.
- Webhooks.

## Choose A Strategy

Use the strategy approved in `docs/architecture.md`:

- In-process limits for local/internal tools.
- Platform edge limits.
- Gateway or reverse-proxy limits.
- Datastore-backed counters.
- Queue-based throttling.
- Provider-native quotas.

## Design Questions

- What identity is limited: user, IP, tenant, API key, device, or action?
- What is the window and limit?
- What happens when the limit is reached?
- How are admins or support staff notified?
- How are false positives handled?

## Verification

- Test normal usage.
- Test burst usage.
- Test repeated abuse attempts.
- Confirm error messages are useful and do not leak internals.
- Confirm limits are observable in logs or metrics.

## Checklist

- [ ] Abuse-prone actions identified.
- [ ] Limit strategy approved by architecture.
- [ ] User-facing failure behavior defined.
- [ ] Observability path documented.
- [ ] Tests or manual verification completed.
