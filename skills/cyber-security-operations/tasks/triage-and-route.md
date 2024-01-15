# Task: Triage and Route

Use this task on every request. It selects one playbook and hands off to it.

## Steps
1. Restate the objective in one sentence: what outcome, on which systems, by when.
2. Establish authorization:
   - Defensive, detection, forensic, or compliance work on systems you own or operate:
     proceed.
   - Any offensive category (red-team, penetration testing, credential access, C2,
     social-engineering simulation): stop and run tasks/engagement-intake.md first. Do
     not continue without a signed rules-of-engagement.
3. Classify into one category (see SKILL.md). If two fit, pick the primary objective and
   note the secondary for a possible second pass.
4. Open references/INDEX.md, then references/index/<category>.md. Match a single playbook
   by name, tags, or ATT&CK technique ID. Do not read every playbook - locate one.
5. Read playbooks/<category>/<name>/PLAYBOOK.md and its local references/, scripts/, and
   assets/. Follow it exactly; it is the source of truth for the technique.
6. Execute with the loop: observe -> orient -> decide -> act -> verify. Record each
   command, output, and decision.
7. If the objective needs another technique, return to step 3 for the next playbook.
8. Close with the right artifact (see templates/): a forensic evidence report for DFIR,
   an engagement record for offensive work, a detection or remediation note otherwise.

## Rules
- One playbook at a time. Route, do not improvise.
- Confirm the target's exact version and platform before selecting version-specific steps.
- Pair any offensive technique with its detection mapping (ATT&CK <-> D3FEND).
- If no playbook fits, say so and describe the gap; do not invent an unvetted procedure.
