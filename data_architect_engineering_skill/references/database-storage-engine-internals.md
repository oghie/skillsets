# Database Storage Engine Internals

Use this when a decision depends on how a DBMS stores, fetches, mutates, caches, indexes, compresses, or reclaims data. Do not treat storage as only "disk size"; storage design shapes query latency, write amplification, crash safety, vacuum/compaction, and operational headroom.

## Storage Hierarchy
- Separate volatile memory from non-volatile storage. Memory is byte-addressable and fast; persistent media is typically page/block-addressable and far slower.
- Prefer sequential I/O when the workload and engine permit it. Random I/O dominates many disk-oriented designs.
- Treat page size as a workload decision: smaller pages help point updates and cache fit; larger pages can help scans and read-mostly systems.
- If database page size exceeds hardware atomic-write size, verify torn-page protection, checksum, WAL, doublewrite, or equivalent safeguards.

## File And Page Layer
Map the logical data path:
1. SQL or API request selects a logical object.
2. Execution engine asks for a page or key range.
3. Buffer pool resolves page table state.
4. Storage manager maps page id through the page directory to file and offset.
5. Page is read, latched, interpreted, mutated, and eventually flushed.

Review:
- File layout: single file, file-per-table, tablespace, segment, extent, object-storage file, or custom storage layer.
- Page directory durability and synchronization with actual files.
- Page header metadata: page size, checksum, version, visibility, free space, page type.
- Free-space tracking, empty-page lists, page type separation, and allocation strategy.
- Record ID semantics: physical identifiers are not stable application IDs.

## Page And Tuple Layout
Common page layouts:
- Tuple-oriented slotted pages: page header and slot array grow from one side, tuple data grows from the other. Good general-purpose row-store layout; handle deletes, variable-length fields, and fragmentation explicitly.
- Log-structured storage: write updates sequentially into memtables/SSTables or logs, then compact. Good write path and append-only media fit; read path, compaction, and write amplification must be managed.
- Index-organized storage: table data lives inside an index structure. Good clustered access; update and split behavior must be understood.

Tuple layout checks:
- Tuple header carries visibility/null metadata, not full schema metadata.
- Attribute order, alignment, null bitmap, fixed vs variable length values, overflow pages, and external value storage affect scan and update cost.
- Large values need a policy for inlining prefix bytes, overflow pages, external files, deduplication, compression, and transaction/durability guarantees.

Red flags:
- Application stores or depends on physical record IDs.
- BLOB/external file storage is claimed durable/transactional without evidence.
- Updates to variable-length rows have no fragmentation or vacuum/compaction strategy.
- Page checksum or torn-write behavior is unknown for critical data.

## Buffer Pool
The buffer pool is not just "cache"; it is the correctness boundary between volatile memory and persistent pages.

Check:
- Page table vs page directory are understood: page table is in-memory page-to-frame mapping; page directory maps durable page ids to files/offsets.
- Dirty flag, pin/reference counter, page latch, and eviction safety are tracked.
- Pinned pages cannot be evicted; long scans or long transactions can starve the pool.
- Dirty pages need background writing or checkpoint integration.
- Replacement policy handles workload shape: LRU, CLOCK, LRU-K, ARC, old/young lists, per-query localization, priority hints.
- Sequential flooding is mitigated for large scans.
- Buffer pool bypass is available for one-pass scans, temporary sort/join data, or non-reused pages.
- Prefetching follows query plan and index leaf order, not merely physical next page.
- Multiple buffer pools or page-type pools reduce contention and improve locality when the engine supports them.

OS interaction:
- Avoid assuming OS page cache and DB buffer pool cooperate. Many engines use direct I/O to avoid double caching; some engines deliberately use OS cache.
- Verify fsync, O_DIRECT, mmap, madvise, mlock, msync, TLB shootdown, kernel page-cache behavior, and silent I/O error semantics per engine.

## Storage Models
Match physical model to workload:
- NSM / row store: attributes for a tuple are colocated; good for OLTP point reads/writes and full-row access.
- DSM / column store: values for one attribute are colocated; good for OLAP scans over few columns, compression, late materialization, and vectorized execution.
- PAX / row-group columnar: columns stored within row groups; common in analytic file formats and columnar engines.
- HTAP split designs: fractured mirror or delta-store style designs can isolate writes from analytics but add freshness, compaction, and consistency tradeoffs.

Decision checks:
- Does query need whole tuple, few columns, many rows, or many point updates?
- Is late materialization useful?
- Is compression applied before or after scan predicates?
- How are updates moved from row-oriented delta store to columnar read store?

## Compression
Compression is a CPU, memory, I/O, and query-planning decision.

Use:
- General compression for page/block/file size when decompression overhead is acceptable.
- Columnar encodings when operators can run on encoded values: RLE, bit-packing, mostly/patching, bitmap, delta, dictionary.
- Order-preserving dictionary encoding when range predicates and sorting must operate on codes.
- Roaring or similar bitmap representations when low-cardinality or sparse bitmaps appear.

Validate:
- Compression ratio.
- Encode/decode CPU.
- Predicate execution before decompression.
- Write amplification during update or compaction.
- Effect on buffer pool residency and cache locality.

## Index And Filter Internals
Index design must include maintenance, concurrency, and storage overhead, not just lookup speed.

Structures:
- Hash tables: good for equality, not range or prefix lookup.
- B+Trees: default order-preserving index; support point, range, prefix, sibling leaf scans, clustering, and index-only reads.
- Bloom/Cuckoo/range filters: reduce negative lookups and remote/disk probes; false positives must be acceptable.
- Skip lists: common in in-memory memtables; poor locality for disk/cache compared with page-oriented trees.
- Tries/radix trees: prefix-oriented keys, possible compression, useful for specific key domains.
- Inverted indexes: term-to-posting-list mapping for search; segment immutability and merge policy matter.
- Vector indexes: IVF-like clustering or graph/HNSW-like nearest-neighbor search; recall, filtering order, and rebuild cost are first-class concerns.

B+Tree checks:
- Composite key order and prefix usability.
- Duplicate key handling: record-id suffix vs overflow chains.
- Clustered vs unclustered access and page-id sorting for tuple fetches.
- Node size chosen for storage medium, cache fit, point/range mix.
- Merge threshold avoids split/merge thrashing.
- Variable-length keys use indirection or key maps rather than wasteful padding.
- Intra-node search can be linear, binary, interpolation, or SIMD-assisted.
- Prefix compression, deduplication, suffix truncation, pointer swizzling, bulk build, and write-optimized variants are available where appropriate.

## Hashing Internals
Hashing appears in page tables, joins, aggregates, indexes, and partitions.

Review:
- Hash function quality, CPU cost, and collision behavior.
- Linear probing vs cuckoo vs chained hashing vs extendible/linear hashing.
- Load factor, tombstones, resize policy, and cache locality.
- Whether deletion and concurrent updates are safe.
- Whether the structure is for memory-only metadata, durable indexes, or temporary query state.

## Storage Internals Questions
- What is the working set in pages, not only bytes?
- Which operations touch heap pages, index pages, WAL pages, temp pages, and catalog pages?
- What is the dirty-page generation rate and flush rate?
- What is the compaction/vacuum/rewrite debt?
- What data structures are on the critical path: page table, lock table, B+Tree latch, memtable, WAL buffer, dictionary, zone map?
- Which pages or keys are hot and why?
- What evidence proves the page/cache/index design works under realistic skew?
