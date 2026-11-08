<!-- Purpose: every issue the human raises during review, and the AI's handling of it. It is the cross-round "open items list".
     A review card records "what happened this round"; this table records "where each issue stands now".
     The AI turns each line under "Issues" in the review card into one entry, with Source written as "M1·r1".
     Date, dimension and severity follow the review card; for Repro, enter a summary of the debug info or the seed. -->
# User feedback log

| ID | Source | Dimension | Severity | Human's words | What they want | Repro | Status | Handling |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FB-001 | {{M1·r1}} | {{Feel}} | {{High}} | {{the jump feels floaty}} | {{landing should be crisp}} | {{seed 123}} | Open | |

Status: Open → Fixed, awaiting re-check → Closed / Won't fix (state the reason).
If the same kind of issue appears a second time, the rule hasn't been captured: propose adding it to `contracts/taste.md`, effective once the human confirms.
