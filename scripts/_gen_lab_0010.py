"""Generate labs/0010-checkpoint-spurious-signal.ipynb (blanks) and its filled solution.

Run:  ./.venv/bin/python scripts/_gen_lab_0010.py
"""
import json, copy, os

def md(src):
    return {"cell_type": "markdown", "metadata": {}, "source": src.splitlines(keepends=True)}

def code(src):
    return {"cell_type": "code", "metadata": {}, "execution_count": None,
            "outputs": [], "source": src.rstrip("\n").splitlines(keepends=True)}

cells = []

cells.append(md(
"""# Lab 010 — Q1 Checkpoint: is this signal real, or spurious?

**Lesson:** [`0010-q1-checkpoint.html`](../lessons/0010-q1-checkpoint.html)

**The one skill (the whole quarter):** you are handed a returns-analysis notebook that has
*already discovered* a signal predicting next month's return, with a **headline t-statistic that
looks spectacular**. Nobody tells you whether it is real. Run the full **statistical-hygiene
audit** — heteroskedasticity (White), autocorrelation/overlap (Newey–West), effective sample size,
the best-of-*M* selection haircut, and a proper empirical null — then deliver a verdict: **real, or
spurious?** One signal here is *planted* to fool the analyst who stops at t = 1.96.

**Exit criteria:** every CHECK passes and the EXIT TICKET prints the correct verdict (spurious),
naming *which* audits killed it.

**How this notebook works**

| Cell tag | You do |
|----------|--------|
| **PROVIDED** | Run it. Imports, the \"research\" data, helpers. |
| **TODO** | Fill the `____` blanks. This is where the learning is. |
| **CHECK** | Run it — immediate assertions. Don't edit. |
| **EXIT TICKET** | Final deliverable. Prints your verdict. |

**Environment:** Python 3 + `numpy` + `scipy` + `statsmodels`. Fully self-contained (simulated —
no network). One cell runs a small Monte-Carlo null (~15–30 s). See [`labs/README.md`](./README.md)."""))

cells.append(md(
"""### Running on Google Colab?

Colab opens only this single file, so the lab dependencies (numpy, scipy, statsmodels, …) and
the course repo are **not** guaranteed to be present. The cell below fixes that: on Colab it
shallow-clones the course repo, installs `requirements-labs.txt`, and switches into `labs/` so
relative paths resolve. **On a local venv or Binder it does nothing — just run it and continue.**"""))

cells.append(code(
"""# @colab-bootstrap — PROVIDED. Makes the lab self-sufficient on Google Colab; a no-op elsewhere.
import os, sys

if "google.colab" in sys.modules:
    if not os.path.isdir("/content/financial-engineering"):
        !git clone --depth 1 https://github.com/Avistian/financial-engineering.git /content/financial-engineering
    %pip install -q -r /content/financial-engineering/requirements-labs.txt
    os.chdir("/content/financial-engineering/labs")
    print("Colab ready — working dir:", os.getcwd())
else:
    print("Not on Colab — using the local environment as-is.")"""))

cells.append(md(
r"""## Concept recap — the five questions (read before coding)

You are auditing a claimed edge. In **every** failure mode below the point estimate $\hat\beta$ can
be fine — it is the **standard error**, and therefore the **t-statistic (your claim)**, that lies.

| # | Question | Failure mode | The test |
|---|----------|--------------|----------|
| 1 | Measurable? | edge smaller than its SE | $SE\propto 1/\sqrt n$; CI excludes 0 |
| 2 | How many tried? | selection / multiple testing | fair bar = $E[\max\text{ of }M]$, not 1.96 |
| 3 | Independent obs? | autocorrelation / overlap | **Newey–West** SE; $n_\text{eff}=n/\text{inflation}^2$ |
| 4 | Constant variance? | heteroskedasticity | **White / HC** SE |
| 5 | Future leaked? | look-ahead / non-stationary | temporal discipline; regress *returns* |

**The autopsy chain:** $\;t_\text{reported}\;\to\;t_\text{NW}=t_\text{reported}/\sqrt{(1+\varphi)/(1-\varphi)}\;\to\;t_\text{survives}=t_\text{NW}-E[\max\text{ of }M].$

**Ground truth of this lab (so you can grade yourself):** the daily returns are **pure
heteroskedastic noise with zero true edge** from any signal. Every \"discovery\" here is therefore
spurious *by construction* — the audit must be able to *reveal* that without being told."""))

cells.append(code(
'''# PROVIDED — the "research notebook" you were handed. Run it; do not change it.
# A junior researcher searched M persistent signals for one that predicts the next month's
# (h=21-day) return, sampled DAILY so the forward windows overlap. They report the best signal's
# naive t-statistic and are ready to trade. You know (they do not) that returns are pure noise.
import numpy as np
import statsmodels.api as sm
from scipy import stats, integrate

def build_research_case(seed=2024, n=800, h=21, M=60):
    rng = np.random.default_rng(seed)
    T = n + h + 1
    # Daily returns: PURE NOISE with volatility clustering (heteroskedastic), NO signal edge.
    lv = np.zeros(T)
    for t in range(1, T):
        lv[t] = 0.9 * lv[t-1] + rng.normal(0, 1)
    vol = 0.01 * (1 + 0.5 * np.abs((lv - lv.mean()) / lv.std()))
    daily_ret = vol * rng.normal(0, 1, size=T)
    # Overlapping h-day FORWARD return aligned to each day t.
    y = np.array([daily_ret[t+1:t+1+h].sum() for t in range(n)])
    # M candidate persistent (AR(1)) signals, all INDEPENDENT of returns.
    sigs = np.zeros((M, n))
    for j in range(M):
        s = np.zeros(T)
        for t in range(1, T):
            s[t] = 0.95 * s[t-1] + rng.normal(0, 1)
        sigs[j] = ((s - s.mean()) / s.std())[:n]
    # The search: pick the signal with the biggest naive |t| (this is the "discovery").
    naive_t = np.array([sm.OLS(y, sm.add_constant(sigs[j])).fit().tvalues[1] for j in range(M)])
    best = int(np.argmax(np.abs(naive_t)))
    return y, sigs[best], best, naive_t, n, h, M

y, x, best_j, naive_t, n, h, M = build_research_case()
print(f"Searched M = {M} signals over n = {n} overlapping {h}-day windows.")
print(f"WINNER: signal #{best_j}  ->  headline naive t = {naive_t[best_j]:.2f}   (looks amazing!)")
print(f"(for context, |t| of the M candidates ranged {np.abs(naive_t).min():.1f} to {np.abs(naive_t).max():.1f})")


def expected_max_normal(M):
    """E[max of M i.i.d. standard normals] — the fair 'best-of-M' bar under the null."""
    if M <= 1:
        return 0.0
    f = lambda z: z * M * stats.norm.pdf(z) * stats.norm.cdf(z) ** (M - 1)
    val, _ = integrate.quad(f, -8, 10, limit=200)
    return val'''))

# ---- Task 1 ----
cells.append(md(
r"""### Task 1 — Reproduce the headline t (the naïve claim)
**Goal:** regress the overlapping forward return `y` on the winning signal `x` with plain OLS and
read off the naïve slope t-statistic. Store `t_classical` and `se_classical`.

**Why:** this is the number the researcher is excited about. Everything after this is you refusing
to take it at face value.

**Hint boundary:** `t_classical = fit.tvalues[1]`, `se_classical = fit.bse[1]`."""))

cells.append(code(
'''# TODO — reproduce the naive OLS t-statistic on the winning signal.
X = sm.add_constant(x)
fit = sm.OLS(y, X).fit()
beta1 = fit.params[1]
t_classical = ____                    # fit.tvalues[1]
se_classical = ____                   # fit.bse[1]
print(f"beta1 = {beta1:.4f},  classical SE = {se_classical:.4f},  naive t = {t_classical:.2f}")'''))

cells.append(code(
'''# CHECK — do not edit
assert abs(t_classical) > 6, "the headline naive t should be gaudy (the search + overlap saw to that)"
assert np.isclose(t_classical, fit.tvalues[1]) and np.isclose(se_classical, fit.bse[1])
print(f"Task 1 OK — reproduced the headline: naive |t| = {abs(t_classical):.1f}. Now audit it.")'''))

# ---- Task 2 ----
cells.append(md(
r"""### Task 2 — Question 4: heteroskedasticity (White / HC)
**Goal:** recompute the slope's SE with **White HC1** robust errors. Store `se_white`, `t_white`.

**Why:** returns cluster in volatility, so heteroskedasticity is the prime suspect. But watch what
happens — if White barely moves the t, that near-equality is itself a **diagnostic**: the problem
is *not* variance, it is dependence (Task 3).

**Hint boundary:** `fit_white = fit.get_robustcov_results(cov_type="HC1")`, `se_white = fit_white.bse[1]`."""))

cells.append(code(
'''# TODO — White (heteroskedasticity-robust) SE.
fit_white = fit.get_robustcov_results(cov_type="HC1")
se_white = ____                       # fit_white.bse[1]
t_white = fit_white.tvalues[1]
print(f"classical : SE = {se_classical:.4f},  t = {t_classical:.2f}")
print(f"White HC1 : SE = {se_white:.4f},  t = {t_white:.2f}   (ratio White/classical = {se_white/se_classical:.2f})")'''))

cells.append(code(
'''# CHECK — do not edit
assert se_white > 0 and np.isfinite(t_white)
assert abs(se_white / se_classical - 1) < 0.25, "White ~ classical here: heteroskedasticity is NOT the main issue"
print("Task 2 OK — White barely moves the t. That is a clue: the culprit is autocorrelation, not variance.")'''))

# ---- Task 3 ----
cells.append(md(
r"""### Task 3 — Question 3: overlap / autocorrelation (Newey–West) and effective n
**Goal:** recompute the SE with **Newey–West (HAC)** using `maxlags = h`, then convert the SE
inflation into an **effective sample size**. Store `se_nw`, `t_nw`, `inflation`, `n_eff`.

**Why:** consecutive 21-day windows share 20 days, so the errors are massively autocorrelated and
the naïve SE is far too small. Newey–West restores an honest (larger) SE; `n_eff = n / inflation²`
tells you how few *independent* observations you truly had.

**Hint boundary:** `fit_nw = fit.get_robustcov_results(cov_type="HAC", maxlags=h, use_correction=True)`;
`inflation = se_nw / se_classical`; `n_eff = n / inflation**2`."""))

cells.append(code(
'''# TODO — Newey-West (HAC) SE + effective sample size.
fit_nw = fit.get_robustcov_results(cov_type="HAC", maxlags=h, use_correction=True)
se_nw = ____                          # fit_nw.bse[1]
t_nw = fit_nw.tvalues[1]
inflation = se_nw / se_classical
n_eff = ____                          # n / inflation**2
print(f"Newey-West: SE = {se_nw:.4f},  t = {t_nw:.2f}   (maxlags = {h})")
print(f"SE inflation = {inflation:.2f}x   ->   n_eff = {n_eff:.0f} independent obs (out of {n})")'''))

cells.append(code(
'''# CHECK — do not edit
assert se_nw > 1.5 * se_classical, "with 21-day overlap the HAC SE should dwarf the naive one"
assert abs(t_nw) < abs(t_classical), "the naive t must deflate once autocorrelation is accounted for"
assert n_eff < n
print(f"Task 3 OK — the headline t deflated to {t_nw:.2f}; you really had ~{n_eff:.0f} independent obs.")'''))

# ---- Task 4 ----
cells.append(md(
r"""### Task 4 — Question 2: the best-of-*M* selection haircut
**Goal:** the reported signal was the **winner of a search over M candidates**, so the fair bar is
not 1.96 — it is `E[max of M]` draws under the null. Compute the **surviving margin**
`surviving = |t_nw| - E[max of M]`. Store `emax` and `surviving`.

**Why:** picking the best of many noisy tries manufactures large statistics for free (Lesson 007).
Only the margin *above* the best-of-M bar is potential evidence.

**Hint boundary:** `emax = expected_max_normal(M)`; `surviving = abs(t_nw) - emax`."""))

cells.append(code(
'''# TODO — subtract the fair best-of-M null bar.
emax = expected_max_normal(M)         # E[max of M standard normals]
surviving = ____                      # abs(t_nw) - emax
print(f"best-of-{M} bar  E[max] = {emax:.2f}")
print(f"surviving margin = |t_nw| - E[max] = {abs(t_nw):.2f} - {emax:.2f} = {surviving:.2f}")'''))

cells.append(code(
'''# CHECK — do not edit
assert emax > 1.5, "E[max of 60 normals] should be well above the single-test 1.96"
assert surviving < 1.96, "after de-overlapping AND the selection haircut, the signal must not clear the bar"
print(f"Task 4 OK — surviving margin {surviving:.2f} < 1.96: the 'edge' does not clear an honest bar.")'''))

# ---- Task 5 ----
cells.append(md(
r"""### Task 5 — The decisive test: a proper empirical null (kill or confirm)
**Goal:** the analytic haircut is a shortcut; the rigorous test is to simulate the *whole search
under the null* and ask how often pure noise produces a best-of-M Newey–West |t| at least as big
as ours. Compute a Monte-Carlo `p_value` and set the verdict `is_spurious`.

**Why:** this fuses Lesson 007 (multiple testing) and Lesson 009 (HAC) into one honest number — the
probability that the whole *procedure* (search + overlap) fakes a result this good with no edge at
all. A large p-value means "indistinguishable from noise."

**Hint boundary:** `p_value = (np.sum(null_best >= abs(t_nw)) + 1) / (len(null_best) + 1)`;
`is_spurious = p_value > 0.10`. (The null is PROVIDED; ~15–30 s to run.)"""))

cells.append(code(
'''# PROVIDED — simulate the best-of-M Newey-West |t| under NO edge (fresh noise each rep). ~15-30s.
def best_of_M_nw_t_under_null(rng, n=n, h=h, M=M):
    T = n + h + 1
    lv = np.zeros(T)
    for t in range(1, T):
        lv[t] = 0.9 * lv[t-1] + rng.normal(0, 1)
    vol = 0.01 * (1 + 0.5 * np.abs((lv - lv.mean()) / lv.std()))
    daily = vol * rng.normal(0, 1, size=T)
    yy = np.array([daily[t+1:t+1+h].sum() for t in range(n)])
    best = 0.0
    for j in range(M):
        s = np.zeros(T)
        for t in range(1, T):
            s[t] = 0.95 * s[t-1] + rng.normal(0, 1)
        xx = ((s - s.mean()) / s.std())[:n]
        f = sm.OLS(yy, sm.add_constant(xx)).fit()
        fn = f.get_robustcov_results(cov_type="HAC", maxlags=h, use_correction=True)
        best = max(best, abs(fn.tvalues[1]))
    return best

rng_null = np.random.default_rng(0)
null_best = np.array([best_of_M_nw_t_under_null(rng_null) for _ in range(200)])
print(f"null best-of-{M} NW |t|: mean {null_best.mean():.2f}, 95th pct {np.quantile(null_best,0.95):.2f}, max {null_best.max():.2f}")'''))

cells.append(code(
'''# TODO — turn the empirical null into a p-value and a verdict.
p_value = ____                        # (np.sum(null_best >= abs(t_nw)) + 1) / (len(null_best) + 1)
is_spurious = ____                    # p_value > 0.10
print(f"observed best-of-{M} NW |t| = {abs(t_nw):.2f}")
print(f"empirical p-value = {p_value:.3f}   ->   is_spurious = {is_spurious}")'''))

cells.append(code(
'''# CHECK — do not edit
assert 0 < p_value <= 1
assert is_spurious, "the winning signal is noise by construction; a proper null must fail to reject"
print(f"Task 5 OK — p = {p_value:.2f}: the headline is exactly what a search over pure noise produces.")'''))

# ---- EXIT ----
cells.append(code(
'''# EXIT TICKET — paste this output to your teacher.
print("=== Q1 CHECKPOINT: spurious-signal autopsy ===")
print(f"Claim              : signal #{best_j} predicts {h}-day fwd returns  (searched M = {M})")
print(f"Q1 measurable?     : n = {n} overlapping obs, but effective n_eff = {n_eff:.0f}")
print(f"Q4 heteroskedastic?: White t = {t_white:.2f}  vs classical {t_classical:.2f}  -> not the issue")
print(f"Q3 overlap/autocorr: Newey-West t = {t_nw:.2f}  (SE inflated {inflation:.1f}x)  <- big deflation")
print(f"Q2 selection (M={M}): E[max] bar = {emax:.2f}  ->  surviving margin = {surviving:.2f}")
print(f"Decisive null test : empirical p = {p_value:.2f}  (best-of-M under pure noise)")
print()
print(f"VERDICT: {'SPURIOUS - do not trade' if is_spurious else 'survives - investigate further'}")
print()
print("One-sentence defense (edit me):")
print(f"A headline t of {abs(t_classical):.0f} collapsed to an honest t of {abs(t_nw):.1f} once 21-day overlap was")
print(f"accounted for (n_eff ~ {n_eff:.0f}), and even that is a routine best-of-{M} outcome under pure noise")
print(f"(p = {p_value:.2f}) - the standard error and the silent search, not the slope, were the lie.")'''))

# ---- Stretch ----
cells.append(md(
r"""### Stretch (optional, ungraded)
- **Non-overlapping baseline.** Rebuild `y` sampling every `h`-th day (no overlap) and re-audit the
  same winning signal: classical and Newey–West SEs should now roughly agree and `n_eff ≈ n`. The
  cleanest fix is not to overlap in the first place.
- **Vary M.** Re-run `build_research_case` with `M ∈ {1, 5, 20, 100}` and watch the headline naïve t
  climb purely because you searched harder — while the empirical p-value stays unremarkable.
- **Spurious regression (Q5).** Regress one random-walk *level* (`np.cumsum` of noise) on another,
  independent one. Watch a huge R² and |t| > 4 appear between two unrelated series — then confirm it
  vanishes when you regress their *differences* (returns). This is Q3 (units 021/027) previewed.
- **Plant a real edge.** Add a tiny true slope (`y += 0.02 * x`) to the winner and re-audit: now the
  Newey–West t and the empirical p-value should tell a different, honest story. Prove to yourself the
  audit does not kill *everything* — only the unearned claims."""))

nb = {"cells": cells,
      "metadata": {"kernelspec": {"display_name": "Financial Eng Labs (.venv)",
                                   "language": "python", "name": "feq-labs"},
                   "language_info": {"name": "python", "version": "3.12"}},
      "nbformat": 4, "nbformat_minor": 5}

lab_path = "labs/0010-checkpoint-spurious-signal.ipynb"
with open(lab_path, "w") as f:
    json.dump(nb, f, indent=1)
    f.write("\n")
print("wrote", lab_path)

# ---- Build the filled SOLUTION by replacing the ____ blanks with the hinted answers ----
answers = {
    "t_classical = ____": "t_classical = fit.tvalues[1]",
    "se_classical = ____": "se_classical = fit.bse[1]",
    "se_white = ____": "se_white = fit_white.bse[1]",
    "se_nw = ____": "se_nw = fit_nw.bse[1]",
    "n_eff = ____": "n_eff = n / inflation**2",
    "surviving = ____": "surviving = abs(t_nw) - emax",
    "p_value = ____": "p_value = (np.sum(null_best >= abs(t_nw)) + 1) / (len(null_best) + 1)",
    "is_spurious = ____": "is_spurious = p_value > 0.10",
}
sol = copy.deepcopy(nb)
for c in sol["cells"]:
    if c["cell_type"] != "code":
        continue
    new = []
    for line in c["source"]:
        for k, v in answers.items():
            if line.lstrip().startswith(k):
                indent = line[:len(line) - len(line.lstrip())]
                # keep any trailing inline comment after the original blank
                comment = ""
                if "#" in line:
                    comment = "  # " + line.split("#", 1)[1].strip()
                line = indent + v + comment + ("\n" if line.endswith("\n") else "")
                break
        new.append(line)
    c["source"] = new

os.makedirs("solutions", exist_ok=True)
sol_path = "solutions/0010-checkpoint-spurious-signal.ipynb"
with open(sol_path, "w") as f:
    json.dump(sol, f, indent=1)
    f.write("\n")
print("wrote", sol_path)
