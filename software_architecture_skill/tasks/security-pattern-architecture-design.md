# Security Pattern Architecture Design

Use this task when security needs architecture beyond endpoint lists: access-control models, policy engines, enforcement points, security logging, secure middleware, network security, or misuse-case driven design.

## Procedure

1. Define protected assets and actions.
2. Identify subjects, identities, sessions, service accounts, devices, and administrators.
3. Draw trust boundaries and enforcement points.
4. Select policy model: RBAC, ABAC/PBAC, ACL, capability, multilevel, session-based, or hybrid.
5. Model Reference Monitor / PEP / PDP / PIP / PAP if policies are evaluated centrally or repeatedly.
6. Define audit events and tamper-resistance requirements.
7. Add misuse cases for bypass, replay, tenant escape, privilege escalation, policy tampering, and audit deletion.
8. Map each security pattern to functional, information, behavior, deployment, development, and operation views.
9. Define tests: negative authorization tests, policy unit tests, abuse tests, audit evidence tests, and key/secret rotation checks.

## Output

```markdown
## Security Architecture
- Protected resources:
- Subjects:
- Trust boundaries:
- Enforcement points:
- Policy model:
- Selected patterns:
- Audit events:
- Abuse cases:
- View impacts:
- Verification:
```

## Required Reads

- `references/security-architecture-patterns.md`
- `references/iam-auth-architecture.md` when auth endpoints, sessions, MFA, passwordless, or account lifecycle are in scope.
- `references/nfr-tactics-and-conformance.md` for NFR traceability.
