# Security And Reliability Review

## Step
1. Map data classification, tenant boundaries, and system of record.
2. Review authentication and authorization paths.
3. Review database roles, grants, row/column/table controls, views, and service credentials.
4. Review encryption, TLS, secrets, masking/tokenization, and audit logs.
5. Review backup, restore, failover, corruption detection, and incident runbooks.
6. Review derived stores: cache, search, vector, warehouse, lake, exports, and logs.
7. Review release/migration safety.

## Check
- Can unauthorized subjects access data directly or through derived stores?
- Are sensitive fields minimized, masked, encrypted, or tokenized where required?
- Are deletion and retention propagated to all copies?
- Are backups encrypted and access-controlled?
- Has restore been tested?
- Are RPO/RTO and SLOs documented?
- Are privilege changes audited?

## Validate
- Inspect grants/IAM/config where available.
- Run or request restore drill evidence.
- Sample audit logs for sensitive operations.
- Verify tenant filters in all read models.
- Verify data-quality/integrity checks.
- Run static audit on design docs.

## Ship
Deliver findings ordered by severity:
- Data exposure risk.
- Integrity/corruption risk.
- Availability/recovery risk.
- Operational toil or missing ownership.
- Concrete remediation and validation.
