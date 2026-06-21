# Data Model Exploration Matrix

## Scope
- Domain:
- System of record:
- Current artifacts:
- Target model depth: conceptual / logical / physical / operational
- Consumers:
- Out of scope:

## Model Family Comparison
| Model family | Fits because | Fails because | Critical concepts | Notation/artifact | Validation |
| --- | --- | --- | --- | --- | --- |
| Relational | | | Entities, keys, constraints, joins | ERD/crow's foot/schema | Constraint and query tests |
| Key-value | | | Key namespace, value, TTL, CAS | Key catalog | Exact-key lookup and miss path |
| Graph | | | Nodes, edges, paths, labels | Node-edge/RDF/ontology | Bounded traversal tests |
| Document | | | Aggregate, nested fields, arrays | JSON Schema/examples | Document size/update tests |
| Column-family | | | Partition key, clustering key | Query table matrix | Partition/hot-key tests |
| Array/matrix | | | Dimensions, coordinates, chunks | Shape/chunk diagram | Slice/compute locality tests |
| Hierarchical | | | Root, parent, child, path | Tree/path diagram | Subtree/reparenting tests |
| Network | | | Records, owner-member sets | Navigational path map | Legacy path equivalence |
| Vector/embedding | | | Embedding, metadata, metric | Embedding lifecycle | Recall/precision tests |
| Time-series | | | Timestamp, tags, fields | Timeline/tag matrix | Cardinality/rollup tests |
| Spatial/geospatial | | | Geometry, CRS, topology | Map layer/CRS table | Spatial predicate tests |
| Meta-model | | | Types, metaclasses, rules | Metaclass/schema model | Version/constraint tests |

## Concept Inventory
| Concept | Kind | Identity | Owner | Lifecycle | Constraints | Data class |
| --- | --- | --- | --- | --- | --- | --- |
| | entity/value/event/document/vector/series/geometry/metadata | | | | | |

## Operation Matrix
| Operation | Model element | Predicate/path | Cardinality | Sort/order | Consistency | Latency target | Index/access path |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | | | |

## Constraint Matrix
| Invariant | Enforcement point | Transaction boundary | Failure mode | Test |
| --- | --- | --- | --- | --- |
| | | | | |

## Transformation Risk
| Source model | Target model | Risk | Mitigation | Validation |
| --- | --- | --- | --- | --- |
| | | | | |
