# Query Execution And Optimizer Internals

Use this when architecture, schema, indexing, migration, or performance work requires understanding how a DBMS turns a declarative request into physical work.

## From SQL To Work
A relational DBMS typically moves through:
1. Parse SQL into syntax structure.
2. Bind names to catalog objects and types.
3. Rewrite logical expressions where safe.
4. Enumerate physical plans.
5. Estimate plan cost from statistics.
6. Execute operators against storage, memory, CPU, network, and temp space.

Do not treat query text as the workload. The workload is the physical plan plus data distribution plus runtime resources.

## Logical And Physical Plans
- Logical plan: relational intent, independent of access method.
- Physical plan: operator implementation, access path, join algorithm, sort/hash strategy, materialization point, and data format.
- Equivalent logical expressions can have radically different cost.
- Predicate pushdown and projection pushdown reduce intermediate data, but must preserve semantics.
- Nested subqueries may need flattening/de-correlation or decomposition into temporary results.

Review:
- Are filters and projections applied before high-cardinality joins?
- Are Cartesian products replaced with joins?
- Are CTEs/views optimization fences in the target engine?
- Are functions/casts preventing sargability?

## Processing Models
Execution model choices:
- Iterator / Volcano / pull model: each operator exposes `Next`; composable and common in row stores; function-call and branch overhead can matter.
- Materialization model: each operator emits all output at once; reasonable for small OLTP intermediates; dangerous for large OLAP intermediates.
- Vectorized/batch model: operators emit batches; good for scans, SIMD, columnar execution, CPU cache, and fewer virtual calls.
- Push model: child operators push data upward; can improve cache/register control but complicates flow control.

Check:
- Which operators are pipeline breakers: build-side hash join, sort, aggregation, subquery, order by, distinct.
- Where can data stream tuple-by-tuple, batch-by-batch, or must spill to temp storage?
- Does the plan fit memory, or will hash/sort/aggregate operators spill?

## Access Methods
Common access methods:
- Sequential scan: reads all pages; can be optimal when selectivity is low, table is small, or storage is columnar/compressed.
- Index scan: uses one index to identify record IDs or covering values.
- Multi-index scan: combines record-id sets from multiple indexes through bitmap/hash/filter operations.

Sequential scan optimizations:
- Compression-aware scan.
- Prefetch.
- Buffer pool bypass.
- Parallel scan.
- Late materialization in column stores.
- Heap clustering.
- Materialized view/result cache.
- Code specialization/JIT.
- Approximate query when lossy answers are acceptable.
- Zone maps/min-max metadata for lossless data skipping.

Index scan checks:
- Selectivity, uniqueness, predicate composition, domain, value skew, and covering columns.
- Clustered vs unclustered page fetch cost.
- Page-id sorting before heap fetch for unclustered indexes.
- Multi-index bitmap intersection/union cost.

## Joins
Join algorithm selection depends on input size, memory, sortedness, indexes, skew, and output ordering.

Options:
- Nested loop join: simple but expensive unless outer side is small or inner side has cheap index probes.
- Block nested loop: uses buffer pages to reduce rescans.
- Index nested loop: good when inner index probe cost is low and outer cardinality is bounded.
- Sort-merge join: useful when inputs are already sorted or output needs sort order.
- Hash join: often strong for equijoins, but build side memory, skew, and spill behavior matter.
- Grace/partitioned hash join: partition first when build side does not fit memory.
- Hybrid hash join: can keep hot partitions in memory but is harder to implement correctly.

Red flags:
- Join key skew not profiled.
- Build side chosen by tuple count only, ignoring row width and memory.
- Hash join spills ignored.
- Sort-merge chosen without existing order or output sort need.
- Cross-shard or distributed joins treated like local joins.

## Sorts And Aggregations
- External merge sort depends on run generation, merge fan-in, buffer frames, and prefetch/double-buffering.
- Top-N heap can avoid full sort when only a small limit is needed.
- Hash aggregation is efficient when groups fit memory; spills and skew can dominate.
- Sort aggregation may be better when data is already ordered or final ordering is required.
- Aggregation with filters/window functions can produce very different physical plans.

## Optimizer Inputs
Cost-based optimization depends on statistics that are often wrong.

Track:
- Row count.
- Distinct values per column.
- Histograms: equi-width, equi-depth, end-biased/heavy hitters.
- Samples and refresh thresholds.
- Sketches such as count-min or HyperLogLog where approximate statistics are used.
- Null fraction, correlation, most common values, min/max, partition metadata.
- Index statistics and table bloat.

Common broken assumptions:
- Uniform data.
- Independent predicates.
- Join-key containment.
- Stable distribution over time.

If estimated rows differ materially from actual rows, optimizer recommendations are weak until stats or query shape are fixed.

## Parallel And Distributed Execution
Parallel execution is not the same as distributed execution.

Single-node parallelism:
- Inter-query: run independent queries concurrently.
- Intra-query: split one plan into parallel fragments.
- Exchange operators redistribute, gather, or repartition tuples.
- I/O parallelism scans multiple devices/partitions/pages.

Distributed execution:
- Network cost and failure are part of the plan.
- Push filters/projections to data when possible.
- Pull data only when compute location or storage architecture requires it.
- Broadcast small side only when bounded and measured.
- Shuffle joins require disk/network headroom and can fail if temporary space is insufficient.

## Query Review Output
When reviewing a query or schema, produce:
- Logical intent.
- Physical plan summary.
- Access method per table.
- Join and aggregation strategy.
- Cardinality estimate vs actual if available.
- Spill, temp, lock, and I/O risks.
- Index/statistics/schema changes proposed.
- Verification query or benchmark.
