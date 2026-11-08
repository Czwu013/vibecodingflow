<!-- Purpose: the approach, implementation and self-test results of a single milestone. Copy this file and name it Mx_name.md.
     Put evidence such as screenshots in plans/evidence/Mx/. -->
# {{Mx Name}}

Status: {{To do / In progress / In review / Done}} ({{Date}})

## Goal
{{What the user can see / do once this is done}}

## Most likely rework point
{{In this milestone, what is most likely to make the human say "that's not right"? (feel? layout? pacing?) The review card's "Key questions for you" come from here,
  and this point should be reviewed first, before any later polish.}}

## Approach
{{How it will be done; which files are involved; any trade-offs (put major ones in DECISIONS)}}

## Task breakdown
<!-- Each row is the skeleton of one task card. Route: main / sonnet / haiku / opus (rules in references/delegation.md).
     For tasks routed to sonnet / haiku / opus, "File scope" and "Machine check" are required (check_docs.py checks this).
     Result: First pass / Retry 1x / Retry 2x / Escalated; leave blank if unfinished. -->
| # | Task | File scope | Machine check | Route | Result |
| --- | --- | --- | --- | --- | --- |
| T1 | {{One-sentence goal}} | {{src/player.js}} | {{npm test -- player all pass}} | {{main / sonnet / haiku}} | |

## What was done
| File | What was done |
| --- | --- |

## Self-test results (by AI)
| Check | Result | Evidence |
| --- | --- | --- |
| {{Runs, no console errors}} | Pass / Fail | `evidence/{{Mx}}/{{file}}` |

**Not verified:** {{e.g. real-device fonts, different browsers — put these in the review card so the human knows they weren't tested}}

## Review
See `../reviews/{{Mx}}_r1.md` (later rounds are r2, r3, ...)
