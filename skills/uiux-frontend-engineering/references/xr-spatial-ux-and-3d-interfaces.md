# XR Spatial UX And 3D Interfaces

Use this for WebXR, VR, AR, MR, spatial computing, 3D product experiences, avatar systems, immersive training, spatial dashboards, and mixed-reality tools.

## XR Premise

Web/mobile UX principles transfer to XR at the level of human-centered design, but not as flat-screen mechanics. XR design must account for body, space, perception, comfort, agency, and environment.

## XR Discovery

Identify:

- Device class: handheld AR, headset AR, VR, MR passthrough, WebXR, 3D web, spatial computer.
- Input: controller, hand tracking, gaze, pinch, touch, keyboard, voice, haptics, body movement.
- Environment: seated, standing, room-scale, outdoor, industrial, social, private, public.
- Safety: physical obstacles, social exposure, privacy, fatigue, motion sickness, emergency exit.
- Fidelity: storyboard, paper prototype, graybox, 3D mock, game-engine prototype, production scene.

## Spatial Design Objects

Use object-oriented UX for XR before rushing to panels.

| Object | Attributes | Actions | Relationships | States |
| --- | --- | --- | --- | --- |
| User/avatar | Role, body, permissions, comfort profile. | Move, look, speak, grab, point. | Other users, objects, system. | Idle, engaged, blocked, unsafe. |
| Spatial object | Position, scale, affordance, data, ownership. | Select, inspect, move, resize, attach. | Environment, anchors, groups. | Available, hovered, grabbed, locked. |
| Panel/menu | Distance, depth, orientation, density. | Open, close, pin, scroll, filter. | User gaze, hand, object context. | Docked, floating, hidden, modal. |
| Environment | Boundaries, light, sound, occlusion, anchors. | Calibrate, scan, teleport, reset. | User, content, real-world surfaces. | Ready, tracking lost, unsafe. |

## Interaction Rules

- Design around agency: users should know what they can do and how to undo.
- Prefer direct manipulation when it is comfortable and precise.
- Use spatial menus only when their location supports recall and task flow.
- Keep close UI out of the user's face; respect field of view and personal space.
- Provide orientation cues, anchors, and recenter/reset.
- Avoid rapid forced movement, unexpected scale changes, and excessive camera motion.
- Use audio, haptics, and visual feedback together, but let users reduce intensity.
- Onboard by doing: teach one interaction at a time in context.

## Comfort And Safety

Check:

- Locomotion mode and motion sickness risk.
- Resting position, duration, pace, and fatigue.
- Hand/arm reach and repeated gesture load.
- Visual clarity, depth, occlusion, and legibility at distance.
- Safe zones and physical boundary awareness.
- Accessible alternatives for users who cannot use a modality.
- Exit, pause, recenter, and emergency stop.

## Avatar And Social XR

- Avatar behavior affects trust. Manage eye contact, speed, tone, proximity, and animation intensity.
- Provide personal boundaries, blocking/reporting, mute, visibility controls, and safety defaults.
- Avoid always-staring avatars; make attention and engagement intentional.
- Make embodiment optional when the app does not need it.
- Design identity, customization, and privacy as product surfaces.

## WebXR And 3D Web

- Treat WebXR as progressive enhancement: provide non-XR fallback where useful.
- Optimize assets, shaders, textures, and draw calls.
- Provide keyboard/mouse/touch alternatives for 3D interactions when possible.
- Keep text legible and UI stable across device classes.
- Test scene framing, camera, lights, model scale, and input mapping.

## Spatial Analytics And Validation

- Track task completion, dwell, route, gaze/attention proxy, object interaction, error recovery, and comfort feedback.
- Combine quantitative spatial analytics with observation and user interviews.
- For training flows, measure process compliance and repeated error points.
- For commerce or galleries, measure discovery, inspection, confidence, and conversion.

## XR Deliverables

- Spatial object map.
- Interaction storyboard.
- Comfort/safety checklist.
- Graybox prototype.
- Panel/menu layout with distance and anchoring.
- Input modality matrix.
- Analytics event map.
- Accessibility alternatives.
