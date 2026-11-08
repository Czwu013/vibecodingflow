# Idle / incremental (idle_incremental)

Applies to: idle games where numbers grow on their own and progress comes from purchased upgrades and periodic resets.

## Acceptance baseline

| Dimension | What a 4 looks like | Reference |
| --- | --- | --- |
| Usable | Offline earnings are correct; big numbers don't overflow and display properly; saves are reliable (the most critical item, since lost progress hurts the most) | — |
| Looks | Number formatting is clear (K / M / B or scientific notation) and doesn't jitter; the state of purchasable items is visible at a glance | — |
| Feel | Clicks and purchases give instant feedback; numbers ticking up feels satisfying | — |
| Clarity | The player knows what the next goal is and which purchase gives the best return | — |
| Engaging | The next goal is always "just a little longer and I can buy it"; a reset (prestige) opens up a new dimension | e.g. the pacing of Cookie Clicker and Antimatter Dimensions |

## Starting feel parameters

| Parameter | Typical starting point | Notes |
| --- | --- | --- |
| Cost growth factor per item | About 1.07–1.15x per purchase | Larger means hitting the wall sooner |
| Production rate | Set so the first automated item is bought in about 1 minute | Early pacing |
| Offline earnings efficiency and cap | e.g. 50%, capped at 8–24 hours | Keeps offline earnings from swallowing active play |
| Milestone multipliers | Every 25 / 50 / 100 levels | Gives continued buying a small goal |
| Prestige formula | Set so the first reset comes after about 1–2 hours | A reset must bring something new |
| Autosave interval | 10–30 seconds | Prevents accidental progress loss |

## Common rework points

- Growth curve stalls (waiting too long) or runs too fast (loses meaning)
- Big numbers are hard to read
- Offline earnings are miscalculated
- Resets feel stale, just zeroing out the numbers
- Numbers refresh too often and flicker

## Sample test route

- First minute of play → buy the first automated producer, numbers grow on their own
- Close the page for 5 minutes, then reopen → offline earnings are reasonable and clearly shown
- Play for 15 minutes straight → there is always a next goal that is "almost there"
- Reach the first reset point → a new mechanic appears and is worth restarting for
- When numbers get huge → the display is still tidy

## One-minute test

Within one minute the player should buy the first automated producer and see the numbers growing on their own.

## What to check at the greybox stage

Only numbers and buttons. Verify the **growth curve**: write a script that simulates N hours of progress and check whether the wait at each stage is reasonable; use this as evidence for "Verified by AI".
