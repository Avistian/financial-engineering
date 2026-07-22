# Lesson 010 published — Q1 Checkpoint: Statistical Hygiene

Shipped **Lesson 010 — "Q1 Checkpoint: Statistical Hygiene"** (`lessons/0010-q1-checkpoint.html`,
~19 KB) and its checkpoint lab (`labs/0010-checkpoint-spurious-signal.ipynb`, deliverable: audit a
returns-analysis notebook and detect a *planted spurious signal*). This is **Unit 010**, the exit
exam for Year 1 Q1 (Units 001–009). It is the first `checkpoint: true` lesson in the manifest, and
it closes the whole Q1 statistical-hygiene arc (006 SE/bootstrap → 007 multiple testing → 008
covariance geometry → 009 robust regression) by re-assembling the pieces into one audit. Next is
Unit 011 (Q2: measure-theoretic probability, the stochastic-calculus bridge).

**Framing (checkpoint, not new topic).** The lesson certifies one integrative skill: *given a claimed
edge with a headline t-statistic and no hint about the flaw, run the full battery and either kill or
confirm it.* Explicitly strict per SESSION.md — no advancing to Q2 until it passes cold. Ethos
pulled straight from the mission and the `teach` skill: the value of a quant researcher is negative
knowledge, and "a killed bad backtest is a win."

**The synthesis: the five questions of statistical hygiene** (taught as a table, the checklist the
learner carries forward). (1) Measurable? — SE ∝ 1/√n, CI excludes 0 (006). (2) How many tried? —
fair bar is E[max of M], not 1.96 (007). (3) Independent obs? — Newey–West, n_eff = n/inflation²
(009). (4) Constant variance? — White/HC (009). (5) Future leaked / stationary? — temporal
discipline, regress returns not prices (004/008/009). The load-bearing punchline, proved in 009 and
now generalized: **in every failure mode the point estimate can be fine; it is the standard error —
and therefore the t-statistic, the *claim* — that lies.**

**The one skill: the spurious-signal autopsy.** A procedure that deflates a headline t through the
audit chain `t_reported → t_NW = t_reported/√[(1+φ)/(1−φ)] → t_survives = t_NW − E[max of M]`. A
fully worked in-head case (naïve t = 6.2 from 21-day overlap, best of ~50 tries → dies) mirrors the
lab and a real research meeting.

**New visualization** (`assets/autopsy-viz.js`, the checkpoint's single mechanistic beat): three
bars — Reported t, after Newey–West (overlap), after the best-of-M haircut — with the 1.96 line and
a slider for M (log 1→1000). E[max of M] is computed by honest numerical integration of
∫ x·M·φ(x)·Φ(x)^{M−1} dx (verified: E[max of 2]=0.564=1/√π exactly; E[max 10]=1.54, 100=2.51). With
t0=6.2, infl=2.7: M=1 survives (≈2.3), M=10+ dead; default M=50 → ≈0.05 → DEAD. Added to `.smoke.js`
(now 9 widgets, all pass) and `assets/lesson.css` (autopsy-* classes + a `ul.checklist` style for
the exit criteria).

**Pedagogy widgets:** spaced-retrieval warm-up (`upTo: 10`, count 4); a predict-before-reveal on the
t=6.2/M=50 verdict being "no surviving edge"; a teach-back on the full audit walkthrough; four MCQs;
an objections `<dl>` (why run all five, double-counting corrections, how to know M, White-barely-
moved, quizzes-vs-lab-readiness); a no-peek reflection; and the exit-criteria checklist. Added four
`retrieval-pool.js` items (`l010-se-lie`, `l010-selection-bar` [misconception], `l010-neff`,
`l010-verdict`).

**Lab verified end-to-end** (filled solution executed via nbconvert; all CHECK cells pass, EXIT
TICKET clean). DGP: daily returns are **pure heteroskedastic noise, zero true edge**; a search over
M=60 persistent signals picks the best naïve t on 21-day *overlapping* forward returns (n=800,
seed=2024). Arc: headline **naïve t = −10.43** → White HC barely moves it (−10.75, ratio 0.97 → *not*
heteroskedasticity, a diagnostic) → **Newey–West deflates to −3.17** (SE inflation 3.3×, n_eff ≈ 74
of 800) → minus the best-of-60 bar E[max]=2.32 → **surviving margin 0.85 < 1.96** → decisive
**Monte-Carlo empirical null** (200 reps of the whole search under fresh noise; ~15–30 s) gives
**p = 0.63** → `is_spurious = True`. Verdict: SPURIOUS. Teacher solution in `solutions/` (gitignored).
Rendered `labs/html/0010-*.html` for the browser View.

**Wiring:** manifest bumped to version 6 (index/notebooks meta → 6) with the checkpoint entry +
labPath; L009 forward-nav now points to the lesson (not the curriculum ref); GLOSSARY updated
(statistical hygiene, spurious-signal autopsy, n_eff, best-of-M haircut); labs README index updated.
HLZ 2016 was already in RESOURCES (used as the checkpoint's consolidation reading).

**Watch-points for next sessions.** (1) The learner has *not* yet passed — this ships the checkpoint;
grade the lab EXIT TICKET and a fresh un-seen scenario before advancing to Q2. (2) The "explain
everything" standing decision means the deflated-Sharpe connection is only *previewed* (unit 055);
if the learner asks, give the one-line intuition, don't front-load it. (3) GLOSSARY rows for 010 (and
all of 006–009) are still unfilled — fill them only when the learner can define each cold.
