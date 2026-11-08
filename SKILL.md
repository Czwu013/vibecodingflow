---
name: vibecodingflow
description: Right-sized workflow for AI-built projects (tools, websites, apps, games) where AI writes the code and a human decides direction and signs off. Sizes the task (S/M/L), interviews the human to pin scope into DESIGN, plans small checkable tasks, builds with self-tests, then a fast click-to-score human review. Also adopts half-built projects and routes bounded tasks to subagents. Not for one-off small fixes. 触发词：新项目开工、接手项目、里程碑验收、试玩反馈、打分、返工太多、省token、分派子任务、docs/dev。
---

# vibecodingflow: 90% to the AI, the last 10% to human judgement

Lets the AI in every new conversation know, without asking the human, which rules to follow, where things stand and what is still owed; keeps the verdict on "is it good?" with the human, while compressing the human's judgement into a few minutes of clicking.

**Design premise: human attention is the most expensive resource in the whole flow, and the source of rework and token burn.** The vaguer the scope and the feedback, the more the AI guesses and the more round trips. So the kit does three things:

1. Pin the scope down up front: the AI interviews the human (with recommended answers) instead of the human filling blank forms.
2. Never make the human do what a machine can: the AI self-tests before delivery; the human judges only feel, look and trade-offs.
3. Make the judgement the human must give fast and precise: a shared scoring yardstick, structured feedback the machine can parse directly.

## Language

The kit supports `--lang en|zh` (default `en`). The choice is stored in `docs/dev/.lang`, and all scripts accept both languages. When the user writes Chinese, run `init.py` with `--lang zh`. References live in `references/en/` and `references/zh/`; read the one matching the project language. Templates: `assets/templates/<lang>/{core,game,full}`; genres: `assets/genres/<lang>/`; agents: `assets/agents/<lang>/`. Status words, headings and the panel paste-back text appear in the project language (examples below are English).

## Step 0: size the task first

Say in one line which tier you chose. When unsure, start one tier lower.

| Tier | What it is | What to do |
| --- | --- | --- |
| **S** small | One bug, copy or style tweak; ≤3 files; no design trade-off | **Don't run this flow.** Make the change, verify it (run / tests), commit. No `docs/dev`, no milestone, no review card. If the project already has `docs/dev`, run `check_docs.py` at the end and log any new debt |
| **M** feature | A feature in an existing project, or a small tool / app prototype | `init.py` lean set (no `--full`); interview rounds 1-2; one milestone per feature; verifier optional |
| **L** large | New product, cross-module work, several milestones | `init.py --full --agents --hooks`; interview rounds 1-3 and again when planning; verifier and reviewer before every human review |

Upgrade rule: an S task that touches more than 3 files or needs a design trade-off becomes M.

## Pick the scenario

| Scenario | What to do |
| --- | --- |
| A. New M / L project, no `docs/dev` yet | Initialize + interview |
| B. `docs/dev` exists, new session starting work | Read the start-up summary, follow the start-up order, read only what's needed |
| H. A milestone is about to start | Plan it, run the consistency check, build task by task |
| C. A milestone is finished | Deliver for review (the core of this skill) |
| D. Human gave feedback (text copied from the panel, or a verbal gripe) | Handle feedback |
| E. Human complains about rework / wants to see results | `python docs/dev/tools/check_docs.py --stats`; for progress, `--progress` |
| F. Existing half-built project to be continued by AI | Adopt |
| G. A milestone has bounded, machine-verifiable tasks | Delegate to subagents |

## A. Initialize and interview

1. Confirm the project name and type. **Ask for the type once** (`python scripts/init.py --genre list` lists: platformer, roguelite survivor, puzzle, tower defense, idle/incremental, minimal management, top-down action, website/tool); if one is chosen use `--genre`, which writes that genre's acceptance baseline and starting feel parameters into DESIGN. Other games use `--game`; the default is the lean set, and add `--full` only for tier L or if the human explicitly wants the review / performance / roadmap / research / release-notes templates.
2. Run: `python <this skill dir>/scripts/init.py <project dir> --name "<project name>" [--genre <type>] [--full] [--lang en|zh]`. Existing files are never overwritten.
   - For Claude Code users, suggest `--agents` (installs the 4 subagents) and `--hooks` (installs the Stop guard and start-up summary; it writes `.claude/settings.json`, so tell the human first).
   - Scripts, the panel template and detailed docs are copied into the project too, so AI tools without this skill (Codex, Cursor) can use them.
3. **Interview the human; don't fill DESIGN alone.** If a `grill-me` skill is available, use it for the mechanics; otherwise run it yourself: ask in rounds (one round = every question you can ask now), give a recommended answer with each question worded so "yes" accepts it, look facts up yourself (existing code, stack, the genre baseline) instead of asking, and stop only when no branch is open and the human says the shared understanding is reached. The question bank and where each answer lands in DESIGN: `references/<lang>/grill.md`. Write answers into DESIGN as you go (§0 critical questions, §4 MVP in / out, §5 parameters, **§6 acceptance baseline**) and log real trade-offs in DECISIONS. With a genre preset, use its baseline as the recommended answer for §6, then **calibrate it to the human's taste after the first review** and log it in DECISIONS. Anything still assumed goes in §9, marked as an assumption. Without the §6 yardstick, scores are meaningless and the AI doesn't know the target; it is the biggest source of rework.
4. Lay out milestones in `plans/README.md`: put the most rework-prone first (`docs/design/genre_notes.md` has the genre's common rework points); each milestone's experience should take no more than 10 minutes.

## B. Start-up order

With the hook installed, a status summary of ≤15 lines (including task progress) appears automatically at the start of a new session; otherwise run `check_docs.py --brief`. Then read `docs/dev/README.md` → `CURRENT_STATE.md` → `plans/README.md` → `contracts/` (including `taste.md`). If there is an unfinished review card or "Open" feedback, read the latest card first. Don't read through `archive/ research/ references/ audits/` or past review cards.

## H. Plan and build a milestone

1. **Write `plans/Mx_*.md`** from the template: goal, the most rework-prone point, approach, and the **task table**. Cut tasks by complete operation chains (input → validate → save → show → still there after reload), not by layer or page, so something runnable exists after the first task. Every task needs a file scope, a **check that decides pass or fail** (command, assertion or screenshot) and a route.
2. **Consistency check before building.** Compare DESIGN and the plan: every MVP "in" item and every acceptance-baseline dimension has a task; no task builds an "out" item; every task has a check; delegable tasks pass the four questions (see G). Fix gaps and tell the human about anything that changes scope. Then run `check_docs.py` (it catches a missing plan file, tasks without a check, and a milestone put in review with unfinished tasks).
3. **Task loop, one task at a time.** Read only the files in the task's scope. If the task can be tested, write the failing test first, then implement; never edit a test to make it pass. Run the checks that apply (tests, typecheck, lint, build). For UI, open the page, operate it, and look at the screenshot and console. Fill the task's Result (First pass / Retry Nx) and make one small commit. **If the same check fails twice, stop guessing**: report the symptom and your hypothesis, then escalate or change approach (see G); don't try a third time in place. After a task, suggest `/clear` or a fresh session: state lives in the files, not in the conversation.
4. **Progress** at any time: `python docs/dev/tools/check_docs.py --progress` (also in the start-up summary). A task Result means "AI self-tested"; a milestone is "Done" only with the human's signature.
5. When every task has a result, go to C.

## C. Deliver for review

1. **Self-test first.** It runs, no errors, smoke test of key paths, screenshots of key states; script what can be scripted. Tier L: hand it to `dk-verifier` on a cold context (see G); tier M: optional. Then tick DESIGN §4's done criteria against the evidence and list unmet items under "Known shortcomings". Tier L: before the human sees it, `dk-reviewer` audits spec compliance and risk. Write the results into "Self-test results" in `plans/Mx_*.md`, stating what was not verified.
2. `python docs/dev/tools/new_review.py Mx` generates the review card (rounds auto-increment; from round 2 it automatically brings in feedback awaiting re-check).
3. Fill the card's **AI part**. Write what the human needs to know, not how hard you worked:
   - How to run: one command / one double-click; an entry that jumps straight to the scene.
   - 3-minute test route: ≤7 steps, "do what → expect to see what", **starting from the most likely rework point** (genre presets have sample routes).
   - Verified by AI: tell the human what needs no retesting.
   - Key questions for you: turn subjective trade-offs into explicit questions with the current value, so the human can answer "OK / not OK".
   - Known shortcomings: don't let the human spend time on these.
4. `python docs/dev/tools/build_panel.py docs/dev/reviews/Mx_rN.md` builds the click-to-score panel; hand the html path to the human.
5. Set the milestone status to "In review" and tell the human one sentence: open the panel, it takes a few minutes. **Never mark it "Done" yourself.**

Writing details and good/bad examples are in `references/<lang>/human-loop.md`.

## D. Handle feedback

The human's panel text looks like this (it may also be a verbal gripe; handle both):

```
[Review M1 round 1] Reviewer: Sam  Date: 2026-10-31
Scores: Usable 4  Looks 3  Feel 2  Clarity 4  Engaging 3
Reasons: Feel = the jump is floaty
Key questions: Q1 No (wants it snappier)
Issues:
1. [Feel][High] the jump landing is floaty | wants it crisp
Good: loves the colour palette
Verdict: Rework (matches suggestion)
```

1. **Write back to the card's "Human part"**: score table, issue lines, what's good, verdict, reviewer, date. Follow the suggested-verdict rule; if the human overrides, record theirs plus the override reason. Check with `check_docs.py --suggest <card>`. If the feedback is verbal and unsigned, **don't invent a reviewer and date for the human**; ask. This step is pure transcription and can go to `dk-scribe`.
2. **Turn each issue into one `feedback_log.md` entry** (source `M1·r1`, status "Open").
3. **Branch by verdict:**
   - Pass: mark the milestone "Done" (the human has signed), update `CURRENT_STATE.md`; propose "What's good" for `taste.md` (status pending confirmation).
   - Pass with tweaks: fix as one batch, set the feedback to "Fixed, awaiting re-check", generate the next round's card. The human re-checks only the changed items.
   - Rework: back to "In progress", likewise merged into one batch.
4. **Fix in one batch; don't read and fix as you go.** Read all feedback first, merge by root cause, then act. For subjective opinions, restate your understanding in ≤3 lines first; turn what can be a parameter into a tunable parameter (see `contracts/feedback_friendly.md`), since dragging a slider is faster than describing. When you must ask, combine the questions into one. **Interpreting subjective feedback must be done by the main session; don't delegate it.**
5. **Circuit breaker.** If the same issue fails 2 consecutive rounds, stop tweaking: change approach, log it in `DECISIONS.md`, and if needed ask the human for a concrete reference (a work, a screenshot, a number), or hand to `dk-reviewer` for root-cause analysis. `check_docs.py` warns after 2 consecutive reworks.
6. **Capture taste.** When the same kind of feedback appears a second time, the rule hasn't been captured: propose adding it to `contracts/taste.md`; it takes effect once the human confirms. Unconfirmed items aren't enforced as rules.

## F. Adopt an existing project

Goal: bring an existing project into this flow, **without inventing design intent**, and let the human confirm the AI's understanding.

1. Run `init.py <project dir> [--genre <type>]` (doesn't overwrite existing files), then run `python docs/dev/tools/adopt.py <project dir>` to get the **fact list**: engine and version, structure, existing docs, a reviewability check, a debt draft.
2. Read only entry files, config files and the core large files the list flags; don't read everything.
3. Write `CURRENT_STATE.md` (≤100 lines); in `DESIGN.md` write only what can be established from the README and code, **marking inferences "(inferred, to be confirmed)"**; organize the debt draft into `DEVELOP_DEBT.md`; log README/code disagreements in `known_mismatches.md`; record historical decisions only with evidence, marked "(retroactive)".
4. In `plans/README.md` create **M0 "Adoption baseline"** with status "In review", and generate a review card. Under "Key questions for you" write: is CURRENT_STATE's description accurate? Are the inferences about design intent right?
5. Adoption is complete only when the human signs the M0 review card. After that, follow H / C / D as with a new project.

## G. Delegate to subagents (Claude Code)

Use only in Claude Code, and only if `.claude/agents/dk-*.md` exists. Full rules are in `references/<lang>/delegation.md`; the essentials:

1. In the plan file's "Task breakdown" table, mark each task with a **route**: main / sonnet / haiku / opus.
2. Delegate only if all **four questions** are "yes": goal stated in one sentence? bounded scope (file scope listable)? machine-verifiable? free of subjective judgement and architecture? Any "no" keeps it in the main session. Tasks routed to subagents must fill in "File scope" and "Machine check"; `check_docs.py` checks this.
3. Use the Agent tool with `subagent_type` set to `dk-implementer` (sonnet, implementation) / `dk-verifier` (sonnet, independent verification) / `dk-scribe` (haiku, transcription) / `dk-reviewer` (opus, review). Pass the `model` parameter to swap models temporarily. The task card must be self-contained; the format is in delegation.md.
4. Spot-check subagent reports; for high-risk tasks re-run the check command.
5. Record the "Result" in the table: First pass / Retry 1x / Retry 2x / Escalated. **After 2 failures, escalate** (one model level up, or the main session takes over); don't retry a third time in place.
6. Don't run tasks with overlapping file scope in parallel.
7. **Status, sign-off, interpreting subjective feedback and changing approach after the circuit breaker always belong to the main session and the human; never delegate them.**
8. The routing table is only a starting point. `check_docs.py --stats` reports first-pass rate per route, so the project's own data calibrates "who should do what".

## Hooks (after installing with `--hooks`)

- **SessionStart**: injects the status summary into a new session, saving a pile of file reads.
- **Stop**: blocks wrap-up when the docs check has an ERROR. When blocked, **don't bypass it**; if the item needs a human decision (e.g. review sign-off), set the milestone back to "In review" or "In progress" and tell the human what they need to do. The same set of errors blocks at most 2 times, then lets through, to avoid deadlock.
- **git pre-commit**: the same check; `git commit --no-verify` skips it.

## Iron rules (and why)

1. **Write intent and reality separately.** The design doc says only what is meant to be built, `CURRENT_STATE.md` says only what exists now, and mismatches go into `known_mismatches.md`. The most common mistake of an AI in a new conversation is treating the design as the current state.
2. **The AI cannot declare itself done.** Status goes to "In review" at most. Only `Verdict: Pass` in the review card with a reviewer and date counts as done; `check_docs.py` and the hook block violations. AI is naturally optimistic about its own work.
3. **Don't make the human do what a machine can.** The human's few minutes go to feel and trade-offs, not to discovering blank screens and errors.
4. **Leave reasons for major decisions; when overturning, write a new entry, don't delete the old one.**
5. **If you run out of time, log the debt.** Debt must state "payoff criteria". A stale doc that isn't logged is more dangerous than no doc.
6. **One entry point for all docs.** A stale doc is either updated or moved into `archive/`.
7. **One thing at a time.** One milestone → self-test → human review → archive.
8. **Right-size the process.** Small changes skip the flow entirely; the ceremony must be cheaper than the rework it prevents.

## Token-saving practices

- Size the task first: tier S uses no docs at all.
- Start from the summary and read only 4-5 files; `CURRENT_STATE.md` ≤100 lines, `AGENTS.md` ≤40 lines (scripts check this).
- One task, one context: `/clear` after each task and let the files carry the state; use `--brief` / `--progress` instead of re-reading plans.
- One batch of fixes per feedback round; re-check only the changed items, don't rerun everything.
- Use the tuning panel instead of the "too floaty → change → look again → still floaty" loop.
- Delegate bounded tasks so the main session receives only a report; but don't delegate tiny tasks, since cold-start overhead exceeds the task.
- After two failures or the circuit breaker, change approach; don't keep spending tokens in the wrong direction.
- When updating docs, change the relevant lines; don't rewrite the whole file.

## Scripts (all in `scripts/`, pure Python standard library; after init also in the project's `docs/dev/tools/`)

| Script | What it does |
| --- | --- |
| `init.py` | Lays out the skeleton; `--genre` genre preset; `--agents` subagents; `--hooks` hooks; `--lang en` or `--lang zh` project language; generates `CLAUDE.md` (a single line `@AGENTS.md`) |
| `new_review.py Mx` | Generates the next round's review card |
| `build_panel.py <card>` | Generates the click-to-score review web page |
| `check_docs.py [--brief] [--progress] [--stats] [--strict]` | Checks the rules (including plan / status consistency); `--brief` summary; `--progress` per-milestone task progress bars; `--stats` first-round pass rate, average rounds, delegation stats; `--suggest <card>` computes the suggested verdict |
| `adopt.py [dir]` | Scans an existing project, outputs a fact list |
| `dk_hook.py start|stop` | Claude Code hook entry point |

## When to read the reference docs

- `references/<lang>/grill.md`: the kick-off interview: question bank by round, where each answer lands in DESIGN, tool / website and game extras, closing check.
- `references/<lang>/human-loop.md`: designing or adjusting the review flow, writing review cards, scoring and verdict rules, panel text format, tiered review, tuning panel, metrics.
- `references/<lang>/delegation.md`: routing criteria, task cards, escalation ladder, calibration.
- `references/<lang>/game-layer.md`: game projects (greybox first, feel parameters, determinism, playtest method, minimal F8/F9 implementation).
- `references/<lang>/guide.md`: the full human-facing explanation and rationale; read it when you need to explain this method to the user.
- `assets/genres/<lang>/*.md`: full text of each genre preset (acceptance baseline, parameter starting points, common rework points, sample test route).
