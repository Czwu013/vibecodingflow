<!-- Purpose: game design document (GDD). Write only "what we intend to build", not the current state of the code. If the design changes, change this first, then the code.
     Game-version focus: section 3 core loop, section 5 feel parameter table, section 6 acceptance baseline — they decide how many rounds of rework follow. -->
# {{Game name}} Design Doc

{{Date}} · {{Author}}

## 0. Critical questions before starting

| # | Question | This project's answer |
| --- | --- | --- |
| 1 | Is what we're about to build inside the minimum playable version? | {{}} |
| 2 | Can the AI fully read and modify this project? (no dependence on graphical editors the AI can't touch) | {{Engine / tech choices}} |
| 3 | If something breaks, can we roll back in one step? | {{git / backup method}} |
| 4 | Does this change only one thing? | One milestone → self-test → human playtest → archive |
| 5 | Is there enough information when reporting a bug? | F8 one-click copy of debug info (including seed) |
| 6 | Does the AI in a new conversation know the rules? | Reads AGENTS.md and docs/dev |
| 7 | Can feel parameters be tuned live by the human? | F9 tuning panel + config file |
| 8 | Does the new system really change player decisions, or is it just a reskin? | Answer this question for every addition |
| 9 | Copyright, compliance, and store-listing risks? | {{Asset sources / licenses, see ledgers/assets_ledger.md}} |

## 1. References and benchmarks
{{Similar games and the specific thing worth borrowing from each (put detailed research in docs/research/)}}

## 2. Overview
{{One-sentence positioning · core experience · target players · platform · session length}}

## 3. Core loop
{{The thing players do over and over: do what → get what feedback → why they want another go. Spell out the rules one by one.}}

**One-minute test:** a new player playing for one minute should experience {{}}.

## 4. Minimum playable version (MVP) scope
| In | Out (postponed) |
| --- | --- |
| {{}} | {{}} |

**Definition of done:**
- [ ] {{}}

## 5. Entities and feel parameters
{{Main objects and their attributes. Feel parameter table: name · initial value · range · unit · notes. All parameters go into the config file and appear in the F9 tuning panel.}}

| Parameter | Initial value | Range | Notes |
| --- | --- | --- | --- |
| {{Move speed}} | {{}} | {{}} | {{}} |

## 6. Acceptance baseline (how playtests are scored)

Playtest cards score five dimensions from 1 to 5. Write down what a **4 (satisfied) looks like for this game**, ideally pointing at one specific moment of a reference title.

| Dimension | What a 4 looks like in this game | Reference |
| --- | --- | --- |
| Usable | Playable from start to finish, no crashes, no lag | — |
| Looks | {{Visual recognizability, clarity of feedback}} | {{}} |
| Feel | {{Input-to-feedback latency, impact, rhythm}} | {{e.g. the jump in some game}} |
| Clarity | {{Players know the goal, dangers and interactables at a glance}} | {{}} |
| Engaging | {{Where the urge to play another round comes from}} | {{}} |

## 7. Technical approach and milestones
{{Engine · file structure · M0…Mn.
  Ordering: greybox first to check feel and the core loop (M1); only after it passes add art, sound and effects. Each milestone's playtest takes no more than 10 minutes.}}

## 8. Roadmap (after the MVP)
| Order | System | Content | New decision for the player |
| --- | --- | --- | --- |

## 9. Open questions
- [ ] {{Question}} (default approach: {{}})
