"""Generate labs/0013-ito-lemma.ipynb (blanks) and its filled solution.

Run:  ./.venv/bin/python scripts/_gen_lab_0013.py
"""
import json, copy, os

def md(src):
    return {"cell_type": "markdown", "metadata": {}, "source": src.splitlines(keepends=True)}

def code(src):
    return {"cell_type": "code", "metadata": {}, "execution_count": None,
            "outputs": [], "source": src.rstrip("\n").splitlines(keepends=True)}

cells = []

cells.append(md(
"""# Lab 013 — The Itô integral &amp; Itô's lemma

**Lesson:** [`0013-ito-lemma.html`](../lessons/0013-ito-lemma.html)
· **Reference:** [`ito-lemma.html`](../reference/ito-lemma.html)

**The one skill:** apply Itô's lemma and *verify it numerically* rather than taking it on faith. By the
end you will have checked, with numbers, that (1) simulated geometric Brownian motion carries the
**−½σ²** correction, (2) `d(W²) = 2W dW + dt` — the Itô integral `∫2W dW` is a **martingale** and the
drift the naive chain rule misses is exactly the **quadratic variation → t**, (3) `log S` drifts at
**μ − ½σ²**, not μ, (4) `d(S²)` grows at **2μ + σ²**, (5) the **mean beats the median** by the
volatility drag, and (6) the correction appears for a *different* function too — `E[e^{W_t}] = e^{t/2}`.

**Exit criteria:** every CHECK passes and the EXIT TICKET prints cleanly.

**How this notebook works**

| Cell tag | You do |
|----------|--------|
| **PROVIDED** | Run it. Imports, the simulator, helpers. |
| **TODO** | Fill the `____` blanks. This is where the learning is. |
| **CHECK** | Run it — immediate assertions. Don't edit. |
| **EXIT TICKET** | Final deliverable. Prints your summary. |

**Environment:** Python 3 + `numpy` only. Fully self-contained (no network, runs in seconds).
See [`labs/README.md`](./README.md)."""))

cells.append(md(
"""### Running on Google Colab?

Colab opens only this single file, so the lab dependencies and the course repo are **not**
guaranteed to be present. The cell below fixes that: on Colab it shallow-clones the course repo,
installs `requirements-labs.txt`, and switches into `labs/` so relative paths resolve. **On a local
venv or Binder it does nothing — just run it and continue.**"""))

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
r"""## Concept recap (read before coding)

**The keep/drop rule.** Over a tiny step, $(dW)^2 = dt$ (kept — Lesson 012), while $dW\,dt$ and $(dt)^2$
vanish. Everything below is that one substitution inside a Taylor expansion.

**Itô's lemma.**

| Case | Formula |
|------|---------|
| $f(W)$ | $df = f'(W)\,dW + \tfrac12 f''(W)\,dt$ |
| Itô process | $dX = a\,dt + b\,dW$, so $(dX)^2 = b^2\,dt$ |
| $f(t,X)$ | $df = \big(f_t + a\,f_x + \tfrac12 b^2 f_{xx}\big)dt + b\,f_x\,dW$ |

The $dW$ term is always a **martingale** (mean 0); all drift is in the $dt$ bracket. The **Itô
correction** $\tfrac12 b^2 f_{xx}$ has the sign of the curvature.

**Geometric Brownian motion.** $dS = \mu S\,dt + \sigma S\,dW$ solves to
$S_t = S_0 \exp\!\big((\mu - \tfrac12\sigma^2)t + \sigma W_t\big)$. Facts you will check:

| Function | Itô says $d(\cdot)$ = | Consequence |
|----------|----------------------|-------------|
| $W^2$ | $2W\,dW + dt$ | $W_t^2 = \int 2W\,dW + t$, so $E[W_t^2]=t$ |
| $\log S$ | $(\mu - \tfrac12\sigma^2)dt + \sigma\,dW$ | log-price drifts at $\mu - \tfrac12\sigma^2$ |
| $S^2$ | $(2\mu + \sigma^2)S^2\,dt + 2\sigma S^2\,dW$ | $E[S_t^2]$ grows at $2\mu + \sigma^2$ |
| $e^{W}$ | $e^{W}\,dW + \tfrac12 e^{W}\,dt$ | $E[e^{W_t}] = e^{t/2}$ |

**Volatility drag.** Mean price grows at $\mu$; the typical (median) path grows at $\mu - \tfrac12\sigma^2$."""))

cells.append(code(
"""# PROVIDED — RNG, market parameters, and the Brownian-motion simulator. Run it.
import numpy as np

rng = np.random.default_rng(20130525)

S0    = 100.0    # starting price
MU    = 0.08     # drift  (average growth rate, per unit time)
SIGMA = 0.20     # volatility (size of the random wiggle)
T     = 1.0      # horizon
N_PATHS = 60000
N_STEPS = 250
dt = T / N_STEPS
tgrid = np.linspace(0.0, T, N_STEPS + 1)   # shape (N_STEPS+1,)

def sample_bm(n_paths, n_steps, T, rng):
    \"\"\"n_paths Brownian paths on [0, T], shape (n_paths, n_steps+1), W[:,0]=0.\"\"\"
    dt = T / n_steps
    incr = rng.standard_normal((n_paths, n_steps)) * np.sqrt(dt)   # N(0, dt)
    W = np.zeros((n_paths, n_steps + 1))
    W[:, 1:] = np.cumsum(incr, axis=1)
    return W

W = sample_bm(N_PATHS, N_STEPS, T, rng)   # the SAME Brownian paths drive every task
dW = np.diff(W, axis=1)                    # increments, shape (N_PATHS, N_STEPS)
print("numpy", np.__version__, "| paths", N_PATHS, "| steps", N_STEPS, "| dt", dt)
print("Var(W_T) =", round(W[:, -1].var(), 4), "(should be ~ T =", T, ")")"""))

# ---- Task 1 ----
cells.append(md(
r"""### Task 1 — Simulate GBM with the Itô-corrected drift

**Goal:** build the geometric-Brownian-motion price
$S_t = S_0\exp\!\big((\mu - \tfrac12\sigma^2)t + \sigma W_t\big)$ from the Brownian paths `W`.

**Why:** this solved form *is* Itô's lemma applied to $\log S$ (you will confirm the drift in Task 3).
The $-\tfrac12\sigma^2$ is the correction; leave it out and every simulated price drifts too high.

**Hint boundary:** the exponent is `drift_t + SIGMA * W`, where `drift_t = (mu - ½σ²)·tgrid` broadcast
across time. Fill the corrected drift coefficient."""))

cells.append(code(
"""# TODO — the Itô-corrected log-drift of GBM.
drift_coef = ____                          # MU - 0.5 * SIGMA**2    <- the -1/2 sigma^2 correction
S = S0 * np.exp(drift_coef * tgrid[None, :] + SIGMA * W)

print(f"drift coefficient (mu - 1/2 sigma^2) = {drift_coef:.4f}   (mu alone would be {MU})")
print(f"E[S_T]       = {S[:, -1].mean():8.3f}   (should be ~ S0*e^(mu T) = {S0*np.exp(MU*T):.3f})")
print(f"median S_T   = {np.median(S[:, -1]):8.3f}   (should be ~ S0*e^((mu-1/2 s^2)T) = {S0*np.exp((MU-0.5*SIGMA**2)*T):.3f})")"""))

cells.append(code(
"""# CHECK — do not edit
assert abs(drift_coef - (MU - 0.5 * SIGMA**2)) < 1e-12, "drift must carry the -1/2 sigma^2 correction"
assert S.shape == (N_PATHS, N_STEPS + 1) and np.allclose(S[:, 0], S0), "S starts at S0, right shape"
assert abs(S[:, -1].mean() - S0 * np.exp(MU * T)) < 0.6, "E[S_T] must be ~ S0 e^(mu T)"
print("Task 1 OK — GBM simulated with the -1/2 sigma^2 Ito correction; E[S_T] = S0 e^(mu T).")"""))

# ---- Task 2 ----
cells.append(md(
r"""### Task 2 — `d(W²) = 2W dW + dt`: the missing drift is the quadratic variation

**Goal:** for each path, form the **Itô integral** $I_T = \sum_i 2\,W_{t_{i-1}}\,\Delta W_i$ (integrand at
the **left** endpoint `W[:, :-1]`) and the quadratic-variation piece $Q_T = \sum_i (\Delta W_i)^2$. Then
check the exact identity $W_T^2 = I_T + Q_T$, that $E[I_T]\approx 0$ (a martingale — the naive chain rule),
and that $E[Q_T]\approx T$ (the drift the naive rule *misses*).

**Why:** this is Itô's lemma in the raw. The whole rise of $E[W_t^2]$ from 0 to $t$ is the $+dt$ term; the
$2W\,dW$ part is a fair game that averages to zero.

**Hint boundary:** left endpoints are `W[:, :-1]`; the Itô integral sums `2 * W[:, :-1] * dW` along time."""))

cells.append(code(
"""# TODO — the LEFT-endpoint Ito integral of 2W dW.
ito_int = ____                             # np.sum(2.0 * W[:, :-1] * dW, axis=1)
qv = np.sum(dW**2, axis=1)                 # provided: quadratic variation Sum (dW)^2, per path
WT2 = W[:, -1] ** 2

print(f"E[ integral 2W dW ] = {ito_int.mean():+.4f}   (should be ~ 0: a martingale)")
print(f"E[ Sum (dW)^2 ]     = {qv.mean():.4f}   (should be ~ T = {T}: the missing drift)")
print(f"max|W_T^2 - (I + Q)| = {np.max(np.abs(WT2 - (ito_int + qv))):.2e}   (identity: exactly 0)")"""))

cells.append(code(
"""# CHECK — do not edit
assert np.allclose(WT2, ito_int + qv, atol=1e-9), "identity W_T^2 = integral(2W dW) + Sum(dW)^2 must hold exactly"
assert abs(ito_int.mean()) < 0.03, "the Ito integral 2W dW must average to ~0 (martingale)"
assert abs(qv.mean() - T) < 0.02, "the missing drift Sum(dW)^2 must be ~ T (the quadratic variation)"
# so E[W_T^2] = 0 + T = T, i.e. W_t^2 - t is the martingale (Lesson 012)
assert abs(WT2.mean() - T) < 0.03, "E[W_T^2] must be ~ T"
print("Task 2 OK — d(W^2) = 2W dW + dt: the 2W dW part is a martingale, the +dt is the whole drift.")"""))

# ---- Task 3 ----
cells.append(md(
r"""### Task 3 — `d(log S)` drifts at μ − ½σ² (not μ)

**Goal:** measure the drift of the log price. Average $\log(S_t/S_0)$ across paths at each time and fit a
straight line in $t$; its slope is the empirical log-drift. Confirm it matches $\mu - \tfrac12\sigma^2$
and is clearly **below** the naive $\mu$.

**Why:** this is the single most consequential Itô result in finance — the number that goes into every
option price and Monte-Carlo simulator. Get the sign or the ½ wrong and prices are biased.

**Hint boundary:** fill the *predicted* drift $\mu - \tfrac12\sigma^2$; the empirical slope is provided."""))

cells.append(code(
"""# TODO — the Ito-predicted drift of log S.
pred_log_drift = ____                      # MU - 0.5 * SIGMA**2

mean_logret = np.log(S / S0).mean(axis=0)          # provided: E[log(S_t/S0)] at each t
emp_log_drift = np.polyfit(tgrid, mean_logret, 1)[0]   # provided: slope = empirical drift

print(f"predicted drift  (mu - 1/2 sigma^2) = {pred_log_drift:.4f}")
print(f"empirical  drift (fitted slope)     = {emp_log_drift:.4f}")
print(f"naive drift mu (WRONG)              = {MU:.4f}   <- log-price does NOT grow this fast")"""))

cells.append(code(
"""# CHECK — do not edit
assert abs(pred_log_drift - (MU - 0.5 * SIGMA**2)) < 1e-12, "predicted drift must be mu - 1/2 sigma^2"
assert abs(emp_log_drift - pred_log_drift) < 0.006, "the measured log-drift must match mu - 1/2 sigma^2"
assert emp_log_drift < MU - 0.5 * (0.5 * SIGMA**2), "the measured drift must sit clearly below the naive mu"
print(f"Task 3 OK — log S drifts at {emp_log_drift:.4f} ~ mu - 1/2 sigma^2 = {pred_log_drift:.4f}, below mu = {MU}.")"""))

# ---- Task 4 ----
cells.append(md(
r"""### Task 4 — `d(S²)` grows at 2μ + σ²

**Goal:** apply Itô to $f(S)=S^2$ on GBM. The one-liner is
$d(S^2) = (2\mu + \sigma^2)S^2\,dt + 2\sigma S^2\,dW$, so $E[S_t^2]$ grows exponentially at rate
$2\mu + \sigma^2$. Fit the slope of $\log E[S_t^2]$ in $t$ and confirm.

**Why:** a second, curving-**up** function (so the correction is a *bonus*, +σ², not a drag). Same recipe,
opposite sign — proof you can turn the crank on any payoff.

**Hint boundary:** fill the predicted growth rate $2\mu + \sigma^2$; the fit is provided."""))

cells.append(code(
"""# TODO — the Ito-predicted growth rate of E[S^2].
pred_s2_rate = ____                        # 2*MU + SIGMA**2

mean_S2 = (S**2).mean(axis=0)                      # provided: E[S_t^2] at each t
emp_s2_rate = np.polyfit(tgrid, np.log(mean_S2), 1)[0]   # provided: slope of log E[S_t^2]

print(f"predicted rate (2mu + sigma^2) = {pred_s2_rate:.4f}")
print(f"empirical rate (fitted slope)  = {emp_s2_rate:.4f}")
print(f"E[S_T^2] = {mean_S2[-1]:.1f}   (should be ~ S0^2 e^((2mu+s^2)T) = {S0**2*np.exp(pred_s2_rate*T):.1f})")"""))

cells.append(code(
"""# CHECK — do not edit
assert abs(pred_s2_rate - (2*MU + SIGMA**2)) < 1e-12, "predicted rate must be 2mu + sigma^2"
assert abs(emp_s2_rate - pred_s2_rate) < 0.01, "the measured growth rate of E[S^2] must match 2mu + sigma^2"
assert pred_s2_rate > 2*MU, "note the correction is +sigma^2 here (S^2 curves UP), a bonus not a drag"
print(f"Task 4 OK — E[S^2] grows at {emp_s2_rate:.4f} ~ 2mu + sigma^2 = {pred_s2_rate:.4f}.")"""))

# ---- Task 5 ----
cells.append(md(
r"""### Task 5 — Mean beats median: the volatility drag

**Goal:** compare the **mean** price $E[S_T]=S_0 e^{\mu T}$ with the **median** (typical) price
$S_0 e^{(\mu-\frac12\sigma^2)T}$. Confirm the mean exceeds the median, and that the gap is the drag
$\tfrac12\sigma^2$.

**Why:** "average return" and "what you'll most likely get" are different questions for a stock; the gap
is pure Itô correction. This is the practical face of Trap 6 in the lesson.

**Hint boundary:** fill the median formula $S_0 e^{(\mu-\frac12\sigma^2)T}$; the empirical stats are given."""))

cells.append(code(
"""# TODO — the theoretical median terminal price.
median_theory = ____                       # S0 * np.exp((MU - 0.5*SIGMA**2) * T)

emp_mean   = S[:, -1].mean()
emp_median = np.median(S[:, -1])
print(f"mean   E[S_T] = {emp_mean:8.3f}   (theory S0 e^(mu T)          = {S0*np.exp(MU*T):.3f})")
print(f"median  S_T   = {emp_median:8.3f}   (theory S0 e^((mu-1/2 s^2)T) = {median_theory:.3f})")
print(f"drag = 1/2 sigma^2 = {0.5*SIGMA**2:.4f} per unit time  ->  mean/median gap grows with sigma")"""))

cells.append(code(
"""# CHECK — do not edit
assert abs(median_theory - S0*np.exp((MU - 0.5*SIGMA**2)*T)) < 1e-9, "median = S0 e^((mu - 1/2 sigma^2) T)"
assert emp_mean > emp_median, "for a stock the mean must exceed the median (lognormal is right-skewed)"
assert abs(emp_median - median_theory) < 1.0, "empirical median must match the theoretical median"
assert abs(emp_mean - S0*np.exp(MU*T)) < 0.6, "empirical mean must match S0 e^(mu T)"
print("Task 5 OK — mean (grows at mu) > median (grows at mu - 1/2 sigma^2): the volatility drag.")"""))

# ---- Task 6 ----
cells.append(md(
r"""### Task 6 — The correction for a *different* function: `E[e^{W_t}] = e^{t/2}`

**Goal:** apply Itô to $f(W)=e^{W}$: $d(e^{W}) = e^{W}\,dW + \tfrac12 e^{W}\,dt$. The $dW$ part is a
martingale, so $E[e^{W_t}]$ grows purely from the $\tfrac12 e^{W}\,dt$ correction, giving
$E[e^{W_t}] = e^{t/2}$. Confirm it, and note the naive chain rule (no correction) would wrongly predict
$E[e^{W_t}]$ stays at 1.

**Why:** proof the correction is not special to $\log$ or $S^2$ — *every* curved function gets
$\tfrac12 f''\,dt$. This is also the moment-generating-function fact behind the GBM mean.

**Hint boundary:** fill the Itô prediction $e^{t/2}$ across `tgrid`; the empirical mean is provided."""))

cells.append(code(
"""# TODO — the Ito prediction for E[e^{W_t}].
pred_expW = ____                           # np.exp(0.5 * tgrid)

emp_expW = np.exp(W).mean(axis=0)                  # provided: E[e^{W_t}] at each t
print(f"E[e^(W_T)] empirical = {emp_expW[-1]:.4f}   Ito prediction e^(T/2) = {pred_expW[-1]:.4f}")
print(f"naive chain rule would say it stays at 1.0  ->  off by {emp_expW[-1]-1:.4f}")
print(f"max abs error over t = {np.max(np.abs(emp_expW - pred_expW)):.4f}")"""))

cells.append(code(
"""# CHECK — do not edit
assert np.allclose(pred_expW, np.exp(0.5 * tgrid)), "prediction must be e^(t/2) (the 1/2 f'' dt correction)"
assert np.max(np.abs(emp_expW - pred_expW)) < 0.03, "E[e^{W_t}] must track e^(t/2)"
assert abs(emp_expW[-1] - 1.0) > 0.5, "the naive 'stays at 1' prediction must be clearly wrong at T"
print(f"Task 6 OK — E[e^(W_t)] = e^(t/2): the 1/2 f'' dt correction shows up for e^W too.")"""))

# ---- Exit ticket ----
cells.append(code(
r"""# EXIT TICKET — paste this output to your teacher.
print("=== Lab 013: the Ito integral & Ito's lemma ===")
print(f"GBM               : drift coef = {MU-0.5*SIGMA**2:.4f} (mu - 1/2 s^2); E[S_T] = {S[:,-1].mean():.3f} = S0 e^(mu T)")
print(f"d(W^2)=2W dW+dt    : E[int 2W dW] = {ito_int.mean():+.4f} (~0, martingale); E[Sum dW^2] = {qv.mean():.4f} (~T)")
print(f"                    identity W_T^2 = I + Q holds to {np.max(np.abs(WT2-(ito_int+qv))):.1e}")
print(f"d(log S)           : drift = {emp_log_drift:.4f} ~ mu - 1/2 s^2 = {MU-0.5*SIGMA**2:.4f}  (NOT mu = {MU})")
print(f"d(S^2)             : E[S^2] grows at {emp_s2_rate:.4f} ~ 2mu + s^2 = {2*MU+SIGMA**2:.4f}  (+s^2: curves up)")
print(f"Vol drag           : mean {S[:,-1].mean():.2f} > median {np.median(S[:,-1]):.2f}; gap rate 1/2 s^2 = {0.5*SIGMA**2:.4f}")
print(f"d(e^W)             : E[e^(W_T)] = {emp_expW[-1]:.4f} ~ e^(T/2) = {np.exp(0.5*T):.4f}  (naive says 1.0)")
print()
print("One-sentence takeaway (edit me):")
print("Ito's lemma is the ordinary chain rule plus a 1/2 f'' dt term born from (dW)^2 = dt: the dW part")
print("is always a martingale, and the extra drift's sign is the curvature's sign - which is why log S")
print("drifts at mu - 1/2 sigma^2 (a drag), S^2 at 2mu + sigma^2 (a bonus), and E[e^W] = e^(t/2).")"""))

# ---- Stretch ----
cells.append(md(
r"""### Stretch (optional, ungraded)

- **Black–Scholes preview (Lesson 016).** For a European call with strike $K$, price it by Monte Carlo:
  $C = e^{-rT}\,E[(S_T - K)^+]$ under the *risk-neutral* drift $\mu = r$. Compare to the closed-form
  Black–Scholes value. (Why $\mu = r$? That is the measure change of Lesson 015.)
- **Gamma / the hedging P&L.** Hold a function $f(S)$ and delta-hedge it (subtract $f_x\,dS$). Show the
  leftover per step is $\tfrac12 f_{xx}(dS)^2 = \tfrac12 f_{xx}\sigma^2 S^2\,dt$ — the "gamma P&L", which is
  the Itô correction you just met, and the term the Black–Scholes PDE balances against time decay.
- **Stratonovich vs Itô.** Recompute Task 2 using the **right** endpoint `W[:, 1:]` in the integral. Show
  its mean is $+T$, not $0$ — the midpoint/right choice is not a martingale, and in finance it peeks at
  the future.
- **Ornstein–Uhlenbeck (Lesson 014 preview).** Simulate $dX = \theta(m - X)dt + \sigma\,dW$ (mean-reverting)
  and watch it pull back toward $m$. Apply Itô to $f=e^{\theta t}X$ to solve it in closed form.
- **Convergence.** Halve `dt` and show the discrete Itô integral $\sum 2W_{i-1}\Delta W$ converges (its
  error to $W_T^2 - T$ shrinks like $\sqrt{dt}$)."""))

nb = {"cells": cells,
      "metadata": {"kernelspec": {"display_name": "Financial Eng Labs (.venv)",
                                   "language": "python", "name": "feq-labs"},
                   "language_info": {"name": "python", "version": "3.12"}},
      "nbformat": 4, "nbformat_minor": 5}

lab_path = "labs/0013-ito-lemma.ipynb"
with open(lab_path, "w") as f:
    json.dump(nb, f, indent=1)
    f.write("\n")
print("wrote", lab_path)

# ---- Build the filled SOLUTION by replacing the ____ blanks with the hinted answers ----
answers = {
    "drift_coef = ____": "drift_coef = MU - 0.5 * SIGMA**2",
    "ito_int = ____": "ito_int = np.sum(2.0 * W[:, :-1] * dW, axis=1)",
    "pred_log_drift = ____": "pred_log_drift = MU - 0.5 * SIGMA**2",
    "pred_s2_rate = ____": "pred_s2_rate = 2*MU + SIGMA**2",
    "median_theory = ____": "median_theory = S0 * np.exp((MU - 0.5*SIGMA**2) * T)",
    "pred_expW = ____": "pred_expW = np.exp(0.5 * tgrid)",
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
                comment = ""
                if "#" in line:
                    comment = "  # " + line.split("#", 1)[1].strip()
                line = indent + v + comment + ("\n" if line.endswith("\n") else "")
                break
        new.append(line)
    c["source"] = new

os.makedirs("solutions", exist_ok=True)
sol_path = "solutions/0013-ito-lemma.ipynb"
with open(sol_path, "w") as f:
    json.dump(sol, f, indent=1)
    f.write("\n")
print("wrote", sol_path)
