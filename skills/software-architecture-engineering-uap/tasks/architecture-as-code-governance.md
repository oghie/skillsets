# Architecture-As-Code Governance

Use this task when architecture boundaries should be checked continuously against repository structure, imports, generated code, manifests, contracts, or operational artifacts.

## Procedure

1. Select the smallest valuable architecture rule.
2. Name logical components exactly as diagrams/ADRs use them.
3. Map logical components to physical paths, packages, namespaces, services, or manifests.
4. Define allowed and forbidden dependencies.
5. Define exceptions and revisit triggers.
6. Create or update a constraint spec.
7. Run a local fitness check.
8. Decide whether violations indicate code drift, stale diagrams, stale constraints, or intentional architecture change.
9. Add the check to CI only when the rule and remediation path are agreed.

## Output

```markdown
## Architecture Fitness Function
- Governed decision:
- Logical components:
- Physical mapping:
- Allowed dependencies:
- Forbidden dependencies:
- Exceptions:
- Check command:
- Current result:
- Remediation:
```

## Required Reads

- `references/architecture-as-code-and-fitness-functions.md`
- `references/development-and-operation-views.md`
- `references/design-principles-and-modularity.md`
