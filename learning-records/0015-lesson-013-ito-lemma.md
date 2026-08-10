# Lesson 013 published — The Itô Integral & Itô's Lemma (Q2 continues)

Shipped **Lesson 013 — "The Itô Integral & Itô's Lemma"**
(`lessons/0013-ito-lemma.html`, **~47 KB**, 17 `<h2>`) and its lab
(`labs/0013-ito-lemma.ipynb`, 6 tasks). This is **Unit 013**, the third unit of **Year 1 Q2**, the
curriculum's designated topic "the Itô integral & Itô's lemma," primary source **Shreve II Ch. 4**
(§4.2–4.4). Lab brief matched exactly: "apply Itô to `d(log S)`, `d(S²)`."

**The through-line honours the 012 watch-points.** (1) *013 reuses the same picture* — Itô's lemma is
introduced as literally "Taylor + `(dW)²=dt`," pointing back to the `W²−t` martingale and the quadratic
variation of Lesson 012; the lead worked example `d(W²)=2W dW+dt` **re-derives** that martingale in one
line, so the lineage tree → walk → BM → Itô is unbroken. (2) *`(dW)²=dt` made automatic* — the whole
lesson is built on the keep/drop table (`(dW)²`→`dt`, drop `dW·dt` and `(dt)²`), and the teach-back is
graded specifically on *why* `(dW)²` survives while the others vanish, exactly the 012 watch-point. (3)
*The 7.475 / `p*` debt is untouched* — no Girsanov front-loading; the `p*=½` question stays deferred to
015 and is only re-promised in the arc closer.

**The one skill, taught intuition-first.** The single load-bearing idea is **Itô's lemma:
`df = f′(W)·dW + ½ f″(W)·dt`**, generalised to `df = (f_t + a f_x + ½ b² f_xx)dt + b f_x dW` for an Itô
process `dX = a dt + b dW`. The `½ f″ dt` correction is motivated *before* any symbol: "curvature plus
wiggle manufactures drift" (up-wiggle helps more than the down-wiggle hurts when `f` is curved — the
continuous-time cousin of Jensen). The **Itô integral** is taught as "position set at the *left* edge of
each step × the next shock, summed," and the left-endpoint choice is given its plain meaning ("you bet
before the coin is flipped") and its consequence (every `∫…dW` is a martingale, so all drift lives in the
`dt` bracket). Two fully worked slow-lane derivations, every step licensed: `d(W²)` and the flagship
`d(log S) = (μ−½σ²)dt + σ dW` (each cancellation of `S` shown).

**Two visualizations, one per distinct mechanism** (per `lesson-visuals`), delivered as **one reusable
asset `assets/ito-viz.js`** with two mount modes sharing a seeded Brownian bank (built the Lesson-012
way — cumulative `√dt·N(0,1)`):

- **`Ito.mountDrift`** — the correction term as a *visible* drift. Splits each path exactly into
  `W_t² = (∫2W dW) + Σ(ΔW)²`; the Itô integral (what the naive chain rule keeps) averages to 0 (flat
  martingale), while `E[W_t²]` climbs the drift line `y=t`. The entire rise is the `(dW)²=dt` term. Slider
  = number of paths `N=2^k` (2→256); the y-range is recomputed each draw so noisy small-`N` averages stay
  in bounds while the `0` and `+1` labels remain visible.
- **`Ito.mountGBM`** — the `−½σ²` drag. GBM sample paths with the **mean** line `S₀e^{μt}` (grows at `μ`,
  unaffected by `σ`) and the **median** line `S₀e^{(μ−½σ²)t}`. Slider = `σ` (5%→80%); as `σ` rises the
  median falls below the mean, and past `σ≈45% (=√(2μ))` the median drift turns negative while the mean
  keeps climbing — the volatility drag made concrete.

**Verification.** `.smoke.js` extended to **23 checks** (from 19): `ito-viz.js` added to the eval list,
plus four traps reusing `withRecordedCanvas`/`assertInBounds` — geometry in bounds across **every slider
position of both modes**, and numeric checks: `meanW2(256)≈1` and `meanIto(256)≈0` (with the identity
`E[W²]−E[∫2W dW] ≈ 1` = the QV drift), `meanRate=μ` fixed, and `medianRate(σ)=μ−½σ²` strictly decreasing
in `σ`. **All 23 pass.** The lab's filled solution was executed cell-by-cell in the venv (via
`nbconvert --execute`, kernel `python3`): **all 6 CHECK groups + EXIT ticket pass** — GBM drift coef
`0.060 = μ−½σ²` with `E[S_T]=108.30=S₀e^{μT}`; `E[∫2W dW]=−0.009 (~0)`, `E[Σ(ΔW)²]=1.0001 (~T)`, identity
`W_T²=I+Q` to `3.6e-15`; measured `log S` drift `0.0595 ≈ 0.06` (clearly below `μ=0.08`); `E[S²]` growth
rate `0.198 ≈ 2μ+σ²=0.20`; mean `108.30 >` median `106.20`; `E[e^{W_T}]=1.639 ≈ e^{0.5}=1.649` (naive
"stays at 1" is off by 0.64). Student `.ipynb` rendered to `labs/html/0013-ito-lemma.html`. No lint errors.

**Size calibration (the open A/B still stands).** 013 landed at **~47 KB / 17 `<h2>`** — deliberately kept
to the leaner 012 calibration (one idea per beat) rather than the ~70 KB of 011, since **the learner has
still not answered which felt better in one sitting.** This is now a *three-point* series (011 ~70 KB,
012 ~49 KB, 013 ~47 KB); the length question should finally be put to the learner directly (see
watch-points). Depth-over-length stands; the only open question is how much per lesson.

**New reference sheet:** `reference/ito-lemma.html` — the printable working rules (keep/drop table, the
Itô integral + martingale fact, the three cases of Itô's lemma, the five worked one-liners, the GBM
mean/median table, the six traps). Intended as the page units 014–020 link to instead of re-reading 013.

**Wiring:** manifest → **v10** (lesson 13, `year 1 / quarter 2`, `labPath` set); `index.html` /
`notebooks.html` version meta bumped to 10 and the new cheat sheet added to the Reference nav; Lesson 012's
forward-nav now points at Lesson 013 (it pointed at the curriculum page); **five** `retrieval-pool.js`
items added (`l013-lemma`, `l013-dw2` [misconception], `l013-ito-integral`, `l013-logdrift`
[misconception], `l013-correction-sign`) — 52 items total, ids unique, option-label spread ≤ 4 chars;
seven `GLOSSARY.md` rows; `labs/README.md` index; `RESOURCES.md` gained a Wilmott *Introduces Quantitative
Finance* (◆) entry, a Baxter–Rennie Ch. 3 (Itô) pointer, and a Shreve II Ch.4 §4.2–4.4 unit-013 pointer.

**Watch-points for next sessions.**
1. **Ask the length question, finally (third time of asking).** 011 ~70 KB, 012 ~49 KB, 013 ~47 KB — a
   real three-point series now. Ask the learner which felt best in one sitting and *record the answer*;
   calibrate 014–020 on it, not on my "leaner is better" assumption.
2. **Grade the teach-back, not the MCQs.** The lesson's claim to depth is the `d(log S)` derivation and
   the left-endpoint-⇒-martingale argument. Recognition MCQs cannot test either. Ask the learner to derive
   `μ−½σ²` cold (every cancellation) and to say *why* `∫…dW` has zero drift. If they can, both go into the
   "Derivations I own" list and GLOSSARY.
3. **The `−½σ²` sign must be automatic before 014/016.** SDE solutions (014) and the Black–Scholes PDE
   (016) both carry it. Drill specifically: *which way does the correction push?* (sign of curvature) —
   `log S` down (drag), `S²`/`e^W` up (bonus). The lab's Task 3 vs Task 4 split is designed to keep the
   two signs distinct; if the learner conflates them, re-drill before 014.
4. **014 must reuse the same trick.** SDEs (GBM solved, then Ornstein–Uhlenbeck) should be introduced as
   "apply Itô to the right function" — `log S` for GBM, `e^{θt}X` for OU — so the lineage stays unbroken.
   Reuse `ito-viz`'s seeded GBM bank if a diagram helps.
5. **Glossary drill still owed.** Rows for 006–013 are all still blank (39 terms now). Do one cold-
   definition pass and fill only what the learner defines unaided. Lesson 010 also remains **self-reported**
   as passed — still worth a fresh checkpoint scenario at the next natural break.
