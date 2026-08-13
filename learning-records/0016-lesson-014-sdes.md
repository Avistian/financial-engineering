# Lesson 014 published — SDEs: GBM & Ornstein–Uhlenbeck (Q2 continues) + "even more basic" turn

Shipped **Lesson 014 — "Stochastic Differential Equations: GBM & Ornstein–Uhlenbeck"**
(`lessons/0014-sdes.html`, ~30 KB, 19 `<h2>`) and its lab
(`labs/0014-ornstein-uhlenbeck.ipynb`, 6 tasks). This is **Unit 014**, the fourth unit of **Year 1 Q2**,
the curriculum's designated topic "SDEs: GBM, Ornstein-Uhlenbeck, existence/uniqueness intuition,"
primary source **Øksendal Ch. 5** (§5.1–5.2) with Shreve II §4.4–4.5 as the finance companion. Lab brief
matched exactly: "Simulate & fit an OU process."

## The trigger: learner asked for "even more basic (still in math terms)"
The learner reported **difficulty understanding Lessons 012 and 013** and asked to make lessons even more
basic while keeping the math. Read as *clarity, not length* — the symbols were never grounded hard enough.
Response, now a **standing decision** (see `NOTES.md` 2026-08-13 and `lesson-pedagogy` skill "Even more
basic"): every load-bearing equation gets a **say-it-in-words box (`.aloud`)** reading it aloud symbol by
symbol, and abstract results get a **with-real-numbers box (`.numplay`)** that plugs in small numbers and
computes a step by hand. Applied throughout 014; **retro-fitted to 013** (three boxes: the simple lemma,
a `d(W²)` numeric play, the general lemma) since the learner said they will revisit it.

## The one skill, taught the new way
Load-bearing idea: **solving an SDE = apply Itô to a function that cancels the state, then integrate.**
Stated as a one-sentence refrain and used twice — `log S` for GBM (⇒ `S_t = S₀ exp((μ−½σ²)t + σW_t)`,
re-using 013's `−½σ²`) and the **integrating factor `e^{θt}X`** for OU. The OU solve is the through-line
payoff of 013's "linear function ⇒ no correction" rule: `e^{θt}X` has `f_xx = 0`, so the `±θe^{θt}X` terms
cancel and no Itô correction appears — explicitly contrasted with the GBM/log solve that *does* carry one.
Full slow-lane derivation to `X_t = X₀e^{−θt} + m(1−e^{−θt}) + σ∫e^{−θ(t−s)}dW`, then read off mean → `m`,
variance → `σ²/2θ` (via a re-warmed **Itô isometry**), stationary law `N(m, σ²/2θ)`, half-life `ln2/θ`.
Existence/uniqueness delivered as intuition only: **bounded steepness (Lipschitz) ⇒ uniqueness**, **no
faster-than-linear growth ⇒ no finite-time blow-up**, with the `dx/dt = x²` explosion (`t* = 1/x₀`) as the
counter-example. Failure-mode-first: OU's constant-θ/m assumption breaks in real spreads; θ is biased high
on short samples.

## Mission tie-in
OU is framed straight onto the learner's buy-side alpha mission: pairs-trading spreads, Vasicek rates,
"anything that normalises," with half-life as the PM-facing horizon and `σ²/2θ` as the drawdown width.

## Two new visualizations, one per distinct mechanism (per `lesson-visuals`)
Delivered as **one reusable asset `assets/sde-viz.js`** (seeded Brownian bank built the 012/013 way):
- **`SDE.mountOU`** — mean reversion: faint OU paths from `X₀=80` pulled to `m=100`, mean curve
  `X₀e^{−θt}+m(1−e^{−θt})`, and equilibrium band `m ± √(σ²/2θ)`. Slider = θ (pull strength): stronger
  pull ⇒ faster snap-back *and* tighter band. Fixed generous y-window (55–125), all draws clamped.
- **`SDE.mountExplosion`** — existence/uniqueness: deterministic `dx/dt = x` (finite) vs `dx/dt = x²`
  (blows up at the dashed wall `t* = 1/x₀`). Slider = x₀; the wall marches left as x₀ grows. Curves
  clamped to the window so geometry stays in bounds.
The GBM mean/median drag reuses the existing `Ito.mountGBM` (no new code — a third mechanism already
visualised in 013).

## Verification
`.smoke.js` extended to **27 checks** (from 23): `sde-viz.js` added to the eval list, plus four traps —
OU and explosion geometry in bounds across **every slider position**, and numeric checks: OU `endMean(θ)`
strictly increases toward `m` while `statStd(θ)` strictly decreases, `halfLife = ln2/θ`, `statStd(2)=2.5`
(`√(σ²/2θ)`, σ=10); explosion `blowupTime(x0)=1/x0` strictly decreasing, linear-growth stays finite.
**All 27 pass.** The lab's filled solution executed cell-by-cell in the venv (`nbconvert --execute`):
**all 6 CHECK groups + EXIT ticket pass** — `E[X_T]=100.01≈m`; closed-form mean matches sim to 0.078;
`Var(X_T)=10.93≈σ²/2θ=10.67`; measured half-life `0.229≈ln2/θ=0.231`; **long-path fit recovers
θ=2.992, m=99.945, σ=7.992**; **short-window fit is biased high: mean θ̂=4.287 vs true 3.0 (+1.287)** —
the pairs-trade estimation trap, made numeric. Student `.ipynb` rendered to
`labs/html/0014-ornstein-uhlenbeck.html`. No lint errors.

## Wiring
manifest → **v11** (lesson 14, `year 1 / quarter 2`, `labPath` set); `index.html` / `notebooks.html`
version meta bumped to 11 and the SDE cheat sheet added to the Reference nav; Lesson 013's forward-nav now
points at Lesson 014 (it pointed at the curriculum page); **five** `retrieval-pool.js` items added
(`l014-sde-def`, `l014-solve-trick`, `l014-ou-revert` [misconception], `l014-ou-nocorr` [misconception],
`l014-existence`) — 57 items total, ids unique, option-label spread trimmed to ≤ 4 chars; eight
`GLOSSARY.md` rows; `labs/README.md` index entry; `RESOURCES.md` gained a ★ Øksendal Ch. 5 entry (the
existence/uniqueness theorem + OU/GBM solves) with the unit-014 primary-source pointer. New reference
sheet `reference/sdes.html` (SDE definition, the one trick, GBM & OU solved tables, Itô isometry,
existence/uniqueness conditions, six traps). Builder kept as `scripts/_gen_lab_0014.py` (matches the
`_gen_lab_XXXX.py` convention).

## Watch-points for next sessions
1. **Grade the OU solve cold**, not the MCQs. Ask the learner to derive `X_t` via the `e^{θt}X`
   integrating factor unaided and to say *why* there is no Itô correction (linear ⇒ `f_xx=0`). If they can
   — plus the `μ−½σ²` GBM solve — both go into "Derivations I own."
2. **Keep the two OU spreads distinct:** mean → `m` vs stationary wobble → `σ²/2θ`. And check they read
   `θ(m−X)` as a pull *toward* `m` (sign trap #2 in the lesson).
3. **The θ small-sample bias is the lab punchline.** Make sure the learner internalises that short fits
   overstate reversion — it is a real pairs-trade failure mode and an interview topic.
4. **Did the "even more basic" turn land?** This is the key open question. Ask the learner directly whether
   the `.aloud` / `.numplay` boxes in 013 (revisit) and 014 made the difference. If yes, keep them
   mandatory on 015–020 (Girsanov and the BS PDE are the next density spikes). If still unclear, the next
   lever is probably *splitting* a lesson, not more boxes.
5. **015 must reuse the martingale/measure spine.** Girsanov changes the drift of an SDE; introduce it as
   "re-weight the paths so the discounted price becomes a martingale," finally paying the `p*=½ / 7.475`
   debt from Lesson 011. Keep the lineage unbroken.
6. **Glossary drill still owed** (006–014, 47 blank terms). One cold-definition pass; fill only what the
   learner defines unaided. Lesson 010 also still self-reported as passed — a fresh checkpoint scenario is
   due at the next natural break.
