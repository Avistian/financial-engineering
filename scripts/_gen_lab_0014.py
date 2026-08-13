"""One-off builder for Lab 014 (OU). Produces the student notebook and the filled
solution notebook from a single source of truth. Run once, then delete."""
import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

# Each code cell is (solution_source, student_source). If student is None, they are identical.
CELLS = []

def md(text):
    CELLS.append(("md", text, None))

def code(sol, student=None):
    CELLS.append(("code", sol, student))

md(r"""# Lab 014 — Simulate &amp; fit an Ornstein–Uhlenbeck process

**Lesson:** [`0014-sdes.html`](../lessons/0014-sdes.html)
· **Reference:** [`sdes.html`](../reference/sdes.html)

**The one skill:** take a mean-reverting SDE, simulate it, and then *recover its parameters from data* —
the core move behind a pairs-trading signal. By the end you will have checked, with numbers, that (1) the
OU drift `θ(m − X)` pulls the mean from `X₀` up to the target `m`, (2) the closed-form mean
`X₀e^{−θt} + m(1 − e^{−θt})` matches the simulation, (3) the spread settles to the **stationary variance**
`σ²/2θ`, (4) the **half-life** of reversion is `ln2/θ`, (5) you can **fit** `(θ, m, σ)` from one path by
regressing `ΔX` on `X`, and (6) fitting `θ` on **short** samples **overestimates** it — the classic
mean-reversion estimation trap.

**Exit criteria:** every CHECK passes and the EXIT TICKET prints cleanly.

**How this notebook works**

| Cell tag | You do |
|----------|--------|
| **PROVIDED** | Run it. Imports, parameters, the simulator scaffold. |
| **TODO** | Fill the `____` blanks. This is where the learning is. |
| **CHECK** | Run it — immediate assertions. Don't edit. |
| **EXIT TICKET** | Final deliverable. Prints your summary. |

**Environment:** Python 3 + `numpy` only. Fully self-contained (no network, runs in seconds).
See [`labs/README.md`](./README.md).""")

md(r"""### Running on Google Colab?

Colab opens only this single file, so the lab dependencies and the course repo are **not**
guaranteed to be present. The cell below fixes that: on Colab it shallow-clones the course repo,
installs `requirements-labs.txt`, and switches into `labs/` so relative paths resolve. **On a local
venv or Binder it does nothing — just run it and continue.**""")

code(r"""# @colab-bootstrap — PROVIDED. Makes the lab self-sufficient on Google Colab; a no-op elsewhere.
import os, sys

if "google.colab" in sys.modules:
    if not os.path.isdir("/content/financial-engineering"):
        !git clone --depth 1 https://github.com/Avistian/financial-engineering.git /content/financial-engineering
    %pip install -q -r /content/financial-engineering/requirements-labs.txt
    os.chdir("/content/financial-engineering/labs")
    print("Colab ready — working dir:", os.getcwd())
else:
    print("Not on Colab — using the local environment as-is.")""")

md(r"""## Concept recap (read before coding)

**The OU SDE.** $dX = \theta(m - X)\,dt + \sigma\,dW$. Three knobs: $m$ = target level, $\theta$ = pull
strength, $\sigma$ = shove size. The drift $\theta(m-X)$ points *toward* $m$ from either side — that is
mean reversion.

**Solved form** (apply Itô to the linear function $e^{\theta t}X$, so **no** correction term):

$$X_t = X_0 e^{-\theta t} + m\,(1 - e^{-\theta t}) + \sigma\!\int_0^t e^{-\theta(t-s)}\,dW_s$$

| Quantity | Formula | Meaning |
|----------|---------|---------|
| Mean | $E[X_t] = X_0 e^{-\theta t} + m(1 - e^{-\theta t}) \to m$ | pulled to the target |
| Variance | $\dfrac{\sigma^2}{2\theta}(1 - e^{-2\theta t}) \to \dfrac{\sigma^2}{2\theta}$ | stationary spread |
| Stationary law | $N\!\big(m,\ \sigma^2/2\theta\big)$ | the long-run wobble |
| Half-life | $\ln 2 / \theta$ | time for the gap to $m$ to halve |

**Fitting OU from data.** The Euler step $\Delta X = \theta(m - X)\,dt + \sigma\sqrt{dt}\,Z$ is a linear
regression of $\Delta X$ on $X$: $\ \Delta X \approx \alpha + \beta X$ with $\beta = -\theta\,dt$ and
$\alpha = \theta m\,dt$. So $\hat\theta = -\beta/dt$, $\hat m = \alpha/(-\beta)$, and $\hat\sigma$ = (residual
std)$/\sqrt{dt}$.""")

# ---- PROVIDED params ----
code(r"""# PROVIDED — RNG, OU parameters (the "truth" we will recover), and shared Brownian increments. Run it.
import numpy as np

rng = np.random.default_rng(20140613)

THETA = 3.0      # pull strength (mean-reversion speed)
M     = 100.0    # long-run mean (the level it is pulled toward)
SIGMA = 8.0      # shove size (volatility)
X0    = 80.0     # starting value (below M, so we can watch it get pulled up)
T     = 4.0      # horizon
N_PATHS = 20000
N_STEPS = 1000
dt = T / N_STEPS
tgrid = np.linspace(0.0, T, N_STEPS + 1)

# shared Brownian increments N(0, dt), shape (N_PATHS, N_STEPS)
dW = rng.standard_normal((N_PATHS, N_STEPS)) * np.sqrt(dt)

print("numpy", np.__version__, "| paths", N_PATHS, "| steps", N_STEPS, "| dt", dt)
print("half-life ln2/theta =", round(np.log(2)/THETA, 3),
      "| stationary var sigma^2/2theta =", round(SIGMA**2/(2*THETA), 3))""")

# ---- Task 1 ----
md(r"""### Task 1 — Simulate OU with the mean-reverting drift

**Goal:** step the OU SDE forward with Euler:
$X_{i+1} = X_i + \theta(m - X_i)\,dt + \sigma\,\Delta W_i$. Fill the **drift** term — the pull toward `m`.

**Why:** the whole character of OU lives in that one term. Get its sign right and the mean is dragged from
`X₀ = 80` up to `M = 100`; flip it and the process explodes away from `M`.

**Hint boundary:** the drift is `theta * (m - X_now)`.""")

code(r"""# TODO — the OU mean-reverting drift.
def ou_drift(X_now, theta, m):
    return theta * (m - X_now)              # the pull toward m

def simulate_ou(theta, m, sigma, X0, dW):
    n_paths, n_steps = dW.shape
    X = np.empty((n_paths, n_steps + 1))
    X[:, 0] = X0
    for i in range(n_steps):
        X[:, i + 1] = X[:, i] + ou_drift(X[:, i], theta, m) * dt + sigma * dW[:, i]
    return X

X = simulate_ou(THETA, M, SIGMA, X0, dW)
print(f"X shape {X.shape}, starts at {X[:, 0].mean():.1f}")
print(f"E[X_T] = {X[:, -1].mean():.3f}   (should be ~ M = {M}: theta*T is large, so fully reverted)")""",
r"""# TODO — the OU mean-reverting drift.
def ou_drift(X_now, theta, m):
    return ____                             # theta * (m - X_now): the pull toward m

def simulate_ou(theta, m, sigma, X0, dW):
    n_paths, n_steps = dW.shape
    X = np.empty((n_paths, n_steps + 1))
    X[:, 0] = X0
    for i in range(n_steps):
        X[:, i + 1] = X[:, i] + ou_drift(X[:, i], theta, m) * dt + sigma * dW[:, i]
    return X

X = simulate_ou(THETA, M, SIGMA, X0, dW)
print(f"X shape {X.shape}, starts at {X[:, 0].mean():.1f}")
print(f"E[X_T] = {X[:, -1].mean():.3f}   (should be ~ M = {M}: theta*T is large, so fully reverted)")""")

code(r"""# CHECK — do not edit
assert X.shape == (N_PATHS, N_STEPS + 1) and np.allclose(X[:, 0], X0), "X starts at X0, right shape"
assert abs(X[:, -1].mean() - M) < 0.5, "E[X_T] must be ~ M (fully reverted)"
print("Task 1 OK — OU simulated; the drift theta*(m-X) pulled the mean from X0 up to ~ M.")""")

# ---- Task 2 ----
md(r"""### Task 2 — The closed-form mean matches the simulation

**Goal:** fill the closed-form mean $E[X_t] = X_0 e^{-\theta t} + m(1 - e^{-\theta t})$ across `tgrid`, and
confirm it tracks the empirical mean of the simulated paths.

**Why:** this is the solved SDE's first payoff — you can predict the average path exactly, without
simulating, and see the start's memory fade as the pull to `m` takes over.

**Hint boundary:** `X0*np.exp(-THETA*tgrid) + M*(1 - np.exp(-THETA*tgrid))`.""")

code(r"""# TODO — the OU closed-form mean.
mean_theory = X0 * np.exp(-THETA * tgrid) + M * (1.0 - np.exp(-THETA * tgrid))

mean_emp = X.mean(axis=0)                     # provided: empirical mean at each t
i1 = np.argmin(np.abs(tgrid - 1.0))
print(f"max |empirical mean - theory| = {np.max(np.abs(mean_emp - mean_theory)):.4f}")
print(f"mean at t=1: theory {mean_theory[i1]:.3f}, empirical {mean_emp[i1]:.3f}")""",
r"""# TODO — the OU closed-form mean.
mean_theory = ____                           # X0*exp(-theta t) + M*(1 - exp(-theta t))

mean_emp = X.mean(axis=0)                     # provided: empirical mean at each t
i1 = np.argmin(np.abs(tgrid - 1.0))
print(f"max |empirical mean - theory| = {np.max(np.abs(mean_emp - mean_theory)):.4f}")
print(f"mean at t=1: theory {mean_theory[i1]:.3f}, empirical {mean_emp[i1]:.3f}")""")

code(r"""# CHECK — do not edit
assert np.max(np.abs(mean_emp - mean_theory)) < 0.3, "closed-form mean must match the simulated mean"
print("Task 2 OK — E[X_t] = X0 e^{-theta t} + M(1 - e^{-theta t}); memory fades, pull to M wins.")""")

# ---- Task 3 ----
md(r"""### Task 3 — The stationary variance σ²/2θ

**Goal:** fill the stationary variance $\sigma^2/2\theta$ and confirm the simulated variance at the horizon
(where the process is fully reverted) matches it.

**Why:** the long-run *spread* — not the mean — is what tells a pairs trader how wide the swings (and
drawdowns) can get. It is a tug-of-war: more shoving (`σ`) widens it, a stiffer spring (`θ`) narrows it.

**Hint boundary:** `SIGMA**2 / (2*THETA)`.""")

code(r"""# TODO — the OU stationary variance.
var_stat = SIGMA**2 / (2.0 * THETA)

var_emp_T = X[:, -1].var()                    # provided: variance at t = T (stationary)
print(f"stationary variance sigma^2/2theta = {var_stat:.4f}  (std {np.sqrt(var_stat):.3f})")
print(f"empirical Var(X_T)                 = {var_emp_T:.4f}")""",
r"""# TODO — the OU stationary variance.
var_stat = ____                              # SIGMA**2 / (2*THETA)

var_emp_T = X[:, -1].var()                    # provided: variance at t = T (stationary)
print(f"stationary variance sigma^2/2theta = {var_stat:.4f}  (std {np.sqrt(var_stat):.3f})")
print(f"empirical Var(X_T)                 = {var_emp_T:.4f}")""")

code(r"""# CHECK — do not edit
assert abs(var_stat - SIGMA**2/(2*THETA)) < 1e-9, "stationary variance is sigma^2/(2 theta)"
assert abs(var_emp_T - var_stat) < 1.0, "at t=T (fully reverted) Var(X_T) must match the stationary variance"
print(f"Task 3 OK — OU settles to N(M, sigma^2/2theta): variance ~ {var_stat:.3f}.")""")

# ---- Task 4 ----
md(r"""### Task 4 — The half-life of reversion ln2/θ

**Goal:** fill the half-life $\ln 2/\theta$ and confirm the mean closes **half** the initial gap
($X_0 \to M$) in exactly that time.

**Why:** the half-life is the number a PM asks for — "how long is this trade?" It converts the abstract
`θ` into a horizon you can act on.

**Hint boundary:** `np.log(2)/THETA`.""")

code(r"""# TODO — the half-life of mean reversion.
half_life = np.log(2.0) / THETA

gap0 = M - X0                                 # provided: initial gap to the target
target = X0 + 0.5 * gap0                      # halfway to M (= 90)
emp_half = np.interp(target, mean_emp, tgrid) # mean_emp increases here, so interp on it
print(f"half-life ln2/theta = {half_life:.4f}")
print(f"empirical half-life = {emp_half:.4f}  (time for the mean to reach {target:.0f})")""",
r"""# TODO — the half-life of mean reversion.
half_life = ____                             # np.log(2)/THETA

gap0 = M - X0                                 # provided: initial gap to the target
target = X0 + 0.5 * gap0                      # halfway to M (= 90)
emp_half = np.interp(target, mean_emp, tgrid) # mean_emp increases here, so interp on it
print(f"half-life ln2/theta = {half_life:.4f}")
print(f"empirical half-life = {emp_half:.4f}  (time for the mean to reach {target:.0f})")""")

code(r"""# CHECK — do not edit
assert abs(half_life - np.log(2)/THETA) < 1e-9, "half-life is ln2/theta"
assert abs(emp_half - half_life) < 0.03, "measured half-life must match ln2/theta"
print(f"Task 4 OK — the gap to M halves every ln2/theta = {half_life:.3f} time units.")""")

# ---- Task 5 ----
md(r"""### Task 5 — Fit (θ, m, σ) from one long path

**Goal:** simulate one long OU path, then recover its parameters by regressing the step change `ΔX` on the
level `X`. The Euler step makes this a straight line: `ΔX ≈ α + βX` with `β = −θ·dt`, `α = θm·dt`. Fill the
recovery `θ_hat = −β/dt`.

**Why:** this *is* the estimation half of a pairs-trade signal — from a price-gap series you back out how
fast it reverts (`θ`), to what level (`m`), and how noisy it is (`σ`).

**Hint boundary:** `theta_hat = -beta / dt_fit`; `m_hat` and `sigma_hat` are provided.""")

code(r"""# TODO — recover theta from the regression slope.
# one long single OU path, sampled long enough to see many reversions
N_FIT = 200000
dt_fit = 0.02
z = rng.standard_normal(N_FIT)
xf = np.empty(N_FIT + 1)
xf[0] = M
for i in range(N_FIT):
    xf[i + 1] = xf[i] + THETA * (M - xf[i]) * dt_fit + SIGMA * np.sqrt(dt_fit) * z[i]

Xi = xf[:-1]                                  # level at the start of each step
dX = np.diff(xf)                              # the step change
beta, alpha = np.polyfit(Xi, dX, 1)           # dX ~ alpha + beta * Xi

theta_hat = -beta / dt_fit                    # <- fill this
m_hat = alpha / (-beta)                       # provided: = alpha / (theta_hat * dt_fit)
sigma_hat = (dX - (alpha + beta * Xi)).std() / np.sqrt(dt_fit)   # provided: residual std / sqrt(dt)

print(f"theta: true {THETA}, fitted {theta_hat:.3f}")
print(f"m    : true {M}, fitted {m_hat:.3f}")
print(f"sigma: true {SIGMA}, fitted {sigma_hat:.3f}")""",
r"""# TODO — recover theta from the regression slope.
# one long single OU path, sampled long enough to see many reversions
N_FIT = 200000
dt_fit = 0.02
z = rng.standard_normal(N_FIT)
xf = np.empty(N_FIT + 1)
xf[0] = M
for i in range(N_FIT):
    xf[i + 1] = xf[i] + THETA * (M - xf[i]) * dt_fit + SIGMA * np.sqrt(dt_fit) * z[i]

Xi = xf[:-1]                                  # level at the start of each step
dX = np.diff(xf)                              # the step change
beta, alpha = np.polyfit(Xi, dX, 1)           # dX ~ alpha + beta * Xi

theta_hat = ____                             # -beta / dt_fit
m_hat = alpha / (-beta)                       # provided: = alpha / (theta_hat * dt_fit)
sigma_hat = (dX - (alpha + beta * Xi)).std() / np.sqrt(dt_fit)   # provided: residual std / sqrt(dt)

print(f"theta: true {THETA}, fitted {theta_hat:.3f}")
print(f"m    : true {M}, fitted {m_hat:.3f}")
print(f"sigma: true {SIGMA}, fitted {sigma_hat:.3f}")""")

code(r"""# CHECK — do not edit
assert abs(theta_hat - THETA) < 0.3, "fitted theta must be close to the true theta on a long path"
assert abs(m_hat - M) < 0.5, "fitted m must be close to true M"
assert abs(sigma_hat - SIGMA) < 0.3, "fitted sigma must be close to true SIGMA"
print("Task 5 OK — recovered (theta, m, sigma) from one path by regressing dX on X.")""")

# ---- Task 6 ----
md(r"""### Task 6 — The small-sample trap: short fits overestimate θ

**Goal:** fit `θ` on **many short** OU paths and average. Fill the recovery `θ_hat = −β/dt_s`. You will see
the average estimate come out **above** the true `θ` — a real, well-known bias.

**Why:** this is the failure mode of the whole method. A spread fitted on a short window *looks* like it
reverts faster than it does, so a naive pairs trade expects a quicker payoff than reality delivers. Knowing
the model **and** its bias is the point.

**Hint boundary:** `theta_hat_short = -beta_short / dt_s`.""")

code(r"""# TODO — recover theta on each short path (vectorized), then average.
window = 60
dt_s = 0.05
n_short = 8000
zs = rng.standard_normal((n_short, window))
xs = np.empty((n_short, window + 1))
xs[:, 0] = M                                  # start each short path at the long-run mean
for i in range(window):
    xs[:, i + 1] = xs[:, i] + THETA * (M - xs[:, i]) * dt_s + SIGMA * np.sqrt(dt_s) * zs[:, i]

Xi_s = xs[:, :-1]; dX_s = np.diff(xs, axis=1)
Xi_c = Xi_s - Xi_s.mean(axis=1, keepdims=True)         # per-row centering
dX_c = dX_s - dX_s.mean(axis=1, keepdims=True)
beta_short = (Xi_c * dX_c).sum(axis=1) / (Xi_c**2).sum(axis=1)   # per-path slope

theta_hat_short = -beta_short / dt_s          # <- fill this
mean_theta_hat = theta_hat_short.mean()
print(f"true theta        = {THETA}")
print(f"mean fitted theta = {mean_theta_hat:.3f}   ({n_short} short paths of {window} steps, dt={dt_s})")
print(f"upward bias       = {mean_theta_hat - THETA:+.3f}   (short samples OVERestimate mean reversion)")""",
r"""# TODO — recover theta on each short path (vectorized), then average.
window = 60
dt_s = 0.05
n_short = 8000
zs = rng.standard_normal((n_short, window))
xs = np.empty((n_short, window + 1))
xs[:, 0] = M                                  # start each short path at the long-run mean
for i in range(window):
    xs[:, i + 1] = xs[:, i] + THETA * (M - xs[:, i]) * dt_s + SIGMA * np.sqrt(dt_s) * zs[:, i]

Xi_s = xs[:, :-1]; dX_s = np.diff(xs, axis=1)
Xi_c = Xi_s - Xi_s.mean(axis=1, keepdims=True)         # per-row centering
dX_c = dX_s - dX_s.mean(axis=1, keepdims=True)
beta_short = (Xi_c * dX_c).sum(axis=1) / (Xi_c**2).sum(axis=1)   # per-path slope

theta_hat_short = ____                        # -beta_short / dt_s
mean_theta_hat = theta_hat_short.mean()
print(f"true theta        = {THETA}")
print(f"mean fitted theta = {mean_theta_hat:.3f}   ({n_short} short paths of {window} steps, dt={dt_s})")
print(f"upward bias       = {mean_theta_hat - THETA:+.3f}   (short samples OVERestimate mean reversion)")""")

code(r"""# CHECK — do not edit
assert theta_hat_short.shape == (n_short,), "one theta estimate per short path"
assert mean_theta_hat > THETA, "short-sample theta is biased HIGH — the classic OU estimation trap"
print("Task 6 OK — fitting theta on short windows overestimates it: mean reversion looks faster than it is.")""")

# ---- EXIT ----
code(r"""# EXIT TICKET — paste this output to your teacher.
print("=== Lab 014: simulate & fit an Ornstein-Uhlenbeck process ===")
print(f"OU truth         : theta={THETA}, m={M}, sigma={SIGMA}, X0={X0}")
print(f"Simulated mean   : E[X_T]={X[:,-1].mean():.3f} ~ M={M}; matches closed form to {np.max(np.abs(mean_emp-mean_theory)):.3f}")
print(f"Stationary spread: Var(X_T)={X[:,-1].var():.3f} ~ sigma^2/2theta={SIGMA**2/(2*THETA):.3f}")
print(f"Half-life        : ln2/theta={np.log(2)/THETA:.3f}; measured {emp_half:.3f}")
print(f"Fit (long path)  : theta_hat={theta_hat:.3f}, m_hat={m_hat:.3f}, sigma_hat={sigma_hat:.3f}")
print(f"Small-sample bias: mean theta_hat={mean_theta_hat:.3f} > true {THETA} (biased +{mean_theta_hat-THETA:.3f})")
print()
print("One-sentence takeaway (edit me):")
print("OU dX=theta(m-X)dt+sigma dW mean-reverts to m with long-run spread sigma^2/2theta; you can recover")
print("(theta,m,sigma) by regressing dX on X, but SHORT samples overstate theta - the pairs-trade trap.")""")

md(r"""### Stretch (optional, ungraded)

- **Trade the spread.** Turn the fitted OU into a signal: go long when `X` is `k` stationary-std below `m`,
  short when `k` above, exit at `m`. Backtest the P&L on a fresh simulated path and see how it depends on
  the (biased) `θ̂`.
- **Bias vs sample length.** Repeat Task 6 for `window` in `[30, 60, 120, 250, 500]` and plot the mean `θ̂`
  against window length — watch the upward bias shrink as the sample grows.
- **Exact (non-Euler) simulation.** OU has an exact one-step update
  `X_{t+dt} = m + (X_t − m)e^{−θ dt} + √(σ²/2θ (1−e^{−2θ dt}))·Z`. Simulate with it and confirm it matches
  the Euler scheme as `dt → 0` but is exact for any `dt`.
- **GBM cross-check (Lesson 013).** Simulate GBM `S_t = S₀ exp((μ−½σ²)t + σW_t)` and confirm `log S` has
  drift `μ − ½σ²` — the other SDE you solved this quarter.
- **Vasicek rates.** Reinterpret OU as the short interest rate (the Vasicek model) and price a zero-coupon
  bond `E[exp(−∫₀ᵀ X_s ds)]` by Monte Carlo. This is a preview of the rates track.""")

# ---- assemble ----
def build(student):
    nb = new_notebook()
    for kind, sol, stu in CELLS:
        if kind == "md":
            nb.cells.append(new_markdown_cell(sol))
        else:
            src = (stu if (student and stu is not None) else sol)
            nb.cells.append(new_code_cell(src))
    nb.metadata = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3"},
    }
    return nb

nbf.write(build(student=True),  "labs/0014-ornstein-uhlenbeck.ipynb")
nbf.write(build(student=False), "solutions/0014-ornstein-uhlenbeck.ipynb")
print("wrote labs/0014-ornstein-uhlenbeck.ipynb and solutions/0014-ornstein-uhlenbeck.ipynb")
