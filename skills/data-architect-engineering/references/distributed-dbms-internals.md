# Distributed DBMS Internals

Use this when a design crosses one process, node, disk, partition, region, or DBMS boundary.

## Architecture Modes
- Shared everything: single-node style; CPUs share memory and disk.
- Shared memory: processors share an address space and disk; uncommon for ordinary DBMS deployments.
- Shared disk: compute nodes have private memory but shared logical storage; common in cloud/serverless/lakehouse-style designs.
- Shared nothing: each node owns CPU, memory, and disk; coordination is through network messages.

Decision forces:
- Compute/storage decoupling.
- Locality of data and execution.
- Rebalancing cost.
- Failure domain.
- Network latency and packet loss.
- Consistency protocol cost.
- Operator pushdown and remote execution.

## Data Transparency And Routing
A distributed DBMS may hide physical data location, but the architect cannot ignore it.

Ask:
- How does the client or coordinator find the target partition?
- Does the query go to data, or does data move to query?
- Which operators are pushed down: filters, projections, joins, aggregates?
- Which results are gathered, repartitioned, or broadcast?
- What happens when a partition owner changes?

## Partitioning
Goal: maximize single-partition transactions and local joins.

Schemes:
- Naive table placement: simple but weak for joins and skew.
- Vertical partitioning: split columns; reconstruct tuple through identifiers.
- Horizontal partitioning: split rows by hash, range, predicate, tenant, time, or composite key.
- Logical partitioning: node owns key range but storage may be shared.
- Physical partitioning: node physically stores owned keys.
- Consistent hashing/rendezvous hashing: reduce remapping when nodes join/leave.

Partition key checks:
- Query predicates include the key.
- Tenant/key cardinality and skew.
- Hot key/range risk.
- Rebalancing plan and time.
- Secondary-index routing.
- Cross-partition transaction frequency.
- Locality for joins and foreign-key-like invariants.

## Replication
Dimensions:
- Primary-replica vs multi-primary.
- Synchronous vs asynchronous propagation.
- Continuous log shipping vs on-commit propagation.
- Active-passive vs active-active execution.
- Physical vs logical replication.

Review:
- Commit acknowledgment rule.
- Read-your-writes and stale-read contract.
- Replica lag SLI.
- Conflict semantics for multi-primary writes.
- Failover election and fencing.
- Split-brain prevention.
- CDC and replica stream ordering.

## Distributed Transactions And Consensus
Distributed transaction cost is architectural, not incidental.

Two-phase commit:
- Coordinator asks participants to prepare.
- All participants must vote before commit.
- Blocking if coordinator fails after prepare until recovery or protocol-specific resolution.
- Often fewer round trips than consensus when nodes are reliable and close.

Consensus-family protocols:
- Paxos/Raft-style quorum progress can avoid single coordinator blocking under enough live nodes.
- Requires majority/quorum availability and leader/proposer behavior.
- Adds latency, operational complexity, and failure-mode surface.

Validate:
- What is the resource manager per partition?
- Is the coordinator centralized, decentralized, or client-side?
- Are prepare/commit decisions logged durably?
- What happens if coordinator crashes, participant crashes, or network partitions?
- Are transaction retries idempotent?

## CAP/PACELC Framing
Do not use CAP as a slogan.

State:
- During partition: choose availability or linearizable consistency for the affected operation.
- Else, during normal operation: choose lower latency or stronger consistency where the tradeoff exists.
- Partition tolerance is a condition to survive, not a feature to "pick" casually.

## Distributed Joins
Join plans depend on partitioning:
- Replicated small table joined locally with partitioned large table.
- Both tables partitioned on same join key: local joins plus final gather.
- One small table broadcast to all partitions.
- Shuffle both tables by join key: most expensive and needs disk/network headroom.
- Semi-join filters or Bloom filters can reduce movement.

Red flags:
- Broadcast side is not actually bounded.
- Shuffle temp storage is not reserved.
- Join key skew ignored.
- Network egress/cross-region cost ignored.
- Coordinator gather step becomes bottleneck.

## Federated Databases
Federation connects multiple DBMSs behind one logical query layer.

Risks:
- Different data models and query languages.
- Weak global optimizer.
- Connector capability gaps.
- Data copying and freshness ambiguity.
- Security and audit consistency.
- Transaction semantics across engines.

Use federation deliberately for integration and discovery; avoid making it the hidden system of record without a clear ownership and consistency model.
