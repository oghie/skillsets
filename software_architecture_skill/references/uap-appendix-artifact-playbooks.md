# UAP Appendix Artifact Playbooks

Use this quick reference to keep the Unified Architecture Process concrete. It compresses the activity-step-task structure into repeatable artifact playbooks.

## A1 Requirements Refinement

Output:
- stakeholder profile;
- refined functional requirements;
- refined NFR scenarios;
- deficiency log and resolved questions.

Checks:
- stakeholders are not only end users;
- functional requirements include actor, trigger, response, and outcome;
- NFRs include stimulus, environment, response, target, source, and priority;
- ambiguous adjectives are replaced by measurable criteria.

## A2 System Context Analysis

Output:
- boundary/context diagram or DFD;
- functional context/use case model;
- information context/domain or persistent object model;
- behavior context/activity/control-flow model.

Checks:
- external actors, systems, stores, devices, and operators are visible;
- boundary-crossing flows are named;
- persistent data and source-of-truth are identified;
- context-level invocation patterns are explicit.

## A3 Schematic Architecture Design

Output:
- candidate style table;
- selected style rationale;
- integrated schematic architecture;
- connector and structural-element refinement notes.

Checks:
- styles are selected from forces, not fashion;
- multiple styles are integrated deliberately;
- generic style roles are renamed into domain-specific elements;
- connectors have communication, data, control, and failure semantics.

## A4 Architecture Views

Functional view:
- refine use cases;
- define functional components;
- allocate components to tiers/placeholders;
- define provided/required interfaces;
- identify variation points and adaptation schemes.

Information view:
- refine persistent object model;
- define data components;
- allocate data components;
- define data interfaces;
- choose persistence medium and data resilience tactics.

Behavior view:
- refine invocation patterns and control flow;
- identify key behavioral elements;
- define detailed activity/sequence/state models;
- align behavior with functional and information views.

Deployment view:
- define computing device nodes;
- define execution environments;
- define network connectivity;
- allocate software artifacts.

Optional views:
- use `references/development-and-operation-views.md` when code organization or production operation materially affects the architecture.

## A5 NFR Design

Output:
- facts/policies;
- desirable criteria;
- candidate tactics;
- selected tactics;
- impacted architecture views;
- conformance map.

Checks:
- every tactic traces to a fact/policy and criterion;
- selected tactics have cost/benefit reasoning;
- impacted functional, information, behavior, deployment, development, and operation views are updated as needed;
- conformance is verified by tests, models, prototypes, measurements, or operational evidence.

## A6 Architecture Evaluation

Output:
- target elements for evaluation;
- selected evaluation approaches/methods;
- findings, risks, and actions;
- revised architecture or accepted trade-offs.

Checks:
- scenario-based, model-based, formal, PoC, prototype, benchmark, threat model, or operational review methods are matched to risk;
- evaluation report separates evidence, inference, assumptions, and questions;
- findings have severity, impact, owner, and verification.

## SRS Intake Pattern

When starting from an SRS-like document, extract:
- purpose, scope, definitions, and stakeholders;
- functional requirements and use cases;
- external interfaces;
- data requirements;
- NFRs and constraints;
- assumptions and dependencies;
- acceptance or verification criteria.

Then route missing, vague, or conflicting items back into A1 before designing architecture.
