# Task: Engagement Intake (Authorization Gate)

Mandatory before any offensive-security playbook. If any item is missing, request it. No scope, no action.

## Authorization checklist
- [ ] Signed rules-of-engagement or contract on file (templates/rules-of-engagement.md).
- [ ] Named authorizing party with authority over the target systems.
- [ ] In-scope assets listed explicitly (hosts, IP ranges, domains, apps, accounts).
- [ ] Out-of-scope assets and hard prohibitions listed explicitly.
- [ ] Test window (start/end, timezone) and permitted hours.
- [ ] Rules for sensitive actions: data exfiltration limits, DoS prohibition,
      social-engineering targets and consent, third-party or cloud provider notice.
- [ ] Emergency contact and stop condition (how to abort, who to call).
- [ ] Handling and destruction plan for any data or credentials obtained.

## Scoping questions
- What is the goal of the engagement (assumed breach, external, phishing, red-team)?
- What is explicitly forbidden?
- Are production systems in scope, or a staging mirror?
- Who must be notified before high-impact actions?

## Output
Record the confirmed scope and authorization reference at the top of the engagement
record before executing any technique, and cite it in the closing report.
