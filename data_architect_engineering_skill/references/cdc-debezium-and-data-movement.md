# CDC, Debezium, And Data Movement

## CDC Fit
Change Data Capture is useful for:
- Low-downtime migration.
- Feeding search, cache, warehouse, lakehouse, vector, or read-model projections.
- Audit/event streams.
- Strangler modernization.
- Outbox event publication.

CDC is not automatically correct for:
- Cross-store transactions.
- Rebuilding missing history.
- Fixing bad source data.
- Exactly-once end-to-end semantics without idempotent sinks.
- Authorization enforcement in derived stores.

## Debezium Pattern
Debezium captures database changes into change-event streams. Common deployments use Kafka Connect source connectors, but Debezium Server and embedded Debezium Engine are also valid patterns.

Before using Debezium, verify:
- Source connector support and version.
- WAL/binlog/logical replication settings.
- Snapshot mode and locking impact.
- Replication slot/binlog retention and disk pressure.
- Offset storage durability.
- Schema history topic/storage.
- Schema registry/serialization format.
- Delete/tombstone semantics.
- Transaction metadata and ordering needs.
- Heartbeats and liveness.
- Monitoring, lag, and restart behavior.
- Security for captured data and topics.

## Outbox Pattern
Use an outbox table when service state and emitted event must be coupled.

Minimum columns:
- Event id for deduplication.
- Aggregate type.
- Aggregate id or routing key.
- Event type.
- Payload.
- Created timestamp.
- Optional trace/correlation/tenant headers.

Rules:
- Write domain change and outbox row in the same transaction.
- Capture only outbox rows for integration events when possible.
- Make consumers idempotent.
- Preserve ordering by aggregate key where needed.
- Define retention/cleanup after successful publication.

## Migration With CDC
Flow:
1. Baseline snapshot.
2. Start streaming changes from a stable log position.
3. Backfill target.
4. Apply change stream continuously.
5. Shadow read or compare source/target.
6. Freeze or reduce write window if needed.
7. Cut over reads/writes.
8. Keep CDC running through rollback window.
9. Decommission after validation.

## CDC Validation
- Source and target row counts by table/partition.
- Checksums for stable slices.
- Referential integrity checks.
- Event ordering per key.
- Lag and replay duration.
- Duplicate and missing event detection.
- Delete propagation.
- Schema-change handling.
- Sink idempotency.
- Consumer authorization and tenant filters.

## Red Flags
- CDC used without understanding snapshot lock behavior.
- Binlog/WAL retention too small for outage/replay.
- Derived stores receive sensitive fields they should not have.
- Schema changes are not tested through the pipeline.
- Offset storage is ephemeral.
- Consumers assume exactly-once without idempotency.
- Deletes are ignored.
- Outbox table is written outside the domain transaction.
