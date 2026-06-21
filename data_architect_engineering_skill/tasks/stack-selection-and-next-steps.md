# Stack Selection And Next Steps

## Step
1. List candidate datastore classes before products.
2. Score each class against workload, model fit, consistency, latency, scale, security, operations, migration, and cost.
3. Shortlist concrete products already used by the organization first.
4. Verify current product capabilities from official docs when product behavior matters.
5. Define proof-of-concept workload and success criteria.
6. Define next engineering steps after selection.

## Selection Prompts
- Need SQL joins and constraints? Start relational.
- Need relational scale and strong consistency beyond one node? Evaluate distributed SQL/NewSQL.
- Need existing MySQL estate scaling? Evaluate Vitess-style sharding/routing.
- Need MySQL-compatible distributed SQL plus HTAP? Evaluate TiDB-style systems.
- Need partition-key massive writes and global low-latency availability? Evaluate wide-column/key-value systems.
- Need full-text relevance and faceting? Evaluate search engines.
- Need semantic similarity? Evaluate vector store plus hybrid search.
- Need relationship traversal? Evaluate graph.
- Need high-ingest metrics/time windows? Evaluate time-series.
- Need billion-row analytics? Evaluate columnar warehouse/OLAP/lakehouse.
- Need low-latency ephemeral lookups? Evaluate cache/in-memory KV.

## Check
- Did the choice follow access patterns, not trend?
- Are product limitations verified?
- Does the team have operational competence?
- Can data be exported/migrated out?
- Are backup, restore, monitoring, and upgrades understood?

## Validate
- Benchmark with realistic data and skew.
- Test top queries and write paths.
- Test failure and restore.
- Test migration/import/export.
- Validate security controls and tenant boundaries.

## Ship
Output:
- Recommended stack with confidence level.
- Alternatives rejected and why.
- Proof gaps.
- POC plan.
- Production readiness checklist.
