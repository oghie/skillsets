# Database Necessity, SQLite, And Scale

## First Question: Does This Need A DBMS?
Do not default to a database. Classify the state:
- Static configuration: file, environment, build artifact, object storage, or CDN may be enough.
- Immutable content: object storage plus metadata may be enough.
- Local application state: SQLite, embedded KV, or an application file may be enough.
- Temporary computation: in-memory structures or temporary SQLite can be enough.
- Shared mutable business state: use a transactional DBMS or equivalent system of record.
- Search-only experience: search index can serve reads, but source of truth must be defined.
- Event-first workflow: event log plus projections may be correct, but replay, retention, and schema evolution are required.

## SQLite Fit
SQLite is a strong default for:
- Embedded/mobile/edge/local-first apps.
- Application file formats.
- Desktop tools and single-user workflows.
- Local cache of enterprise data.
- Internal/temp analysis.
- Small to medium websites or application-specific servers when writes are serialized by the app layer.
- Per-user/per-tenant shard files where each file has low write concurrency.

Avoid SQLite when:
- Many clients write directly over the network to the same DB file.
- The service needs multiple writer nodes over one shared DB.
- Write-heavy traffic exceeds single-writer constraints.
- Centralized access control, pooling, and operations are required.
- Dataset, backup, or operational model needs a client/server DBMS.

## Millions Of Users Is Not A Database Requirement By Itself
Millions of users can still mean low database load if:
- Most users are anonymous/read-only.
- State is static/CDN-cached.
- Writes are rare or partitioned per user/tenant.
- Requests are served by cache/search/read models.

Millions of users require stronger DB design when:
- Many users mutate shared state.
- The workload has high write fan-in to the same rows/partitions.
- Authorization is data-dependent and per-request.
- Real-time freshness is required.
- Multi-region low-latency writes are required.
- The failure impact is high.

## Scale Assessment
Ask:
- How many active users, concurrent users, and write-active users?
- What is read/write ratio?
- What is the largest tenant/key/partition?
- Which queries are synchronous user-path queries?
- Can reads be cached or precomputed?
- Can writes be partitioned by tenant/user/time?
- Is per-user SQLite/local-first sync acceptable?
- Does offline support matter?
- What are RPO/RTO and conflict semantics?

## Patterns
- Static app data: versioned JSON/Parquet/SQLite file in object storage or CDN.
- Local-first app: SQLite on device plus sync protocol.
- Multi-tenant SaaS small/medium: Postgres/MySQL with strict tenant indexes and constraints.
- Large tenant-skewed SaaS: functional partitioning, tenant-aware sharding, or dedicated tenant clusters.
- Public read-heavy app: relational source of truth plus CDN/search/cache read models.
- Offline analytics: files/lakehouse/warehouse, not OLTP DB.

## Red Flags
- "Millions of users" used as a reason for microservices or distributed SQL without workload math.
- SQLite rejected because it is "not production" without concurrency evidence.
- SQLite chosen for many direct network writers.
- No DB chosen, but the application still needs durable writes and recovery.
- Cache-only design without source of truth.
