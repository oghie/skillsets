# Query Examples: SQL, NoSQL, Vector, Graph, Search, Time-Series, Spatial, And Array

These examples are intentionally small `foo`/`bar` patterns. Adapt syntax to the actual engine.

## Relational SQL: Correctness First

```sql
CREATE TABLE foo_account (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  tenant_id BIGINT NOT NULL,
  email TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('active', 'disabled')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, email)
);

CREATE TABLE bar_order (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  tenant_id BIGINT NOT NULL,
  account_id BIGINT NOT NULL REFERENCES foo_account(id),
  amount_cents BIGINT NOT NULL CHECK (amount_cents >= 0),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX bar_order_tenant_created_idx
  ON bar_order (tenant_id, created_at DESC);
```

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT f.email, sum(b.amount_cents) AS total_cents
FROM foo_account f
JOIN bar_order b ON b.account_id = f.id
WHERE f.tenant_id = 42
  AND b.tenant_id = 42
  AND b.created_at >= now() - interval '30 days'
GROUP BY f.email
ORDER BY total_cents DESC
LIMIT 20;
```

## SQL Transaction Boundary

```sql
BEGIN;

UPDATE foo_account
SET status = 'disabled'
WHERE tenant_id = 42 AND id = 1001 AND status = 'active';

INSERT INTO bar_audit_log (tenant_id, actor_id, action, subject_id, created_at)
VALUES (42, 7, 'disable_account', 1001, now());

COMMIT;
```

If audit insertion must be coupled with the state change, keep it in the same transaction or use a transactional outbox.

## SQL Antipattern Replacement

Bad multi-value column:

```sql
CREATE TABLE foo_issue (
  id BIGINT PRIMARY KEY,
  tag_csv TEXT NOT NULL
);
```

Better intersection table:

```sql
CREATE TABLE foo_tag (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE foo_issue_tag (
  issue_id BIGINT NOT NULL REFERENCES foo_issue(id),
  tag_id BIGINT NOT NULL REFERENCES foo_tag(id),
  PRIMARY KEY (issue_id, tag_id)
);
```

## Document Query

```javascript
db.foo_profiles.find(
  {
    tenantId: 42,
    status: "active",
    "preferences.newsletter": true
  },
  {
    email: 1,
    displayName: 1,
    "preferences.newsletter": 1
  }
).limit(50)
```

Design check: index must match tenant, status, and the nested predicate if this is hot.

## Key-Value / Cache

```text
SET foo:tenant:42:session:abc123 "{...json...}" EX 1800 NX
GET foo:tenant:42:session:abc123
DEL foo:tenant:42:session:abc123
```

Design check: define TTL, maximum value size, eviction policy, and whether miss path is acceptable.

## Wide-Column / CQL

```sql
CREATE TABLE foo_orders_by_tenant_day (
  tenant_id bigint,
  order_day date,
  created_at timestamp,
  order_id uuid,
  amount_cents bigint,
  PRIMARY KEY ((tenant_id, order_day), created_at, order_id)
) WITH CLUSTERING ORDER BY (created_at DESC);

SELECT order_id, amount_cents
FROM foo_orders_by_tenant_day
WHERE tenant_id = 42
  AND order_day = '2026-06-21'
  AND created_at >= '2026-06-21T00:00:00Z';
```

Design check: the partition key is mandatory for performant reads.

## Graph / Cypher

```cypher
MATCH (a:Account {tenantId: 42, id: "foo"})
      -[:OWNS]->(:Device)
      <-[:USES]-(other:Account)
WHERE other.status = "active"
RETURN other.id, count(*) AS shared_devices
ORDER BY shared_devices DESC
LIMIT 20;
```

Design check: bound traversals and index start nodes.

## Vector / PostgreSQL With pgvector

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE foo_chunks (
  id BIGSERIAL PRIMARY KEY,
  tenant_id BIGINT NOT NULL,
  document_id BIGINT NOT NULL,
  embedding_model TEXT NOT NULL,
  content TEXT NOT NULL,
  embedding vector(3) NOT NULL
);

SELECT id, document_id, content
FROM foo_chunks
WHERE tenant_id = 42
  AND embedding_model = 'foo-embedding-v1'
ORDER BY embedding <-> '[0.2,0.4,0.7]'
LIMIT 10;
```

Design check: exact syntax and index choices are engine/version-specific. This needs verification.

## Search Query

```json
{
  "query": {
    "bool": {
      "must": [
        { "match": { "body": "foo bar outage" } }
      ],
      "filter": [
        { "term": { "tenant_id": 42 } },
        { "range": { "created_at": { "gte": "now-30d" } } }
      ]
    }
  },
  "sort": [
    { "_score": "desc" },
    { "created_at": "desc" }
  ],
  "size": 20
}
```

Design check: tenant filter is not optional; source-of-truth and reindex strategy must be known.

## Time-Series

```sql
SELECT
  time_bucket('5 minutes', ts) AS bucket,
  service,
  avg(latency_ms) AS avg_latency_ms,
  percentile_cont(0.99) WITHIN GROUP (ORDER BY latency_ms) AS p99_latency_ms
FROM foo_request_metric
WHERE ts >= now() - interval '6 hours'
  AND tenant_id = 42
GROUP BY bucket, service
ORDER BY bucket DESC;
```

Design check: avoid unbounded cardinality in tags/dimensions.

## Spatial / Geospatial

```sql
CREATE TABLE foo_place (
  id BIGSERIAL PRIMARY KEY,
  tenant_id BIGINT NOT NULL,
  name TEXT NOT NULL,
  geom GEOMETRY(Point, 4326) NOT NULL
);

CREATE INDEX foo_place_geom_idx
  ON foo_place
  USING GIST (geom);

SELECT id, name
FROM foo_place
WHERE tenant_id = 42
  AND ST_DWithin(
    geom::geography,
    ST_SetSRID(ST_MakePoint(106.8272, -6.1754), 4326)::geography,
    1000
  )
ORDER BY ST_Distance(
  geom::geography,
  ST_SetSRID(ST_MakePoint(106.8272, -6.1754), 4326)::geography
)
LIMIT 20;
```

Design check: geometry type, SRID/CRS, precision, topology validity, and spatial index choice are part of the model. Exact functions are engine-specific. This needs verification.

## Array / Matrix

```sql
CREATE TABLE foo_sensor_grid (
  tenant_id BIGINT NOT NULL,
  captured_at TIMESTAMPTZ NOT NULL,
  rows INT NOT NULL,
  cols INT NOT NULL,
  values DOUBLE PRECISION[] NOT NULL,
  PRIMARY KEY (tenant_id, captured_at)
);

SELECT tenant_id, captured_at, values[1:10] AS first_window
FROM foo_sensor_grid
WHERE tenant_id = 42
  AND captured_at >= now() - interval '1 hour'
ORDER BY captured_at DESC
LIMIT 10;
```

Design check: dense vs sparse representation, shape, chunking, axis semantics, compression, and slicing patterns decide whether arrays belong in the database, object storage, or a specialized array engine.

## Columnar Analytics

```sql
SELECT
  event_date,
  campaign_id,
  count() AS events,
  uniqExact(user_id) AS users
FROM foo_events
WHERE event_date >= today() - 7
  AND tenant_id = 42
GROUP BY event_date, campaign_id
ORDER BY event_date DESC, events DESC
LIMIT 100;
```

Design check: partitioning, sort key, insert batch size, and mutation pattern decide whether this stays fast.
