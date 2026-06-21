# Data Model Concepts And Notations

Use this when the work is to explore, decompose, compare, document, reverse-engineer, or transform data models. A data model is a set of concepts and notations for describing data, constraints, identity, relationships, and operations. It is not the same thing as a database product.

## Exploration Ladder
1. Conceptual model: domain meaning, entities, relationships, events, measures, constraints, ownership.
2. Logical model: formal structure in a chosen model family, independent of one product where possible.
3. Physical model: tables, collections, keys, indexes, partitions, encodings, files, pages, storage layout.
4. Operational model: workload, concurrency, security, retention, replication, backup, recovery, migration.

Do not skip levels. Many failures happen when a physical schema is chosen before the conceptual invariants and logical access patterns are known.

## Universal Questions
- What is the unit of identity?
- What is the unit of change?
- What is the unit of consistency?
- What is the common read path?
- What is the common write path?
- Which relationships are mandatory, optional, derived, or historical?
- Which values are facts, observations, states, events, measurements, embeddings, documents, or metadata?
- Which constraints must be enforced by the DBMS, by application code, by pipeline validation, or by governance process?
- What is the growth axis: rows, documents, keys, edges, vectors, series, pixels/cells, files, tenants, or partitions?
- What model transformation is likely later: relational-to-document, document-to-relational, OLTP-to-warehouse, event-to-state, graph projection, vector reindex, or metamodel evolution?

## Relational
Concepts:
- Relation/table, tuple/row, attribute/column, domain/type, primary key, foreign key, candidate key, constraint, view, transaction.
- Relational algebra underlies selection, projection, join, union, intersection, difference, product.
- SQL uses bag semantics by default; duplicates exist unless removed.

Notations:
- ERD, crow's foot, UML class diagram mapped to tables, relational schema notation, dependency diagrams, normal forms.

Use when:
- Integrity, constraints, joins, ad hoc querying, and transactions are central.

Decompose:
- Entities, candidate keys, functional dependencies, relationship cardinality, optionality, referential action, invariant owner.
- Normalization level and deliberate denormalization.
- Transaction boundary per invariant.

Red flags:
- No primary key.
- Foreign keys omitted for critical invariants without a concrete enforcement substitute.
- Multi-valued attributes stored as CSV/JSON while requiring relational integrity.
- Soft deletes break uniqueness or referential logic.

## Key-Value
Concepts:
- Key namespace, value blob, TTL, version/CAS, prefix, shard key, lease, counter, idempotency key.

Notations:
- Key pattern catalog, namespace tree, key lifecycle table, TTL matrix.

Use when:
- Access is exact-key, bounded, and does not require secondary predicates.

Decompose:
- Key composition, tenant prefix, value schema, maximum value size, miss path, eviction/durability semantics.

Red flags:
- Future queries need "find by value".
- Large values hide document or object-store needs.
- TTL or eviction can delete system-of-record data.

## Graph
Concepts:
- Node, edge, label/type, direction, property, path, traversal, subgraph, centrality, community, reachability.
- Distinguish property graph from RDF/triple/knowledge graph.

Notations:
- Node-edge diagram, property graph schema, RDF triples, ontology/class-property diagram, SHACL-like constraint shape where relevant.

Use when:
- Variable-depth relationship traversal is the core query.

Decompose:
- Start nodes, traversal bounds, edge direction, edge cardinality, relationship properties, path filters, cycle handling.

Red flags:
- Unbounded traversal.
- Graph chosen only because "everything is connected".
- Edge semantics are vague or directionless.
- Authorization for traversed nodes is undefined.

## Document
Concepts:
- Document, field, nested object, array, aggregate boundary, embedded vs referenced data, schema validation, document version.

Notations:
- JSON Schema, BSON/JSON examples, aggregate diagrams, document lifecycle diagrams.

Use when:
- Reads/writes are aggregate-local and schema evolves within bounded documents.

Decompose:
- Aggregate root, embedded values, referenced values, document size growth, update path, validation, version migration.

Red flags:
- Documents mirror relational tables without gaining aggregate locality.
- Unbounded arrays.
- Cross-document transactions become common.
- Reporting and constraints are afterthoughts.

## Column-Family / Wide-Column
Concepts:
- Keyspace, table, partition key, clustering key, column family, denormalized query table, consistency level, tombstone, compaction.

Notations:
- Query table matrix, partition-key diagram, clustering-order diagram, access-pattern table.

Use when:
- Massive scale and partition-key access dominate, and duplicate query-specific tables are acceptable.

Decompose:
- One table per query, partition key, clustering order, read/write consistency, hot partition risk, TTL/tombstone policy.

Red flags:
- Query omits partition key.
- Secondary index is used as a relational substitute.
- Cross-partition joins or global uniqueness are central.

## Array / Matrix
Concepts:
- Dense/sparse array, tensor, dimension, coordinate, chunk/tile, cell, axis, shape, stride, mask, linear algebra operation.

Notations:
- Shape notation, axis schema, matrix/tensor diagram, chunk grid, sparse coordinate list.

Use when:
- Data is naturally multidimensional: scientific arrays, images, rasters, features, embeddings at batch scale, numerical simulation.

Decompose:
- Dimensions, coordinate system, chunk size, sparsity, compression, slicing patterns, aggregation axes, compute locality.

Red flags:
- Relational entities are forced into arrays.
- Chunking does not match access windows.
- Sparse data is stored densely without justification.

## Hierarchical
Concepts:
- Root, parent, child, tree, path, level, ancestor, descendant, segment.

Notations:
- Tree diagram, nested record schema, path enumeration, adjacency list, materialized path, nested set.

Use when:
- Data is mostly a strict tree and access follows parent-child paths.

Decompose:
- Root identity, child ordering, depth bound, reparenting behavior, subtree query, cascade delete/update.

Red flags:
- Many-to-many relationships appear.
- Reparenting is frequent but model makes it expensive.
- Cross-tree queries become common.

## Network
Concepts:
- Record type, set type, owner-member relationship, navigational access path, pointer, many-to-many through explicit links.

Notations:
- CODASYL-style owner/member set diagram, navigational path map.

Use when:
- Legacy systems or specialized navigational databases must be understood or migrated.

Decompose:
- Record types, set memberships, navigation paths, ordering, optional membership, physical pointer assumptions.

Red flags:
- Application logic depends on physical traversal order.
- Migration ignores hidden access paths.
- Many-to-many semantics are flattened incorrectly.

## Vector / Embedding
Concepts:
- Vector, embedding model, dimension, distance metric, chunk, metadata, nearest neighbor, approximate index, recall.

Notations:
- Embedding lifecycle diagram, vector schema, chunking map, recall evaluation table.

Use when:
- Similarity search or semantic retrieval is needed.

Decompose:
- Source identity, embedding version, vector dimension, distance metric, metadata filters, tenant filters, deletion/reindex policy, hybrid lexical strategy.

Red flags:
- Vector retrieval replaces exact lookup or authorization.
- No evaluation set.
- Embedding model version is not stored.

## Time-Series
Concepts:
- Timestamp, measurement, tag/dimension, field/measure, series, bucket, retention, downsampling, late/out-of-order event.

Notations:
- Timeline, tag cardinality matrix, retention/downsampling policy, bucket schema.

Use when:
- Writes are append-heavy and queries are time-windowed.

Decompose:
- Timestamp precision, tag cardinality, aggregation grain, retention, rollup, late arrival, tenant isolation.

Red flags:
- User/request/device IDs become unbounded high-cardinality tags.
- Time-series store becomes general OLTP.
- Retention is indefinite without rollups or cold storage.

## Spatial / Geospatial
Concepts:
- Point, line, polygon, multipolygon, raster, coordinate reference system, bounding box, topology, spatial index.

Notations:
- Geometry schema, map layer diagram, CRS table, bounding-box/access matrix, topology constraint list.

Use when:
- Location, distance, containment, intersection, routing, raster analysis, or map layers are core.

Decompose:
- Geometry type, CRS/SRID, precision, valid topology, spatial predicate, index strategy, geofence/routing semantics.

Red flags:
- Latitude/longitude stored as plain floats while needing containment or distance semantics.
- CRS conversion is ignored.
- Invalid polygons or antimeridian cases are not tested.

## Meta-Model
Concepts:
- Model of models: entity types, attribute types, relationship types, constraints, rules, schema evolution, generated schemas, ontology, catalog.

Notations:
- MOF-like layers, metaclass diagram, schema registry, ontology diagram, data catalog model, JSON Schema/OpenAPI/protobuf schema model.

Use when:
- The system stores or generates schemas, forms, workflows, catalogs, ontologies, policies, or configurable domain models.

Decompose:
- What is data vs metadata?
- Which objects define types?
- Which runtime objects instantiate those types?
- How are constraints versioned?
- How are migrations generated and validated?

Red flags:
- "Flexible metadata" becomes an untyped database inside the database.
- Querying, indexing, security, and migration are not planned for dynamic fields.
- Constraints exist only in UI configuration.

## Model Transformation Checks
- Source model and target model preserve identity.
- Cardinality and optionality are not lost.
- Constraints have a new enforcement point.
- Query paths remain feasible.
- History, deletes, and null/unknown semantics are preserved.
- Security labels and tenant boundaries survive transformation.
- Validation includes round-trip samples and invariant checks.
