# Tower defense (tower_defense)

Applies to: games where the player places defensive units on a path or map to hold off waves of enemies.

## Acceptance baseline

| Dimension | What a 4 looks like | Reference |
| --- | --- | --- |
| Usable | A full run can be won or lost; placing, selling and upgrading are bug-free; pathfinding works | — |
| Looks | Tower types, ranges and enemy health are distinguishable at a glance | — |
| Feel | Placing towers is smooth, cancel and sell don't misfire; pause and speed-up work; hits give feedback | — |
| Clarity | When an enemy leaks, the player knows why (which enemy type, where the gap is); stat info is easy to look up | — |
| Engaging | Every wave involves decisions (what to buy, where to place); early choices affect the late game; after winning the player wants to try another build | e.g. the build decisions in Bloons TD and Kingdom Rush |

## Starting feel parameters

| Parameter | Typical starting point | Notes |
| --- | --- | --- |
| Tower: cost / range / attack speed / damage | A separate set per tower | Each tower needs its own role |
| Upgrade curve | Cost grows faster than benefit | Avoids upgrading just one tower |
| Sell refund ratio | 60%–80% | Too high makes experimenting cost-free |
| Enemy: health / speed / armor | A separate set per enemy type | Types should force the player to change approach |
| Per-wave count curve | Increasing wave by wave | The first few waves should be easy |
| Wave interval | Skippable | Lets experienced players avoid waiting |
| Starting gold / income per wave | Set so the first wave allows 2–3 towers | |
| Game speed options | 1x, 2x, 3x | |

## Common rework points

- One tower type is the optimal answer, making choices fake
- The first few waves are too boring, or the opening is too stressful
- Late-game numbers explode
- Bugs where the path gets blocked or detours
- Range is hard to see

## Sample test route

- First 3 waves, placing towers at ease → controls are smooth and feedback is clear
- Waves 5–8 start to apply pressure → decisions are required
- Play to defeat using only one tower type → it should fail at some wave (no universal answer)
- Try pause, speed-up and sell once each → all work normally
- Leak one enemy → you can see where the gap is

## One-minute test

Within one minute, place the first tower and watch it kill an enemy.

## What to check at the greybox stage

Geometric-shape towers and enemies. Verify the **numeric curve** and **decision variety**. Write a script that auto-battles many builds against each other and check whether a single optimum exists, as evidence for "Verified by AI".
