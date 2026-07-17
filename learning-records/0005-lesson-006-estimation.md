# Lesson 006 published — Estimation & Inference

Shipped **Lesson 006 — "Estimation & Inference: From Data to Honest Uncertainty"**
(`lessons/0006-estimation-inference.html`) and its lab
(`labs/0006-bootstrap-sharpe-ci.ipynb`, deliverable: bootstrap a Sharpe-ratio CI).

Covers Wasserman Ch. 6–9: estimand/estimator/estimate and the sampling distribution; bias,
variance, standard error; the **MSE = bias² + variance** decomposition (and why a biased
estimator can win → shrinkage); consistency and the **√n rate** (with the effective-sample-size
caveat under autocorrelation); **maximum likelihood** (log-likelihood, Bernoulli p̂ = k/n
worked, consistency/asymptotic-normality/equivariance, Fisher information as curvature);
**confidence intervals** and their correct frequentist reading; and the **bootstrap**
(plug-in principle, resample-with-replacement, percentile CI). Failure-mode trap: i.i.d. error
bars (formula *and* plain bootstrap) understate uncertainty on dependent financial data →
block bootstrap / Lo's adjustment, plus a forward pointer to multiple testing (Lesson 007).

Pedagogy widgets: spaced-retrieval warm-up (`upTo: 6`), a predict-before-reveal on the √n rate,
a teach-back on "what a 95% CI means + why the bootstrap works," four MCQ checks, an objections
`<dl>`, and a no-peek reflection. Added five `retrieval-pool.js` items (`l006-mse`, `l006-sqrtn`,
`l006-ci` [misconception], `l006-bootstrap`, `l006-mle`).

Built four reusable canvas visualizations (one per mechanism, per the `lesson-visuals` skill):
`biasvariance-viz.js` (dartboard), `likelihood-viz.js` (MLE curve sharpening with n → Fisher
information & CI width), `ci-coverage-viz.js` (20 intervals vs the true value → the meaning of
"95%"), and `bootstrap-viz.js` (resample-with-replacement building a Sharpe distribution + CI).
Verified in headless Chrome (desktop + 375px), no console errors. Bumped `manifest.json` to
version 2 and registered the lesson (with `labPath`).

## Standing decision recorded (applies to all future lessons)
Per the user's instruction: **explain everything a lesson introduces, in full — even if that
makes lessons longer.** Encoded in `NOTES.md` ("Standing decision — explain everything
introduced") and `.agents/skills/lesson-pedagogy/SKILL.md` ("Explain everything you introduce").
Treat the ~22–30 KB / ~55–60 min band as a floor for depth, not a cap.
