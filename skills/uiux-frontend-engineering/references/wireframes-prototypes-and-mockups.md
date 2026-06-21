# Wireframes Prototypes And Mockups

Use this when choosing fidelity, sketching flows, creating wireframes, building prototypes, preparing mockups, writing microcopy, designing microinteractions, or deciding what must be tested before frontend implementation.

## Fidelity Ladder

| Artifact | Tests | Includes | Avoid |
| --- | --- | --- | --- |
| Sketch or paper prototype | Early structure, sequence, and concept fit. | Rough screens, task order, alternatives. | Treating sketch detail as final layout. |
| Low-fidelity wireframe | Layout, IA, content priority, and navigation. | Boxes, labels, hierarchy, main controls. | Color, brand polish, final imagery. |
| Mid-fidelity wireframe | Component placement and interaction detail. | More precise controls, copy placeholders, states. | False precision without data and edge cases. |
| High-fidelity wireframe | Layout close to implementation without full visual styling. | Realistic spacing, content, controls, and responsive hints. | Shipping without testing interaction and accessibility. |
| Prototype | Flow, interaction, transitions, and task completion. | Clickable links, state transitions, data assumptions. | Testing visual polish when the flow is still unclear. |
| Mockup | Visual blueprint for implementation. | Color, type, imagery, spacing, tokens, assets, annotations. | Assuming a static mockup specifies behavior. |

## Prototype Method Selection

| Method | Use When | Guardrail |
| --- | --- | --- |
| Paper prototype | Fast concept validation and team discussion. | Keep feedback about structure, not visual style. |
| Wizard-of-Oz prototype | The experience depends on backend, AI, automation, or service behavior not built yet. | Disclose the test setup internally and do not overstate feasibility. |
| Clickable prototype | Navigation and task comprehension are the main questions. | Include error, empty, and recovery paths, not only the happy path. |
| Coded prototype | Technical interaction, responsiveness, performance, or accessibility is uncertain. | Throw away or harden deliberately; do not accidentally ship prototype code. |

## Wireframe Checks

- Entry point, primary action, secondary action, and exit are visible.
- Content blocks expose real information needs and data limits.
- Navigation and backtracking are explicit.
- Error, empty, loading, disabled, and success states have placeholders.
- Mobile and desktop structure are considered before visual styling.

## Mockup Process

1. Define requirements: product goal, users, platform, constraints, and technical limits.
2. Gather pattern references from comparable products and design systems.
3. Sketch initial layouts.
4. Create low-fidelity mockups for layout and hierarchy.
5. Apply tokens, typography, imagery, component variants, and responsive versions.
6. Annotate behavior, states, assets, copy, accessibility, and handoff notes.
7. Validate with stakeholders, users, and developers before implementation.

## Microcopy

Microcopy includes button labels, field labels, helper text, placeholders, validation messages, errors, empty states, onboarding tips, confirmation text, and recovery guidance.

Effective microcopy is:

- Clear: says what will happen.
- Useful: helps users complete or recover from a task.
- Contextual: appears where the user needs it.
- Consistent: matches product vocabulary and brand voice.
- Trustworthy: avoids guilt, pressure, ambiguity, hidden cost, or false urgency.

## Microinteractions

Define each microinteraction with:

| Part | Question |
| --- | --- |
| Trigger | What starts it: tap, click, key, hover, gesture, system event, or completion? |
| Rules | What changes, what is allowed, and what is prevented? |
| Feedback | What visual, audio, haptic, or text response confirms state? |
| Loop/mode | Does it repeat, persist, time out, or return focus? |

Use microinteractions for feedback, orientation, confirmation, error prevention, and continuity. Respect reduced-motion preferences and avoid decorative motion that delays task completion.
