# IAM And Auth Architecture Reference

Use this reference for identity, authentication, authorization, sessions, MFA, passwordless login, account lifecycle, admin user management, audit logging, and crypto/key-management decisions.

## Contents

- Core model
- Endpoint catalog
- Session and token design
- MFA and recovery
- Passwordless and password flows
- Authorization and admin controls
- Audit logging
- Data model
- Cryptography and key management
- Verification checklist
- Common mistakes

## Core Model

Separate these concepts:

| Concept | Owns |
|---|---|
| Principal | The authenticated actor: user, admin, service account, device, anonymous user |
| Identity | Login identifier or IdP subject: email, phone, username, OIDC subject, passkey credential |
| Credential | Secret or authenticator: password hash, passkey, TOTP secret, recovery code hash, external IdP trust |
| Session | Authenticated continuity: device/browser session, refresh token family, server session |
| Access token | Short-lived authorization proof for APIs |
| Refresh token | Longer-lived secret used to mint new access tokens |
| Role/policy | Authorization rules for actions and resources |
| Audit event | Immutable security-relevant record |

Do not let one table or token type silently own all concerns. Account lifecycle, credential lifecycle, session lifecycle, and authorization lifecycle change for different reasons.

## Decision Drivers And Trade-offs

Record IAM decisions with rationale, alternatives, and consequences. Minimum decisions:

| Decision | Alternatives | Main Trade-off |
|---|---|---|
| Auth provider model | First-party, OIDC/SAML IdP, hybrid | Control and customization vs operational burden |
| Session model | Opaque session, JWT, hybrid | Central revocation vs stateless verification |
| Client token storage | HttpOnly/SameSite cookie, platform secret storage, bearer token | CSRF exposure vs XSS/exfiltration exposure |
| MFA policy | Optional, required, risk-based step-up | Usability vs account takeover resistance |
| Authorization model | RBAC, ABAC, relationship-based, policy engine | Simplicity vs expressiveness and governance |
| Audit storage | App database, append-only store, SIEM/event pipeline | Query convenience vs tamper resistance and retention |

Every selected alternative should name the attack or operational failure it is meant to reduce.

## Endpoint Catalog

Use the user's endpoint list as a candidate surface, then tailor by product risk and client type.

### Core Auth

| Endpoint | Purpose | Architecture Checks |
|---|---|---|
| `POST /auth/anonymous` | Create anonymous or guest principal | Upgrade path, data ownership, abuse limits, merge rules |
| `POST /auth/register` | Create account | Enumeration resistance, email verification state, password policy |
| `POST /auth/login` | Create session | Rate limits, MFA step-up, device metadata, audit event |
| `POST /auth/refresh` | Rotate/refresh session | Refresh token rotation, reuse detection, revocation |
| `POST /auth/logout` | Revoke current session | Cookie/token clearing, server-side revocation |
| `GET /auth/me` | Return current principal | Scope minimization, cache rules, tenant context |

### MFA

| Endpoint | Purpose | Architecture Checks |
|---|---|---|
| `POST /auth/mfa/setup` | Begin factor enrollment | Re-auth required, factor type, secret handling |
| `POST /auth/mfa/verify-setup` | Confirm enrollment | Challenge expiry, one-time use, audit |
| `GET /auth/mfa` | Get MFA status | Do not expose secrets, list verified factors only |
| `POST /auth/mfa/verify` | Complete login challenge | Attempt limits, replay protection, step-up context |
| `POST /auth/mfa/disable` | Disable MFA | Re-auth/step-up required, audit, recovery path |
| `POST /auth/mfa/recovery-codes/regenerate` | Rotate recovery codes | Invalidate old hashes, show plaintext once |
| `POST /auth/mfa/recovery/verify` | Use recovery code | One-time use, high-risk audit, follow-up step-up |
| `GET /auth/mfa/methods` | List factors | Redact identifiers, include risk metadata |
| `POST /auth/mfa/challenge` | Create MFA challenge | Bind to session/login attempt, expiry |
| `POST /auth/mfa/resend` | Resend challenge | Rate limit, anti-spam, provider failure handling |
| `DELETE /auth/mfa/methods/:id` | Remove factor | Re-auth/step-up, cannot remove last factor without policy |

### Passwordless And Password Recovery

| Endpoint | Purpose | Architecture Checks |
|---|---|---|
| `POST /auth/passwordless/request` | Request magic link/OTP | Enumeration resistance, channel risk, TTL, rate limit |
| `POST /auth/passwordless/verify` | Verify link/OTP | One-time use, session binding, replay protection |
| `POST /auth/passwordless/resend` | Resend link/OTP | Throttle, provider failure, generic response |
| `POST /auth/forgot-password` | Start reset | Generic response, token TTL, audit |
| `POST /auth/reset-password` | Complete reset | Reset token one-time use, revoke sessions, password hash upgrade |
| `PATCH /auth/change-password` | Authenticated password change | Current password or step-up, revoke other sessions |
| `POST /auth/verify-email` | Confirm email | Token binding, expiry, duplicate email rules |
| `POST /auth/resend-verification` | Resend verification | Throttle and generic response |

### Account And Sessions

| Endpoint | Purpose | Architecture Checks |
|---|---|---|
| `POST /auth/deactivate` | Deactivate own account | Re-auth, retention/deletion, session revocation |
| `GET /auth/sessions` | List sessions/devices | Device metadata, last used, IP/geolocation privacy |
| `DELETE /auth/sessions/:id` | Revoke one session | Cannot revoke wrong tenant/user |
| `DELETE /auth/sessions` | Revoke selected/all sessions | Clarify current-session behavior |
| `POST /auth/logout-all` | Revoke all sessions | Refresh token family revocation, audit |

### Admin And Audit

| Endpoint | Purpose | Architecture Checks |
|---|---|---|
| `GET /admin/users` | Search/list users | Admin authz, pagination, privacy, tenant scope |
| `PATCH /admin/users/:id/role` | Change role | Separation of duties, privilege escalation prevention, audit |
| `PATCH /admin/users/:id/status` | Lock/suspend/activate | State transition rules, session revocation |
| `GET /audit/logs` | Read audit events | Tamper resistance, filtering, retention, export controls |

## Session And Token Design

Choose deliberately:

| Model | Use When | Risks |
|---|---|---|
| Opaque server session | Central revocation and introspection are important | Session store availability and scaling |
| JWT access token | Low-latency stateless verification matters | Revocation lag, key rotation, claim bloat |
| Refresh token rotation | Long-lived sessions are required | Reuse detection and token-family state |
| Cookie session | Browser app needs CSRF-aware same-site session handling | CSRF, cross-site embedding, cookie scope |
| Bearer token | Native/mobile/API clients need explicit Authorization header | Token exfiltration and replay |

Token/session matrix:

```markdown
| Token/Session | Storage | TTL | Rotation | Revocation | Audience | Claims | Verification |
|---|---|---|---|---|---|---|---|
```

Required rules:
- Access tokens are short-lived.
- Refresh tokens rotate or are bound to a server-side session.
- Logout and account lock revoke refresh tokens or server sessions.
- Token issuer, audience, expiry, not-before, algorithm, and key ID are verified.
- Browser cookie flows include CSRF strategy.
- JWT signing keys have rotation, rollback, and compromise procedures.

## MFA And Recovery

Model MFA as authenticator lifecycle, not just an endpoint:
- Enrollment: setup challenge, verification, verified state.
- Challenge: login step-up, high-risk action step-up, admin action step-up.
- Recovery: recovery codes, backup factor, support workflow, lockout policy.
- Removal: re-auth required, cannot silently remove last required factor.

Factor considerations:
- TOTP: protect secret, show QR once, rate-limit verification.
- WebAuthn/passkeys: prefer phishing-resistant factor when product can support it.
- SMS/email OTP: treat as weaker factors; add risk controls and rate limits.
- Recovery codes: store only hashes, show plaintext once, single use, regenerate invalidates old codes.

## Passwordless And Password Flows

Passwordless:
- Link/OTP tokens are one-time use and short-lived.
- Verification binds to request intent and client context where practical.
- Responses do not reveal whether the account exists.
- Resend is rate-limited and audited.

Password storage:
- Store password hashes only.
- Prefer memory-hard password hashing such as Argon2id where available; otherwise use a well-reviewed modern KDF with parameters recorded.
- Use per-password salt; consider a server-side pepper in KMS/HSM when operationally justified.
- Support hash parameter upgrades on login/password change.

Password reset:
- Reset token is one-time use, short-lived, and stored hashed.
- Successful reset revokes other sessions unless product policy says otherwise.
- Reset flow creates audit events and may trigger user notification.

## Authorization And Admin Controls

Authorization must be checked at the resource/action boundary, not just in the UI.

Choose a model:
- RBAC for simple role-to-permission systems.
- ABAC for context, tenant, status, risk, or ownership-sensitive systems.
- Relationship-based access for sharing/collaboration graphs.
- Policy engine when rules need central governance and testing.

Admin API rules:
- Admin role changes require stronger authorization than ordinary admin reads.
- Prevent self-escalation and uncontrolled demotion of the last owner/super-admin.
- Role/status changes create high-severity audit events.
- Suspended/locked users have session and token consequences.
- Tenant-scoped admins cannot cross tenant boundaries.

## Audit Logging

Audit security-relevant events:
- register, login success/failure, logout, refresh, refresh reuse detection.
- password reset/change, email verification, MFA enroll/disable/challenge/recovery.
- session revocation, logout-all, account deactivate/delete.
- admin role/status changes and audit log access.
- provider errors and suspicious abuse signals when useful.

Audit event shape:

```markdown
| Field | Meaning |
|---|---|
| event_id | Immutable event identifier |
| event_type | Security event type |
| actor_id | Principal performing action, if known |
| subject_id | User/resource affected |
| session_id | Session or token family, if applicable |
| ip/device | Client metadata with privacy policy |
| result | success, failure, denied, challenged |
| reason | Normalized reason code |
| correlation_id | Traceability across services |
| timestamp | Trusted server timestamp |
```

Protect audit logs from ordinary application writes, unauthorized reads, and silent deletion. Define retention and export rules.

## Data Model

Common entities:
- users
- identities
- credentials
- email_verifications
- password_reset_tokens
- mfa_methods
- mfa_challenges
- recovery_codes
- sessions
- refresh_token_families
- roles
- permissions
- user_roles
- policies
- audit_events

Data rules:
- Store token secrets, reset tokens, verification tokens, and recovery codes hashed.
- Keep unique constraints and normalization rules for identifiers.
- Separate PII from auth metadata where privacy and deletion requirements demand it.
- Treat anonymous users as real principals with upgrade/merge rules.

## Cryptography And Key Management

Use well-reviewed libraries and protocols. Do not invent cryptographic protocols for auth.

Architecture checks inspired by hardened cryptographic libraries:
- Public entry points validate input length and format explicitly.
- Secret key material and temporary secret state are zeroized where the runtime allows.
- Verification and decapsulation paths avoid obvious secret-dependent branching when constant-time behavior matters.
- Malformed ciphertexts, signatures, tokens, and truncated inputs are rejected and tested.
- Key storage, process isolation, transport security, and side-channel review remain application responsibilities.
- Pre-standard algorithms and serialized key formats require compatibility and migration planning.

When post-quantum cryptography is relevant:
- Use KEMs for shared-secret establishment, not as password hashing or session storage.
- Use signature schemes for signing artifacts, tokens, device attestations, or audit bundles only when algorithm fit, key sizes, latency, and operational maturity are acceptable.
- Treat demo encryption layers as proof-only unless they use production AEAD, framing, nonce, associated-data, and key-derivation designs.
- Benchmark keygen, encapsulation/decapsulation, signing, and verification under expected platform constraints.
- Document algorithm status, parameter set, key lifecycle, rotation, and migration plan.

## Verification Checklist

- Registration/login/reset responses resist account enumeration.
- Rate limits exist for login, register, reset, passwordless, MFA, resend, and admin search.
- Refresh token rotation detects reuse and revokes token family.
- Logout, logout-all, password reset, status change, and admin lock revoke expected sessions.
- JWT verification checks issuer, audience, expiry, algorithm, and key ID.
- Password hashes use approved parameters and upgrade path.
- MFA setup, challenge, disable, recovery, and deletion require proper step-up.
- Role/status APIs prevent self-escalation and tenant escape.
- Audit logs contain required events and cannot be modified by ordinary app paths.
- Token/session storage matches client threat model.
- Crypto boundary rejects malformed/tampered inputs.

## Common Mistakes

- Treating authentication as the same thing as authorization.
- Using JWTs without revocation, key rotation, or claim governance.
- Storing reset tokens or recovery codes in plaintext.
- Letting MFA recovery become the weakest bypass.
- Returning different errors that reveal whether an account exists.
- Allowing role changes without separation of duties and audit.
- Designing `/auth/me` as a broad user profile endpoint.
- Forgetting session revocation on password reset, account lock, and MFA compromise.
- Assuming cryptographic library correctness removes key storage, deployment, and side-channel responsibilities.
