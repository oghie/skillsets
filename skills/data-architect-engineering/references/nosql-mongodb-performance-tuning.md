# MongoDB And Document-Store Performance Tuning

Engine-specific companion to `performance-indexing-and-query-optimization.md` and
`database-problem-prevention-and-diagnosis.md`. Use it for MongoDB, WiredTiger, and
document-store (NoSQL aggregate-model) tuning. The general triage order in those files
still applies; this file adds the document-model specifics those generic playbooks omit.

## Method: Tune Top-Down, Not Symptom-First
Tune in layer order. The load on each layer is set by the layer above, so fixing a lower
layer to relieve an upper-layer cause wastes money and downtime (the classic failure:
sharding or buying IOPS to mask one missing index).
1. Reduce application demand to its logical minimum: document model, indexes, query and
   aggregation shape, fewer round trips. This is where 100x–1000x wins live.
2. Reduce physical I/O: size the WiredTiger cache so the working set stays in memory.
3. Optimize disk I/O: provision IOPS/bandwidth for the now-realistic physical demand.
4. Tune the cluster: read preference, write concern, shard key.
Never start at step 3 or 4. Confirm a cause with evidence before mitigating.

## Diagnostic Tools (mongosh)
- `explain("executionStats")` is the core tool. Read `inputStage` from the inside out.
  Key numbers: `nReturned` vs `totalKeysExamined` + `totalDocsExamined` — aim near 1:1; a
  large examined:returned ratio is a wasteful access path. A `SORT` stage means the sort
  is not served by an index (in-memory blocking sort). `executionStats` actually runs the
  query (load); plain `explain()`/`queryPlanner` does not.
- Stages to recognize: `COLLSCAN` (full scan), `IXSCAN`, `FETCH`, `SORT`, `PROJECTION_COVERED`
  (covered query, no FETCH), `AND_SORTED`/`OR`/`SUBPLAN` (index intersection/merge),
  `IDHACK` (`_id` lookup), `SHARD_MERGE`/`SINGLE_SHARD`/`SHARD_MERGE_SORT` (sharded).
- Database profiler (`db.setProfilingLevel(1, {slowms, sampleRate})`) finds *which*
  statements need tuning; aggregate `system.profile` by `queryHash` (and `cursorid` to
  merge `getMore` batches). Profiling has overhead and is not available on a `mongos` —
  turn it on for a representative capture, then off.
- Slow-query log (above `slowms`): `planSummary`, `keysExamined`, `docsExamined`,
  `hasSortStage`, `usedDisk`. `serverStatus()` for rates (sample twice, diff): opcounters,
  `wiredTiger.cache`, `opLatencies`, `metrics`. `currentOp()`/`killOp()` for runaway ops
  (confirm data safety before killing). `mongostat`/`mongotop`/Atlas or Compass dashboards.
- explain output shape shifts with the slot-based execution engine on modern versions;
  read the stages, not a memorized layout. `This needs verification` for the exact shape on
  the target version.

## Document Model And Schema — The Performance Ceiling
The model sets how much work every request does and how many documents fit in cache. It is
hard to change after deployment. Model around the read/write access patterns, not around
normalized entities — third normal form is almost always wrong here.
- Embed vs link is the core trade-off. Embedding wins when you read all of an entity at once
  or delete it whole. Linking wins for aggregate/count over a sub-entity, inserts that would
  grow a parent document, and updates to duplicated data (an embedded update touches every
  copy). Mix both to favor the critical operations.
- Limits: 16MB per document; ~100 levels of nesting. Large documents cut cache density.
- Patterns: subsetting/bucket (embed the most-recent N details, link the rest);
  vertical partitioning (move large rarely-read fields — BLOBs, images — to a side
  collection so the hot document stays small and scannable); attribute pattern (turn many
  same-typed fields into an array of `{k, v}` subdocuments indexed once on the key).
- Use schema validation (`$jsonSchema`) for invariants; co-locate atomically-updated data in
  one document to avoid needing a multi-document transaction.

## Indexing — The Highest-Leverage Lever
- ESR rule for compound key order: Equality fields first, then Sort fields, then Range
  fields. Equality narrows; an index-served sort avoids a blocking `SORT`; range goes last.
- Leading-prefix rule: a compound index serves a query only if the query includes the
  leading key(s). `{a,b,c}` serves `a` and `a,b` — not `b` alone or `c` alone.
- Covered query: when the index alone satisfies filter + sort + projection there is no
  `FETCH` (`PROJECTION_COVERED`) — large memory/I/O win.
- Selectivity: prefer the most selective index for point lookups. But WiredTiger prefix
  compression shrinks an index most when the leading field is *less* selective — a smaller
  index that fits memory can beat a more selective one. Measure.
- Specialized indexes: `partialFilterExpression` (index a subset; the query must include the
  filter), sparse (skips missing-field docs; serves `$exists:true`, not `$exists:false`),
  multikey (array elements; `$size` cannot use an index), text (one per collection, suffix
  stemming, cost grows with term count — prefer a dedicated search engine / Atlas Search for
  real full-text), geospatial `2dsphere`/`2d` (`$near`/`$geoNear` require the index; bound
  with `min`/`maxDistance`). Wildcard `$**` only for genuinely unpredictable attribute sets —
  its write overhead matches indexing every field.
- Index overhead: every insert/delete maintains all indexes; an update maintains indexes on
  changed fields — often the majority of write cost. Find dead weight with `$indexStats`
  (`accesses.ops == 0`), but keep unique (constraint) and TTL (lifecycle) indexes regardless.
- A case-insensitive search needs a collation index (`{locale, strength: 1|2}`) used by both
  index and query; a regex `/^x$/i` otherwise scans the whole index.

## Query Tuning (find)
- Project only the fields you use — large win on bulk reads over a network. Co-locate the
  application near the database; cut round trips (batch in code; `batchSize` only helps for
  many small documents over a slow link — test, it can hurt). Cache small static lookup data.
- Index vs collection scan is not always "index." For random-ordered data a scan beats an
  index past roughly a single-digit percent of the collection; for clustered data the index
  wins much further. Large proportion → scan; single document from a large collection →
  index; the middle is workload-dependent. `hint({$natural:1})` forces a scan as a last
  resort (hints can block future-index/optimizer improvements).
- Sort: no index on the sort key → a blocking in-memory sort that cannot emit the first
  document until fully sorted and fails past its memory cap. An index-served sort streams
  the first page immediately (best for pagination); a blocking sort can still be faster for
  the whole set. To serve filter + sort, order the index by ESR.
- Filter antipatterns: `$ne` runs two range scans and usually reads the bulk → a scan is
  often better; a wide `$gt`/range over most of the domain → scan; `$or` reverts to a full
  scan if *any* branch is unindexed (index every branch); anchor regex to the start
  (`/^x/`); `$exists:true` scans `[MinKey,MaxKey]` (seek a value or use a sparse index);
  `$size` cannot use an index. `$in`/`$or` on indexed fields merge via `OR`/`SUBPLAN`.

## Aggregation Pipeline Tuning
- Filter early, filter often: shrink data in the earliest stages. `$lookup` ordering is not
  fixed for you — place `$match`/`$sort`/`$limit` before the join (each source document
  triggers one lookup). Index the `$lookup` `foreignField` and the `$graphLookup`
  `connectToField`, or joins degrade steeply; explain does not reveal whether the inner
  lookup used an index — confirm by timing. Join order: filter first, prefer the side with a
  supporting index, then small → large.
- Memory model: the 16MB limit applies to result documents (intermediates may exceed it
  transiently). Per-stage memory cap is 100MB; spilling to disk is governed by
  `allowDiskUse`. On modern versions `allowDiskUseByDefault` is true, so stages spill by
  default; the 100MB cap applies when disk use is off. The `$addToSet`/`$push` accumulators
  build an in-memory array that cannot spill, so they can exceed the limit even with disk use
  enabled — shrink what they accumulate. An aggregation sort uses an index only when it
  is early enough to roll into the initial data access; otherwise it is a disk sort, which is
  a scalability cliff.
- Views re-run their pipeline on the base collection and generally cannot use the base
  collection's indexes — optimize the defining pipeline or query the collection directly. For
  precomputed results use a materialized view via `$merge` (incremental) or `$out` (replace),
  refreshed on a schedule or a change stream — never more often than it is read.

## Writes: Insert, Update, Delete
- Optimize the update/delete filter exactly like a find; `explain` works on writes
  (`executionStats` matches without modifying). Never insert non-trivial volume one document
  at a time — use `insertMany`/bulk ops. Move/transform data inside the database with `$merge`
  / `$out` instead of pulling it across the network and back. Use an update pipeline to set
  fields from other fields in one statement; use `upsert`/bulk `$merge` instead of
  check-then-write. Do not set `multi:true` when a single document matches — it keeps
  scanning. Deletes maintain every index; for high-churn/streaming data prefer a TTL index or
  a logical-delete flag purged in a window.

## Transactions
MongoDB uses MVCC and a snapshot read concern with no blocking locks: conflicting writers
get a `WriteConflict` / `TransientTransactionError` and must retry (drivers retry
automatically). Retries are the dominant transaction cost (watch
`serverStatus().transactions.totalAborted`); transactions reduce concurrency. Minimize
retries by, in order: avoiding the transaction (co-locate atomically-updated data in one
document), ordering the hot/contended write last (shrink the conflict window), and
partitioning a hot document across N documents.

## Memory And WiredTiger Cache
- The working set must fit in RAM; swap is a response-time cliff. WiredTiger cache defaults to
  about half of RAM minus 1GB — a starting point, rarely optimal (`cacheSizeGB`).
- A high cache hit ratio does not prove good tuning (pathological re-reads inflate it); for an
  already-tuned workload a low hit rate suggests the working set does not fit. Evictions are
  LRU; clean pages evict instantly, dirty pages must be written first — sustained dirty load
  causes blocking evictions. Checkpoints flush dirty pages (~60s) as random writes, producing
  sawtooth throughput; the journal/WAL is sequential and cheap. Tune eviction/checkpoint
  internals only with care.
- Concurrency is gated by read/write tickets; on modern versions the cap (128/128) is managed
  dynamically and setting `wiredTigerConcurrentRead/WriteTransactions` disables that
  algorithm. Ticket exhaustion usually means the real bottleneck is elsewhere (CPU run queue
  or internal locks).

## Disk I/O
Reduce demand before tuning disks. Latency and throughput trade off — past ~50–70% of a
device's rated IOPS, queuing makes latency climb; aggregate throughput scales with the number
of devices. Use SSD (NVMe over SATA, SLC over MLC); RAID 10 (stripe + mirror), never RAID 5/6
for a write workload. The best I/O-health metric is the average disk-to-cache page-read time
(`wiredTiger.cache`): under ~1ms on SSD, problematic above a few ms. Journal sync time is the
journal-contention signal; datafile writes are async (sessions wait on the journal, not the
datafile). Disk sorts/aggregations write to `_tmp` and can be hidden — find them via
`usedDisk:true` in the slow log; relieve by raising sort memory or moving `_tmp` to a fast
device. Cloud/Atlas: provision by IOPS, not capacity; ephemeral NVMe is fastest but unsafe for
datafiles.

## Replica Sets And Read Scaling
Replica sets exist for availability, not performance, but reads can scale across secondaries.
Read preference `secondaryPreferred` or `nearest` offloads the primary and cuts latency, at
the cost of possibly stale reads; bound staleness with `maxStalenessSeconds`. Tag sets pin
reads to specific nodes (analytics node, or one collection per node for cache locality).
Write concern (`w`, `j`, `wtimeout`) is a durability control, not a performance knob:
replication is sequential after the primary write, so higher `w` lowers write throughput;
`w:0` is fast but unsafe; `w:"majority"` is the safe default on modern versions. Drive it by
fault tolerance, then measure the throughput cost.

## Sharding — Scale-Out, Last Resort
Shard only when a write workload genuinely exceeds a single primary, after exhausting workload,
server, replica-set, and scale-up tuning — sharding adds overhead and often makes individual
operations slower. Choose a shard key with high cardinality, even distribution, presence in the
common query filters (so queries target a single shard), and non-monotonic values (a
monotonically increasing key creates a hot shard — hash it). Range sharding gives efficient
shard-key range scans but risks hot chunks; hash sharding distributes evenly but scatters
range/sort queries. A query that includes the shard key resolves on a `SINGLE_SHARD`; without
it, a scatter-gather `SHARD_MERGE` — add the shard key to the filter when possible, and ensure
each shard's query is indexed. Zone sharding pins ranges to geographies or storage tiers.
Watch jumbo chunks (one shard-key value too big to split) and confine rebalancing to a
maintenance window. Refining a shard key adds suffix fields; modern versions support full
online resharding and joining into sharded collections — `This needs verification` for the
exact capabilities on the target version.

## Version-Sensitive Behavior — Verify, Do Not Assume
Behavior here has changed materially across releases and is `This needs verification` against
the deployment's exact MongoDB version: aggregation `allowDiskUse`/100MB default, the
slot-based execution engine and explain shape, default write concern, dynamic WiredTiger
tickets, online resharding and `$lookup` into sharded collections, time-series and clustered
collections, find-sort memory cap, and `compact` locking behavior. Confirm against current
documentation before quoting a number, a default, or a "since version X" claim. Use `mongosh`
(the legacy `mongo` shell is removed).

## MongoDB Performance Red Flags
- Sharding or buying IOPS proposed before the document model, indexes, and queries are tuned.
- An examined:returned ratio far from 1:1, or a `COLLSCAN`/blocking `SORT` on a hot path.
- `$ne`, unanchored regex, `$size`, `$exists`, or a wide range presented as "indexed."
- An `$or` with one unindexed branch; a `$lookup`/`$graphLookup` without an index on the
  joined field.
- A monotonically increasing shard key; a query that scatter-gathers because it omits the
  shard key; jumbo chunks.
- Write concern lowered for speed; secondary reads used without accepting staleness.
- WiredTiger cache swapped to disk; tuning checkpoint/eviction internals before sizing memory.
- A 2020-era number or default quoted as current without verifying the running version.
