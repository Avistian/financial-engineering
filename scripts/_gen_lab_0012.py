"""Generate labs/0012-brownian-motion.ipynb (blanks) and its filled solution.

Run:  ./.venv/bin/python scripts/_gen_lab_0012.py
"""
import json, copy, os

def md(src):
    return {"cell_type": "markdown", "metadata": {}, "source": src.splitlines(keepends=True)}

def code(src):
    return {"cell_type": "code", "metadata": {}, "execution_count": None,
            "outputs": [], "source": src.rstrip("\n").splitlines(keepends=True)}

cells = []

cells.append(md(
"""# Lab 012 — Random walks &amp; Brownian motion

**Lesson:** [`0012-brownian-motion.html`](../lessons/0012-brownian-motion.html)
· **Reference:** [`brownian-motion.html`](../reference/brownian-motion.html)

**The one skill:** simulate Brownian motion and *verify its theory numerically* rather than taking it
on faith. By the end you will have checked, with numbers, that (1) the scaled random walk keeps
**Var(W_t) = t** for every step count, (2) simulated Brownian increments are i.i.d. **N(0, dt)**,
(3) W_t is a **martingale** (and W_t² − t is too), (4) the **quadratic variation** of Brownian motion
is **t** while a smooth curve's is **0**, and (5) the first-order path length **explodes** — the
numerical face of "continuous but nowhere differentiable".

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

**Random walk.** $M_n = X_1 + \dots + X_n$ with each $X_i = \pm 1$ (prob $\tfrac12$), so $E[M_n]=0$ and
$\operatorname{Var}(M_n)=n$ — the walk spreads like $\sqrt n$.

**Scaled walk.** Put $n$ steps into $[0,1]$ and divide by $\sqrt n$: $W^{(n)}_t = M_{nt}/\sqrt n$. Then
$\operatorname{Var}(W^{(n)}_t) = nt/n = t$ at every $n$ — the $\sqrt n$ is the unique scaling that keeps
the spread finite. Its limit is Brownian motion.

**Brownian motion $W_t$** (four rules): $W_0=0$; increments independent of the past; $W_t-W_s\sim
N(0,\,t-s)$; continuous paths. Consequences you will check:

| Fact | Statement |
|------|-----------|
| Distribution | $W_t \sim N(0,t)$, so $\operatorname{Var}(W_t)=t$ |
| Martingale | $E[W_t\mid\mathcal F_s]=W_s$; and $E[W_t^2\mid\mathcal F_s]=W_s^2+(t-s)$, so $W_t^2-t$ is a martingale |
| Quadratic variation | $[W]_t=\lim\sum(\Delta W)^2 = t$ (a smooth curve gives $0$) |
| Roughness | first-order length $\sum|\Delta W|\to\infty$; nowhere differentiable |

**Heuristic:** $(dW)^2 = dt$ (keep it); $dW\,dt$ and $(dt)^2$ are dropped."""))

# ---- PROVIDED: simulator + helpers ----
cells.append(code(
'''# PROVIDED — one RNG (seeded, reproducible) and the horizon. Run it.
import numpy as np

rng = np.random.default_rng(12345)
T = 1.0   # we simulate Brownian motion on [0, T]

print("numpy", np.__version__, "| horizon T =", T)'''))

# ---- Task 1 ----
cells.append(md(
r"""### Task 1 — The scaled random walk keeps $\operatorname{Var}(W_t)=t$

**Goal:** build $W^{(n)}_1 = M_n/\sqrt n$ from $n$ coin flips and confirm its variance is $\approx 1$ no
matter how large $n$ is.

**Why:** this is the whole reason the scaling is $\sqrt n$ and not $n$. Dividing by $n$ would send the
variance to $0$ (a flat line); dividing by $\sqrt n$ pins it at $t$.

**Hint boundary:** `steps` are already the $\pm 1$ coins; you divide the row-sum $M_n$ by $\sqrt n$."""))

cells.append(code(
'''# TODO — scale the random walk by sqrt(n).
def scaled_walk_endpoint(n_paths, n, rng):
    """n_paths independent values of W^(n)_1 = (sum of n +/-1 flips) / sqrt(n)."""
    steps = rng.choice([-1.0, 1.0], size=(n_paths, n))
    M = steps.sum(axis=1)
    w_scaled = ____                      # M / np.sqrt(n)
    return w_scaled

print(f"{'n':>6} {'Var(W^n_1)':>12}")
for n in [1, 4, 16, 64, 256, 1024]:
    v = scaled_walk_endpoint(40000, n, rng).var()
    print(f"{n:>6} {v:12.4f}")'''))

cells.append(code(
'''# CHECK — do not edit
for n in [1, 4, 64, 1024]:
    v = scaled_walk_endpoint(40000, n, rng).var()
    assert abs(v - 1.0) < 0.06, f"Var(W^{n}_1) should be ~1 (=t), got {v:.4f}"
# and dividing by n instead of sqrt(n) would collapse the spread:
steps = rng.choice([-1.0, 1.0], size=(40000, 256))
assert (steps.sum(axis=1) / 256).var() < 0.02, "dividing by n sends the variance to 0"
print("Task 1 OK — Var(W^n_1) stays ~1 = t for every n; the sqrt(n) scaling is what does it.")'''))

# ---- Task 2 ----
cells.append(md(
r"""### Task 2 — Simulate Brownian motion on a grid

**Goal:** write `sample_bm(n_paths, n_steps, T, rng)` returning an array of shape
`(n_paths, n_steps+1)` with $W[:,0]=0$, built from independent $N(0,\,dt)$ increments, $dt=T/n_{steps}$.

**Why:** you cannot store the true continuous path, so you sample it on a grid — exactly the scaled
random walk, with Gaussian steps. Every later lab (GBM, option pricing, Monte Carlo) calls a function
just like this.

**Hint boundary:** an $N(0,dt)$ increment is a standard normal times $\sqrt{dt}$; cumulative-sum the
increments along the time axis."""))

cells.append(code(
'''# TODO — the Brownian-motion simulator.
def sample_bm(n_paths, n_steps, T, rng):
    """n_paths Brownian paths on [0, T] with n_steps grid points; W[:, 0] = 0."""
    dt = T / n_steps
    Z = rng.standard_normal((n_paths, n_steps))
    incr = ____                          # Z * np.sqrt(dt)   <- N(0, dt) increments
    W = np.zeros((n_paths, n_steps + 1))
    W[:, 1:] = np.cumsum(incr, axis=1)
    return W

W = sample_bm(60000, 500, T, rng)
print("shape:", W.shape, "| W[:,0] all zero:", np.allclose(W[:, 0], 0.0))
print(f"empirical Var(W_T) = {W[:, -1].var():.4f}   (should be ~ T = {T})")'''))

cells.append(code(
'''# CHECK — do not edit
assert W.shape == (60000, 501) and np.allclose(W[:, 0], 0.0), "start at 0, right shape"
assert abs(W[:, -1].var() - T) < 0.03, "Var(W_T) must be ~ T"
# variance should grow linearly in time: Var(W_t) = t
half = W.shape[1] // 2
assert abs(W[:, half].var() - T / 2) < 0.03, "Var(W_{T/2}) must be ~ T/2 (variance grows like t)"
print("Task 2 OK — simulated BM starts at 0 and has Var(W_t) = t (linear in time).")'''))

# ---- Task 3 ----
cells.append(md(
r"""### Task 3 — Increments are i.i.d. $N(0,\,dt)$

**Goal:** extract the increments $\Delta W$ of the simulated paths and confirm they have mean $\approx 0$,
variance $\approx dt$, and essentially zero lag-1 autocorrelation (the numerical face of *independent
increments*).

**Why:** properties (2) and (3) of the definition — independent, Gaussian, mean-0, variance-$dt$
increments — are the assumptions every derivation in Q2 leans on. Here you see them hold in data.

**Hint boundary:** `np.diff(W, axis=1)` gives the increments along the time axis."""))

cells.append(code(
'''# TODO — the increments of the paths.
n_steps = 500
dt = T / n_steps
incr3 = ____                             # np.diff(W, axis=1)

flat = incr3.reshape(-1)
lag1 = np.corrcoef(flat[:-1], flat[1:])[0, 1]   # provided: lag-1 autocorrelation
print(f"mean(dW)   = {flat.mean():+.5f}   (should be ~ 0)")
print(f"var(dW)    = {flat.var():.6f}   (should be ~ dt = {dt})")
print(f"lag-1 corr = {lag1:+.5f}   (should be ~ 0: increments are independent)")'''))

cells.append(code(
'''# CHECK — do not edit
assert incr3.shape == (60000, 500), "one increment per step"
assert abs(flat.mean()) < 5e-4, "increments have mean 0"
assert abs(flat.var() - dt) < 5e-5, "increments have variance dt"
assert abs(lag1) < 0.02, "successive increments are (near) uncorrelated — independence"
print("Task 3 OK — increments are i.i.d. N(0, dt): mean 0, variance dt, no autocorrelation.")'''))

# ---- Task 4 ----
cells.append(md(
r"""### Task 4 — Martingale: $E[W_t\mid\mathcal F_s]=W_s$ (and $W_t^2-t$ too)

**Goal:** two checks. (a) Knowing $W_s$ tells you *nothing* about the future increment $W_T-W_s$ — its
average is $0$ regardless of $W_s$, so a regression of the increment on $W_s$ has slope $\approx 0$.
(b) $W_t^2-t$ is a martingale, so $E[W_T^2]\approx T$.

**Why:** the martingale property is the bridge from Lesson 011 to pricing. And the leftover $t$ in
$W_t^2-t$ is the quadratic variation, previewed — you will meet it head-on in Task 5.

**Hint boundary:** $E[W_T^2]$ is just the sample mean of `W[:, -1] ** 2`."""))

cells.append(code(
'''# TODO — the two martingale checks.
s_idx = n_steps // 2
W_s = W[:, s_idx]
future_incr = W[:, -1] - W_s
slope = np.polyfit(W_s, future_incr, 1)[0]          # provided: does W_s predict the future move?

mean_WT2 = ____                          # np.mean(W[:, -1] ** 2)   <- E[W_T^2]
print(f"slope of (W_T - W_s) on W_s = {slope:+.4f}   (should be ~ 0: fair game)")
print(f"E[W_T^2] = {mean_WT2:.4f}   (should be ~ T = {T}, so W_t^2 - t is a martingale)")'''))

cells.append(code(
'''# CHECK — do not edit
assert abs(slope) < 0.02, "knowing W_s must not predict the future increment (martingale)"
assert abs(mean_WT2 - T) < 0.03, "E[W_T^2] = T, i.e. E[W_T^2 - T] = 0"
# stronger: E[W_T^2 | W_s bucket] should track W_s^2 + (T - s)
s_time = s_idx * dt
lo, hi = np.quantile(W_s, [0.45, 0.55])
mid = (W_s > lo) & (W_s < hi)
pred = W_s[mid] ** 2 + (T - s_time)
assert abs((W[mid, -1] ** 2).mean() - pred.mean()) < 0.05, "E[W_T^2|F_s] = W_s^2 + (T - s)"
print(f"Task 4 OK — W_t is a martingale (slope ~ 0) and E[W_T^2] = {mean_WT2:.3f} = T.")'''))

# ---- Task 5 ----
cells.append(md(
r"""### Task 5 — Quadratic variation: $[W]_t=t$ (a smooth curve gives $0$)

**Goal:** write `quad_var(path)` = sum of squared increments. Compute it for one fine Brownian path
(should be $\approx T$) and for the smooth line $f(t)=t$ on the same grid (should be $\approx 0$). Then
watch the Brownian value's *wobble* shrink as the mesh refines.

**Why:** this is the headline of the lesson and the seed of Itô. The squared wiggles of Brownian motion
do **not** vanish; they accumulate to exactly $t$. A smooth curve's do vanish — which is the assumption
ordinary calculus rests on.

**Hint boundary:** `d = np.diff(path)`; the quadratic variation is the sum of `d ** 2`."""))

cells.append(code(
'''# TODO — quadratic variation.
def quad_var(path):
    """Sum of squared increments of a 1-D path: an approximation to [path]_T."""
    d = np.diff(path)
    qv = ____                            # np.sum(d ** 2)
    return qv

fine = sample_bm(1, 20000, T, rng)[0]          # one fine Brownian path
grid = np.linspace(0.0, T, 20001)              # the smooth line f(t) = t on the same grid
print(f"[W]_T  (Brownian, 20000 steps) = {quad_var(fine):.4f}   (should be ~ T = {T})")
print(f"[f]_T  (smooth f(t)=t)         = {quad_var(grid):.6f}   (should be ~ 0)")

print(f"\\n{'mesh m':>8} {'mean QV':>9} {'std QV':>9}")
qv_std = []
for m in [50, 500, 5000]:
    qvs = np.array([quad_var(sample_bm(1, m, T, rng)[0]) for _ in range(300)])
    qv_std.append(qvs.std())
    print(f"{m:>8} {qvs.mean():9.4f} {qvs.std():9.4f}")'''))

cells.append(code(
'''# CHECK — do not edit
assert abs(quad_var(fine) - T) < 0.1, "[W]_T must be ~ T for a fine Brownian path"
assert quad_var(grid) < 1e-3, "a smooth curve has (essentially) zero quadratic variation"
assert qv_std[0] > qv_std[1] > qv_std[2], "QV concentrates on t: its wobble must shrink as the mesh refines"
# the smooth sum literally equals 1/m and marches to 0
assert np.isclose(quad_var(np.linspace(0.0, T, 101)), T * T / 100), "smooth QV = T^2/m -> 0"
print("Task 5 OK — [W]_T ~ T, smooth QV ~ 0, and the Brownian QV locks onto t as the mesh refines.")'''))

# ---- Task 6 ----
cells.append(md(
r"""### Task 6 — First-order variation explodes (continuous, nowhere differentiable)

**Goal:** write `total_var(path)` = sum of the *absolute* increments $\sum|\Delta W|$, and show it grows
without bound as the mesh refines (it scales like $\sqrt m$), while a smooth curve's stays fixed at its
length. Then watch the largest local slope $|\Delta W|/\Delta t$ blow up.

**Why:** this is the numerical face of "continuous but nowhere differentiable". The path length is
infinite in the limit and the slope has no finite value — which is exactly why we write $dW$, never
$W'(t)$, and why $(dW)^2$ cannot be dropped.

**Hint boundary:** `np.sum(np.abs(np.diff(path)))` for the first-order variation."""))

cells.append(code(
'''# TODO — first-order variation.
def total_var(path):
    """Sum of |increments|: the path's first-order variation (its length)."""
    tv = ____                            # np.sum(np.abs(np.diff(path)))
    return tv

print(f"{'mesh m':>8} {'Sum|dW|':>9} {'max|dW|/dt':>12}")
tv_vals, max_slope = [], []
for m in [100, 400, 1600, 6400]:
    p = sample_bm(1, m, T, rng)[0]
    tv_vals.append(total_var(p))
    max_slope.append(np.max(np.abs(np.diff(p))) * m)   # |dW|/dt with dt = T/m
    print(f"{m:>8} {tv_vals[-1]:9.3f} {max_slope[-1]:12.1f}")

# a smooth curve's length is fixed no matter how finely you chop it:
print(f"\\nsmooth f(t)=t length at m=100: {total_var(np.linspace(0,T,101)):.4f}  "
      f"| at m=6400: {total_var(np.linspace(0,T,6401)):.4f}  (both = T)")'''))

cells.append(code(
'''# CHECK — do not edit
assert tv_vals[0] < tv_vals[1] < tv_vals[2] < tv_vals[3], "first-order variation must grow with the mesh"
ratio = tv_vals[-1] / tv_vals[0]           # expected ~ sqrt(6400/100) = 8
assert 4.0 < ratio < 12.0, f"Sum|dW| should scale like sqrt(m); ratio {ratio:.1f} off"
assert max_slope[-1] > max_slope[0], "the largest local slope blows up as dt -> 0 (nowhere differentiable)"
assert np.isclose(total_var(np.linspace(0, T, 101)), T) and np.isclose(total_var(np.linspace(0, T, 6401)), T), \\
    "a smooth curve's length is fixed at T"
print(f"Task 6 OK — Sum|dW| grew {ratio:.1f}x (~sqrt(m)); slopes explode; smooth length stays T.")'''))

# ---- EXIT ----
cells.append(code(
'''# EXIT TICKET — paste this output to your teacher.
print("=== Lab 012: random walks & Brownian motion ===")
print(f"Scaling           : Var(W^n_1) for n=1,64,1024 = "
      f"{[round(scaled_walk_endpoint(40000, n, rng).var(), 3) for n in (1, 64, 1024)]}  (all ~1 = t)")
print(f"Simulated BM      : Var(W_t) linear in t? Var(W_T)={W[:,-1].var():.3f}, "
      f"Var(W_T/2)={W[:, W.shape[1]//2].var():.3f}")
print(f"Increments        : mean {flat.mean():+.4f}, var {flat.var():.5f} (~dt={dt}), lag1 corr {lag1:+.4f}")
print(f"Martingale        : slope(W_T-W_s | W_s) = {slope:+.4f} (~0);  E[W_T^2] = {mean_WT2:.3f} (=T)")
print(f"Quadratic var.    : [W]_T = {quad_var(fine):.4f} (~T);  smooth [f]_T = {quad_var(grid):.2e} (~0);  "
      f"QV std shrinks {['%.3f' % s for s in qv_std]}")
print(f"First-order var.  : Sum|dW| = {['%.2f' % v for v in tv_vals]} (grows ~sqrt(m));  "
      f"max|dW|/dt = {['%.0f' % s for s in max_slope]} (explodes)")
print()
print("One-sentence takeaway (edit me):")
print("Brownian motion is the sqrt(n)-scaled random walk: mean 0, Var(W_t)=t, independent Gaussian")
print("increments, a martingale, continuous but nowhere differentiable - and its quadratic variation")
print("[W]_t = t (i.e. (dW)^2 = dt) is the non-vanishing squared wiggle that ordinary calculus cannot")
print("drop, which is exactly why Ito's lemma (Lesson 013) needs an extra second-order term.")'''))

# ---- Stretch ----
cells.append(md(
r"""### Stretch (optional, ungraded)

- **Geometric Brownian motion (Lesson 014 preview).** Build $S_t = S_0\exp\big((\mu-\tfrac12\sigma^2)t
  + \sigma W_t\big)$ with $S_0=100,\mu=0.05,\sigma=0.2$. Check that $E[S_T]\approx S_0 e^{\mu T}$ and that
  $\log S_t$ has the straight-line-plus-Brownian shape. (Why the $-\tfrac12\sigma^2$? That is the Itô
  correction — the quadratic variation showing up. You will derive it next lesson.)
- **Realized variance with noise.** Add tiny i.i.d. measurement noise to each observed price and recompute
  $\sum(\Delta W)^2$. Watch the estimate blow up as the mesh refines — microstructure noise is why naive
  realized variance is biased (Year 1 Q3, Lesson 024).
- **Reflection principle.** Estimate $P(\max_{t\le T} W_t > a)$ by simulation and compare with the exact
  $2\,P(W_T > a)$. This is the key identity behind barrier-option pricing.
- **Convergence rate.** For the scaled walk, measure how fast the distribution of $W^{(n)}_1$ approaches
  $N(0,1)$ (e.g. via a Kolmogorov–Smirnov distance) as $n$ grows — a hands-on view of the CLT rate.
- **Correlated increments break the martingale.** Replace the independent increments with an AR(1) (add
  a little momentum) and show the "slope of future increment on $W_s$" is no longer $0$ — the process
  now has a predictable drift."""))

nb = {"cells": cells,
      "metadata": {"kernelspec": {"display_name": "Financial Eng Labs (.venv)",
                                   "language": "python", "name": "feq-labs"},
                   "language_info": {"name": "python", "version": "3.12"}},
      "nbformat": 4, "nbformat_minor": 5}

lab_path = "labs/0012-brownian-motion.ipynb"
with open(lab_path, "w") as f:
    json.dump(nb, f, indent=1)
    f.write("\n")
print("wrote", lab_path)

# ---- Build the filled SOLUTION by replacing the ____ blanks with the hinted answers ----
answers = {
    "w_scaled = ____": "w_scaled = M / np.sqrt(n)",
    "incr = ____": "incr = Z * np.sqrt(dt)",
    "incr3 = ____": "incr3 = np.diff(W, axis=1)",
    "mean_WT2 = ____": "mean_WT2 = np.mean(W[:, -1] ** 2)",
    "qv = ____": "qv = np.sum(d ** 2)",
    "tv = ____": "tv = np.sum(np.abs(np.diff(path)))",
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
sol_path = "solutions/0012-brownian-motion.ipynb"
with open(sol_path, "w") as f:
    json.dump(sol, f, indent=1)
    f.write("\n")
print("wrote", sol_path)
