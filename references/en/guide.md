# AI Collaborative Development Docs Framework · User Guide

For projects where "the human sets direction and does acceptance, the AI writes the code" (games, websites and tools all work).
Core idea: **AI can finish 90%; the last 10% is judgement only a human can make. Make that 10% fast and accurate, and rework, bug-fixing and token use all drop.**

In practice that means two things:

1. **The next AI to pick up the project knows what to follow, where things stand and what is still owed, without asking you.**
2. **Your judgement becomes a few minutes of clicking: score, flag issues, one-click copy, directly machine-readable.**

## 1. Seven principles

1. **Write intent and reality separately.** The design doc only says "what we intend to build"; `CURRENT_STATE.md` only says "what the code actually does now". Where they disagree, log it in `known_mismatches.md`.
2. **Leave reasons for major decisions.** Write one entry per decision in `DECISIONS.md`: what changed, why, what was dropped. When overturning an old decision, write a new entry; don't delete the old one.
3. **If you run out of time, log the debt.** When there's no time to update docs or fix an issue, first note it in `DEVELOP_DEBT.md` with "what counts as paid off". A stale doc that isn't logged is more dangerous than no doc.
4. **One entry point for all docs.** `docs/dev/README.md` lists each doc's purpose, last update and status (Current / Stale / Archived). Stale docs are either updated or moved into `archive/`.
5. **The AI cannot declare itself done.** Status flow: To do → In progress → In review → Done. The AI can mark at most "In review", with self-test evidence attached; only when the human signs the review card with the verdict "Pass" is it "Done". Scripts check this.
6. **Don't make the human do what a machine can.** Runs, no errors, smoke test of key paths: the AI checks these before delivery. The human's time goes only to feel, look and trade-offs.
7. **Make the human's judgement cheap and accurate.** A shared scoring yardstick, a fixed feedback format, and subjective opinions turned into draggable parameters wherever possible.

## 2. What each document is for

| Document | Question it answers | Who writes | When updated | In the lean set |
| --- | --- | --- | --- | --- |
| `README.md` (root) | What is this project? How to run it? How to review it? | AI | When the way to run changes | ✓ |
| `AGENTS.md` / `CLAUDE.md` | What should the AI read first on opening the project? | Human decides, AI maintains | Rarely changes | ✓ |
| `docs/design/DESIGN.md` | What do we intend to build? **What does a 4 look like?** (GDD / product requirements) | Human + AI discussion | When design changes; change this first, then the code | ✓ |
| `docs/dev/README.md` | Index of all docs, status flow, AI start-up order | AI | Whenever any doc changes | ✓ |
| `docs/dev/CURRENT_STATE.md` | What the code can actually do now, where the key implementation is (≤100 lines) | AI | At the end of each milestone | ✓ |
| `docs/dev/DECISIONS.md` | Why is it like this? What was dropped at the time? | AI records, human confirms | Every major decision | ✓ |
| `docs/dev/DEVELOP_DEBT.md` | What is still unresolved? What counts as resolved? | AI | When debt is found, when paid off | ✓ |
| `docs/dev/known_mismatches.md` | Where do code and design disagree? Which side wins? | AI | When a deviation is found | ✓ |
| `docs/dev/feedback_log.md` | Where is each issue you raised now? | AI, from review cards | After each review round | ✓ |
| `docs/dev/contracts/` | Rules code must follow, feedback-friendliness requirements, your taste profile | Human decides, AI adds | When a new rule is set | ✓ |
| `docs/dev/plans/` | Per milestone: what, how, what the self-test verified (with screenshot evidence) | AI | Every milestone | ✓ |
| `docs/dev/reviews/` | **Review cards**: AI's delivery notes + your scores and verdict + review panel | AI writes the first half, human fills the second | Every review round | ✓ |
| `docs/dev/archive/` | Retired docs (not deleted, kept on file) | AI | When a doc goes stale | ✓ (may be empty) |
| `docs/dev/audits/` | Code review records | AI or a second AI | Periodically or after big changes | Create when needed |
| `docs/dev/ledgers/` | Itemized ledgers of assets, content, copy (source, licence) | AI | When assets start being added | Games / create when needed |
| `docs/dev/references/` | External material, technical doc summaries | AI | When researching | Create when needed |
| `docs/dev/roadmaps/` | What goals each version aims to complete | Human + AI | When planning a new version | Create when needed |
| `docs/dev/bench/` | Performance test plans, measured data | AI | When stutter appears | Create when needed |
| `docs/research/` | Competitor, benchmark, mechanic research | AI | Project start and design phase | Create when needed |
| `docs/release_notes/` | What each release changed (for users) | AI drafts, human confirms | Every release | Create at first release |

**Lean set** (for a project just starting): create only the rows marked ✓. Create the rest when they have real content; empty folders make the AI think there is something to maintain.

> Changes from the original version: the former `checklists/` (acceptance checklists) became `reviews/` (review cards), upgrading the "flow / visual / feel" ticking into five-dimension scoring, structured issues and a clickable panel; `feedback_log` gained dimension and severity; new `contracts/feedback_friendly.md` and `contracts/taste.md`.

## 3. One full development loop

1. **Start:** the AI reads `AGENTS.md` → `docs/dev/README.md` → `CURRENT_STATE.md` → `plans/README.md` → `contracts/`.
2. **Pay high-priority debt first:** check `DEVELOP_DEBT.md` and the "High" items in `feedback_log.md`.
3. **Do one milestone only:** write the plan in `plans/` → write code → **self-test** (run, screenshots, smoke test, check errors) → put evidence in `plans/evidence/`.
4. **Deliver for review:** `new_review.py` generates the review card; the AI fills in the test route, verified items and key questions; `build_panel.py` generates the clickable panel; status becomes "In review".
5. **Human review (a few minutes):** open the panel, follow the route, score, flag issues, click "Copy for AI", paste back into the chat.
6. **AI handles feedback:** write back to the review card, issues go to `feedback_log`, then branch by verdict:
   - **Pass** → you have signed; mark "Done", commit to git as an archive;
   - **Pass with tweaks** → fix as one batch; next round you only re-check the changed items;
   - **Rework** → back to "In progress", fix as one batch; after two consecutive reworks, change approach.
7. **Wrap up:** update `CURRENT_STATE.md`, `plans/`, `DECISIONS.md` (if any), the index table; run `check_docs.py`.

## 4. Critical questions to ask at project start (put at the top of the design doc)

1. Is what we're about to build inside the minimum viable version?
2. Can the AI fully read and change this project? (Is the tech stack entirely in code, with no dependence on graphical editors the AI can't operate?)
3. If it breaks, can we roll back in one step? (git or folder backup)
4. Did this change touch only one thing?
5. When a bug is reported, is there enough information to locate it? (Can the program copy debug info in one click?)
6. Does the AI in a new conversation know the rules set earlier? (→ this framework)
7. Can the human tune the subjective feel / look parameters live?
8. Do the theme and new features really change users' decisions, or just reskin?
9. Are there copyright, compliance or store-listing risks?

## 5. How to use

1. Run `python scripts/init.py <project dir> --name "<project name>" [--game] [--full] [--lang en|zh]`, or simply ask Claude with this skill installed to initialize for you.
2. Search globally for `{{` and replace the placeholders with your project's content; write DESIGN section 6, "Acceptance baseline", with real care.
3. When starting work with an AI tool, tell it: "Read AGENTS.md first".
4. The design doc can also live online (online docs are easy to edit and comment on); in that case replace `docs/design/DESIGN.md` with a one-line link, and **don't keep two copies**.
5. For daily checks use `python docs/dev/tools/check_docs.py`; use `--stats` to see rework trends.

## 6. Advanced capabilities

1. **Genre acceptance-baseline presets.** `init.py --genre platformer` and the like bring "what a 4 looks like for this kind of game", starting feel parameters, common rework points and a sample test route straight into the project. You don't invent the yardstick from scratch; calibrate it to your taste after the first review.
2. **Delegation to subagents (Claude Code).** Tasks that are clearly bounded and machine-verifiable go to Sonnet / Haiku subagents; interpreting your subjective feedback, status and sign-off always stay with the main session and you. Routes are written in the plan's task table, and the stats show "which kind of task is most worthwhile to hand to whom". See `delegation.md`.
3. **Enforcement.** `init.py --hooks` stops "AI can't declare itself done" from relying on AI discipline: an ERROR at wrap-up blocks it, and so does a commit; a new session automatically sees a status summary.
4. **Adopting an existing project.** `adopt.py` scans the facts, the AI writes CURRENT_STATE and a debt draft, all inferences are marked "to be confirmed", and you confirm by signing the M0 review card.
