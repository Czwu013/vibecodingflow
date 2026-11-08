# Genre notes: Platformer (platformer)

<!-- From ai-dev-kit genre preset platformer. A starting point, not a verdict. When writing a review card, take the most likely rework points and the sample test route from here. -->

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
