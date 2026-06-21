# Implementation Planning

Use this after architecture direction is selected or when turning ADR/RFC output into engineering work.

## Planning Inputs

Require:
- Selected decision and alternatives.
- Affected components, data, behavior, and deployment views.
- Development/operation view impacts when repository structure, CI checks, runbooks, upgrades, or production controls are involved.
- NFR tactics and verification targets.
- Cost/estimate assumptions and uncertainty drivers when delivery or runtime cost matters.
- Compatibility and migration constraints.
- Repository and ownership context.

## Work Breakdown

Plan in this order:
1. Contracts and boundaries.
2. Data model and migrations.
3. Internal components and dependency direction.
4. Behavior flows and failure handling.
5. NFR tactics and operational controls.
6. Tests and verification automation.
7. Architecture fitness checks and CI guardrails.
8. Deployment, rollout, monitoring, and rollback.
9. Cleanup and documentation.

## Task Template

```markdown
| Task | Architecture Link | Files/Modules | Tests | Risk | Done When |
|---|---|---|---|---|---|
```

## Compatibility Checklist

- API versions and backward compatibility.
- Event schema evolution.
- Database migration forward/backward safety.
- Dual-read/dual-write requirements.
- Feature flags or staged rollout.
- Consumer/client upgrade path.
- Rollback constraints.

## Verification Plan

Include:
- Unit tests for local behavior.
- Integration tests for components and data.
- Contract tests for APIs/events.
- Migration tests and rollback dry run.
- Load/performance checks for NFRs.
- Security/privacy tests where applicable.
- Architecture constraint checks for enforced package/layer/service boundaries.
- Cost/performance model update checks when estimates drove the decision.
- Observability checks.
- Production smoke/canary criteria.

## Handoff Output

```markdown
## Implementation Plan
- Architecture decision:
- Affected views:
- Work sequence:
- Tests:
- Rollout:
- Observability:
- Rollback:
- Open risks:
```
