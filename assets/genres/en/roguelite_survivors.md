# Roguelite / survivors (roguelite_survivors)

Applies to: run-based games with auto-attack or simple attacks, level-up choices over time and meta progression (Vampire Survivors-like, lightweight roguelites).

## Acceptance baseline

| Dimension | What a 4 looks like | Reference |
| --- | --- | --- |
| Usable | A run can be played from start to results screen; frame rate is stable with many enemies on screen; meta progression and saves are not lost | — |
| Looks | Even with lots of projectiles and enemies, the player's position, health and key dangers are still easy to see | e.g. Vampire Survivors' readability at high density |
| Feel | Movement is agile; hits give clear feedback (knockback, numbers, sound); the moment of leveling up gives a sense of "I got stronger" | — |
| Clarity | The benefit of each upgrade option is clear at a glance; after dying the player can trace back "what killed me" | — |
| Engaging | At the end of a run there is an urge to "go again"; meta progression is visible; each run's build differs | e.g. the "one more run" pull of Vampire Survivors and Hades |

## Starting feel parameters

| Parameter | Typical starting point | Notes |
| --- | --- | --- |
| Run length | Set per project, commonly 10–30 minutes | Determines the whole numeric curve |
| Player move speed / health / pickup range | Set by enemy speed | Move speed should be slightly faster than most ordinary enemies |
| Enemy spawn rate curve | Increasing over time | The first 3 minutes decide retention |
| Enemy health and damage scaling over time | Linear first, then tune | Avoid runaway number inflation |
| XP requirement curve | Fast for the first few levels, slowing later | The first level-up must come very quickly |
| Weapon cooldown, damage, area | A separate set per weapon | Weapon strength must be balanced |
| Drop probability | By item rarity | |
| Number of upgrade options | Pick 1 of 3 is common | Needs a real trade-off |
| Hit invincibility duration | 0.3–1.0 seconds | Prevents being killed instantly |

## Common rework points

- The first 3 minutes are too boring, or too hard
- Number inflation runs away and late game one-shots everything
- Upgrade options offer no real choice (one is always clearly best)
- The screen is too messy to see yourself and dangers
- Weapon strength is lopsided, so only one or two are viable
- Meta progression slows the pace, or removes challenge from the early game

## Sample test route

- First 3 minutes of a run → enemies increase gradually and the first level-up arrives in reasonable time
- Pick one weapon direction and play to 10 minutes → the build visibly comes together
- Deliberately don't dodge and die once → the results screen is clear and offers a way into another run
- At the moment with the most enemies on screen → you and the health bar are still easy to see
- Buy one meta upgrade and start another run → the difference is noticeable

## One-minute test

Within one minute the player should kill the first wave of enemies and gain a level, feeling "I'm getting stronger".

## What to check at the greybox stage

Squares and dots, a fixed few enemy types and three weapons. Verify only the **numeric curve** and whether **upgrade choices** involve real trade-offs. The numeric curve can be checked by scripting a simulated run, as evidence for "Verified by AI".
