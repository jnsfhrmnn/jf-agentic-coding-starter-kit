# Web Security Controls

Use this guide only when the chosen architecture exposes a web surface.

## Goal

Reduce common browser-side risks such as clickjacking, MIME sniffing, unsafe referrers, downgrade attacks, and script injection.

## Baseline Controls

Choose the platform-specific implementation during `/3-csk-architecture` or `/7-csk-deploy`.

Recommended controls for most web apps:

- Force HTTPS in production.
- Prevent framing unless embedding is explicitly required.
- Disable MIME sniffing.
- Set a strict referrer policy.
- Add a Content Security Policy when the app surface is stable enough.
- Restrict cross-origin access where applicable.
- Mark cookies secure, HTTP-only, and same-site where applicable.

## Verification

- Inspect production response headers.
- Confirm HTTPS redirect or enforcement.
- Confirm the app cannot be framed unless intended.
- Confirm cookies do not expose sensitive values to client scripts.
- Confirm CSP does not break expected assets or integrations.

## Checklist

- [ ] Web security controls selected for the chosen platform.
- [ ] Controls configured in the approved code/config location.
- [ ] Production responses verified.
- [ ] Any intentional exceptions documented.
