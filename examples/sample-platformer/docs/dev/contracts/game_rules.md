<!-- Purpose: extra hard rules for game projects (on top of code_rules.md and feedback_friendly.md).
     Each rule has a reason: when one is violated the AI knows where the boundary is, and can generalize to cases not covered. -->
# Game rules

1. **Determinism.** All randomness goes through a seeded random number generator; the same seed gives the same result.
   *Reason: to reproduce bugs; and only then are before/after comparisons of tuning fair.*
2. **Logic independent of frame rate.** Advance with a fixed time step or by delta time; never depend on the machine's frame rate.
   *Reason: feel is tuned, and when the frame rate changes the feel changes, which invalidates the human's feedback.*
3. **All feel parameters go into config, with ranges.** Speed, acceleration, gravity, jump, cooldown, damage and animation duration are all in config and appear in the F9 tuning panel.
   *Reason: "too floaty" should be solved by dragging a slider, not by describing it and editing code back and forth.*
4. **Greybox first, art later.** Until the core loop and feel pass review, no art, sound or effects.
   *Reason: once those three exist, the cost of overturning the gameplay multiplies.*
5. **Saves carry a version number.** Changing the save structure requires a migration, or explicitly dropping old saves and recording it in DECISIONS.
   *Reason: players' (and your own) old saves shouldn't quietly break after an update.*
6. **A debug entry that jumps straight to a level.** `?scene=xxx&seed=xxx` or a shortcut, going directly to the scene under review.
7. **Performance budget.** Target frame rate {{60}} FPS; when below budget, record measurements in `bench/` first, then optimize.
8. **Asset registration.** Register the source and license of every asset (including AI-generated ones) in `ledgers/assets_ledger.md`.
   *Reason: needed for store-listing review and copyright checks.*
