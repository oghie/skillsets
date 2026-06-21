# Database Necessity And Scale Assessment

## Step
1. Identify the state: static, immutable, local, temporary, shared mutable, event stream, search, analytical, or cache.
2. Decide if the app needs no DB, a file/object store, SQLite/embedded store, cache, event log, search/vector store, or client/server DBMS.
3. Estimate active users, concurrent users, write-active users, read/write ratio, largest tenant/key, and freshness needs.
4. Identify consistency, recovery, security, and offline/local-first requirements.
5. Pick the smallest storage architecture that satisfies correctness and operations.
6. Define the scale path if users or writes grow.

## Check
- Is durable shared mutable state required?
- Are writes concurrent and centralized?
- Could SQLite or local files satisfy the actual constraints?
- Are "millions of users" mostly reads, mostly cacheable, or write-heavy?
- Is the proposed store a source of truth or derived?
- Is migration path clear if the simple option stops being enough?

## Validate
- Run a small workload model: requests/user/day, writes/user/day, cache hit ratio, peak concurrency.
- Test SQLite/file/object-store option if it is plausible.
- Test contention, locking, and backup/restore.
- Define exit criteria for moving to client/server or distributed DB.

## Ship
Deliver:
- Minimal sufficient storage choice.
- Why heavier DBMS options were rejected.
- Scale trigger thresholds.
- Backup/recovery plan.
- Migration path if requirements grow.
