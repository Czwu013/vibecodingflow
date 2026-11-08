<!-- Purpose: rules and boundaries that must be followed when writing code. Changes that violate them are sent straight back at review.
     Rules come from pitfalls hit and platform requirements; state the reason for each where possible. Items with {{}} are for you to fill in per project; the rest are general defaults, delete any that don't apply. -->
# Code rules

## Runtime environment
1. {{e.g. runs by double-clicking index.html, no server needed (reason: zero barrier for the human reviewing)}}
2. {{e.g. runs offline, loads no resources from the web (reason: reproducible, compliant)}}

## Code organization
3. Tunable parameters live only in config files, not scattered through the code (reason: the human must be able to tune feel live, and the AI changes parameters without touching logic).
4. UI text lives only in language files; add all languages at once.
5. Split any file that exceeds about 500 lines, and make the split its own change (reason: a split mixed into a feature change can't be reviewed).

## Reviewability
6. Follow `contracts/feedback_friendly.md`: one-click copy of debug info, a tuning panel, one-click jump to the state under review.
7. Each milestone's test route is at most 10 minutes; if longer, split it into two milestones.

## Compliance
8. {{e.g. do not use others' trademarks or assets}}

## Wrapping up every change
9. No errors; at least one screenshot or run record as evidence (put it in `plans/evidence/`).
10. Update CURRENT_STATE, plans and the review card; mark a milestone "In review" at most.
