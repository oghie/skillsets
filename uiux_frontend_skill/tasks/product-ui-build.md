# Product UI Build

Use this when asked to build a new UI, app screen, landing/product surface, dashboard, editor, tool, or redesign from requirements.

## Steps

1. Frame the product.
   - Identify users, job-to-be-done, business goal, target surface, constraints, and success metric.
   - Verify: one primary user task and one measurable outcome are named.
2. Choose process depth.
   - Lightweight for small component changes; full Plan -> Discover -> Explore -> Define -> Design -> Validate -> Deliver for ambiguous or high-impact work.
   - Verify: assumptions and evidence gaps are visible.
3. Define information architecture and flow.
   - Map entry, primary path, alternative path, empty/error states, and completion.
   - Verify: user can recover from failure without restarting.
4. Select visual system.
   - Use existing app design if present. If not, choose a `theme/` style by product fit and read its style file.
   - Verify: token source and mode are named.
5. Build component/state model.
   - Define components, variants, states, accessibility roles, and responsive behavior.
   - Verify: state matrix covers default, focus, loading, empty, error, success, disabled.
6. Implement frontend.
   - Use platform conventions and existing stack. Map tokens to variables/classes before hand styling.
   - Verify: no parallel one-off design system is created.
7. Validate.
   - Run lint/tests when available; inspect screenshots across widths; check keyboard and accessibility basics.
   - Verify: include command output or explicit blocker.

## Required Output

- Product judgment.
- Users and task.
- Theme/style decision.
- Flow/state summary.
- Components built or changed.
- Responsive/accessibility/performance checks.
- Residual risks.
