# Hardware Acceleration And Chipset-Aware Database Design

## Rule
Use acceleration only when profiling proves the bottleneck matches the hardware. Accelerators can improve scan, join, aggregation, decompression, encryption, vector search, ML-adjacent retrieval, and ETL, but they can also add data movement, driver, cost, and operational risk.

## CPU-Aware Database Work
Profile:
- SIMD/vectorized execution: AVX/AVX2/AVX-512/NEON class support depending on CPU.
- Cache locality, branch misprediction, and memory bandwidth.
- NUMA placement.
- Compression/decompression instructions.
- AES/SHA acceleration for encryption and hashing.
- Huge pages and TLB pressure.
- Thread scheduling and contention.

Good fit:
- Columnar scans.
- Vectorized aggregation.
- Compression-heavy analytics.
- Hash joins and bloom filters.

## GPU Acceleration
Good fit:
- Large analytical scans, joins, group by, geospatial, vector similarity, and batch processing.
- Columnar formats and workloads with enough parallelism.
- Pipelines that can avoid repeated CPU-GPU copies.

Check:
- GPU memory capacity and HBM bandwidth.
- PCIe/NVLink topology.
- GPUDirect Storage/RDMA support when data path matters.
- SQL operator coverage.
- Fallback behavior when a query cannot run on GPU.
- Reproducibility against CPU execution.
- Driver/CUDA/runtime lifecycle.

Red flag: accelerating OLTP point writes with a GPU because "GPU is faster."

## FPGA / CPU-FPGA Acceleration
Good fit:
- Streaming filters, decompression, regex/search, encryption, packet/data ingestion, projection, and fixed-function pipelines.
- Low-latency deterministic operations where reconfigurability is valuable.

Check:
- Development/toolchain cost.
- Operator coverage and data movement.
- PCIe/CCIX/CXL/SmartNIC placement.
- Bitstream lifecycle.
- Observability and rollback.
- Correctness testing against CPU reference.

## DPU, SmartNIC, RDMA, And Network Offload
Good fit:
- High-throughput replication, distributed shuffle, storage disaggregation, kernel bypass, low-latency RPC, and security offload.

Check:
- RDMA/RoCE/InfiniBand support end to end.
- Congestion control and loss behavior.
- NIC queueing, IRQ affinity, RSS, and NUMA locality.
- TLS/IPsec/offload implications.
- Operational debugging complexity.

## Storage And Memory Technologies
Consider:
- NVMe and NVMe-oF for low-latency storage.
- Persistent memory/NVM where engine explicitly supports it.
- HBM for accelerator memory bandwidth.
- CXL for memory expansion/pooling and coherent accelerator attachment.
- Zoned storage or object storage only when engine/table format supports it.

This needs verification for current hardware, firmware, OS, driver, and DB engine support.

## Chipset-Aware Decision Checklist
- What exact operator is bottlenecked?
- Is bottleneck CPU, memory bandwidth, I/O, network, lock contention, or query plan?
- Is data movement cost lower than acceleration gain?
- Does the DB engine support the accelerator natively?
- Can results be validated against CPU/reference execution?
- What happens on accelerator failure?
- Can the team operate drivers, firmware, monitoring, and upgrades?
- Is cost lower than simpler alternatives: index, partition, materialized view, CPU/RAM/NVMe upgrade, or query rewrite?
