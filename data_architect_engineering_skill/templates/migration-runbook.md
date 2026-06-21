# Migration Runbook

## Scope
- Source:
- Target:
- Data owner:
- Cutover owner:
- Systems affected:
- Rollback owner:

## Pre-Checks
- Backup completed:
- Restore tested:
- Source schema frozen or compatibility plan:
- Target schema ready:
- Permissions ready:
- Monitoring ready:
- Consumer inventory complete:

## Migration Method
- Dump/load, CDC, dual write, event replay, backfill, shadow read, or strangler:
- Ordering requirements:
- Idempotency strategy:
- Conflict strategy:
- Data validation:

## Execution
1. Announce maintenance/cutover window.
2. Enable compatibility code.
3. Start backfill or initial load.
4. Start CDC/dual write if used.
5. Validate counts/checksums/invariants.
6. Shadow read or compare query results.
7. Switch traffic.
8. Monitor SLOs and errors.
9. Freeze rollback window decision.
10. Decommission old path after criteria are met.

## Rollback
- Trigger conditions:
- Steps:
- Data reconciliation needed:
- Time limit:
- Communication:

## Validation Evidence
- Row counts:
- Checksums:
- Referential integrity:
- Query parity:
- Performance:
- Security:
- Restore:

## Decommission
- Consumers moved:
- Backups retained:
- Legal/audit retention:
- Derived stores cleaned:
- Credentials revoked:
- Cost removed:
