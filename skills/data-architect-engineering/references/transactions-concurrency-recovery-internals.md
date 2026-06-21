# Transactions, Concurrency, And Recovery Internals

Use this when correctness, isolation, durability, migration safety, CDC, replication, or incident recovery depends on transaction internals.

## Transaction Model
A transaction is the unit of atomic change. The DBMS sees reads and writes over database objects; effects outside the DBMS, such as emails or external API calls, cannot be rolled back by the DBMS.

ACID checks:
- Atomicity: all actions happen or none happen.
- Consistency: constraints and invariants hold before and after each transaction.
- Isolation: concurrent execution appears equivalent to an acceptable serial order or documented weaker level.
- Durability: committed changes survive crash and restart.

Red flags:
- External side effects happen before transaction commit without outbox/idempotency.
- Integrity is enforced only in application code for critical invariants.
- Isolation level is assumed, not verified.
- A migration relies on partial transactions being acceptable.

## Locks, Latches, And Granularity
Separate:
- Locks: logical transaction-level protection of database objects; may be held until commit; must support rollback semantics.
- Latches: short internal critical-section protection for pages, indexes, hash tables, and memory structures.

Lock granularities:
- Database, table, page, tuple, attribute.
- Intent locks communicate lower-level locks to higher levels.
- Lock escalation can reduce lock-manager overhead but reduce concurrency.

Review:
- Which path takes S locks, X locks, intention locks, row locks, gap/predicate locks, or table locks?
- Are `FOR UPDATE`, `FOR SHARE`, `SKIP LOCKED`, or equivalent constructs needed?
- Are lock waits and deadlocks observable?
- Can online DDL acquire blocking locks?

## Two-Phase Locking
Two-phase locking:
- Growing phase: acquire locks.
- Shrinking phase: release locks; no new locks.
- Guarantees conflict serializability but may deadlock and can limit concurrency.

Strong strict 2PL:
- Holds locks until commit.
- Avoids cascading aborts.
- More conservative and may reduce concurrency.

Deadlock strategies:
- Detection: wait-for graph plus victim selection.
- Prevention: priority schemes such as wait-die or wound-wait.
- Victim selection must consider age, progress, locks held, rollback cost, and starvation.

## Timestamp, OCC, And Phantoms
Optimistic protocols assume conflicts are rare and validate later.

Check:
- Read set and write set tracking.
- Validation point and retry behavior.
- Starvation under high conflict.
- Phantom protection for predicate/range reads.
- Whether uniqueness and secondary-index checks are protected under concurrency.

Isolation review:
- Dirty read, non-repeatable read, phantom read, lost update, write skew.
- Snapshot isolation is not the same as serializability.
- Serializable snapshot isolation needs runtime anomaly detection and retry strategy.

## MVCC Design
MVCC affects storage, index, GC, vacuum, replication, and backups.

Core idea:
- Store multiple physical versions of a logical object.
- Readers choose visible versions by snapshot/timestamps.
- Writers usually do not block readers, and readers usually do not block writers.
- Writers may still conflict with writers.

Version storage choices:
- Append-only: store all versions in same table space; newest-to-oldest chains optimize current reads but can require index pointer updates.
- Time-travel table: move old full versions to separate storage.
- Delta storage: store changes; faster writes, potentially slower historical reads.

MVCC checks:
- Version chain direction and traversal cost.
- Overflow-page sharing for large values and reclaim safety.
- Tuple-level vs transaction-level garbage collection.
- Background vacuum vs cooperative cleanup.
- Dirty-page bitmap or equivalent optimization for GC scans.
- Deleted flag vs tombstone tuple.
- Block compaction policy and locality.
- Primary and secondary index management: logical vs physical pointers.
- Duplicate key support across snapshots.
- Transaction ID wraparound or timestamp exhaustion behavior.

Red flags:
- Long-running transactions prevent vacuum/GC.
- Secondary index update cost ignored for high-write tables.
- Snapshot isolation used for invariants vulnerable to write skew.
- Vacuum/compaction headroom absent during migration or backfill.

## Logging And WAL
Recovery design is shaped by buffer pool policy:
- STEAL: dirty uncommitted pages may reach disk.
- NO-STEAL: uncommitted changes stay out of disk pages.
- FORCE: commit forces updated pages to disk.
- NO-FORCE: commit does not force all updated data pages.

Most high-performance systems use STEAL + NO-FORCE with write-ahead logging. That gives fast runtime behavior but requires undo/redo recovery.

WAL checks:
- Log record contains enough information for undo/redo or equivalent recovery.
- Commit acknowledgment occurs only after required log records are durable.
- Dirty page flush obeys pageLSN <= flushedLSN or equivalent.
- Group commit latency/throughput tradeoff is explicit.
- WAL archiving/retention supports PITR, CDC, replicas, and rollback windows.
- Checkpoint frequency balances runtime write pressure against crash recovery time.
- Logical, physical, or physiological logging is understood.

CDC note:
- WAL/binlog/logical replication streams are recovery-adjacent but not automatically business-event streams. Ordering, schema, idempotency, deletes, backfills, and retention still need design.

## ARIES-Style Recovery Evidence
Ask for recovery evidence, not claims.

Concepts to recognize:
- Log sequence number (LSN).
- pageLSN on each data page.
- flushedLSN for durable WAL boundary.
- recLSN in dirty page table.
- active transaction table.
- compensation log records for undo actions.
- fuzzy checkpoint with begin/end records.

Recovery phases:
- Analysis: reconstruct dirty pages and active transactions.
- Redo: repeat history from safe log point.
- Undo: reverse transactions active at crash.

Validation:
- Crash during transaction body.
- Crash after commit log flush before data page flush.
- Crash during checkpoint.
- Crash during rollback.
- Crash during migration/backfill.
- Restore plus consistency queries, checksums, and application smoke tests.
