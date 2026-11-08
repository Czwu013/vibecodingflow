<!-- Purpose: game design document (GDD). Write only "what we intend to build", not the current state of the code. If the design changes, change this first, then the code.
     Game-version focus: section 3 core loop, section 5 feel parameter table, section 6 acceptance baseline — they decide how many rounds of rework follow. -->
# Sample Platformer Design Doc

2026-10-31 · {{Author}}

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

| Parameter | Typical starting point | Notes |
| --- | --- | --- |
| Max move speed | Set by level scale | Fix this first; other parameters are built around it |
| Acceleration / braking time | 0.05–0.2 seconds | Too long feels slippery, too short feels stiff |
| Jump height | About 2–4 character heights | Determines platform spacing |
| Short-hop cut factor | 0.4–0.6 | Reduction of upward velocity when the jump key is released |
| Fall gravity multiplier | 1.3–2.0x | Above 1 makes falling crisper and eases the "floaty" feel |
| Coyote time | 0.05–0.15 seconds | Grace period to still jump after leaving a platform edge |
| Jump buffer | 0.08–0.15 seconds | Press jump just before landing and the jump fires on landing |
| Max fall speed | Set by level | Prevents falling so fast the player passes through the floor |
| Air control factor | 0.6–1.0 | Ability to steer in the air |

> Starting values from genre preset "Platformer (platformer)". Feel wins: drag them in the tuning panel.

## 6. Acceptance baseline (how playtests are scored)

Playtest cards score five dimensions from 1 to 5. Write down what a **4 (satisfied) looks like for this game**, ideally pointing at one specific moment of a reference title.

| Dimension | What a 4 looks like | Reference |
| --- | --- | --- |
| Usable | Can be played from start to finish without crashing; collision is stable, with no wall-sticking or falling through the floor; respawn after death is reliable | — |
| Looks | The character, standable platforms and hazards can be told apart within 1 second; the silhouettes at takeoff and landing are readable | e.g. Celeste's visual readability |
| Feel | No perceptible delay from key press to takeoff; jump height is controllable (tap low, hold high); landings are crisp, not floaty; coyote time and jump buffering exist, so a mistake feels like "I mishit the button" rather than "the game ate my input" | e.g. the controls of Celeste and Super Meat Boy |
| Clarity | It's obvious at a glance where you can stand and where you will die; the player can state the cause of every death | — |
| Engaging | Retry within 1–2 seconds of dying; every death teaches something; the player wants another go | e.g. Super Meat Boy's retry pacing |

> From genre preset "Platformer (platformer)" — a starting point, not a verdict: calibrate to your taste after the first review and log it in DECISIONS.md.

## 7. Technical approach and milestones
{{Engine · file structure · M0…Mn.
  Ordering: greybox first to check feel and the core loop (M1); only after it passes add art, sound and effects. Each milestone's playtest takes no more than 10 minutes.}}

## 8. Roadmap (after the MVP)
| Order | System | Content | New decision for the player |
| --- | --- | --- | --- |

## 9. Open questions
- [ ] {{Question}} (default approach: {{}})
