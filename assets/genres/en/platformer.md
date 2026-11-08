# Platformer (platformer)

Applies to: 2D / 2.5D platformers centered on jumping, movement and precise landings.

## Acceptance baseline

| Dimension | What a 4 looks like | Reference |
| --- | --- | --- |
| Usable | Can be played from start to finish without crashing; collision is stable, with no wall-sticking or falling through the floor; respawn after death is reliable | — |
| Looks | The character, standable platforms and hazards can be told apart within 1 second; the silhouettes at takeoff and landing are readable | e.g. Celeste's visual readability |
| Feel | No perceptible delay from key press to takeoff; jump height is controllable (tap low, hold high); landings are crisp, not floaty; coyote time and jump buffering exist, so a mistake feels like "I mishit the button" rather than "the game ate my input" | e.g. the controls of Celeste and Super Meat Boy |
| Clarity | It's obvious at a glance where you can stand and where you will die; the player can state the cause of every death | — |
| Engaging | Retry within 1–2 seconds of dying; every death teaches something; the player wants another go | e.g. Super Meat Boy's retry pacing |

## Starting feel parameters

These are only common starting values. Go by feel and drag them in the F9 tuning panel.

| Parameter | Typical starting point | Notes |
| --- | --- | --- |
| Max move speed | Set by level scale | Fix this first; other parameters are built around it |
| Acceleration / braking time | 0.05–0.2 seconds | Too long feels slippery, too short feels stiff |
| Jump height | About 2–4 character heights | Determines platform spacing |
| Short-hop cut factor | 0.4–0.6 | Reduction of upward velocity when the jump key is released |
| Fall gravity multiplier | 1.3–2.0x | Above 1 makes falling crisper and eases the "floaty" feel |
| Coyote time | 0.05–0.15 seconds | Grace period to still jump after leaving a platform edge |
| Jump buffer | 0.08–0.15 seconds | Press jump just before landing and the jump fires on landing |
| Max fall speed | Set by level | Prevents falling so fast the player passes through the floor |
| Air control factor | 0.6–1.0 | Ability to steer in the air |

## Common rework points

- Jump is too floaty or too heavy (the most common)
- Sliding on sudden stops, sluggish turnarounds
- Platform edge detection is too strict, so the player falls by a hair
- Cause of death is unclear and the player doesn't know why they died
- Camera follow is jittery or laggy
- Steep difficulty curve, with the first hard spot arriving too early

## Sample test route

- On flat ground, tap, hold and mash the jump key, one jump each → height is controllable and landings are crisp
- Move left and right, stop suddenly, then reverse → stops within 0.2 seconds with no sliding
- Walk off a platform edge and then jump → pressing slightly late still jumps (coyote time)
- Press jump just before landing → jumps on landing (jump buffer)
- Deliberately fall into a pit → respawn at the checkpoint within 1 second

## One-minute test

A new player should be able to clear the first pit within one minute and understand that "dying means an instant restart".

## What to check at the greybox stage

Only a block character and rectangular platforms. This stage verifies just two things, **feel** and **retry pacing**; add no art, sound or effects until they pass.
