---
paths:
  - "**/.env*"
  - "api/**"
  - "backend/**"
  - "db/**"
  - "server/**"
  - "services/**"
  - "src/**"
---

# Security Rules

## Secrets Management
- Never commit secrets, API keys, credentials, tokens, private keys, or production config.
- Keep local secrets in ignored environment/config files.
- Document required environment variables with dummy values only.
- Treat public/client-exposed variables as non-secret.

## Data Locality And Privacy
- For any pipeline, classify whether data is processed offline/local, online/cloud, or hybrid according to `docs/architecture.md`.
- Do not send prompts, files, embeddings, logs, telemetry, caches, intermediate artifacts, model outputs, identifiers, secrets, or sensitive payloads across a trust boundary unless architecture explicitly approves it.
- Minimize, redact, encrypt, retain, delete, and log data according to the approved architecture.
- If the local/cloud boundary is unclear, stop and return to `/3-csk-architecture`.

## Input And Output Safety
- Validate untrusted input at the trusted boundary chosen by the architecture.
- Sanitize or encode output according to the rendering context.
- Do not rely on client-side validation alone when a server or shared data layer exists.

## Authentication And Authorization
- If the architecture includes users, accounts, or permissions, verify authentication before protected operations.
- Enforce authorization at data/service boundaries, not only in UI.
- Re-check access control on every mutation and sensitive read.

## Production Security
- For web apps, configure appropriate transport, framing, content sniffing, referrer, and content security headers.
- Add rate limiting, abuse controls, or quotas to public write endpoints when relevant.
- Log security-relevant failures without logging secrets or sensitive payloads.

## Review Triggers
- Any auth, authorization, encryption, key handling, or data isolation change requires explicit user review.
- Any new external service or environment variable must be documented.
- Any local/cloud/hybrid boundary, AI provider/model, external inference, telemetry, log, cache, file-transfer, or data-retention change requires the review-loop gate from `.claude/rules/loop-policy.md`.
