# Lesson 008 published — Linear Algebra for Quants: Covariance, Eigendecomposition, PCA

Shipped **Lesson 008 — "Linear Algebra for Quants: Covariance, Eigendecomposition, PCA"**
(`lessons/0008-linear-algebra-pca.html`) and its lab (`labs/0008-pca-returns-panel.ipynb`,
deliverable: PCA of a returns panel by hand). Covers Unit 008 (Strang *Introduction to Linear
Algebra* for the geometry; Axler for the spectral theorem). This opens the linear-algebra pillar of
Year 1 Q1, alongside the statistics thread (004→007).

Concepts, each fully explained with a worked numeric example (per the standing "explain everything
you introduce" decision): the returns panel as an `n×d` matrix; portfolio variance `wᵀΣw`; centering
vs standardizing; **covariance** (with Bessel's `n−1`) and the **covariance matrix**
`Σ = (1/(n−1)) X̃ᵀX̃` (symmetric, PSD); covariance vs **correlation** and the scale trap;
**eigenvectors/eigenvalues** (`Mv = λv`) as the "only-stretched, not-rotated" directions; the
**spectral theorem** (symmetric ⇒ real λ, orthogonal eigenvectors) and eigendecomposition
`Σ = QΛQᵀ`; a fully worked 2×2 decomposition of `Σ = [[2.5,2.0],[2.0,2.0]]` → λ₁≈4.27, λ₂≈0.23,
PC1≈(0.75,0.66), trace conserved (4.5); **PCA** = sorted eigendecomposition of Σ, each PC an
uncorrelated portfolio; **variance explained** `λ_k/tr(Σ)`; the **scree plot** and the
**market factor** via the closed-form equicorrelation spectrum `λ₁ = 1+(d−1)ρ`, `λ₂..=1−ρ`
(so crises `ρ→1` ⇒ `λ₁→d`, diversification fails); **projection/scores** `Z = X̃Q` and
best-rank-k **reconstruction** (Eckart–Young); SVD↔PCA equivalence.

Failure-mode trap (4 ways PCA lies): (1) **scale** — decompose the correlation matrix / standardize;
(2) **non-stationarity** — Σ drifts, crises spike ρ; (3) **noise eigenvalues** — most small λ are
estimation noise (Marchenko–Pastur / Ledoit–Wolf preview, units 082–083); (4) **leakage** — fitting
PCA on the full sample is look-ahead in a backtest.

Pedagogy widgets: spaced-retrieval warm-up (`upTo: 8`); a predict-before-reveal on PC1's variance
share at ρ=0.9 (→95%); a teach-back on "what is PC1 / why is it the market / what does a rising share
mean"; four MCQ checks; an objections `<dl>` (statistical vs economic factors, SVD vs eig, sign
ambiguity, how many PCs, index vs PCA); a no-peek reflection. Added four `retrieval-pool.js` items
(`l008-eigen`, `l008-var-explained`, `l008-scale` [misconception], `l008-market-factor`).

Built two reusable visualizations (one per mechanism, per `lesson-visuals`):
`covariance-ellipse-viz.js` (2D returns cloud + 2σ covariance ellipse + PC1/PC2 eigenvector arrows,
ρ slider showing the ellipse collapse to a line) and `scree-viz.js` (closed-form equicorrelation
scree bars + cumulative-% line, ρ slider showing PC1 devour the panel). Added lesson-008 CSS to
`assets/lesson.css`. Bumped `manifest.json` to version 4 and registered the lesson (with `labPath`).
Updated `GLOSSARY.md` (covariance matrix, eigenvector/eigenvalue, PCA, variance explained, market
factor), added a **Math foundations** section to `RESOURCES.md` (Strang, Axler, Wasserman), and the
labs README index.

Lab verified: the filled solution runs and all CHECK cells pass on the simulated factor panel — PC1
share ≈65%, PC1↔true-market corr ≈0.98, PC scores uncorrelated, trace identity holds, 8/12 PCs for
90%. Next is Unit 009 (Regression done right — OLS as projection, the same geometry).

Also in this session: fixed the notebook Colab/Binder running path (see the notebooks-infra change) —
`labs/html/` was empty so the home-page "lab" links 404'd. Added the relational-style running stack.
