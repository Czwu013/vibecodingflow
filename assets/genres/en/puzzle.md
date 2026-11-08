# Puzzle (puzzle)

Applies to: level-based, rule-driven puzzle games won by thinking rather than reflexes.

## Acceptance baseline

| Dimension | What a 4 looks like | Reference |
| --- | --- | --- |
| Usable | Every level is solvable; undo and reset are reliable; no dead ends without a hint | — |
| Looks | Rule-relevant elements are recognizable at a glance, with no decoration that distracts from thinking | — |
| Feel | Controls are precise and don't misfire; undo is instant; animations don't slow down repeated actions and can be skipped | — |
| Clarity | Rules are taught naturally by the first few levels, not by a manual; the cause of failure is visible | e.g. how Baba Is You and Monument Valley communicate their rules |
| Engaging | Solving gives an "aha" insight rather than a lucky guess by trial and error; difficulty ramps up; the next level holds some suspense | — |

## Starting feel parameters

| Parameter | Typical starting point | Notes |
| --- | --- | --- |
| Animation duration | 0.1–0.3 seconds | Must not feel slow during repeated actions |
| Hint delay | Optional after 30–60 seconds stuck | Hints must be optional, never forced |
| Undo stack depth | Unlimited or the whole level | In a puzzle game, undo is the key to encouraging experimentation |
| Level difficulty curve | Element count / step count grows level by level | Introduce a new rule every 3–5 levels |

## Common rework points

- Tutorial is too long or too short; new players are either bored or lost
- A level has an unintended solution that bypasses the rules
- A dead end exists and the game gives no hint
- Animations slow down repeated actions
- Players need a walkthrough to understand the rules

## Sample test route

- First level with no instructions → the player works out the rules on their own
- Deliberately go wrong → failure feedback is clear and undo is immediately available
- Play 5 levels in a row → difficulty progresses without repeating
- Reset a level midway → state returns fully to the start
- Close and reopen → progress is kept

## One-minute test

Within one minute the player should solve the first level and be able to state what the rule is.

## What to check at the greybox stage

Plain color blocks plus text. Verify the **rules** and **level solvability**. Don't verify solvability by having humans play; write a solver or script that checks each level, and use it as evidence for "Verified by AI".
