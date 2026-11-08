<!-- Purpose: build requirements that make human feedback fast and precise. This is the key to cutting rework and token use.
     Every item saves the human typing and saves the AI follow-up questions. Trim to the project type (a command-line tool can skip the tuning panel). -->
# Feedback-friendliness rules

Goal: after trying it, the human can state a problem in as few words as possible; once the AI has the feedback, it can reproduce and fix it without follow-up questions.

1. **One-click copy of debug info.** The F8 shortcut (or a button in a corner of the UI) copies the following to the clipboard: version / milestone number, random seed, current scene and a summary of key state, the last 20 events, console errors.
   *Reason: it's hard for a human to fully describe "what I did"; with one copy the AI has the conditions to reproduce.*
2. **Subjective feel parameters can be tuned live.** Speed, acceleration, gravity, jump, cooldown, animation duration, easing, colour, spacing... go into a tuning panel (F9 or `?debug=1`), take effect in real time as they are dragged, and have a "Copy current parameters" button that outputs a snippet ready to paste into the config file.
   *Reason: "too floaty" or "too fast" takes five or six rounds of talking; the human drags until it feels right, pastes the numbers back, and the round is over.*
3. **One-click jump to the state under review.** Use URL parameters or a shortcut to go straight to the scene under review (`?scene=boss&seed=123`), so the human doesn't replay from the start each time.
   *Reason: review time goes into experiencing the target, not repeating the opening.*
4. **Repeatable starting point.** All randomness goes through a seeded random number generator; the same seed gives the same result.
5. **Visible version.** Show the version / milestone number in a corner of the UI so feedback can be matched to the right build.
6. **One-click reset.** Clear saves and state and return to a clean starting point.

The review card's "How to run" must say how to use these entry points.
