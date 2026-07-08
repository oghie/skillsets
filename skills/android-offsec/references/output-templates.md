# Output Templates

Every investigation produces TWO reports.

## Output A: Operational Action Plan

For the field operator. Operational and technical.

```markdown
# [OPERATIONAL] Offensive Action Plan: [Case ID / Target]

## Situation Assessment
- Target device: [model, OS version, patch level]
- Current access level: [no access / locked / ADB / root]
- Intel gathered: [key findings from OSINT/recon]

## Strategic Attack Chain
[Map the full chain from current state to evidence goal]

## Phase-by-Phase Execution Plan

### Phase N: [Name]
1. **Command:**
   ```bash
   [exact command]
   ```
   **Expected result:** [what to observe]

2. **Command:**
   ```bash
   [next command]
   ```
   **Expected result:** [what to observe]

## Contingency Plans
- If [technique] fails: fallback to [alternative]
- If device reboots: [recovery procedure]
- If tripped: [cover/exit procedure]

## Required Equipment
- [Hardware list]
- [Software/tools list with versions]
```

## Output B: Forensic Evidence Report

For the analyst. Evidentiary and court-ready.

```markdown
# [FORENSIC] Evidence Extraction Report: [Case ID]

## Chain of Custody
- Operator: [ID/badge]
- Device received: [timestamp UTC]
- Device state: [locked/unlocked, battery %, connectivity state]
- All operations performed on forensic workstation ID: [workstation identifier]

## Extraction Summary

| Artifact ID | Evidence Type | Source | Timestamp (UTC) | SHA-256 |
|-------------|---------------|--------|-----------------|---------|
| EV-001 | Call log DB | mmssms.db | 2026-01-15T10:30:00Z | a1b2c3... |
| EV-002 | WhatsApp chat | msgstore.db.crypt14 | 2026-01-15T10:31:00Z | d4e5f6... |

## Evidence Analysis

### Communication Map
- [Who contacted whom, when, frequency]
- [Key conversations relevant to investigation]

### Financial Trail
- [Wallet addresses discovered]
- [Transaction hashes]
- [Exchange account links]

### Location Timeline
- [Movement reconstruction from location data]
- [Key locations visited, correlated with timeline]

### Digital Relationships
- [Contact graph from multiple data sources]
- [Shared accounts, linked devices]

## Methodology
- [Tools and techniques used]
- [Limitations encountered]

## Forensic Integrity Statement
I certify that the above evidence was extracted using forensically sound methods.
All original data is preserved with verified SHA-256 hashes.
No modifications were made to original evidence files.
```
