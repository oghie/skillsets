# Database Problem Risk Register

## Context
- System:
- Release/change:
- Workload:
- Expected growth:
- Critical tables/collections/indexes:
- Critical endpoints/jobs:

## Risk Register
| Problem | Risk | Trigger | Evidence to collect | Prevention | Mitigation | Durable fix | Rollback | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Locking | | | Lock waits, blocker graph, transaction age | | | | | |
| Blocking | | | Blocked sessions, wait graph, pool wait | | | | | |
| Deadlocks | | | Deadlock logs/graph, victim retries | | | | | |
| Slow query | | | Actual plan, p95/p99, waits, rows read/returned | | | | | |
| Connection exhaustion | | | Active/idle sessions, pool wait, max connection errors | | | | | |
| High I/O wait | | | iowait, disk p99, queue depth, buffer hits, fsync | | | | | |
| Bad queries | | | Query text, lint findings, plan smell, ORM trace | | | | | |
| Full table scan | | | Sequential scan, rows read, pruning/index usage | | | | | |
| Data-growth regression | | | Plan drift, table growth, stats error, bloat, skew | | | | | |

## Guardrails
- Statement timeout:
- Lock timeout:
- Pool max and acquisition timeout:
- Retry/idempotency rule:
- Slow query threshold:
- Migration lock policy:
- Backpressure policy:
- Kill/cancel policy:

## Validation
- Production-like data volume:
- Skew scenario:
- Cold cache test:
- Warm cache test:
- Concurrent write test:
- Migration/backfill test:
- Rollback test:

## Ship Criteria
- Abort threshold:
- Dashboard:
- On-call owner:
- Rollback owner:
- Residual risk accepted by:
