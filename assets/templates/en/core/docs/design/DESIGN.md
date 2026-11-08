<!-- Purpose: write only "what we intend to build" (a GDD for games, a PRD for products). Do not write the current state of the code.
     If the design changes, change this first, then the code. Section 6 "Acceptance baseline" matters most: it tells the AI the target and gives the human's scores a common ruler. -->
# {{Project name}} Design Doc

{{Date}} · {{Author}}

## 0. Critical questions before starting

| # | Question | This project's answer |
| --- | --- | --- |
| 1 | Is what we're about to build inside the minimum viable version? | {{}} |
| 2 | Can the AI fully read and modify this project? | {{Tech choices}} |
| 3 | If something breaks, can we roll back in one step? | {{git / backup method}} |
| 4 | Does this change only one thing? | One milestone → self-test → human review → archive |
| 5 | Is there enough information when reporting a bug? | One-click copy of debug info in the program (see contracts/feedback_friendly.md) |
| 6 | Does the AI in a new conversation know the rules? | Reads AGENTS.md and docs/dev |
| 7 | Can subjective feel / look parameters be tuned live by the human? | {{Tuning panel / config file}} |
| 8 | Does the new feature really change user decisions? | Answer this question for every addition |
| 9 | Copyright, compliance, and store-listing risks? | {{}} |

## 1. References and benchmarks
{{Similar products and what each is worth borrowing (put detailed research in docs/research/)}}

## 2. Overview
{{One-sentence positioning · core experience · target users · platform}}

## 3. Core loop / core flow
{{The thing users do over and over; spell out the rules one by one}}

## 4. Minimum viable version (MVP) scope
| In | Out (postponed) |
| --- | --- |
| {{}} | {{}} |

**Definition of done:**
- [ ] {{}}

## 5. Entities and tunable parameters
{{Main objects and their attributes; parameter table: name · initial value · range · notes}}

## 6. Acceptance baseline (how a human scores)

Review cards score five dimensions from 1 to 5. Write down here what a **4 (satisfied) looks like for this project**, ideally pointing at a reference. The AI aims for it, the human uses it as the ruler, and it reduces "it's finished but isn't what I wanted".

| Dimension | What a 4 looks like here | Reference |
| --- | --- | --- |
| Usable | The flow works end to end, no crashes, no lag | — |
| Looks | {{}} | {{}} |
| Feel | {{}} | {{}} |
| Clarity | {{You know what to do at a glance and the information is readable}} | {{}} |
| Engaging | {{What makes people want to keep using / playing}} | {{}} |

## 7. Technical approach and milestones
{{Tech choices · file structure · milestones M0…Mn. After each milestone it should be usable and show visible change, and a human should be able to try it in under 10 minutes.
  Ordering principle: review the point most likely to need rework first (check feel before adding art).}}

## 8. Roadmap (after the MVP)
| Order | System | Content | New decision for the user |
| --- | --- | --- | --- |

## 9. Open questions
- [ ] {{Question}} (default approach: {{}})
