# Delegation Layer: Give the Right Task to the Right Model

Contents: 1 Why delegate · 2 Routing criteria · 3 Task card · 4 Parallelism · 5 Escalation ladder · 6 Recording and calibration · 7 Anti-patterns · 8 Platform notes

## 1. Why delegate, and when not to

Delegation has two benefits: it keeps long execution traces out of the main session (the main session only gets a report, saving context), and it lets cheaper models do what they are good at (saving cost).

The price is that every subagent cold-starts and must re-read project context. If the task is too small, the cold-start overhead exceeds the task itself, and doing it directly is cheaper. So more delegation isn't better; only delegate work that is "clearly bounded and machine-verifiable".

## 2. Routing criteria

**Pass the four questions first.** To hand a task to a subagent, all four answers must be "yes":

1. Can the goal be stated in one sentence, without design trade-offs first?
2. Is the scope bounded: can you list the file scope, usually no more than three files?
3. Is it machine-verifiable: is there a command, assertion or screenshot comparison that decides pass or fail?
4. Does it avoid subjective judgement, cross-module architecture and save-file migration?

If any answer is "no", keep it in the main session.

**Routing table (a starting point; calibrate with your own data, see section 6):**

| Route | Suitable tasks | Subagent |
| --- | --- | --- |
| main | Ambiguous requirements; interpreting subjective feedback; merging feedback into root causes; architecture and cross-module changes; writing "Key questions for you"; DECISIONS; changing approach after the circuit breaker; the first task of a new milestone (it sets the code patterns) | the main session itself |
| sonnet | Clearly bounded implementation: write one feature, one module, or one fix with tests per the task card; write smoke scripts and screenshots; independent verification | `dk-implementer`, `dk-verifier` |
| haiku | Purely mechanical transfer: write panel text back into the review card, transcribe feedback_log, update index dates, fill config with numbers the human gave, format conversion | `dk-scribe` |
| opus | Independent review: root-cause analysis after two failed rounds; high-risk changes such as save-file migration; audit before a milestone delivery | `dk-reviewer` |

**Why subjective feedback must stay in the main session:** when a human says "a bit floaty", translating that into a concrete change requires understanding the acceptance baseline in DESIGN and checking `taste.md` and earlier rounds of feedback. It is the step needing the most judgement in the whole flow, and delegating it only amplifies misunderstanding.

## 3. Task card

The brief handed to a subagent must be self-contained, because the subagent knows nothing:

```
Task: <one-sentence goal>
Plan: task T2 in docs/dev/plans/Mx_xxx.md
File scope: src/player.js, src/config.js
Must read: AGENTS.md; contracts/code_rules.md; T-001 in taste.md
Machine check: npm test -- player (all pass), and screenshot evidence/M1/player.png
Do not: touch files outside scope; change docs or milestone status
Report: use the dk-implementer report format
```

The task card's content comes from the plan file's task table. Each row of the table is the skeleton of one task card.

## 4. Parallelism

- Tasks with non-overlapping file scopes can run in parallel, at most three at a time. If they overlap, run serially. `check_docs.py` warns about overlapping unfinished delegated tasks.
- Parallel subagents share one working directory. When there is conflict risk, run each subagent in its own git worktree (the Agent tool supports `isolation: "worktree"`) and have the main session merge afterwards.
- A verifier works well in parallel with the implementer's next task: while the implementer does T3, the verifier checks T2.

## 5. Escalation ladder

| Situation | Action |
| --- | --- |
| Subagent reports "pass" | Main session spot-checks key claims: for high-risk tasks re-run the check command; otherwise trust the report |
| First attempt fails | Add the missing information to the task card and re-dispatch. Record `Retry 1x` in the plan table's Result column |
| Second attempt fails | Escalate one level: swap sonnet for opus, or the main session takes over. Record `Escalated` |
| Main session still fails | Trigger the circuit breaker, hand to `dk-reviewer` for root-cause analysis, change approach |

Why escalate after two failures: a third attempt by the same model on the same task card is no more likely to succeed just for being another try; it more likely means the card is unclear or the task is beyond that tier.

## 6. Recording and calibration

Each row of the plan file's task table has two columns: `Route` (main / sonnet / haiku / opus) and `Result` (First pass / Retry 1x / Retry 2x / Escalated). `check_docs.py --stats` summarizes by route: tasks completed, first-pass rate, average retries, escalation rate.

**How to use the data (rules of thumb, not conclusions):**

- Only look once a route has ≥10 completed tasks; less data is meaningless.
- Sonnet first-pass rate <60%: the task cards may be unclear, or the "four questions" were applied too loosely; tighten the delegation conditions first.
- Sonnet first-pass rate ≥90%: try delegating more tasks, or use haiku for more mechanical work.
- For task types with a high escalation rate, keep them in the main session next time.

There is no official guidance on "which task goes to which model"; this routing table is a starting point. **Deciding from your own project's data beats anyone's intuition.**

## 7. Anti-patterns

- Handing "make the feel a bit better" to a subagent: there is no acceptance check and no boundary.
- Delegating tasks with no "Machine check": you can't know whether it was done right.
- Dispatching ten tiny tasks at once: cold-start overhead outweighs the benefit. Merge them into one bounded task.
- Accepting reports at face value: high-risk tasks must be spot-checked.
- Letting subagents edit docs and status: status belongs to the main session and the human; once a subagent changes it, "AI can't declare itself done" is bypassed.

## 8. Platform notes

- **Claude Code:** subagent definitions live in `.claude/agents/` (`init.py --agents` copies them). Each definition's `model` field sets the default model; the value can be `sonnet`, `opus`, `haiku`, `fable`, a full model ID or `inherit`. At call time the Agent tool's `model` parameter can override temporarily, taking precedence over the definition's `model`. The main session decides when to delegate from the subagent's `description`. Subagent descriptions count toward the startup token budget, so only 4 are shipped and the descriptions are kept short.
- **Subagents don't delegate further:** none of the 4 definitions has Agent in its `tools` allowlist, to avoid nesting.
- **claude.ai:** there is no subagent mechanism; the main session executes the task cards itself. The routing table can still be used to decide "which work deserves extra attention".
- **Codex, Cursor and others:** task cards and task tables are generic; you can manually hand a task card to another session in the tool.
