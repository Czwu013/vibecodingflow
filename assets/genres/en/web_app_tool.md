# Website / tool (web_app_tool)

Applies to: websites, web apps and small tools. Projects like this have no game sense of "feel"; the equivalent is **interaction responsiveness**.

## Acceptance baseline

| Dimension | What a 4 looks like | Reference |
| --- | --- | --- |
| Usable | The main flow works end to end; errors show a message instead of a blank screen; refresh or back doesn't lose data; works in major browsers and at phone width | — |
| Looks | Hierarchy, alignment, whitespace and type sizes are consistent, and it doesn't look stitched together from templates | — |
| Feel | Clicks and typing feel instant; loading has a visible state; animations don't slow down actions (interaction responsiveness) | — |
| Clarity | A new user can complete the main task without instructions; button labels and copy are unambiguous; empty and error states give guidance | — |
| Engaging | Solves a real problem; faster than the old way; users are willing to come back | — |

## Starting feel parameters

Here "feel" means interaction responsiveness, and the parameters are design variables.

| Parameter | Typical starting point | Notes |
| --- | --- | --- |
| Theme color / font size / spacing / corner radius | Managed centrally as a set of design variables | Change one place, applies everywhere |
| Animation duration and easing | 0.15–0.3 seconds | Too long feels slow |
| Input debounce delay | 200–400 milliseconds | For search boxes and the like |
| Page size | Set by scenario, commonly 20–50 | |
| Request timeout and retry | Set per endpoint | Failures must be surfaced to the user |
| Touch target size | No smaller than about 44 pixels | Prevents misses on phones |

## Common rework points

- Layout breaks at phone width
- Missing the three states: loading, empty and error
- Vague copy and button names
- Insufficient color contrast, so text is hard to read
- Poor form validation experience (only tells you what's wrong after submit)
- Slow (large images, render-blocking resources)

## Sample test route

- First open, complete the main task without any instructions → can finish it and knows the next step
- Go offline or enter invalid input → a clear error message appears, no blank screen
- Shrink the window to phone width → layout is fine and buttons are clickable
- Refresh the page → state is kept or there is a clear notice
- After finishing the main task → you know where the result is and how to continue

## One-minute test

A new user should complete one main task within one minute.

## What to check at the greybox stage

Wireframes with real data. Verify the **flow** and **information architecture**; add visual design only after they pass.
