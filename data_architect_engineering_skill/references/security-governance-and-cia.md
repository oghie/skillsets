# Security, Governance, And CIA

## CIA For Data Systems
Confidentiality:
- Authentication, least privilege, TLS, encryption at rest, masking/tokenization, row/column/table-level controls, tenant isolation, secret handling, and audit.

Integrity:
- Normalization, referential integrity, check constraints, transactions, locks, idempotency, validation, append-only audit logs, checksums, hashing, and reconciliation.

Availability:
- Backups, tested restores, replication, failover, capacity, rate limits, DDoS controls, maintenance windows, incident runbooks, and corruption recovery.

## Access Control
Define:
- Subjects: users, services, analysts, admins, jobs, support staff, model pipelines.
- Resources: tables, columns, rows, collections, indices, topics, buckets, dashboards, backups.
- Actions: read, write, delete, export, administer, decrypt, restore, impersonate.
- Enforcement points: application, database roles, views, row-level security, column masking, policy engine, warehouse grants, object storage IAM, search/vector filters.
- Audit events: login, failed auth, privilege change, data export, sensitive read, admin action, restore, delete, retention override.

Use roles for job functions, not individual one-off privilege sprawl.

## Encryption And Secrets
- TLS for client-server and node-node traffic when supported.
- Encryption at rest for database files, disks, object storage, backups, and snapshots.
- Application-level encryption or tokenization for fields whose DB admins should not read.
- KMS/HSM where key governance matters.
- Rotate keys with tested procedures.
- Never store plaintext passwords. Password hashing is separate from database encryption.

## Data Privacy And Governance
Track:
- Data classification.
- PII, PHI, PCI, secrets, credentials, biometrics, location, and confidential business data.
- Retention and deletion policy.
- Right-to-delete or legal hold conflict.
- Cross-border transfer constraints.
- Data lineage and consumer inventory.
- Export controls and analyst access.

This needs verification for current regulations, contractual duties, and compliance standards.

## Injection And Query Safety
- Parameterize queries.
- Avoid string-concatenated SQL/DSL/search queries from untrusted input.
- Validate identifiers separately; parameter binding usually does not bind table/column names.
- Apply tenant/security filters server-side, not only in UI.
- Review stored procedures and dynamic SQL.

## Multi-Tenant Data Security
Minimum checks:
- Tenant ID included in system-of-record schema and derived stores.
- Unique constraints include tenant context when needed.
- Indexes support tenant-scoped access.
- Search/vector/cache keys include tenant boundary.
- Backups and exports preserve tenant separation.
- Admin/support access is audited and just-in-time when possible.

## Backup Security
- Backups often contain the most sensitive complete copy of data.
- Encrypt backups.
- Restrict restore and download privileges.
- Test restore in isolated environments.
- Scrub or synthesize data for non-production unless production data use is justified and controlled.

## Security Red Flags
- Shared production admin account.
- Analysts use application credentials.
- No audit of privilege changes.
- Search/vector index omits tenant or authorization filter.
- Encryption claimed but backups/snapshots are not covered.
- Restore test requires production secrets in plaintext.
- Data deletion only deletes application row but not search/vector/cache/warehouse copies.
- Logs contain tokens, passwords, PII, or full query parameters.
