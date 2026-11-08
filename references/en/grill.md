# Kick-off interview: pin the scope down before building

Contents: 1 How to ask · 2 Where answers land · 3 Round 1: goal and scope · 4 Round 2: flow, data, yardstick · 5 Round 3: pacing and risk · 6 Tool / website extras · 7 Game extras · 8 Closing check · 9 Anti-patterns

## 1. How to ask

The most expensive mistake at kick-off is building before the scope is clear. DESIGN is not a blank form for the human to fill; the AI interviews and the human mostly answers "agree / disagree".

- If a `grill-me` skill is installed, use it for the interview mechanics; otherwise follow the rules below yourself.
- **Ask in rounds.** One round = every question you can ask right now (none depends on an unanswered question). Questions that depend on earlier answers wait for the next round.
- **Give a recommended answer with every question**, worded so that "yes" accepts it.
- **Look facts up; don't ask for them.** Existing code, stack, dependency versions and the genre preset's acceptance baseline are yours to read. Only decisions go to the human.
- **Done when** no branch is left open and the human says the shared understanding is reached. Until then, no plans and no code.
- Scale the depth: tier M asks rounds 1 and 2 only; tier L asks all three, and asks about the technical approach once more when writing the plan.

## 2. Where answers land

Write each answer into its place immediately, don't save them up:

| What you asked | Lands in |
| --- | --- |
| Who it is for, what problem it solves, one-line positioning | DESIGN §2 Overview |
| Core flow / core loop | DESIGN §3 |
| In scope / out of scope, done criteria | DESIGN §4 MVP scope |
| Parameters, tunables | DESIGN §5 |
| What a 4 looks like on each dimension | DESIGN §6 Acceptance baseline |
| Tech choices, milestone order | DESIGN §7 |
| Pre-flight critical questions (rollback, debug info, compliance) | DESIGN §0 |
| Undecided items proceeding on a default | DESIGN §9 Open questions (mark as an assumption) |
| Real trade-offs and what was given up | DECISIONS.md |

## 3. Round 1: goal and scope (every M / L task)

1. **Users and context:** who uses it, and in what situation? (Recommended: serve one kind of user first)
2. **The problem:** what happens if this isn't built? Say it in one sentence.
3. **Behaviours the MVP must have:** 3 to 7, each written as "user does what -> sees what".
4. **Explicitly out of scope:** accounts, collaboration, cloud sync, payments, i18n, admin back-end: confirm each one. (Recommended: exclude everything you can)
5. **Done criteria:** what counts as this round being finished? Write it as a tickable list.

## 4. Round 2: flow, data, yardstick

6. **Core flow:** what does the user do over and over, step by step?
7. **Where data comes from and where it lives:** typed in, imported, an API? Memory, local storage, files, a database? Must it survive a reload?
8. **How demo data is marked:** how can it be told apart from real data at a glance, so they never mix?
9. **Tech choice:** reuse the existing stack; for a new project offer two candidates with reasons. (Recommended: the one the AI can fully read and change, with the fewest dependencies)
10. **Acceptance baseline:** what does a 4 look like on each dimension? With a genre preset, use its baseline as the recommended answer and let the human edit it.
11. **Rollback:** can a bad change be undone in one step? (Recommended: git, one small commit per task)

## 5. Round 3: pacing and risk (tier L always; tier M picks what applies)

12. **Milestone order:** which part is most likely to get "that's wrong"? Put it first. Each milestone should take no more than 10 minutes to experience.
13. **Failure cases:** what happens on invalid input, a network failure, corrupted data?
14. **Which parameters should be tunable live:** don't iterate subjective feel through descriptions.
15. **How it is verified:** what can be tested automatically, and what must a human experience?
16. **Copyright, compliance, privacy:** does data leave the machine? Any asset licensing issues?
17. **Biggest risk:** which part is most likely to be impossible or go wrong? Run a small experiment on it first.

## 6. Tool / website extras (web_app_tool)

- **Context of use:** office, personal, for other people? How long per session?
- **Where input comes from:** paste, upload, typing? Which formats? What happens on invalid input?
- **Who gets the output and how:** glance at it, copy it, export in which format?
- **The three states:** what do loading, empty and error each look like?
- **Devices:** desktop, phone width, both? Must it work offline?
- **Data volume:** a handful of rows or tens of thousands? Pagination, search, filters?
- **Privacy:** does data stay on the machine? Is a login needed? (Recommended: no login and no cloud this round)

## 7. Game extras

- **Core loop in one sentence; how long is one session?**
- **Greybox first to test feel:** which feel parameters exist, and where does the F9 tuning panel live? (See `game-layer.md`)
- **Saves, seed reproduction, determinism:** needed?
- **Go through the genre preset's "common rework points" and confirm which apply.**

## 8. Closing check (confirm each before the branches are empty)

- [ ] Every "must do" has a matching acceptance scenario
- [ ] Every "out of scope" item is explicit and won't be quietly added back
- [ ] Data source, storage and demo-data marking all have an answer
- [ ] Placeholders in DESIGN §6 are replaced (`check_docs.py` blocks a milestone from entering review otherwise)
- [ ] Every assumption is marked as an assumption, in §9
- [ ] The human has said the shared understanding is reached

## 9. Anti-patterns

- Dumping a dozen questions at once: the human loses patience and answers get worse. Go in rounds.
- Asking for facts you can look up: it wastes the human's attention.
- No recommended answer: the human has to think from scratch and answers slowly.
- Writing assumptions into DESIGN as if agreed: the main source of later rework.
- Turning the interview into a debate: when the human says "that's it", record it and move on.
