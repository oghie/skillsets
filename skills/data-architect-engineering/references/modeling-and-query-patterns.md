# Modeling And Query Patterns

## Model From Invariants And Queries
Do not begin with tables, collections, or vendors. Begin with:
- Entities and invariants.
- Write commands and idempotency keys.
- Read queries and sort/filter dimensions.
- Cardinality and growth.
- Consistency and transaction boundaries.
- Retention and deletion.
- Tenant and access-control boundaries.

For formal model families and notations, read `data-model-concepts-and-notations.md` before choosing a datastore product.

## Relational Model
Use when data correctness depends on relationships and constraints.

Modeling steps:
1. Identify entities and candidate keys.
2. Normalize to remove update, insert, and delete anomalies.
3. Add primary keys, foreign keys, unique constraints, check constraints, and not-null constraints.
4. Define transaction boundaries for invariants.
5. Add indexes from observed query predicates and join paths.
6. Denormalize only when a measured access pattern requires it.

## Document Model
Use aggregate boundaries:
- Embed data that is read and written together.
- Reference data that changes independently or grows without bound.
- Keep document size bounded and update paths predictable.
- Add schema validation even when the database allows flexible schema.

Red flag: document model mirrors relational tables but loses joins and constraints without gaining aggregate-local efficiency.

## Wide-Column / Partition Model
Model around queries:
- One table per query pattern is normal.
- Partition key must be present in performant queries.
- Clustering keys define sort/range behavior inside a partition.
- Duplicate data deliberately and reconcile through write discipline.

Red flag: query requires "find all rows where non-key column equals X" at scale.

## Key-Value Model
Define:
- Key namespace and tenant prefix.
- Value size and serialization.
- TTL and eviction behavior.
- CAS/versioning where concurrent writes are possible.
- Whether data loss is acceptable.

## Graph Model
Define:
- Node labels and identity keys.
- Relationship types, direction, cardinality, and properties.
- Traversal bounds.
- Path queries and indexes for traversal start points.

Use graph when relationship traversal is the primary query, not because the ERD looks connected.

## Time-Series Model
Define:
- Measurement/table, timestamp precision, tags/dimensions, fields/measures.
- Retention and downsampling.
- Expected series cardinality.
- Late/out-of-order data policy.
- Query windows and aggregation grain.

High-cardinality tags can create operational pain. Treat user IDs, request IDs, trace IDs, and device IDs carefully.

## Vector Model
Define:
- Source document/object identity.
- Embedding model and version.
- Chunking strategy and metadata.
- Distance metric and index type.
- Recall/precision evaluation set.
- Metadata filters, tenant filters, and deletion/reindex policy.
- Hybrid lexical/vector strategy and re-ranking where needed.

Vector retrieval is not a substitute for authorization or exact lookup.

## Search Model
Define:
- Source of truth and indexing pipeline.
- Field mappings and analyzers.
- Relevance expectations.
- Facets/filters/sort fields.
- Reindex strategy and alias/cutover pattern.
- Index lag SLO and backfill path.

## Warehouse / Dimensional Model
Define:
- Facts, dimensions, grain, slowly changing dimensions, conformed dimensions, and semantic layer.
- Batch or streaming ingestion.
- Partitioning and clustering.
- Data quality contracts.
- Lineage and access governance.

## Modeling Deliverables
For design output, include:
- System-of-record map.
- Conceptual/logical/physical model depth appropriate to risk.
- Query matrix: operation, predicate, sort, expected cardinality, consistency, p95/p99 target.
- Consistency matrix: invariant, owner, transaction boundary, failure/retry behavior.
- Security matrix: subject, data class, operation, enforcement point, audit event.
- Migration impact matrix if changing existing data.
