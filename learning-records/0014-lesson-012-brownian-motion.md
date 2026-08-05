# Lesson 012 published — Random Walks & Brownian Motion (Q2 continues)

Shipped **Lesson 012 — "Random Walks & Brownian Motion"**
(`lessons/0012-brownian-motion.html`, **~49 KB**, 15 `<h2>` / 6 `<h3>`) and its lab
(`labs/0012-brownian-motion.ipynb`, 6 tasks). This is **Unit 012**, the second unit of **Year 1 Q2**,
the curriculum's designated topic "random walks → Brownian motion: construction, properties, quadratic
variation," primary source **Shreve II Ch. 3** (§3.2–3.4).

**The through-line honours the 011 watch-points.** (1) *Do not lose the tree* — Brownian motion is built
explicitly as the continuous limit of the Lesson-011 coin flips, now **added and rescaled by `1/√n`**
instead of multiplied; the `bm-viz` path widget is driven by the same up/down flips so the visual
lineage is unbroken. (2) *The type error is drilled* — the whole "`E[X|ℱ_t]` is a random variable"
apparatus from 011 is reused verbatim in the martingale proof (split into known + increment, take out
what is known, independence kills the increment). (3) *The 7.475 debt is untouched* — no Girsanov
front-loading; the `p* = ½` question stays deferred to 015, only re-promised in the arc closer.

**The one skill, taught failure-mode-first.** The lesson's single load-bearing idea is **quadratic
variation `[W]_t = t`, i.e. `(dW)² = dt`** — the non-vanishing squared wiggle that ordinary calculus
cannot drop. Everything routes to it: the `√n` scaling (variance lives in squared units), the martingale
`W_t² − t` (its compensator *is* the QV), the nowhere-differentiability (`|ΔW|/Δt ≈ 1/√Δt → ∞`), and the
explicit statement that this is *the* reason Itô's lemma (013) needs an extra term. The `.trap` names six
misuses; the honest warning that BM is the *first* log-price model, not a faithful one, ties back to the
Lesson-004 stylized facts it violates (fat tails, vol clustering).

**Slow-lane rigour, per the standing decisions.** Two annotated derivations with every step licensed: the
martingale property (A–E, each citing a Lesson-011 rule) and `[W]_t = t` (mean `m·Δt = t`, wobble
`2t²/m → 0`, so the limit is the non-random `t`). Plain-language-first throughout: random walk = a
drunkard's running total; increment = "how much it moved"; variance re-warmed as "squared units, which is
why the scaling is a square root." Every symbol is preceded by its plain-English picture.

**Two visualizations, one per distinct mechanism** (per `lesson-visuals`), delivered as **one reusable
asset `assets/bm-viz.js`** with two mount modes sharing a seeded path:

- **`BM.mountPaths`** — the scaled random walk `M_{nt}/√n` over `[0,1]`; slider `n = 2..512`. The dark
  walk fills in toward a fixed pale limit as `n` grows, and the readout keeps hammering the invariant
  `Var(W_t) = t` at every resolution.
- **`BM.mountQVar`** — the same fixed path cut into `m` pieces; the readout compares `Σ(ΔW)²` (hovers at
  `1 = t`, locks to exactly `1.00` at the finest mesh) against the smooth line's `Σ(Δf)² = 1/m` (marches
  to 0). One screen, the whole contrast.

The default path uses **seed 2322** — chosen by a scan (not seed 7, which was an outlier with endpoint
`−2.03` and noisy coarse QV). Seed 2322 gives a typical excursion (`|max| = 1.28`, endpoint
`W₁ = −0.707 = −16/√512`) whose subsampled QV hugs 1 cleanly (`0.89, 1.09, 1.02, …`). The `yMax` axis is
data-driven so no clamping distorts the path.

**Verification.** `.smoke.js` extended to **19 checks** (from 15): `bm-viz.js` added to the eval list, plus
four new traps reusing `withRecordedCanvas`/`assertInBounds` — geometry in bounds across **every slider
position of both modes**, and numeric checks (`qvSmooth(m)=1/m`, `qvBM(512)=1` exactly, endpoint/excursion
pinned, and `qvBM(m)` stays in the O(1) band above the shrinking smooth sum). **All 19 pass.** The lab's
filled solution was executed cell-by-cell in the venv: **all 6 CHECK groups + EXIT ticket pass**
(`Var(W^n_1) ≈ 1` for `n = 1..1024`; increments `N(0,dt)` with lag-1 corr `−2e-5`; martingale slope
`+2e-4`, `E[W_T²] = 1.005`; `[W]_T = 0.98` with QV std shrinking `0.185 → 0.060 → 0.019`; first-order sum
grew `8.9×` over a `64×` mesh refinement, i.e. `~√m`). Student `.ipynb` rendered to `labs/html/`.

**Size calibration (resolves an open NOTES watch-point).** 011 was ~70 KB and flagged as possibly too much
for one sitting; I have **not yet had the learner's answer**. I calibrated 012 to **~49 KB / 15 `<h2>`** —
still comfortably above the depth floor and fully self-contained, but ~30% leaner than 011 by keeping one
idea per beat and not repeating the four-layer build. This is a *provisional* choice; the length question
should still be put to the learner directly (see watch-points).

**New reference sheet:** `reference/brownian-motion.html` — the printable working rules (random walk → BM
table, the four defining properties, the martingale facts, `[W]_t = t` with the slow-lane reason, the
smooth-vs-BM contrast table, the simulate-it recipe, and the six traps). Intended as the page units 013–020
link to instead of re-reading 012.

**Wiring:** manifest → **v9** (lesson 12, `year 1 / quarter 2`, `labPath` set); `index.html` /
`notebooks.html` version meta bumped to 9 and the new cheat sheet added to the Reference nav; Lesson 011's
forward-nav now points at Lesson 012 (it pointed at the curriculum page); **five** `retrieval-pool.js` items
added (`l012-scaling`, `l012-bm-def`, `l012-qvar`, `l012-nowhere-diff` [misconception], `l012-dw2dt`
[misconception]) — 47 items total, ids unique, option-label spread ≤ 3 chars; eight `GLOSSARY.md` rows;
`labs/README.md` index; `RESOURCES.md` gained Mörters & Peres *Brownian Motion* (◆) and a Shreve Ch.3
§3.2–3.4 pointer.

**Watch-points for next sessions.**
1. **Ask the length question, finally.** 011 (~70 KB) vs 012 (~49 KB) is now a real A/B. Ask the learner
   which felt better in one sitting and *record the answer* — calibrate 013–020 on it rather than my guess
   that leaner is better.
2. **`(dW)² = dt` must be automatic before 013.** Itô's lemma is nothing but this substitution inside a
   Taylor expansion. Grade the teach-back specifically for "why `(dW)²` survives but `dW·dt` and `(dt)²` are
   dropped" — recognition MCQs cannot test that.
3. **Guard against the two-variances confusion (Trap 4).** `Var(W_t)=t` (across paths) vs `[W]_t=t` (one
   path's squared wiggles) share the value `t` by Gaussian coincidence; the lab's Task 4/5 split is designed
   to keep them distinct. If the learner conflates them, drill it before 013.
4. **013 must reuse the same picture.** Itô's lemma should be introduced as "Taylor + `(dW)²=dt`," pointing
   back to the `W_t²−t` preview and the `qvar` widget, so the lineage (tree → walk → BM → Itô) stays
   unbroken. Reuse `bm-viz`'s seeded path if a diagram helps.
5. **Glossary drill still owed.** Rows for 006–012 are all still blank (32 terms now). Do one cold-definition
   pass and fill only what the learner defines unaided.
