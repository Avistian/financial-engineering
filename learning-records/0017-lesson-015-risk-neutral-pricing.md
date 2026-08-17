# Lesson 015 published — Risk-neutral pricing & the Girsanov theorem (Q2 continues)

Shipped **Lesson 015 — "Risk-Neutral Pricing & the Girsanov Theorem"**
(`lessons/0015-risk-neutral-pricing-girsanov.html`, ~72 KB, 21 `<h2>`) and its lab
(`labs/0015-risk-neutral-pricing.ipynb`, 8 tasks). This is **Unit 015**, the fifth unit of **Year 1 Q2**,
the curriculum's designated topic "Risk-neutral pricing & the Girsanov theorem: measure change, market
price of risk," primary source **Shreve II Ch. 5** (§5.1–5.4) with Shreve I Ch. 1–2 as the discrete
warm-up. Lab brief matched exactly: "Change measure on a binomial → BS limit."

## The one skill, and the order it is built in
Load-bearing idea: **a price is a hedging cost, and that cost can be rewritten as an average under
re-weighted probabilities.** The lesson refuses to state the pricing formula until the learner has seen
why the obvious formula is wrong, so the chain is:

1. "Discounted expected payoff" fails — two plain reasons (you get one outcome, not the average; nobody
   agrees on `p`, yet markets quote one price).
2. **Replication**, five annotated steps on the 011 tree: `Δ = 0.5`, `B = −45`, price `5`. The
   probability `p` never appears in the two equations. Arbitrage made numeric: selling at the "average
   payoff" price of 7 hands the buyer a risk-free 2.
3. The **algebra that hides a probability**: regroup the replication cost and out falls
   `(1/R)[p*C_u + (1−p*)C_d]` with `p* = (R−d)/(u−d)`. Flagged that `0 < p* < 1` ⟺ `d < R < u` ⟺ no
   arbitrage — the first hint of FTAP 1.
4. **Why "risk-neutral"**: `p*` is the unique weight that reprices the stock (`102/1.02 = 100`), i.e.
   makes the *discounted* stock a martingale (re-warmed from 011).
5. **Lesson 011's IOU paid**: the `p* = ½` and the `7.475` were `(R−d)/(u−d)` at `u=1.1, d=0.9, r=0`.
   Noted that `u = 1.2` would give `1/3` with nothing about the world changed.
6. **Change of measure** in general: same outcomes, new weights; `Z = dQ/dP`, `E_Q[X] = E_P[ZX]`,
   `E_P[Z] = 1`, and **equivalence** (`Z > 0`: you may re-weight a ticket, never shred it).
7. **Girsanov**, with two things checked rather than asserted: `E_P[Z_T] = 1` via 013's
   `E[e^{aW_T}] = e^{½a²T}`, and a full **completing-the-square** derivation showing `W_T` goes from
   `N(0,T)` to `N(−θT, T)` — *centre moves, width does not*.
8. **Market price of risk** `θ = (μ−r)/σ` derived by substituting `dW = dW̃ − θdt`; named as the Sharpe
   ratio the learner will quote for the rest of their career.
9. **Why σ survives and μ does not** — the deepest beat. Quadratic variation `[W]_t = t` is path-wise;
   equivalent measures agree on almost-sure path facts. Mission tie-in made numeric: `se(μ̂) = σ/√T`, so
   pinning a 20%-vol drift to ±1% needs **400 years** — the statistical reason Q1 was all hygiene.
10. **Pricing formula** `V_t = E_Q[e^{−r(T−t)}V_T | ℱ_t]`, with a three-step Itô check that
    `d(e^{−rt}S) = σe^{−rt}S dW̃` (re-using 013's "linear ⇒ no correction"). The **martingale
    representation theorem** is named as the honest gap, not hidden, with its Shreve section.
11. **Black–Scholes as one expectation** (`d1 = 0.35`, `d2 = 0.15`, `C = 10.45`), then the tree → formula
    limit.
12. **FTAP 1 / FTAP 2** in a plain-words table, with incompleteness (jumps, stochastic vol) as the reason
    desks *choose* a `Q` by calibration.

Pacing devices per the 2026-08-13 standing decision: **9 `.plain` notes and 8 `.numplay` boxes**, every
derivation in the slow lane with each step's licence stated.

## Failure-mode-first
Seven traps, the top one being the `P`-vs-`Q` confusion made numeric: `N(d₂) = 56%` is a *pricing weight*,
the real-world exercise chance is `N(0.65) = 74%`. Also: Girsanov cannot move `σ`; simulating with `μ`
instead of `r`; dropping the `e^{−rT}`; thinking "risk-neutral" describes investors; assuming `Q` exists
and is unique; breaking equivalence.

## Three visualizations, one per distinct mechanism (per `lesson-visuals`)
Delivered as one reusable asset `assets/rnpricing-viz.js` (`global.RN`):
- **`RN.mountReplication`** — slider is the *real-world* `p`: the replication price is a flat line at
  5.00 while the discounted-expected-payoff line sweeps through it, crossing only at the marked `p*`.
  This is the lesson's thesis in one picture.
- **`RN.mountWeights`** — Girsanov as **re-weighting, not shifting**. The same seeded paths are drawn at
  their weight `Z = e^{−θW−½θ²t}` (darker/thicker = counts more under `Q`); the solid curve is the
  `P`-mean `S₀e^{μt}`, the dashed curve the *weighted* mean, which sits on `S₀e^{rt}` for every `μ`.
  Implementation note: a naive path bank made the weighted mean wander by ~2% at large `θ`
  (importance-sampling noise, which would have undercut the whole claim), so the bank lays terminal
  Brownian values on **equally-likely strata via a Brownian bridge** — worst error now 0.02 on 105.13
  across the whole slider, with `μ` capped at 20% (θ ≤ 0.75) to keep it exact to the displayed decimal.
- **`RN.mountConvergence`** — CRR tree price at every `n` (dots) against the Black–Scholes line;
  the odd/even zig-zag is visible and closes in.

## Verification
`.smoke.js` extended to **33 checks** (from 27): the new asset added to the eval list plus six traps —
geometry in bounds at every slider position for all three widgets, and numeric checks: replication
`Δ=0.5 / B=−45 / price=5` with `expPrice` strictly increasing in `p` and agreeing only at `p*`, `p*=0.6`
and price `6/1.02` at `R=1.02`; `θ(0.15)=0.5`, `θ(r)=0`, the Q-weighted mean tracking `S₀e^{rt}` at every
sampled time and every `μ`, and an up-path's weight falling as `θ` grows; `d1=0.35`, `d2=0.15`,
`bs=10.4506`, `|binom(400) − bs| < 0.02`, and the gap shrinking monotonically along each parity.
**All 33 pass.** The filled solution notebook executed cell-by-cell in the venv
(`nbconvert --execute`): **all 8 CHECK groups + EXIT ticket pass** — replication price 5.000 flat across
`p`; `p* = 0.5` reprices the stock to 100.0000; three-period tree **7.4750** (= Lesson 011);
`d1=0.3500, d2=0.1500`, BS **10.4506**; 2000-step CRR **10.4496** (gap −0.0010); MC under `Q`
**10.4135**, and **the `μ` bug prints 18.0465, +72.7%**; Girsanov weights on real-world paths give
`E_P[Z]=0.9992`, `E_P[Z·S_T]=105.098` (vs `S₀e^{rT}=105.127`) and price **10.4541**; exercise
probabilities **0.5596 (Q) vs 0.7422 (P)**, both confirmed by simulation. Student `.ipynb` rendered to
`labs/html/0015-risk-neutral-pricing.html`. Browser spot-check was explicitly skipped at the learner's
request this session — the geometry traps in `.smoke.js` cover the layout regressions it would have
caught, but the widgets have **not** been eyeballed at 375px.

## Wiring
manifest → **v12** (lesson 15, `year 1 / quarter 2`, `labPath` set); `index.html` / `notebooks.html`
version meta bumped to 12 and the Girsanov cheat sheet added to the Reference nav; Lesson 014's
forward-nav now points at Lesson 015 (it pointed at the curriculum page); **five** `retrieval-pool.js`
items added (`l015-replication` [misconception], `l015-pstar`, `l015-girsanov` [misconception],
`l015-mpr`, `l015-qnotp` [misconception]) — 62 items total, ids unique, option-label spread ≤ 1 char;
twelve `GLOSSARY.md` rows; `labs/README.md` index entry; `RESOURCES.md` gained unit-015 pointers into
Shreve II Ch. 5 (Girsanov §5.2.2, martingale representation §5.3, market price of risk §5.4) and
Shreve I Ch. 1–2. New reference sheet `reference/girsanov.html`. Builder kept as
`scripts/_gen_lab_0015.py`. Incidental fix: `assets/lesson.css` never got the `.ou-*`/`.expl-*` rules
when Lesson 014 shipped, so those canvases rendered without the shared border/readout styling — the new
block covers them alongside the 015 prefixes.

## Watch-points for next sessions
1. **Grade the measure change cold, not the MCQs.** Ask for three things unaided: (a) set up and solve
   the two replication equations, (b) derive `p* = (R−d)/(u−d)` by regrouping the cost, (c) derive
   `θ = (μ−r)/σ` from `dS = μS dt + σS dW`. If all three land, add "the risk-neutral price" to
   "Derivations I own." The completing-the-square step (`N(0,T) → N(−θT,T)`) is the stretch goal.
2. **The `P`/`Q` confusion is the trap that matters.** Probe it sideways: "the market implies a 56%
   chance this option is exercised — is that a forecast?" A confident yes means the lesson did not land,
   and it is the same error as reading a risk-neutral default probability as a default rate.
3. **`σ` survives, `μ` does not.** Check the learner can say *why* (quadratic variation is path-wise;
   equivalent measures agree on almost-sure facts) and connect it to the 400-year drift-estimation
   number. This is the bridge from Q2 pricing back to the Q1 hygiene thesis, and it is worth re-asking
   at the Q2 checkpoint.
4. **016 arrives next with the same price by a different route.** Feynman–Kac should be introduced as
   "the PDE and today's expectation are the same object," and the BS PDE derivation carries the
   `−½σ²`-style bookkeeping again — so grade the 013/014 teach-backs cold *before* teaching 016, as
   flagged in the 014 record.
5. **Did the `.plain` / `.numplay` scaffolding land?** Still the open question from 014, now with a
   second data point. Ask directly. 015 is the longest lesson since 011 (~72 KB); if the learner reports
   it as clear *but long*, the next lever is splitting 016 rather than trimming boxes.
6. **Browser verification is owed for 015's three widgets** (skipped this session). Worth doing at the
   next natural break, particularly the mobile 375px pass.
7. **Glossary drill still owed** (006–015, 59 blank terms now). One cold-definition pass; fill only what
   the learner defines unaided. Lesson 010 also still self-reported as passed — a fresh checkpoint
   scenario is due.
