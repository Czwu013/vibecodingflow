<!-- Purpose: the main entry point of the dev log. The AI reads this first at every start-up.
     Maintenance rule: whenever you change any doc under docs/dev, update the "Last updated" and "Status" columns in the table below.
     docs/dev/tools/check_docs.py checks the links, status values and staleness here. -->
# Dev log entry point

> Design intent lives only in the design doc: `../design/DESIGN.md`. This folder records only **what the code actually is**, plus decisions, debt and reviews along the way.

## Document index

Status: **Current** = consistent with the code · **Stale** = known to be out of date, logged in the debt file · **Archived** = moved to `archive/`

| Document | Purpose | Last updated | Status |
| --- | --- | --- | --- |
| [CURRENT_STATE.md](CURRENT_STATE.md) | What the code actually does now (≤100 lines) | {{Date · milestone}} | Current |
| [DECISIONS.md](DECISIONS.md) | Major decisions and reasons | {{Date}} | Current |
| [DEVELOP_DEBT.md](DEVELOP_DEBT.md) | Debt and payoff criteria | {{Date}} | Current |
| [known_mismatches.md](known_mismatches.md) | Known deviations between code and design | {{Date}} | Current |
| [feedback_log.md](feedback_log.md) | Human feedback items and their handling status | {{Date}} | Current |
| [contracts/](contracts/) | Rules that must be followed + the human's taste profile | {{Date}} | Current |
| [plans/README.md](plans/README.md) | Milestone status and next steps | {{Date}} | Current |
| [reviews/](reviews/) | Review cards: AI's delivery notes + the human's scores and verdict | {{Date}} | Current |

**Create when needed:** `audits/` `ledgers/` `references/` `roadmaps/` `bench/` `../research/` `../release_notes/` (add `--full` at init to get the templates).

## Milestone status flow

```
To do → In progress → In review → Done
          ↑              │
          └──────────────┘  Verdict "Rework": sent back
                            Verdict "Pass with tweaks": AI batches the fixes; next round the human re-checks only the changed items
```

- **In review**: the AI has finished and self-tested (run / screenshots / no errors), generated the review card, and spelled out "what was verified and what the human should focus on".
- **Done**: may be set only when the review card says `Verdict: Pass`, with a reviewer and date. **The AI must not mark "Done" itself.**

## AI start-up order (read only these)

1. This file → `CURRENT_STATE.md` → `plans/README.md` → `contracts/` (including `taste.md`)
2. If there is an unclosed review card / feedback: read the latest review card and the "Open" items in `feedback_log.md`
3. Do only the next milestone; when done, update `CURRENT_STATE.md`, `plans/`, the review card, `DECISIONS.md` (if any), and this table
4. For docs that can't be updated in time: log it in `DEVELOP_DEBT.md` and set the status in this table to "Stale"
5. Before wrapping up, run `python docs/dev/tools/check_docs.py`

**Not read by default:** `archive/` `research/` `references/` `audits/` and past review cards. Look them up when needed, to save context.

## Document change log

| Date | Change |
| --- | --- |
| {{Date}} | Set up the docs/dev documentation system |
