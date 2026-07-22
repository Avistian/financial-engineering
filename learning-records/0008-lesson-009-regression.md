# Lesson 009 published — Regression Done Right: OLS, Robust SEs, and When Regression Lies

Shipped **Lesson 009 — "Regression Done Right: OLS, Robust Standard Errors, and When Regression
Lies"** (`lessons/0009-regression-done-right.html`, ~37 KB) and its lab
(`labs/0009-robust-standard-errors.ipynb`, deliverable: robust vs naïve standard errors). Covers
Unit 009 (Wooldridge for OLS + heteroskedasticity; Newey–West 1987 for HAC). This closes the
statistical-hygiene thread of Year 1 Q1 (006 SE/bootstrap → 007 multiple testing → 008 covariance
geometry → 009 the regression workhorse with a trustworthy error bar). Next is Unit 010, the Q1
checkpoint (reproduce a returns-analysis notebook; catch a planted spurious signal).

Concepts, each fully explained with a worked numeric example (per the standing "explain everything
you introduce" decision): the linear model `y = Xβ + ε` (design matrix, coefficients, error ε vs
observed residual e); **OLS** `β̂ = (XᵀX)⁻¹Xᵀy`, the normal equations, and the one-predictor
identity `β̂₁ = Cov(x,y)/Var(x)`, `β̂₀ = ȳ − β̂₁x̄`; **OLS as projection** — `ŷ = Hy`, hat matrix
`H = X(XᵀX)⁻¹Xᵀ`, residuals `(I−H)y` orthogonal to the column space (the direct payoff of Lesson
008's projection geometry); `σ̂² = SSR/(n−p)` and **R²** `= 1 − SSR/SST` (with the finance warning:
tiny R² is normal, high R² on returns usually means leakage); the classical
`Var(β̂) = σ²(XᵀX)⁻¹`, `SE`, and **t-stat** (tying back to Lesson 007); **Gauss–Markov / BLUE** and
the load-bearing caveat "under those assumptions." A fully worked 5-point example
(x=(−2,−1,0,1,2), y=(−1.5,−0.5,0.5,0.5,2.0)) gives β̂₁=0.8, β̂₀=0.2, Σe=0, Σxe=0, σ̂²=0.133,
SE=0.115, t≈6.9, R²≈0.94 — the orthogonality check makes "projection" concrete.

Failure-mode core (two violations, both leave β̂ unbiased — only the SE breaks):
**(1) Heteroskedasticity** (vol clustering, noisy small-caps) → classical SE mis-stated, usually
too small → t too big; fix = **White/HC** SE `Σxc²e²/Sxx²`. **(2) Autocorrelation / overlapping
returns** → effective n shrinks, naïve SE far too small, t inflated by multiples
(√[(1+φ)/(1−φ)] for AR(1)); fix = **Newey–West (HAC)** with Bartlett kernel `1−l/(L+1)`,
`L ≈ h` lags. Trap box also covers spurious regression (non-stationary levels — preview units
021/027), omitted-variable bias, multicollinearity, influential outliers, and leakage.

Pedagogy widgets: spaced-retrieval warm-up (`upTo: 9`); a predict-before-reveal on the
overlapping-monthly-returns t-stat being *too large*; a teach-back on "why β̂ survives but the
t-stat doesn't, and what to do"; four MCQ checks; an objections `<dl>` (robust-SE-everywhere,
why-care-if-β̂-unbiased, OLS-vs-correlation-vs-beta, returns-not-prices, how-many-lags); a no-peek
reflection. Added four `retrieval-pool.js` items (`l009-slope`, `l009-hetero` [misconception],
`l009-overlap` [misconception], `l009-hac`).

Built three reusable visualizations (one per mechanism, per `lesson-visuals`):
`ols-fit-viz.js` (scatter + candidate line through (x̄,ȳ); slider rotates it and SSR bottoms out
exactly at the OLS/projection slope, residuals ⟂ x); `hsk-viz.js` (a ±2σ fan that widens with |x|;
slider raises heteroskedasticity and the White SE pulls away from the classical one while β̂ stays
unbiased — verified numerically: robust/classical SE ratio climbs 0.91→1.24); `hac-viz.js` (AR(1)
error path that visibly "sticks" as φ rises; readout compares naïve, Newey–West, and closed-form
true SE — verified: VIF matches (1+φ)/(1−φ), NW tracks true, naïve stays flat). Added lesson-009
CSS to `assets/lesson.css` and all three viz to `.smoke.js` (all 8 widgets pass). Bumped
`manifest.json` to version 5 (index/notebooks meta → 5) and registered the lesson with `labPath`;
updated the L008 forward nav link. Updated `GLOSSARY.md` (OLS, β̂, R², heteroskedasticity, White SE,
Newey–West), added Wooldridge to `RESOURCES.md` Math foundations and Newey–West 1987 (+ White 1980)
to the papers list, and the labs README index.

Lab verified end-to-end (filled solution executed via nbconvert; all CHECK cells pass, EXIT TICKET
clean): 21-day overlapping forward returns regressed on a persistent signal give a **naïve t ≈ 16.6**
that White barely moves (t ≈ 16.6 — here autocorrelation, not heteroskedasticity, is the violation)
but **Newey–West deflates to t ≈ 6.1** (SE inflation 2.7×), implying only ≈107 independent
observations out of 800 — a visceral demonstration that the standard error, not the slope, was the
lie. Stretch tasks: vary maxlags, non-overlapping baseline (SEs re-agree), spurious random-walk
regression, isolated heteroskedasticity. Teacher solution lives in `solutions/` (gitignored).
