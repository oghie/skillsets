# Explore And Decompose Data Model

Use this playbook when the task is to understand, document, compare, reverse-engineer, or redesign the data model before picking or changing a database.

1. Define modeling scope.
   - Name the domain, system of record, consumers, current artifacts, and whether the target is conceptual, logical, physical, or operational.
   - Verify: scope states what is intentionally out of model.

2. Classify candidate data model families.
   - Consider relational, key-value, graph, document, column-family, array/matrix, hierarchical, network, vector/embedding, time-series, spatial/geospatial, and metamodel.
   - Verify: each candidate is accepted or rejected by invariant and access pattern, not trend or vendor preference.

3. Extract concepts.
   - Identify entities, values, events, relationships, measurements, documents, keys, vectors, coordinates, metadata, and constraints.
   - Verify: every concept has identity, lifecycle, owner, and data classification.

4. Map operations.
   - List commands, queries, traversals, aggregations, searches, similarity lookups, spatial predicates, and analytical reads.
   - Verify: each operation has predicate, cardinality, sort/order, consistency need, and latency target.

5. Map constraints and failure modes.
   - Capture uniqueness, referential integrity, cardinality, temporal validity, topology, schema versioning, authorization, retention, and deletion.
   - Verify: each critical constraint has an enforcement point and test.

6. Choose notation and artifacts.
   - Use ERD/crow's foot for relational, JSON Schema for document, key pattern catalog for KV, node-edge/triple diagram for graph, partition matrix for column-family, shape/chunk diagram for arrays, timeline for time-series, map layer/CRS table for spatial, metaclass diagram for metamodel.
   - Verify: notation makes hidden assumptions visible.

7. Decide model fit and transformation risk.
   - State selected model(s), rejected alternatives, transformation risks, migration needs, and operational implications.
   - Verify: output includes query matrix, constraint matrix, security matrix, and validation plan.
