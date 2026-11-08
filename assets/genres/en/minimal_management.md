# Minimal management / scheduling (minimal_management)

Applies to: games that express system state through minimal geometry and color, where the player plans routes, resources or schedules (Mini Metro-like).

## Acceptance baseline

| Dimension | What a 4 looks like | Reference |
| --- | --- | --- |
| Usable | A run can be played from start to finish; random generation is stable and seeds are reproducible; pause and speed-up work | — |
| Looks | Minimal shapes and colors convey all the information; congestion and pressure give visual warning in advance | e.g. Mini Metro's control of information density |
| Feel | Dragging, connecting and adjusting are precise and easy to undo; switching between pause and speed-up is smooth | — |
| Clarity | Which station or line is under pressure is visible at a glance; the cause of failure is traceable | — |
| Engaging | Pressure ramps so there is "just enough time to handle it"; every plan involves a trade-off; on failure the player feels "I can do better next time" | — |

## Starting feel parameters

| Parameter | Typical starting point | Notes |
| --- | --- | --- |
| Demand spawn rate curve | Slowly increasing over time | Sets the pressure pacing |
| Capacity limit | Set by what can be carried at once | Overload threshold |
| Passenger / task patience | Set by line length | Too short makes failure feel sudden |
| Resource gain pacing | e.g. a new line or vehicle each week | Gives the player a moment to re-plan |
| Speed-up multiplier | 1x, 2x, 4x | Speed up at low pressure, slow down at high pressure |
| Random seed | Optionally fixed | The same seed must give the same opening |

## Common rework points

- Pressure curve is steep, so failure arrives suddenly with no warning
- Planning is fiddly and adjusting lines is a hassle
- One kind of layout always wins
- Too much randomness, so a bad seed is nearly a guaranteed loss
- The cause of failure can't be seen afterwards

## Sample test route

- First 2 minutes of a run → the player can learn to connect lines
- Deliberately leave it alone → there is warning as pressure builds toward failure
- Restart twice with the same seed → the opening is identical
- Adjust lines under heavy pressure → controls don't lag or misfire
- Switch between speed-up and pause → state is not lost

## One-minute test

Within one minute the player should make the first connection and see the first batch of passengers carried away.

## What to check at the greybox stage

Circles, squares, triangles and lines. Verify the **pressure curve** and the **controls**. For the pressure curve, write a script that simulates many seeds in bulk and look at the distribution of failure times; use this as evidence for "Verified by AI".
