# Lesson 011 published — Information, Filtrations & Conditional Expectation (Q2 opens)

Shipped **Lesson 011 — "Information, Filtrations & Conditional Expectation"**
(`lessons/0011-filtrations-conditional-expectation.html`, **~69 KB**, 20 `<h2>` / 14 `<h3>`) and its lab
(`labs/0011-conditional-expectation-tree.ipynb`, 8 tasks). This is **Unit 011**, the first unit of
**Year 1 Q2** (Units 011–020: measure theory → Brownian motion → Itô → SDEs → pricing) and the
curriculum's designated topic "measure-theoretic probability (lite): spaces, filtrations, conditional
expectation as projection," primary source **Shreve II Ch. 1–2**.

**Size is deliberate and is the story of this lesson.** At ~69 KB it is nearly double the previous
largest (009, 37 KB). The 2026-07-23 standing decision made the 22–30 KB band a *floor, not a target*
for math-heavy units, and named Q2 as its primary test. Every abstraction is introduced only after the
concrete object it names, one idea per beat, with the prerequisite re-warmed inline (dot products from
008, OLS-as-projection from 009, plain expectation from 005). **Do not "trim" this lesson later
without re-reading that decision** — the length is the pedagogy, not bloat.

**The four levers, as applied.** (1) *Intuition before symbols*: a σ-algebra is introduced as "the
list of yes/no questions you can answer" and only then given its three axioms — each axiom justified
by that reading rather than asserted. (2) *Smaller steps*: conditional expectation is built in
**four labelled layers** (plain E → conditioning on an event → conditioning on a σ-algebra → the
general partial-averaging definition), so the load-bearing idea arrives in four small pieces instead
of one definition. (3) *Re-warm inline*: L² is introduced by showing `E[XZ]` **is** the ordinary dot
product of 8-vectors reweighted by probability. (4) *Slow lane*: the projection theorem is proved in
five annotated steps (A–E), each naming the rule that licenses it, with the cross-term death (Step D)
broken into four sub-lines citing tower / taking-out-what-is-known / linearity individually. Ban on
"it can be shown that" respected throughout.

**One running example, verified numerically.** `S₀ = 100`, `u = 1.1`, `d = 0.9`, three periods,
`p = ½`, call payoff `V = (S₃−100)⁺`. Every number in the prose is machine-checked (see below):
`E[V] = 7.475`; `E[V|ℱ₁] = (12.725, 2.225)`; `E[V|ℱ₂] = (21.00, 4.45, 4.45, 0)`; partial averaging on
`A = {H··}` gives `6.3625` both ways; min MSE `E[(V−E[V|ℱ₁])²] = 83.216875`; variance splits
`110.779 = 83.217 + 27.563` (24.9% explained by the first flip). Because `(u+d)/2 = 1`, the price is a
martingale under `p = ½` — which is *also* `p* = (1−d)/(u−d)`, so the lesson **prices the call at
7.475** two units before Girsanov. That is flagged explicitly as a preview (per the "explain
everything / no front-loading" rule), with the *why* deferred to unit 015.

**The synthesis that makes Q2 continuous with Q1** (the section to reuse in later lessons):
`E[r_{t+1}|ℱ_t]` is what a signal estimates, so **alpha is the claim that a conditional expectation is
non-zero**; OLS (009) was that projection restricted to *linear* functions of one feature; the residual
is unpredictable *by construction* (Step D orthogonality), which is what "no remaining edge" means;
and **leakage is conditioning on a σ-algebra strictly bigger than ℱ_t**, which — because a bigger
subspace always has a smaller residual (Step E) — *always* flatters a backtest. Purged CV (Year 2 Q2)
is re-described as machinery for keeping the conditioning set inside ℱ_t.

**Three visualizations, one per mechanism** (per `lesson-visuals`), delivered as **two reusable
assets**:

- **`assets/tree-viz.js`** — a *non-recombining* **path** tree (2^t nodes at level t, so `HT` and `TH`
  stay distinct), mounted **twice** because it carries two different mechanisms: `mode:"filtration"`
  shades the **atoms of ℱ_t** (1→2→4→8 cells, with the answerable-question count 2^(2^t) = 2, 4, 16,
  256) and dims unobserved edges; `mode:"condexp"` labels every node with `E[X|ℱ_level]` so the learner
  *sees* backward averaging and the tower property (re-averaging a column reproduces the one to its
  left). Parameterised by `payoff: "price" | "call"`.
- **`assets/projection-viz.js`** — the L² geometry, honestly labelled as a 2-D slice of the 8-dimensional
  space: the subspace of ℱ₁-measurable guesses as a line, V at perpendicular distance `√83.22 = 9.12`,
  and a slider stepping along the subspace. The readout `83.22 + s²` is *exactly* Pythagoras with the
  lesson's real numbers, so picture and algebra cannot drift apart.

**Verification — note the new harness.** No browser is available in this environment, so `.smoke.js`
was extended from 9 to **15 checks**, and two of them are a genuinely new capability: a **recording
canvas** that captures every `fillText`/`fillRect`/`arc`/`moveTo`/`lineTo`/`roundRect` coordinate and
asserts it lands inside the canvas, run across **every slider position of both new widgets**. It
immediately earned its keep (it is why the projection distance label is right-aligned — the original
left-aligned version ran ~90 px off the canvas), and it was itself negative-tested to confirm it is not
vacuous. Three further checks assert the *numbers*: the call's backward-averaged values (21 / 12.725 /
7.475) and `E[S₃|ℱ_t] = S_t` for the price payoff. **Future lessons should reuse `withRecordedCanvas` /
`assertInBounds` for any new viz.** Still worth an eyeball on a real phone viewport when the learner
next opens the lesson — the harness proves bounds, not beauty.

**Pedagogy widgets:** warm-up (`upTo: 11`, count 4 — draws only from 001–010, verified `lesson < upTo`);
a predict-before-reveal on the genuinely non-obvious *type* question ("what kind of object is
`E[V|ℱ₁]`?" — a random variable, the field's most common confusion); a teach-back on
conditional-expectation-as-projection *and its link to leakage*; **five** MCQs; a six-item objections
`<dl>` (including the honest "is measure theory used in the job or is it interview theater?"); a
six-point `.trap`; a no-peek reflection; and a "Where you are in the arc" closer mapping 012→020.

**Lab verified end-to-end** (filled solution executed via nbconvert; **all 8 CHECK groups pass, EXIT
TICKET clean**; 11 blanks in the student copy, 0 in the solution). The lab's design principle is
*verify the theory numerically rather than trusting it*: build `atoms(t)` and prove the filtration
refines; `is_measurable` as the formal no-look-ahead predicate; `cond_exp`; then partial averaging
checked on **every one of the 2^(2^t) events** (gap 0.0e+00) plus a deliberate failing candidate to
show the property is restrictive; the tower property over all `s ≤ t`; a **grid search** that
rediscovers `(12.725, 2.225)` as the least-squares minimiser with an orthogonal residual and a clean
variance split; the martingale `p*` (and its failure at `p = 0.6`, gross drift 1.02); and finally a
**leakage demo** — an ℱ₃-measurable "strategy" earning `+9.95` out of thin air while every adapted rule
earns exactly `0.000` under the martingale measure. Teacher solution in `solutions/` (gitignored);
rendered `labs/html/0011-*.html` for the browser View.

**New reference sheet:** `reference/conditional-expectation.html` — "Filtrations, Conditional
Expectation & Martingales," the printable working rules (four objects; the three equivalent views;
tower / take-out / independence / linearity / Jensen / variance-split; martingale definition; the
standard tree's numbers; the six traps). This is the first reference doc added since day one and is
**intended as the page units 012–020 link to instead of re-reading Lesson 011** — keep feeding it
rather than duplicating rules in each lesson.

**Wiring:** manifest → **v7** with the first `quarter: 2` entry (+ `labPath`); `index.html` /
`notebooks.html` version meta bumped and the new cheat sheet added to the Reference nav; Lesson 010's
forward-nav now points at Lesson 011 (it pointed at the curriculum page); five `retrieval-pool.js`
items added (`l011-condexp-type` [misconception], `l011-measurable-leak` [misconception], `l011-tower`,
`l011-projection`, `l011-martingale` [misconception]) — 42 items total, all ids unique, option-label
length spread ≤ 4 chars; twelve `GLOSSARY.md` rows; `labs/README.md` index; `RESOURCES.md` gained
Williams *Probability with Martingales* (◆) and section pointers for Shreve Vol I Ch. 2 / Baxter–Rennie
§3.1–3.3 as the gentler on-ramps.

**Watch-points for next sessions.**
1. **Grade the teach-back, not just the quizzes.** The lesson's whole claim to depth is the projection
   view; recognition MCQs cannot test it. Ask for the teach-back prose and check specifically whether
   the learner can say *why* the cross term vanishes (tower + taking out what is known) without
   prompting.
2. **The type error is the one to drill.** Three of the five new pool items are misconception-tagged
   for a reason: "E[X|ℱ_t] is a random variable" is the belief that must be automatic before unit 013,
   because the Itô integral is built out of exactly these objects.
3. **Unit 012 must not lose the tree.** The lesson promises that a confusing continuous-time
   manipulation can be redrawn as a three-step tree. Keep that promise: 012 should build Brownian
   motion *as the limit of this specific random walk*, reusing `tree-viz.js` if possible so the visual
   lineage is unbroken.
4. **The 7.475 preview is a debt.** The learner has now priced an option without knowing why `p* = ½`
   is legitimate. If they push on it before unit 015, give the one-line replication intuition ("the
   hedge, not the forecast, sets the price") and hold the rest — do not front-load Girsanov.
5. **Difficulty check-in.** This is the first lesson written entirely under the "struggling learner /
   depth over length" decision. Ask directly whether the four-layer build and the annotated derivation
   helped or whether ~70 KB is now too much in one sitting, and record the answer — the next nine units
   should be calibrated on real feedback, not on my assumption that longer is better.
