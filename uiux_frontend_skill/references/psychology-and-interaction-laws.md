# Psychology And Interaction Laws

Use psychology as a constraint system. It should reduce cognitive load, improve task success, and prevent manipulation.

## Practical Laws

| Law | Frontend Meaning | Apply In |
| --- | --- | --- |
| Jakob's Law | Users transfer expectations from familiar products. | Navigation, checkout, forms, account flows, search, settings. |
| Fitts's Law | Target acquisition depends on size and distance. | Buttons, touch targets, menus, toolbars, XR object selection. |
| Hick's Law | Decision time grows with number and complexity of choices. | Menus, pricing, onboarding, filters, dashboards, settings. |
| Miller's Law | Working memory is limited; chunk information. | Forms, dashboards, onboarding, multi-step flows. |
| Postel's Law | Be tolerant in input and clear in output. | Validation, parsing, forms, import flows, recovery. |
| Peak-End Rule | Users remember intense moments and endings. | Onboarding, checkout, completion, failure recovery. |
| Aesthetic-Usability Effect | Attractive interfaces are often perceived as easier. | Visual polish, trust, onboarding, premium surfaces. |
| Von Restorff Effect | Distinct items are more memorable. | Primary CTA, alerts, selected states, plan comparison. |
| Tesler's Law | Complexity cannot disappear; it moves. | Advanced settings, automation, defaults, progressive disclosure. |
| Doherty Threshold | Responsive feedback sustains flow. | Loading, optimistic UI, transitions, latency masking. |

## Decision Rules

- Start with familiarity, then add novelty only where it improves the primary task.
- Make targets large enough for the input method and separate destructive actions from frequent actions.
- Group choices into meaningful categories before reducing functionality.
- Chunk long forms into sections with clear progress and recovery.
- Accept forgiving input, but make output precise and explain validation failures.
- Make endings explicit: completion message, next step, receipt, undo, or summary.
- Use visual distinction for priority, not for random decoration.
- Keep response feedback fast enough that users know the system is alive.

## Ethical Design

Avoid patterns that exploit attention, fear, inertia, or misunderstanding.

| Risk | Problem | Safer Alternative |
| --- | --- | --- |
| Infinite loops | Passive consumption without deliberate stopping points. | Natural breaks, progress summaries, reminders, user controls. |
| Hidden defaults | Users consent by accident. | Clear defaults, explicit opt-in for sensitive choices. |
| Forced continuity | Cancellation or decline is harder than purchase. | Symmetric paths for start, stop, upgrade, downgrade. |
| Scarcity pressure | Artificial urgency distorts decisions. | Show real constraints and timestamps. |
| Obscured cost | User discovers consequences late. | Upfront pricing, renewal, data use, and irreversible action warnings. |
| Dark pattern copy | Microcopy manipulates emotion. | Plain language, neutral options, clear consequences. |

## Design Principle Mapping

When a team defines a principle, connect it to a law and a rule.

| Principle | Related Law | Example Rule |
| --- | --- | --- |
| Familiarity over novelty | Jakob's Law | Use common account, cart, search, and settings patterns unless tested otherwise. |
| Clarity over abundance | Hick's Law | Show the next 1-3 meaningful choices at a decision point. |
| Action within reach | Fitts's Law | Place frequent actions near active content and make touch targets forgiving. |
| Memory outside the head | Miller's Law | Show selected filters, previous choices, and progress instead of requiring recall. |
| Fast visible response | Doherty Threshold | Every action gets immediate visual feedback, even if work continues. |

## Review Questions

- What expectation will users bring from similar products?
- Which choices can be delayed, grouped, or progressively disclosed?
- What targets are hard to hit on touch, pointer, controller, gaze, or hand tracking?
- Where does complexity move when the UI is simplified?
- What is the most memorable bad moment, and how is it recovered?
- Is any user behavior being shaped in a way that conflicts with user well-being?
