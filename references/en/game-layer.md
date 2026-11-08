# Game Layer: Extra Points

A game's "last 10%" is almost entirely feel and fun, which is hardest to describe in words and costliest to rework. So game projects add these constraints on top of the general flow. `init.py --game` brings the matching templates (GDD-style design doc, `contracts/game_rules.md`, asset ledger).

## 1. Engine choice limits how much the AI can do

AI is good at reading and writing text. If the engine's scenes and resources are human-readable text, the AI can change them fully; if they are binary assets or only clickable in an editor, the AI can't reach them, and it is hard to have it reproduce things during review.

- Friendly: Godot (`.gd` / `.tscn` are text), Three.js, Phaser, PixiJS, Pygame, LÖVE, Bevy.
- Harder: Unity and Unreal scenes, prefabs, blueprints, which are binary or editor-only. Usable, but keep logic in C# / C++ code as much as possible.

This is what DESIGN section 0, question 2, answers at project start.

## 2. Greybox first

The first milestone is boxes + text only. Only after it passes review on "Feel" and "Engaging" do you add art, sound and effects. Once those three exist, the cost of overturning the gameplay multiplies.

## 3. Feel parameters

Put every value people might call "too floaty / too fast / too slow / too soft" into config, with units and ranges:

Move speed, acceleration, friction, gravity, jump initial velocity, coyote time, jump buffer, dash distance, attack windup and recovery, hit stop, camera shake, hit invincibility time, animation duration, easing curve.

Make the F9 tuning panel sliders, with "Copy current parameters" outputting a config snippet. The human tunes, pastes it back, and the AI writes it into config.

## 4. Determinism and reproducibility

- All randomness uses a seeded RNG: same seed, same result.
- Logic uses a fixed time step or delta, independent of frame rate.
- Show the version and seed in a corner of the screen.
- Together these mean that when the human says "the monster in level 3 got stuck", the AI can reproduce it from the seed and debug info.

## 5. Minimal implementation

### Web (Three.js / Phaser / Canvas)

```js
// F8: copy debug info
const events = [];                       // at key events: events.push(`${t} ${msg}`), keep the latest 20
window.addEventListener('error', e => events.push('ERR ' + e.message));
window.addEventListener('keydown', e => {
  if (e.key !== 'F8') return;
  e.preventDefault();
  const report = JSON.stringify({
    version: VERSION, milestone: 'M1', seed: game.seed,
    scene: game.scene, state: game.debugState(), events: events.slice(-20),
  }, null, 2);
  navigator.clipboard.writeText(report);
});
// F9: toggle the tuning panel; URL params ?scene=boss&seed=123 jump straight to a scene
const q = new URLSearchParams(location.search);
```

### Godot 4

```gdscript
func _unhandled_input(event):
    if event is InputEventKey and event.pressed and event.keycode == KEY_F8:
        DisplayServer.clipboard_set(JSON.stringify(debug_report()))
```

`debug_report()` returns a dictionary with version, seed, scene, key state and recent events. The tuning panel can be a simple `Control` scene that reads and writes a `config` resource.

## 6. Playtest method

- Have the human actually play, not "take a glance". State the goal to complete in the route.
- Fresh eyes are worth more than familiar ones: confusion on first contact best exposes "Clarity" problems. Consider asking a second person to score only "Clarity" and "Engaging".
- The time from first launch to the first "oh, interesting" is the most honest indicator of the core loop; the "One-minute test" in DESIGN checks exactly that.
- Before a milestone enters polish, have at least 3 playtest records from different people / different times.

## 7. Saves and versions

Saves carry a version number; changing the structure requires a migration, or explicitly dropping old saves and logging it in DECISIONS. Otherwise the human's test progress is silently lost, and later feedback becomes distorted.

## 8. Assets and compliance

Register every asset (including AI-generated) with its source and licence in `ledgers/assets_ledger.md`. Store review (e.g. Steam) asks for disclosure of AI-generated content; the ledger means you no longer scramble to dig it up.
