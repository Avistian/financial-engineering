---
name: lesson-visuals
description: Decide when a lesson needs a visualization, build or reuse assets/, and verify correctness in the browser before publishing.
---

Use when creating or editing lesson HTML in this workspace.

## Decision tree

1. **Text or a small table is enough** — skip a viz (definitions, bullet lists, short code snippets, a
   moments table).
2. **Spatial, temporal, or mechanistic concept** — add a viz:
   - limit order book: levels, best bid/ask, a market order walking the book
   - option payoff diagrams (call/put hockey-stick, non-linearity)
   - return distributions: histogram vs Gaussian, QQ-plots, fat tails
   - volatility clustering: |returns| over time, autocorrelation decay
   - Brownian / random-walk paths, drift vs diffusion (Q2)
   - temporal splits, purged/embargoed CV, backtest overfitting (Y2 Q2)

## How many visuals per lesson? (one per distinct mechanism)

Default to **one visual per distinct mechanism, claim, or "fact" the lesson teaches** — not one per lesson.
A lesson with three mechanistic beats should have three visuals. The one-viz-per-lesson habit is a cap to
break, not a target.

- **Every mechanistic beat gets its own visual.** If a section makes a spatial/temporal/mechanistic claim
  and the next makes a *different* one, each earns its own viz. A results table where the mechanism is
  visualizable is an under-served beat — add the viz.
- **Split multi-mode widgets when the modes teach different ideas.** One widget with a knob is right when the
  modes are *the same mechanism under a parameter* (e.g. order size slider on one book). It is wrong when each
  "mode" is a *separate concept* the prose treats as its own section.
- **Place each viz next to the prose that explains it.** A viz referenced from two sections is a smell that it
  should have been two viz.
- **Reuse still applies.** Multiple viz in one lesson can each be a separate reusable asset, or several mounts
  of the same parameterised asset — as long as each mechanism is *seen*, not just described.

## Build rules

- **Reuse first:** read `./assets/` before authoring new JS.
- **New reusable component:** add to `./assets/<name>-viz.js`; never inline one-off JS in the lesson. (A tiny
  static diagram — like the CSS-only order book in Lesson 003 — may stay lesson-local, but anything a second
  lesson could reuse becomes an asset.)
- **Document expected states** in a comment at the top of each viz file.
- **Companion CSS:** lesson-local `<style>` with a class prefix matching the viz (e.g. `.lob`, `.payoff`).

## Verification checklist (mandatory before publish)

Open the lesson in a browser (`file://` or a local server). Run this for **every viz and widget in the
lesson**, not just the first:

- [ ] Each viz/widget renders without console errors (all mount IDs resolve)
- [ ] Each viz's default state matches its prose caption
- [ ] Each interactive mode/toggle shows the behaviour described in text
- [ ] Labels (prices, levels, axis units, fold IDs) match lesson terminology and the GLOSSARY
- [ ] Mobile viewport: every viz remains readable (375px width)
- [ ] Multiple viz in one lesson are visually consistent (shared CSS conventions, inline with their section)

Use the `browser-testing-with-devtools` skill if available; otherwise eyeball via `file://`.
