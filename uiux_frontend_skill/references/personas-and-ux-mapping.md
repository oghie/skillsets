# Personas And UX Mapping

Use this when a UI/UX task needs user segmentation, persona choice, persona comparison, journey mapping, empathy mapping, experience mapping, touchpoint analysis, service blueprinting, or friction discovery.

Reusable templates: `templates/persona-comparison-matrix.md` and `templates/ux-mapping-matrix.md`.

## Persona Evidence Ladder

| Persona Type | Use When | Minimum Evidence | Guardrail |
| --- | --- | --- | --- |
| Goal-directed persona | Product decisions depend on what users are trying to accomplish and which tasks matter most. | Goals, motivations, essential tasks, pain points, behavior patterns, scenarios. | Do not reduce the persona to demographics; rank goals and tasks. |
| Role-based persona | Workflows differ by job role, responsibility, authority, collaboration, or operating context. | Role, duties, environment, routines, tools, handoffs, collaboration needs. | Do not generalize one role into all users. |
| Fictional persona | Early ideation needs a hypothetical lens before research exists. | Clearly labeled assumptions, scenario, expected behaviors, risk questions. | Treat as provisional; replace or revise with research. |
| Engaging persona | Teams need empathy and memory for a user segment. | Story, environment, technology context, motivations, fears, goals, constraints. | Narrative must not override observed data. |

## Comparing Key Persona Types

| Type | Focus | Primary Use | Key Fields | Risk |
| --- | --- | --- | --- | --- |
| Buyer persona | Ideal prospect before purchase. | Marketing, acquisition, offer framing, sales copy. | Buying trigger, budget, channel, objections, loyalty, decision criteria. | Can bias product toward acquisition rather than long-term use. |
| Customer persona | Existing customer relationship. | Retention, support, loyalty, lifecycle improvements. | Current experience, satisfaction drivers, service issues, repeat behavior. | Can miss non-customer users who still operate the product. |
| User persona | Person completing tasks in the product. | UX, interaction design, information architecture, accessibility, workflows. | Goals, context, device, knowledge level, tasks, pain points, scenarios. | Weak if it ignores business constraints and account/customer context. |
| Proto-persona | Team hypothesis before research. | Fast alignment and research planning. | Assumptions, expected needs, suspected behaviors, validation questions. | Must be labeled as an assumption, not evidence. |

Every persona should support a design decision. Include only fields that affect task flow, information architecture, copy, trust, accessibility, device constraints, or validation.

## Persona Components

- Identity: name or label, segment, role, context, and device environment.
- Background: relevant experience, domain knowledge, constraints, and accessibility considerations.
- Goals and needs: primary goal, secondary goals, and unmet needs.
- Behavior patterns: task frequency, channels, decision style, collaboration, and error recovery habits.
- Pain points and challenges: blockers, frustrations, trust risks, and workarounds.
- Motivations: intrinsic drivers, external incentives, and success criteria.
- Quotes: short evidence-backed statements only when they clarify mindset.
- Scenarios: realistic entry point, task path, and completion condition.

## UX Map Frame

Before drawing a map, state:

| Dimension | Decision |
| --- | --- |
| Point of view | Whose experience is being mapped: persona, role, buyer, customer, support staff, or operator. |
| Scope | Whole lifecycle, single journey, route, feature, service episode, or one critical task. |
| Focus | Emotions, actions, touchpoints, information needs, operations, channels, or failure recovery. |
| Structure | Timeline, stage matrix, service blueprint, empathy map, or flow diagram. |

## Journey And Experience Mapping Process

1. Develop or select a persona.
2. Perform research: interviews, observation, analytics, support tickets, surveys, or field data.
3. Define journey stages.
4. List customer interactions and touchpoints.
5. Capture user intent, thoughts, feelings, actions, channels, and evidence.
6. Pinpoint friction points, drop-offs, trust gaps, and unmet needs.
7. Propose fixes and assign owners.
8. Update the map after testing or release evidence.

## Map Artifact Selection

| Artifact | Best For | Structure | Output |
| --- | --- | --- | --- |
| Customer journey map | Brand/product-specific journey over time. | Stages, touchpoints, actions, emotions, pain points, opportunities. | Experience fixes, channel alignment, funnel or lifecycle improvements. |
| Empathy map | Shared understanding of what a segment thinks, feels, sees, hears, says, and does. | Goal, say/do/think/feel, pains, gains, context signals. | Persona refinement, copy direction, trust and motivation decisions. |
| Experience map | Broad human process not tied to one product. | Phases, actions, thoughts, feelings, opportunities. | Market-level opportunities and common friction patterns. |
| Service blueprint | User-visible journey plus internal delivery system. | Evidence, customer actions, frontstage, backstage, support processes. | Operational fixes, ownership boundaries, handoff and failure-path design. |

## Non-Negotiable Checks

- Label whether each persona is research-backed, synthesized, fictional, or proto.
- Do not use a persona without connecting it to flow, IA, copy, component states, or validation.
- Do not use journey maps as decorative posters; each pain point needs an owner or decision.
- Service blueprints must include internal support processes when the user experience depends on operations.
