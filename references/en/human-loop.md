# The Human Review Loop: Details

Contents: 1 Where the cost comes from · 2 Five dimensions and the yardstick · 3 Suggested-verdict rules · 4 Panel text format · 5 Writing a good review card · 6 Tiered review · 7 Parameterizing subjective issues · 8 Incremental re-check · 9 Circuit breaker · 10 Capturing taste · 11 Metrics · 12 Anti-patterns

## 1. Where rework cost comes from

AI can finish 90%. The remaining 10% is "is this what I wanted?", which only a human can judge. If that 10% is done sloppily, later rework and bug-fixing burn tokens many times over. The cost comes from three places, each with a matching mechanism:

| Cost source | Symptom | Mechanism |
| --- | --- | --- |
| Unclear goal | You only find out it's not what you wanted after it's built | DESIGN section 6 acceptance baseline; greybox first to check feel |
| Vague feedback | Human says "feels a bit off", AI guesses; back-and-forth questions | Scores + structured issues + one-click copy of debug info |
| Blind changes | Tweak a bit, look a bit, same spot changed five rounds | Batch fixes, parameterization, incremental re-check, circuit breaker |

## 2. Five dimensions and the yardstick

Five dimensions by default. You can add or remove rows in the review card's score table (scripts parse by the rows in the table):

| Dimension | What it asks |
| --- | --- |
| Usable | Does the flow work end to end? Does it crash or stall? |
| Looks | Does the visual impression feel right? |
| Feel | Are the feedback, rhythm and weight of the controls right? |
| Clarity | Do you know what to do at a glance? Is the information understandable? |
| Engaging | Do you want to keep using / playing it? |

Scores: 1 Unusable · 2 Clearly wrong · 3 Acceptable but not satisfied · 4 Satisfied · 5 Delighted.

**Scoring needs a yardstick.** Without a baseline, a "3" means something different every time and trends are meaningless. So at project start, write in DESIGN section 6 what a 4 looks like for each dimension and which specific moment it is benchmarked against. If the yardstick turns out to be off after the first review, change DESIGN and log it in DECISIONS; don't quietly switch standards.

A score of ≤2 or 5 requires a one-line reason: a low score tells the AI where to change, a 5 tells the AI what must not get lost.

## 3. Suggested-verdict rules

| Suggested verdict | Condition | Follow-up |
| --- | --- | --- |
| Rework | Any dimension ≤2, or any "High" severity issue | Back to "In progress"; fix as one batch |
| Pass with tweaks | Not rework, and any dimension =3 or any "Medium" severity issue | Fix as one batch; next round the human re-checks only the changed items |
| Pass | All ≥4 and no Medium/High issues | Human signs off, mark "Done"; Low issues go to feedback_log as to-dos |

Severity meaning: High = must fix, can't continue otherwise · Medium = should fix, hurts the experience · Low = fix when there's time.

The human has the final say. If they pick a verdict different from the suggestion, write theirs and record the override reason; `check_docs.py` raises an ERROR for an unexplained mismatch and lets an explained one through. The rule lives in both `dk_common.suggest_verdict` (Python) and `review_panel.html` (JS); change both together.

## 4. Panel text format

The text the panel's "Copy for AI" produces, and also the minimal format a human can follow when writing by hand:

```
[Review M1 round 2] Reviewer: Sam  Date: 2026-10-31
Scores: Usable 4  Looks 3  Feel 2  Clarity 4  Engaging 3
Reasons: Feel = the jump is floaty
Key questions: Q1 No (wants it snappier); Q2 OK
Re-check: FB-003 ✓; FB-004 ✗ (button still too small)
Skipped: steps 3,5
Issues:
1. [Feel][High] the jump landing is floaty | wants it crisp
2. [Looks][Low] the title font is a bit thin
Good: loves the colour palette
Verdict: Rework (matches suggestion)
Override reason: (appears only if the human changed the verdict)
```

Parsing notes:

- After `Scores:` come "dimension + number" pairs; "?" means not scored.
- Under `Issues:` each line is `[Dimension][Severity] what happened | what they want`; the part after `|` may be absent.
- `Skipped:` says which steps the human missed; discount the verdict's reliability accordingly and add coverage next round if needed.
- `Re-check:` appears only from round 2. Items marked ✓ become "Closed"; items marked ✗ stay "Open" with a note appended.
- If the human gives feedback verbally ("jump is floaty, button too small, rest is fine"), organize it into the format above yourself, write it into the review card, and ask about any uncertain severities or dimensions in one reply; don't ask item by item.

## 5. Writing the AI part of a review card

**3-minute test route**: one action plus one expectation per step, at most 7 steps, starting from the most likely rework point (the plan's "Most likely rework point").

- Bad: `1. Play the game`
- Good: `1. Press Space to jump three times → expect: the third jump is higher than the first, with a brief pause on landing`

**Key questions for you**: replace "how does it feel?" with concrete questions answerable by "OK / not OK", including the current value and where to adjust it.

- Bad: `Q1: How does the feel seem?`
- Good: `Q1: Is the jump too heavy or too light? Current gravity is 2.4, adjustable in the F9 panel`

**Verified by AI**: list the facts checked by machine (it runs, zero console errors, screenshots of three key states) so the human knows these need no retesting. Don't write unverifiable things like "carefully checked".

**Known shortcomings**: honestly state what's unfinished or untested ("only tested in Chrome", "sound effects are placeholders"), so the human doesn't spend time on known issues or assume something was verified.

## 6. Tiered review: check the most expensive first

Rework cost rises with fidelity. Within one milestone, review in fidelity tiers and only move on when a tier passes:

1. **Greybox**: boxes and text only. Verify the core loop and feel. Throwing it away now loses only a few dozen lines.
2. **Feature-complete**: rules, numbers, edge cases. Verify clarity.
3. **Visual**: art, UI, animation. Verify the look.
4. **Polish**: sound, effects, details. Verify "Engaging".

If the earlier tier hasn't passed, don't do the later one. In milestone terms: make "feel review" its own early milestone; don't bury it inside "full first level".

## 7. Parameterize subjective issues

Opinions like "too floaty / too fast / too crowded / wrong colour" take at least three or four rounds through description and regeneration. A faster way is to let the human tune it:

- Put the relevant values in config and expose them as sliders in a tuning panel (F9 or `?debug=1`), taking effect live.
- The panel has a "Copy current parameters" button that outputs a snippet pasteable straight into the config file.
- The human drags until it feels right and pastes the snippet back; the AI writes it into config as the new defaults. Done in one round.
- For things that can't be tuned live (e.g. a layout choice), offer 2–3 presets at once (A heavier / B current / C lighter) and let the human pick; faster than describing.

## 8. Incremental re-check

From round 2, the review card's "Re-check this round" automatically lists items marked "Fixed, awaiting re-check" from the previous round, and the panel only needs ✓ / ✗ clicks. The human need not replay everything, unless the change has wide impact (then the AI states the risk under "Known shortcomings" or "Verified by AI" and adds regression steps to the test route).

## 9. Circuit breaker

If the same issue fails for 2 consecutive rounds, the direction is wrong and more tweaking only burns tokens:

1. Stop changing things.
2. Write down: what was tried, why it didn't work, the likely root cause.
3. Switch approach (a different implementation idea), or ask the human for a concrete reference (a work, a screenshot, a number).
4. Record the new approach and the dropped ones in DECISIONS.md.

If a milestone still hasn't passed after 4 cumulative rounds, it is probably too big; consider splitting it.

## 10. Capturing taste

- Review card "What's good": distill into preferences in `taste.md` so they don't get lost in later changes.
- When the same kind of feedback appears a second time: propose adding it to `taste.md` or `contracts/` with status "Pending confirmation"; it takes effect once the human confirms.
- The AI must read `taste.md` at the start and check against it before writing code, to avoid repeating old problems.
- On conflicting preferences, the latest human-confirmed one wins; mark the old entry "superseded", don't delete it.

## 11. Metrics

`python docs/dev/tools/check_docs.py --stats` gives: rounds per milestone, verdict and average score per round, first-round pass rate, average rounds to pass, and issue distribution by dimension and severity.

How to read it: if the first-round pass rate is rising and average rounds are falling, the acceptance baseline and feedback mechanism are working; if issues in one dimension keep recurring, turn it into a rule or a tunable parameter. With little data (<5 milestones), look at trends only; don't draw conclusions.

## 12. Anti-patterns

- The AI says "done" in chat and there is no review card.
- Asking the human to open the program and "take a look" with no route and no questions.
- The human mentions one thing, the AI fixes one thing, then immediately asks again.
- The scoring baseline changes every round.
- Marking issues "Low" to make the metrics look good. The human sets severity; the AI only suggests.
- Writing long background in the review card that the human won't have patience to read.
