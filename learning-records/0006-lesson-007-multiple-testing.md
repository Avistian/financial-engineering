# Lesson 007 published — Hypothesis Testing & the Multiple-Testing Trap

Shipped **Lesson 007 — "Hypothesis Testing & the Multiple-Testing Trap"**
(`lessons/0007-hypothesis-multiple-testing.html`) and its lab
(`labs/0007-false-discoveries.ipynb`, deliverable: simulate false discoveries under many trials).

Covers Unit 007 (Harvey-Liu-Zhu 2016 ★, plus Wasserman Ch. 10 for the testing mechanics): the
hypothesis-testing frame (H₀/H₁, reject vs fail-to-reject); the **t-statistic** as signal/noise and
the load-bearing identity **t = SR_annual·√years** (worked: Sharpe-1 over 3 yrs → t≈1.73, below 1.96);
the **p-value** with its exact definition and the P(data|H₀) ≠ P(H₀|data) misreading; **Type I/II
errors and power**; the **multiple-testing trap** (p-values are Uniform(0,1) under H₀; FWER =
1−(1−α)^M, worked at M=100 → 99.4%); **Bonferroni** (α/M, FWER control, over-conservative under
correlation); **FDR / Benjamini-Hochberg** step-up (worked example, k=4 vs Bonferroni's 1) and
**BHY** under dependence; the **Sharpe/t-stat haircut** and HLZ's ≈ t>3.0 hurdle, with a forward
pointer to the deflated Sharpe ratio (unit 055) and CPCV (Year 2).

Failure-mode trap: reporting the best of many backtests (selection bias); max of M nulls grows like
√(2 ln M); data snooping, p-hacking, publication/survivorship bias → always report the trial count M.

Pedagogy widgets: spaced-retrieval warm-up (`upTo: 7`); a predict-before-reveal on the 99% FWER of
100 worthless tests; a teach-back on "how many strategies did you try?"; four MCQ checks; an
objections `<dl>`; a no-peek reflection. Added four `retrieval-pool.js` items (`l007-pvalue`
[misconception], `l007-t-sharpe`, `l007-fwer`, `l007-bonf-bh`).

Built three reusable canvas visualizations (one per mechanism, per `lesson-visuals`):
`pvalue-viz.js` (null curve with draggable |t| and shaded two-sided tail = p-value, ±1.96 fences),
`multiple-testing-viz.js` (a field of M zero-edge strategies; ~5% light up red at nominal α; M slider
and a Bonferroni toggle that collapses the false positives), and `haircut-viz.js` (required |t| vs
number of trials on a log axis, with the single-test 1.96 and HLZ ≈3.0 reference lines). Added
lesson-007 CSS to `assets/lesson.css`. Bumped `manifest.json` to version 3 and registered the lesson
(with `labPath`). Updated `GLOSSARY.md` (p-value, t-statistic, FWER, FDR, multiple testing rows) and
the labs README index.

Standing decision still in force (from Lesson 006): explain everything a lesson introduces, in full —
every symbol defined on the spot, worked numeric examples throughout. This lesson closes the
statistics thread of Year 1 Q1 (004 → 005 → 006 → 007); next is Unit 008.
