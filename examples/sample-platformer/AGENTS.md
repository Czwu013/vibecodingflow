<!-- Purpose: the first file AI tools (Claude Code, Codex, Cursor, etc.) read when they open the project. Keep it short; it only points the way.
     Claude Code reads CLAUDE.md; init already generated one whose content is a single line: @AGENTS.md. -->
# Start-up instructions for AI

1. Read `docs/dev/README.md` first and follow its "AI start-up order". Read only those files; do not read through all of docs.
2. Design intent: `docs/design/DESIGN.md`. Actual code state: `docs/dev/CURRENT_STATE.md`. Rules you must follow and the human's preferences: `docs/dev/contracts/`.
3. Work on one milestone at a time. Mark it "In review" at most; **never mark it "Done" yourself**: it counts as done only when the human signs the review card with the verdict "Pass".
4. Before handing over to the human, check whatever a machine can check (it runs, no errors, screenshots, smoke tests). The human's time is only for judging feel, looks and trade-offs.
5. When delivering for review, generate a review card: `python docs/dev/tools/new_review.py Mx`, fill in the AI part, then `python docs/dev/tools/build_panel.py <review card>` to produce the click-through panel for the human.
6. When you receive feedback: batch one round of feedback into one set of changes; don't edit as you read. For subjective opinions, restate your understanding in two or three lines before acting.
7. If the same problem fails two rounds in a row: stop, switch approach, and record it in `DECISIONS.md`; don't keep fine-tuning.
8. If docs can't be updated in time, log it in `docs/dev/DEVELOP_DEBT.md` and state the payoff criteria clearly.
9. Before wrapping up, run `python docs/dev/tools/check_docs.py`; deal with any ERROR first.
10. Genre notes and common rework points: `docs/design/genre_notes.md` (use when writing review cards and test routes).
