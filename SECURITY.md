# Security Policy

## Reporting a vulnerability

Please do not publish an exploitable vulnerability, secret, credential, or private
repository content in a public issue.

Use GitHub's private vulnerability reporting/security-advisory channel for this
repository when available. If that channel is unavailable, contact the maintainer
through the GitHub profile at <https://github.com/jnsfhrmnn> and request a private
reporting path without including sensitive details in the first public message.

Include affected files/versions, impact, reproduction conditions, and a minimal
proof. Do not access data or systems you do not own or have permission to test.

## Scope

Security-sensitive areas include:

- repository-local agent permissions and command boundaries;
- Git remote classification, branch integration, and publication safeguards;
- deterministic state/task mutation and evidence validation;
- path containment, symlink handling, locks, and atomic writes;
- accidental publication of plans, credentials, environment files, or sessions;
- Claude-to-Codex proxy generation and path resolution.

Product code created from this template has its own dependency and deployment
security obligations. The kit's MIT license does not provide a warranty.
