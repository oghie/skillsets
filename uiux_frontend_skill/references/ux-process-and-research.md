# UX Process And Research

Use this when the work needs product framing, discovery, validation, handoff, or a design process rather than immediate visual styling.

## Process Model

| Phase | Purpose | Outputs | Checks |
| --- | --- | --- | --- |
| Plan | Set product strategy, scope, users, business goals, risk, and success metrics. | Design brief, assumptions, user-centered business canvas, feature map, journey hypothesis. | Goals are measurable; scope has explicit non-goals. |
| Discover | Replace assumptions with evidence from users and product data. | Interview notes, observation findings, analytics signals, card-sort results, survey themes, support-ticket patterns. | Evidence explains actual behavior, not only stakeholder opinion. |
| Explore | Generate multiple solution directions before committing. | Sketches, design-studio variants, low-fidelity alternatives, task flows. | At least two viable alternatives were considered. |
| Define | Turn chosen direction into wireframes and interaction details. | Wireframes, IA, microcopy, layout, input/output rules, clickable prototype. | Copy, states, and data edge cases are visible. |
| Design | Apply visual language, hierarchy, tokens, components, motion, and brand feeling. | High-fidelity screens, component specs, design system additions. | Visual treatment supports usability instead of hiding structure. |
| Validate | Test assumptions before full production cost. | First-impression results, click tests, usability findings, A/B plan, iteration log. | Problems are prioritized by task impact. |
| Deliver | Hand off and verify implementation. | Specs, assets, tokens, acceptance criteria, QA notes, release feedback loop. | Coded result matches intent and remains testable. |

## Design Thinking, UCD, And CPS

Use the model that matches uncertainty:

| Model | Best For | Flow |
| --- | --- | --- |
| Design thinking | Ambiguous, human-centered problems that need divergent ideas and iteration. | Empathize -> Define -> Ideate -> Prototype -> Test -> Iterate. |
| User-centered design | Product work where user research should shape each design and build step. | Research -> Align -> Build -> Test -> Iterate. |
| Creative problem solving | Early framing when the team needs to turn a vague issue into an actionable challenge. | Identify problem -> Research -> Formulate challenge -> Explore ideas -> Evaluate ideas -> Action plan -> Take action. |

Use problem statements, brainstorming, mind maps, SCAMPER, and impact/effort priority matrices to move from discovery to testable alternatives. Do not treat ideation output as validated design.

## UX Fundamentals Checks

| Check | Meaning | Design Question |
| --- | --- | --- |
| Consistency | Repeated patterns, language, layout, and behavior teach the interface. | Does the same thing work the same way everywhere? |
| Continuity | Users can move between steps, devices, and states without losing context. | Does the experience preserve progress and orientation? |
| Context | The interface adapts to user situation, task, device, and timing. | Is the next action relevant to where the user is now? |
| Complementary | Content, interaction, visual design, and system behavior support each other. | Do UI, copy, data, and feedback reinforce the same task? |

Use the UX honeycomb as a sanity check: useful, usable, findable, credible, desirable, accessible, and valuable. A design that looks polished but fails one of these dimensions still needs revision.

## Research Inputs

- User interviews: use for motivations, problems, prior knowledge, vocabulary, and unmet needs.
- Observation: use when actual workflow differs from what users say they do.
- Card sorting: use for navigation, category, menu, and information architecture problems.
- Analytics: use for drop-off, conversion, retention, funnels, search, scroll, click, and performance signals.
- Surveys: use for broader preference or segmentation signals, not deep causality.
- Customer support tickets: mine recurring confusion, error recovery, missing information, and trust blockers.
- Usability tests: use on wireframes, visual prototypes, and working product.

## Research Method Selection

| Dimension | Methods | Use For |
| --- | --- | --- |
| Qualitative | Interviews, focus groups, diary studies, field studies, usability tests. | Why users behave a certain way, motivations, confusion, context. |
| Quantitative | Surveys, analytics, A/B tests, click tests, completion metrics. | How many, how often, which variant, how much impact. |
| Behavioral | Usability tests, field studies, tree testing, eye tracking, A/B tests. | What users actually do. |
| Attitudinal | Interviews, surveys, focus groups, diary studies. | What users say, feel, prefer, or believe. |
| Generative | Interviews, field studies, diary studies, open card sorting. | Discover opportunities before the solution is fixed. |
| Evaluative | Usability tests, tree tests, five-second tests, A/B tests. | Validate whether a proposed structure or design works. |

Specialized checks:

- Tree testing evaluates whether users can find items in a proposed IA without visual context.
- Eye tracking is useful for blind spots, stumbling points, and reading patterns on critical screens.
- Five-second tests validate first impression, purpose, visual priority, and recall.
- A/B tests require enough traffic, one primary metric, and controlled variants.

## Planning Artifacts

| Artifact | Use For | Minimum Content |
| --- | --- | --- |
| Persona | Anchoring decisions to a user segment. | Context, goals, fears, constraints, knowledge level, devices. |
| Journey map | Understanding before/during/after experience. | Steps, user intent, emotion, blockers, channels, metrics. |
| Task flow | Designing action sequence. | Entry, decision points, happy path, error path, completion. |
| User story | Capturing need without prescribing UI. | User, goal, reason, acceptance criteria. |
| Design brief | Aligning team before building. | Problem, audience, scope, constraints, metrics, risks, timeline. |

## Wireframe And Prototype Discipline

- Wireframes should expose structure, hierarchy, data needs, navigation, and states without visual polish hiding issues.
- Use clickable wireframes when flow comprehension matters.
- Test both wireframes and visual design. A clean visual layer does not prove structure works.
- Move to high fidelity only after the core task path and content hierarchy are defensible.

## Validation Methods

| Method | Best For | Watch For |
| --- | --- | --- |
| Five-second test | First impression, visual priority, page purpose. | Users remember the right message and action. |
| Click test | Whether users know where to act. | Heatmaps should concentrate around intended controls. |
| Usability test | Task success, confusion, recovery, wording, state handling. | Ask users to think aloud; do not teach the UI. |
| A/B test | Measurable production optimization with traffic. | Requires enough traffic, one clear metric, and controlled variants. |
| Design review | Team critique before cost increases. | Separate subjective taste from task evidence. |
| QA during development | Implementation fidelity. | Compare states, spacing, responsive behavior, accessibility, and performance. |

## Delivery Checklist

- Designs include all states, empty states, loading states, error messages, and recovery paths.
- Handoff includes tokens, component names, responsive behavior, assets, copy, accessibility notes, and interaction timing.
- QA compares coded UI against intent in multiple widths and input modes.
- Post-release metrics close the loop with product outcomes and support feedback.
