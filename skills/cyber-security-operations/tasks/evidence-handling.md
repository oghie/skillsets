# Task: Evidence Handling

Apply whenever you acquire, copy, or analyze data as evidence (DFIR, forensic
extraction, incident response).

## Chain of custody
- Record who collected each item, when (ISO 8601 with timezone), from where, and how.
- Log every transfer of custody: from, to, date/time, reason.
- Keep originals read-only; work only on verified copies.

## Integrity
- Compute a SHA-256 hash of every acquired artifact at acquisition time.
- Re-verify the hash after transfer and before analysis; record both values.
- For disk or memory images, hash the source and the image; they must match.
- Never modify an original. Note any unavoidable change and why.

## Documentation
- Timestamp every action. Prefer tool output over recollection.
- Record tool names and versions used for acquisition and analysis.
- Store hashes, logs, and custody records with the evidence, not separately.

## Output
Produce the forensic evidence report (templates/forensic-evidence-report.md) with the
custody log, per-artifact hashes, analysis, and an integrity statement.
