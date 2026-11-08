# Top-down action (top_down_action)

Applies to: top-down melee or shooter combat, including twin-stick shooters and lightweight ARPGs.

## Acceptance baseline

| Dimension | What a 4 looks like | Reference |
| --- | --- | --- |
| Usable | The whole flow of movement, combat and pickups runs without crashing; collision is stable; enemy AI doesn't get stuck | — |
| Looks | The character, enemies, attack ranges and damage hitboxes are distinguishable at a glance; getting hit has visible feedback | — |
| Feel | Attack windup and recovery are moderate; hits have hitstop, knockback or screen shake; dodging has perceptible invincibility frames; aiming is precise | e.g. Hades' combat feedback |
| Clarity | Enemy attacks have a readable telegraph; the player knows why they got hurt | — |
| Engaging | Combat has a rhythm of offense and defense; loot or growth unlocks new ways to play | — |

## Starting feel parameters

| Parameter | Typical starting point | Notes |
| --- | --- | --- |
| Move speed / acceleration | Set by combat scale | Set move speed first, then attack range |
| Attack windup / active / recovery | 0.05–0.3 seconds each | Windup too long feels clumsy, too short has no weight |
| Hitstop | 2–6 frames | The cheapest "I hit it" feeling |
| Knockback distance | By enemy size | |
| Dodge distance / duration / invincibility frames | 0.2–0.4 seconds | Invincibility frames must be noticeable |
| Enemy sensing range / attack interval | A separate set per enemy type | |
| Enemy attack telegraph duration | 0.3–0.8 seconds | Long enough for the player to react |
| Hit invincibility duration | 0.3–1.0 seconds | |

## Common rework points

- Attacks lack impact (missing hitstop and feedback)
- Enemy attacks are unreadable, so the player feels ambushed
- Dodge is unreliable, or invincibility frames are mistimed
- Camera doesn't follow well
- Mouse or controller aiming is off

## Sample test route

- Attack a single enemy repeatedly → hit feedback is clear
- Dodge an enemy's windup attack → the telegraph is readable and there is time to dodge
- Face 3 enemies at once → the screen stays clear and you can still tell who is about to attack
- Dodge through an attack → invincibility frames take effect
- Get hit → you know who hit you and with what

## One-minute test

Within one minute the player should defeat the first enemy and feel "I hit it".

## What to check at the greybox stage

Blocks and cone-shaped hitboxes. Verify the **impact parameters** (hitstop, knockback) and whether **enemy attack windups are readable**.
