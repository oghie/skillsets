# Architecture As Code And Fitness Functions

Use architecture-as-code when architecture intent must stay aligned with implementation over time. The goal is fast feedback, not ceremonial documentation.

## Table Of Contents
- [Core Model](#core-model)
- [When To Apply](#when-to-apply)
- [ADL-Lite Constraint Spec](#adl-lite-constraint-spec)
- [Fitness Function Types](#fitness-function-types)
- [Layer And Database Constraints](#layer-and-database-constraints)
- [Metrics](#metrics)
- [Workflow](#workflow)
- [Helper Script](#helper-script)

## Core Model

Keep four artifacts aligned:

```text
Architecture diagrams <-> ADL/constraint spec
        ^                    ^
        |                    |
Repository structure <-> executable fitness functions
```

Every governed architectural boundary should have:
- a logical name used in diagrams/ADRs;
- a physical mapping to paths, packages, namespaces, services, or manifests;
- allowed dependencies;
- forbidden dependencies;
- verification command.

## When To Apply

Use lightweight checks when:
- modules or services have clear dependency rules;
- layered architecture has open/closed layer constraints;
- database access must be restricted to persistence/data-access modules;
- domain/subdomain/component names must align with directories/packages;
- architecture documentation drifts from code;
- an existing system is being realigned incrementally.

Avoid heavy architecture-as-code when the system is tiny, volatile, exploratory, or lacks stable boundaries. Start with one high-value constraint.

## ADL-Lite Constraint Spec

Use YAML/JSON for local checks:

```yaml
components:
  presentation:
    paths: ["src/presentation/**"]
    may_depend_on: ["application"]
    forbidden_imports: ["src/persistence", "src/database"]
  application:
    paths: ["src/application/**"]
    may_depend_on: ["domain", "persistence"]
  domain:
    paths: ["src/domain/**"]
    may_depend_on: []
  persistence:
    paths: ["src/persistence/**"]
    may_depend_on: ["domain"]
shared_forbidden_imports:
  - "src/database"
```

Keep logical names stable even if physical path names differ. The mapping is the bridge between architecture diagrams and repository reality.

## Fitness Function Types

| Fitness Function | Evidence |
|---|---|
| Structural alignment | Directories/packages map to domains, subdomains, components, or services. |
| Dependency rule | Imports only follow allowed direction. |
| Layer rule | Closed layers cannot be skipped; open layers document allowed bypass. |
| Database access rule | Only persistence/data access modules call DB clients or SQL/query APIs. |
| API/schema compatibility | Contract tests or schema diff checks prevent breaking changes. |
| Security boundary | Protected operations pass through authorization/audit enforcement. |
| Operational readiness | Runbook, alerts, SLOs, rollback, and migration checks exist. |
| Code metric | Complexity, coupling, instability, and distance from main sequence stay within thresholds. |

Use objective thresholds. A metric gathered without an alarm/check is observation, not a fitness function.

## Layer And Database Constraints

Layered architecture should state:
- allowed layer-to-layer calls;
- which layers are closed and cannot be skipped;
- which layers are open and why bypass is allowed;
- where database logic may live;
- exceptions and expiration/revisit trigger.

Example:

```text
presentation -> application -> domain
application -> persistence -> database
presentation -X-> persistence
domain -X-> persistence
presentation/application/domain -X-> database client
```

## Metrics

Use code-level metrics for trends and guardrails:
- cyclomatic complexity for local complexity;
- afferent/efferent coupling for incoming/outgoing dependency pressure;
- abstractness and instability for package balance;
- normalized distance from main sequence for abstraction/stability risk;
- duplication and package cycle detection for maintainability.

Metrics require local calibration. Do not blindly import thresholds from another system.

## Workflow

1. Select one architecture decision worth governing.
2. Name the logical components and physical mappings.
3. Write a small constraint spec.
4. Run the check and record current violations.
5. Decide whether violations mean code must change, architecture must change, or the spec is wrong.
6. Add the check to CI only after the team agrees on enforcement semantics.
7. Update diagrams, ADL/spec, tests, and directory structure together when architecture changes.

Failed architecture fitness functions are conversation triggers. Treat them as evidence of misalignment, not automatic proof that code is wrong.

## Helper Script

Run:

```bash
python3 software_architecture_skill/scripts/architecture_constraint_audit.py --root <repo> --config <constraints.yml>
```

The helper is intentionally language-light. It scans text imports and paths, so use stronger language-specific tools when available:
- Java: ArchUnit, jQAssistant.
- .NET: NetArchTest.
- TypeScript/JavaScript: dependency-cruiser, eslint boundaries/import rules.
- Python: import-linter.
- Go: custom `go list` checks.
