# Modify, Enhance, Or Remove Data System

## Step
1. Identify affected tables, collections, indices, topics, jobs, caches, search/vector indexes, dashboards, and consumers.
2. Classify change: additive, compatible, destructive, data backfill, index-only, config, topology, or decommission.
3. Map read/write compatibility across old and new versions.
4. Define data migration/backfill and validation.
5. Define rollback or roll-forward.
6. Define observability during and after rollout.
7. Define decommission criteria if removing data or stores.

## Check
- Are consumers inventoried?
- Can old app code read new data and new app code read old data during deployment?
- Are derived stores rebuilt or updated?
- Are backups and retention affected?
- Are permissions and audit rules updated?
- Is the change reversible?

## Validate
- Run migration in staging or sampled production clone.
- Run data diff/count/checksum.
- Run top queries before and after.
- Measure lock duration and replication lag.
- Confirm no stale cache/search/vector copies remain.

## Ship
Deliver:
- Migration/release plan.
- SQL/DDL or data pipeline changes.
- Validation evidence.
- Rollback/roll-forward plan.
- Monitoring and cleanup tasks.
