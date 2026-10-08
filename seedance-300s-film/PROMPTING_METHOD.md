# Seedance 2.5 Prompting Method — Project Standard

This project uses shot choreography instead of one long undifferentiated action paragraph.

## Evidence-based structure

Higgsfield's Seedance 2.5 prompting guidance recommends labeled sections, explicit first-frame blocking, shot-by-shot choreography, camera movement, physics, lighting and audio. ByteDance's Seedance 2.5 launch material demonstrates timestamped action, blocking and camera trajectories and supports reference-driven generation and multi-round extension.

## Production sequence

1. Generate Part 01 from the canonical child, panda and environment references.
2. Extract the actual final frame.
3. Use that real frame as the start-frame reference for Part 02.
4. Repeat through Part 10.
5. Keep canonical identity references active in every generation.
6. Never invent a future start or end frame.

## Prompt order

REFERENCE DECLARATION -> GLOBAL STYLE -> SCENE/INTENTION -> FIRST FRAME/BLOCKING -> SHOT-BY-SHOT TIMELINE -> CAMERA/OPTICS -> PHYSICS/CONTACT -> LIGHTING -> AUDIO -> CONTINUITY/HANDOFF -> NEGATIVE LOCKS.

## Motion choreography

- Give each shot one primary action and one primary camera move.
- Make actions causal: perception -> decision -> acceleration -> contact -> reaction -> recovery.
- Describe body mechanics, contact points, inertia, friction and recovery instead of vague words such as "epic".
- The one-year-old child primarily crawls. Walking attempts are brief, unstable and physically plausible.
- The plush panda moves with visible weight. Its soft body compresses on contact and rebounds naturally.
- Keep important contacts visible: hands on ground, feet on surfaces, hands gripping props, panda body contacting the ground or wall.
- Use motivated camera movement that follows the action rather than hiding it.
- Use close-ups only for decisive details.
- Prefer practical-looking effects: dust, cardboard, soft plush deformation and lightweight breakaway material.
- Do not stack several difficult stunts into one shot.

## 30-second pacing

Use about 5-7 shots per part. Each shot has a defined start pose, action and endpoint. Allow acceleration, reaction and recovery to take real time.

## Continuity

The final shot must create a stable handoff composition. The next part begins from the exact generated final frame.

## Reference economy

Use one deliberate reference per identity-critical element:
- Child: sakhi.Refernce.jpg
- Panda: panda-reference.png
- Environment: environment-references/environment-design.md

## Realism locks

Keep the same sun direction, time of day, architecture, parked vehicles when reused, street geometry, wardrobe, scale, prop appearance and camera grammar. No teleportation, duplicate objects, unexplained jumps, magical facial changes or age changes.

## Audio

Keep one continuous musical identity across the film. Add specific diegetic effects only where they reinforce visible action.

## Iteration

If a clip fails, change one major variable at a time: choreography, reference/start frame, or camera instruction.
