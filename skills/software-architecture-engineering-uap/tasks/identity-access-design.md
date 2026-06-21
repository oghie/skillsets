# Identity And Access Design

Use this when designing authentication, identity, authorization, sessions, MFA, passwordless login, account lifecycle, admin user management, or audit logging.

## Workflow

1. Define identity scope:
   - human users, anonymous users, service accounts, admins, tenants, devices, and external identity providers.
   - account lifecycle: anonymous, registered, pending email verification, active, locked, suspended, deactivated, deleted.
2. Define trust boundaries:
   - browser/mobile/client, API edge, auth service, identity store, session/token store, mail/SMS provider, IdP, admin surface.
3. Choose authentication model:
   - first-party email/password, passwordless magic link/OTP, anonymous account upgrade, OIDC/SAML federation, passkeys/WebAuthn, or service tokens.
4. Choose session model:
   - opaque server sessions, JWT access tokens plus refresh tokens, or hybrid.
   - define expiry, rotation, revocation, device/session listing, logout-all, and stolen-token response.
5. Define authorization model:
   - RBAC, ABAC, relationship-based access, policy engine, tenant scoping, resource ownership, and admin overrides.
6. Design recovery flows:
   - email verification, password reset, MFA recovery, account deactivation/reactivation, compromised account response.
7. Define abuse controls:
   - rate limits, credential stuffing protection, enumeration resistance, risk scoring, step-up authentication, and audit alerts.
8. Map API, data, behavior, deployment, NFR, and verification.

## Required Artifacts

```markdown
| Artifact | Required Content |
|---|---|
| Boundary model | Clients, auth service, identity store, session store, providers, admin surface |
| Endpoint catalog | Public auth endpoints, MFA endpoints, admin endpoints, audit endpoints |
| Token/session matrix | Token type, storage, TTL, rotation, revocation, audience, issuer |
| Authorization matrix | Role/policy/resource/action rules and tenant constraints |
| Account lifecycle | States, transitions, triggers, recovery, deactivation/deletion |
| Threat model | Credential stuffing, token theft, session fixation, CSRF, XSS, replay, enumeration, privilege escalation |
| Audit model | Events, actor, subject, IP/device, correlation ID, retention, integrity |
| Verification plan | Unit, integration, contract, security, abuse, recovery, and audit tests |
```

## Endpoint Design Order

1. Account creation and identity proofing.
2. Login/session creation.
3. Session refresh and revocation.
4. Current principal lookup.
5. MFA enrollment, challenge, recovery, and removal.
6. Passwordless and password recovery flows.
7. Email verification and account lifecycle.
8. Admin user operations.
9. Audit logs and security event export.

## View Mapping

| Architecture View | IAM Design Questions |
|---|---|
| Functional | Which components own registration, login, token issuance, MFA, session listing, admin user changes, and audit? |
| Information | Which stores own users, identities, credentials, MFA methods, sessions, refresh tokens, roles, policies, audit events, and recovery codes? |
| Behavior | How do login, refresh, logout, MFA challenge, reset password, account deactivation, and admin role changes flow? |
| Deployment | Where are secrets, token signing keys, HSM/KMS, IdP callbacks, mail/SMS gateways, WAF/rate limits, and audit sinks deployed? |
| NFR | What are the measurable security, privacy, availability, latency, usability, compliance, and observability targets? |

## Minimum NFRs

Define measurable targets for:
- Login and refresh latency.
- Availability of auth service and token verification.
- Session/token TTL and revocation propagation.
- Password reset and MFA recovery abuse limits.
- Audit retention and search latency.
- Privacy retention/deletion for accounts and audit records.
- Administrative access review cadence.

## Threat Model Checklist

- Credential stuffing and brute force.
- User enumeration through errors, timing, resend, reset, and register flows.
- Token theft, replay, fixation, downgrade, and confused-deputy issues.
- CSRF for browser cookie flows.
- XSS impact on token storage.
- Refresh token reuse and rotation failures.
- MFA bypass, recovery abuse, SIM swap, device loss, and factor downgrade.
- Privilege escalation through role/status APIs.
- Tenant boundary bypass.
- Audit log tampering or missing security events.

## Output Template

```markdown
## IAM Architecture
- Scope:
- Identity types:
- Authentication model:
- Session/token model:
- Authorization model:
- Account lifecycle:
- MFA/recovery model:
- Endpoint groups:
- Data ownership:
- Threat model:
- NFR conformance:
- Audit model:
- Verification plan:
```
