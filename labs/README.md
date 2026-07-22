# Labs

Each unit's exit-ticket lab ships as a Jupyter notebook here, named `NNNN-<slug>.ipynb`
to match its lesson (`lessons/NNNN-<slug>.html`).

## The fill-in convention

| Cell tag | Meaning |
|----------|---------|
| **PROVIDED** | Complete boilerplate (imports, data, helpers). Just run it. |
| **TODO** | Has blanks — `____`. You fill these in. This is where the learning happens. |
| **CHECK** | Auto-runs assertions so you get *immediate* feedback. Don't edit. |
| **EXIT TICKET** | The final deliverable cell. When it prints cleanly, the lab is done. |

Design intent: blanks sit only on the **skill** being practised; everything peripheral is
provided so working memory stays on the one idea. CHECK cells keep the feedback loop tight.
Every lab from Lesson 004 onward opens with a **concept recap** (terms, formulas, a toy worked
example) and a short **goal / why** block before each task, so you can work it without reopening
the lesson HTML.

**No prefilled answers:** TODO cells use `____` only. Teacher copies with filled answers live in
[`../solutions/`](../solutions/) (gitignored).

## Stack

Python-first: `numpy`, `pandas`, `scipy`, `scikit-learn`, `statsmodels`, and later `matplotlib`,
`arch` (GARCH), and `torch` (deep-learning units, Year 2 Q4+). C++/Rust appear only in the
Year-3 systems-awareness track. See [`../requirements-labs.txt`](../requirements-labs.txt).

## Environment (one-time setup)

From the repo root (`financial-engineering/`):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-labs.txt
python -m ipykernel install --user --name feq-labs --display-name "Financial Eng Labs (.venv)"
```

**In Cursor / VS Code:** open a lab → **Select Kernel** → choose `Financial Eng Labs (.venv)` or
the interpreter at `.venv/bin/python`.

## Data

Early labs are **self-contained**: they try real data (e.g. `yfinance`) and fall back to a
realistic simulation so they run offline. Year 2 Q3 microstructure labs need real LOB data —
secure LOBSTER / Databento / the FI-2010 benchmark before Unit 062 (tracked in `../NOTES.md`).

## Index

- `0004-returns-stylized-facts.ipynb` — compute log returns; verify fat tails, absent linear
  autocorrelation, and volatility clustering; contrast with an IID-Gaussian series (Lesson 004).
- `0006-bootstrap-sharpe-ci.ipynb` — bootstrap a 95% confidence interval for a strategy's Sharpe
  ratio; compare to the i.i.d.-normal (Lo) formula; widen it honestly with a block bootstrap that
  respects autocorrelation (Lesson 006).
- `0007-false-discoveries.ipynb` — simulate a universe of zero-edge strategies; measure the
  false-discovery rate and confirm the FWER formula; apply Bonferroni and Benjamini-Hochberg; then
  expose the selection bias of reporting the best-of-M t-stat (Lesson 007).
- `0008-pca-returns-panel.ipynb` — build a returns panel's correlation matrix by hand,
  eigendecompose it, confirm the trace identity, show PC1 is the (same-sign) market factor, and
  measure how many components capture 90% of the panel's risk (Lesson 008).
- `0009-robust-standard-errors.ipynb` — regress overlapping returns on a signal; confirm OLS is
  projection (residuals ⟂ X) and `β̂ = Cov/Var` by hand; then watch a gaudy naïve t-statistic
  deflate under White (HC) and Newey–West (HAC) standard errors, and translate the SE inflation
  into an effective sample size (Lesson 009).
- `0010-checkpoint-spurious-signal.ipynb` — **Q1 checkpoint.** Audit a returns-analysis notebook
  that "discovered" a signal with a gaudy t-statistic: run White (HC), Newey–West (HAC), the
  effective sample size, the best-of-*M* selection haircut, and a Monte-Carlo empirical null, then
  deliver a kill/confirm verdict on a *planted spurious* signal (Lesson 010).

_More labs are added as lessons are published (see the per-lesson lab links on the home page)._

## Reproduction labs build incrementally (from Year 2)

Concept labs are self-contained. Paper-reproduction / experiment labs (CPCV, DeepLOB, RL
execution) will build on a shared, importable package (`labs/feqkit/`) — data loaders, the
CV/eval harness, leakage-safe pipelines, metrics — so each lab leaves the harness stronger and
the thesis baselines trustworthy by the time results matter.
