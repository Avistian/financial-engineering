"""Generate labs/0011-conditional-expectation-tree.ipynb (blanks) and its filled solution.

Run:  ./.venv/bin/python scripts/_gen_lab_0011.py
"""
import json, copy, os

def md(src):
    return {"cell_type": "markdown", "metadata": {}, "source": src.splitlines(keepends=True)}

def code(src):
    return {"cell_type": "code", "metadata": {}, "execution_count": None,
            "outputs": [], "source": src.rstrip("\n").splitlines(keepends=True)}

cells = []

cells.append(md(
"""# Lab 011 — Conditional expectation on a tree

**Lesson:** [`0011-filtrations-conditional-expectation.html`](../lessons/0011-filtrations-conditional-expectation.html)
· **Reference:** [`conditional-expectation.html`](../reference/conditional-expectation.html)

**The one skill:** build a filtration in code and compute **E[X | F_t]** — then *verify the theory
numerically* rather than taking it on faith. By the end you will have checked, with numbers, that
conditional expectation (1) is F_t-measurable, (2) satisfies **partial averaging** on every event,
(3) obeys the **tower property**, (4) is the **least-squares projection** with an orthogonal
residual, and (5) makes the price a **martingale** for exactly one choice of p.

**Exit criteria:** every CHECK passes and the EXIT TICKET prints cleanly.

**How this notebook works**

| Cell tag | You do |
|----------|--------|
| **PROVIDED** | Run it. Imports, the tree, helpers. |
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

**The tree.** $S_0=100$, three periods, up $u=1.1$ / down $d=0.9$, each with probability $p=\tfrac12$.
An outcome $\omega$ is a *complete* path like `HTH`, so $\Omega$ has $2^3=8$ elements.

**Information.** $\mathcal F_t$ = what you know after $t$ flips. Its **atoms** (cells) are the groups
of outcomes sharing the same first $t$ letters: 1 cell at $t=0$, 2 at $t=1$, 4 at $t=2$, 8 at $t=3$.
"$X$ is $\mathcal F_t$-measurable" = "$X$ is constant on every atom" = "$X$ is knowable at time $t$".

**Conditional expectation**, three equivalent ways:

| View | Statement |
|------|-----------|
| Recipe (finite) | $E[X\mid\mathcal F_t]$ averages $X$ within each atom |
| Definition | the $\mathcal F$-measurable $Y$ with $E[Y\mathbf 1_A]=E[X\mathbf 1_A]$ for **all** $A\in\mathcal F$ |
| Projection | $E[X\mid\mathcal F]=\arg\min E[(X-Y)^2]$ over $\mathcal F$-measurable $Y$; residual $\perp$ everything in $\mathcal F$ |

**Rules:** tower $E[E[X|\mathcal F_t]|\mathcal F_s]=E[X|\mathcal F_s]$ ($s\le t$) · take out what is known
$E[YX|\mathcal F]=Y\,E[X|\mathcal F]$ · independence $E[X|\mathcal F]=E[X]$.

**Martingale:** $E[M_t\mid\mathcal F_s]=M_s$. Today's payoff to condition on is the call
$V=(S_3-100)^+$; the answers you should reproduce are $E[V]=7.475$, $E[V|\mathcal F_1]\in\{12.725,\,2.225\}$,
$E[V|\mathcal F_2]\in\{21.00,\,4.45,\,4.45,\,0\}$."""))

cells.append(code(
'''# PROVIDED — the probability space (Omega, F, P) and the two random variables. Run it.
import itertools
import numpy as np

S0, u, d, N, K = 100.0, 1.1, 0.9, 3, 100.0
p_up = 0.5

# Omega: all 8 complete paths, in a FIXED order we index by 0..7 everywhere below.
omega = ["".join(w) for w in itertools.product("HT", repeat=N)]
n_out = len(omega)

# P: each path has probability p^(#H) * (1-p)^(#T); with p=0.5 that is 1/8 each.
def path_prob(w, p=p_up):
    return np.prod([p if c == "H" else (1 - p) for c in w])

P = np.array([path_prob(w) for w in omega])

# Prices: S_t depends only on the FIRST t letters of the path.
def price(w, t):
    s = S0
    for c in w[:t]:
        s *= u if c == "H" else d
    return s

S = np.array([[price(w, t) for t in range(N + 1)] for w in omega])   # S[i, t]
V = np.maximum(S[:, N] - K, 0.0)                                     # the call payoff, an F_3 variable

def E(X, prob=None):
    """Plain expectation E[X] = sum over outcomes of X * P."""
    prob = P if prob is None else prob
    return float(np.dot(prob, X))

print(f"{'omega':>6} {'P':>7} {'S1':>7} {'S2':>7} {'S3':>7} {'V':>7}")
for i, w in enumerate(omega):
    print(f"{w:>6} {P[i]:7.3f} {S[i,1]:7.1f} {S[i,2]:7.1f} {S[i,3]:7.1f} {V[i]:7.1f}")
print(f"\\nE[V] = {E(V):.4f}   (this is the number your conditional expectations must average back to)")'''))

# ---- Task 1: atoms of the filtration ----
cells.append(md(
r"""### Task 1 — Build the filtration: the atoms of $\mathcal F_t$

**Goal:** write `atoms(t)` returning a list of lists of outcome indices — the cells of
$\mathcal F_t$. Two outcomes are in the same cell iff their **first `t` letters agree**.

**Why:** the filtration *is* this family of partitions. Everything else in the lab is computed off it,
and "measurable" will mean "constant on these cells".

**Hint boundary:** group indices by the key `omega[i][:t]`. Keep the cells in sorted key order so the
output is deterministic: `sorted(groups)`."""))

cells.append(code(
'''# TODO — the atoms (cells) of F_t.
def atoms(t):
    """Partition of Omega given the first t flips: list of lists of outcome indices."""
    groups = {}
    for i, w in enumerate(omega):
        key = ____                      # omega[i][:t]  -> the observable prefix
        groups.setdefault(key, []).append(i)
    return [groups[k] for k in sorted(groups)]

for t in range(N + 1):
    cells_t = atoms(t)
    print(f"F_{t}: {len(cells_t)} atom(s) ->", [[omega[i] for i in c] for c in cells_t])'''))

cells.append(code(
'''# CHECK — do not edit
for t in range(N + 1):
    cells_t = atoms(t)
    assert len(cells_t) == 2 ** t, f"F_{t} must have 2^{t} atoms, got {len(cells_t)}"
    flat = sorted(i for c in cells_t for i in c)
    assert flat == list(range(n_out)), "the atoms must partition Omega exactly once"
    assert all(len(c) == n_out // 2 ** t for c in cells_t), "atoms of F_t are all the same size here"
# information only grows: every atom of F_t sits inside an atom of F_{t-1}
for t in range(1, N + 1):
    coarse = [set(c) for c in atoms(t - 1)]
    assert all(any(set(c) <= C for C in coarse) for c in atoms(t)), "F_{t-1} must be coarser than F_t"
print("Task 1 OK — filtration built: 1, 2, 4, 8 atoms, and each F_t refines F_{t-1}.")'''))

# ---- Task 2: measurability ----
cells.append(md(
r"""### Task 2 — Measurability: which variables are knowable when?

**Goal:** write `is_measurable(X, t)` — True iff `X` is constant on every atom of $\mathcal F_t$.

**Why:** this one predicate is the formal no-look-ahead test. A strategy that fails it is *leakage*,
not a modelling choice.

**Hint boundary:** for each cell, compare `X[cell]` against its first element with
`np.allclose(...)`; require it for all cells."""))

cells.append(code(
'''# TODO — is X knowable at time t?
def is_measurable(X, t, tol=1e-9):
    """True iff X is constant on each atom of F_t (i.e. X is F_t-measurable)."""
    return all(____ for c in atoms(t))      # np.allclose(X[c], X[c][0], atol=tol)

for t in range(N + 1):
    print(f"t={t}:  S_1 {is_measurable(S[:,1], t)!s:>5}   "
          f"S_2 {is_measurable(S[:,2], t)!s:>5}   V {is_measurable(V, t)!s:>5}")'''))

cells.append(code(
'''# CHECK — do not edit
assert is_measurable(S[:, 1], 1) and not is_measurable(S[:, 2], 1), "S_2 is not knowable at time 1"
assert is_measurable(S[:, 2], 2) and is_measurable(V, 3)
assert not is_measurable(V, 2), "the call payoff is not knowable before expiry"
assert all(is_measurable(S[:, t], t) for t in range(N + 1)), "the price process must be adapted"
# sigma(S_2) is strictly COARSER than F_2: HT and TH share the price 99 but not the path
same_price = [i for i, w in enumerate(omega) if np.isclose(S[i, 2], 99.0)]
assert {omega[i][:2] for i in same_price} == {"HT", "TH"}, "HT and TH should both reach S_2 = 99"
print("Task 2 OK — S_t is adapted, V is not knowable early, and price info < path info.")'''))

# ---- Task 3: conditional expectation ----
cells.append(md(
r"""### Task 3 — Compute $E[X\mid\mathcal F_t]$ (average within each atom)

**Goal:** write `cond_exp(X, t)` returning an array of length 8 — the conditional expectation as a
**random variable**, constant on each atom. Inside a cell $A$ use the *renormalised* weights:
$$E[X\mid\mathcal F_t](\omega)=\frac{\sum_{i\in A}X_i P_i}{\sum_{i\in A}P_i}\quad\text{for }\omega\in A .$$

**Why:** this is Layer 2 of the lesson. Note the output type: an array, not a scalar — that *is* the
point.

**Hint boundary:** per cell, `val = np.dot(P[c], X[c]) / P[c].sum()`, then assign `Y[c] = val`."""))

cells.append(code(
'''# TODO — conditional expectation as a random variable.
def cond_exp(X, t):
    """E[X | F_t] — an array over outcomes, constant on each atom of F_t."""
    Y = np.zeros(n_out)
    for c in atoms(t):
        c = np.array(c)
        val = ____                      # np.dot(P[c], X[c]) / P[c].sum()
        Y[c] = val
    return Y

for t in range(N + 1):
    Y = cond_exp(V, t)
    print(f"E[V | F_{t}] = ", np.round([Y[c[0]] for c in atoms(t)], 4))'''))

cells.append(code(
'''# CHECK — do not edit
assert np.isclose(cond_exp(V, 0)[0], 7.475), "E[V|F_0] must be the unconditional mean 7.475"
assert np.allclose(sorted({round(v, 4) for v in cond_exp(V, 1)}), [2.225, 12.725])
assert np.allclose(sorted({round(v, 4) for v in cond_exp(V, 2)}), [0.0, 4.45, 21.0])
assert np.allclose(cond_exp(V, 3), V), "with full information there is nothing left to average"
assert all(is_measurable(cond_exp(V, t), t) for t in range(N + 1)), "E[X|F_t] must be F_t-measurable"
print("Task 3 OK — 7.475 / (12.725, 2.225) / (21.00, 4.45, 4.45, 0) / V itself.")'''))

# ---- Task 4: partial averaging (the definition) ----
cells.append(md(
r"""### Task 4 — The *definition*: partial averaging on every event of $\mathcal F_t$

**Goal:** verify $E[Y\mathbf 1_A]=E[X\mathbf 1_A]$ for **every** $A\in\mathcal F_t$, where
$Y=E[X|\mathcal F_t]$. The events of $\mathcal F_t$ are exactly the **unions of atoms**, so enumerate
all $2^{(\#\text{atoms})}$ of them.

**Why:** this is the definition that survives continuous time, where you cannot divide by
$P(\text{atom})=0$. Here you get to see it hold exactly, event by event — including the count
$|\mathcal F_t| = 2^{2^t}$ (2, 4, 16, 256).

**Hint boundary:** indicator of a union of atoms: build `ind = np.zeros(n_out)` then `ind[i] = 1` for
each index in the chosen atoms. `E[X * ind]` is `E(X * ind)`."""))

cells.append(code(
'''# TODO — check partial averaging on all events of F_t.
def events(t):
    """Every A in F_t = every union of atoms of F_t, as a 0/1 indicator array."""
    cells_t = atoms(t)
    for mask in range(2 ** len(cells_t)):
        ind = np.zeros(n_out)
        for j, c in enumerate(cells_t):
            if mask >> j & 1:
                ind[c] = 1.0
        yield ind

def partial_averaging_gap(X, t):
    """Largest |E[Y*1_A] - E[X*1_A]| over all A in F_t, where Y = E[X|F_t]."""
    Y = cond_exp(X, t)
    worst = 0.0
    for ind in events(t):
        gap = abs(____)                 # E(Y * ind) - E(X * ind)
        worst = max(worst, gap)
    return worst

for t in range(N + 1):
    n_events = 2 ** (2 ** t)
    print(f"F_{t}: |F_t| = {n_events:>3} events, worst partial-averaging gap = {partial_averaging_gap(V, t):.2e}")

# the concrete hand-check from the lesson: A = {H..}
A = np.array([1.0 if w[0] == "H" else 0.0 for w in omega])
print(f"\\nA = first move up:  E[V*1_A] = {E(V*A):.4f}   E[E[V|F_1]*1_A] = {E(cond_exp(V,1)*A):.4f}")'''))

cells.append(code(
'''# CHECK — do not edit
for t in range(N + 1):
    assert partial_averaging_gap(V, t) < 1e-9, f"partial averaging must hold for every A in F_{t}"
assert np.isclose(E(V * A), 6.3625) and np.isclose(E(cond_exp(V, 1) * A), 6.3625)
# and it FAILS for a wrong candidate (sanity: the property really is restrictive)
bad = cond_exp(V, 1) + 1.0
assert abs(E(bad * A) - E(V * A)) > 0.1, "a shifted guess should violate partial averaging"
print("Task 4 OK — the cell-averaging recipe satisfies the general definition, exactly (6.3625).")'''))

# ---- Task 5: tower ----
cells.append(md(
r"""### Task 5 — The tower property (and taking out what is known)

**Goal:** verify $E\big[E[V|\mathcal F_t]\,\big|\,\mathcal F_s\big]=E[V|\mathcal F_s]$ for all
$s\le t$, and check *taking out what is known*: $E[S_1V|\mathcal F_1]=S_1E[V|\mathcal F_1]$.

**Why:** these two rules are the workhorses of every Q2 derivation — including the proof that
conditional expectation is a projection (Task 6).

**Hint boundary:** `cond_exp(cond_exp(V, t), s)` for the tower; `S[:,1] * cond_exp(V, 1)` for the
second."""))

cells.append(code(
'''# TODO — iterated conditioning.
tower_max_gap = 0.0
for t in range(N + 1):
    for s in range(t + 1):
        inner = ____                    # cond_exp(cond_exp(V, t), s)
        tower_max_gap = max(tower_max_gap, float(np.max(np.abs(inner - cond_exp(V, s)))))
print(f"tower property: worst gap over all s <= t = {tower_max_gap:.2e}")

takeout_lhs = cond_exp(S[:, 1] * V, 1)
takeout_rhs = ____                      # S[:,1] * cond_exp(V, 1)
print("take out what is known:", np.round(sorted(set(np.round(takeout_lhs, 4))), 4),
      "vs", np.round(sorted(set(np.round(takeout_rhs, 4))), 4))'''))

cells.append(code(
'''# CHECK — do not edit
assert tower_max_gap < 1e-9, "the tower property must hold exactly here"
assert np.allclose(takeout_lhs, takeout_rhs), "an F_1-measurable factor pulls out of E[.|F_1]"
assert np.isclose(sorted(set(np.round(takeout_rhs, 6)))[-1], 110 * 12.725)
# the special case s = 0: averaging any conditional expectation returns E[V]
assert all(np.isclose(E(cond_exp(V, t)), E(V)) for t in range(N + 1))
print(f"Task 5 OK — tower holds, E[E[V|F_t]] = {E(V):.4f} for every t, and known factors pull out.")'''))

# ---- Task 6: projection ----
cells.append(md(
r"""### Task 6 — Conditional expectation IS the least-squares projection

**Goal:** two checks. (a) **Orthogonality:** the residual $V-E[V|\mathcal F_1]$ has
$E[\text{resid}\cdot Z]=0$ for *every* $\mathcal F_1$-measurable $Z$. (b) **Minimality:** brute-force
search over $\mathcal F_1$-measurable guesses $Y=(a$ on $\{H\cdot\cdot\}$, $b$ on $\{T\cdot\cdot\})$
and confirm the minimiser of $E[(V-Y)^2]$ is $(12.725,\,2.225)$.

**Why:** this is the view you will use every week as a researcher — a forecast is a projection of the
future onto what you know, and the residual is by construction unpredictable.

**Hint boundary:** `resid = V - cond_exp(V, 1)`; MSE of a candidate: `E((V - Y) ** 2)`; build the
candidate with `np.where(A == 1, a, b)`."""))

cells.append(code(
'''# TODO — orthogonality of the residual and minimality of the projection.
resid = ____                            # V - cond_exp(V, 1)

# (a) test against a basis of F_1-measurable variables (indicators of the two atoms)
basis = [np.array([1.0 if w[0] == "H" else 0.0 for w in omega]),
         np.array([1.0 if w[0] == "T" else 0.0 for w in omega])]
ortho = [E(resid * Z) for Z in basis]
print("E[resid * 1_cell] for each atom of F_1:", np.round(ortho, 12))

# (b) grid search over F_1-measurable candidates Y = (a on H.., b on T..)
grid = np.arange(0.0, 30.0 + 1e-9, 0.025)
best, best_mse = None, np.inf
for a in grid:
    for b in grid:
        Y = np.where(basis[0] == 1, a, b)
        mse = ____                      # E((V - Y) ** 2)
        if mse < best_mse:
            best, best_mse = (a, b), mse
print(f"grid-search minimiser (a, b) = ({best[0]:.4f}, {best[1]:.4f}),  MSE = {best_mse:.4f}")
print(f"conditional expectation     = (12.725, 2.225),  MSE = {E((V - cond_exp(V,1))**2):.4f}")'''))

cells.append(code(
'''# CHECK — do not edit
assert np.allclose(ortho, 0, atol=1e-9), "the residual must be orthogonal to every F_1-measurable Z"
assert abs(best[0] - 12.725) <= 0.03 and abs(best[1] - 2.225) <= 0.03, "the minimiser IS E[V|F_1]"
mse_star = E((V - cond_exp(V, 1)) ** 2)
assert np.isclose(mse_star, 83.216875), f"minimum MSE should be 83.216875, got {mse_star}"
assert best_mse >= mse_star - 1e-9, "no candidate may beat the projection"
# Pythagoras / variance decomposition: Var(V) = E[Var(V|F_1)] + Var(E[V|F_1])
explained = E((cond_exp(V, 1) - E(V)) ** 2)
assert np.isclose(E((V - E(V)) ** 2), mse_star + explained), "variance must split cleanly"
print(f"Task 6 OK — residual orthogonal; min MSE {mse_star:.4f}; "
      f"Var(V) {E((V-E(V))**2):.4f} = {mse_star:.4f} + {explained:.4f}.")'''))

# ---- Task 7: martingale ----
cells.append(md(
r"""### Task 7 — Which p makes the price a martingale?

**Goal:** the tree so far used $p=\tfrac12$. Write the one-step check
$E[S_{t+1}|\mathcal F_t]\stackrel{?}{=}S_t$ as a function of $p$, find the $p$ that works, and
confirm it equals $p^\*=\frac{1-d}{u-d}$. Then show the property **fails** at $p=0.6$.

**Why:** that $p^\*$ is the risk-neutral probability, and "discounted prices are martingales" is the
engine of all of derivatives pricing (unit 015). You are computing it two units early, by hand.

**Hint boundary:** the probabilities change with `p`, so recompute them: `Pp = np.array([path_prob(w, p)
for w in omega])`, and condition with those weights. `p_star = (1 - d) / (u - d)`."""))

cells.append(code(
'''# TODO — find the martingale measure.
def cond_exp_p(X, t, p):
    """E[X | F_t] under the measure where each up-move has probability p."""
    Pp = np.array([path_prob(w, p) for w in omega])
    Y = np.zeros(n_out)
    for c in atoms(t):
        c = np.array(c)
        Y[c] = np.dot(Pp[c], X[c]) / Pp[c].sum()
    return Y

def martingale_gap(p):
    """Worst |E[S_{t+1}|F_t] - S_t| over all t, under probability p."""
    return max(float(np.max(np.abs(cond_exp_p(S[:, t + 1], t, p) - S[:, t]))) for t in range(N))

p_star = ____                           # (1 - d) / (u - d)
print(f"p* = (1-d)/(u-d) = {p_star:.6f}")
for p in [0.3, 0.4, p_star, 0.6, 0.7]:
    print(f"  p = {p:.2f} -> worst |E[S_t+1|F_t] - S_t| = {martingale_gap(p):8.4f}"
          f"   {'MARTINGALE' if martingale_gap(p) < 1e-9 else ''}")

# and the price of the call under the martingale measure, at zero rates:
call_price = ____                       # E of V under p_star: cond_exp_p(V, 0, p_star)[0]
print(f"\\ncall price = E*[V] = {call_price:.4f}")'''))

cells.append(code(
'''# CHECK — do not edit
assert np.isclose(p_star, 0.5), "with u=1.1, d=0.9 the martingale probability is exactly 1/2"
assert martingale_gap(p_star) < 1e-9, "under p* the price must be a martingale"
assert martingale_gap(0.6) > 1.0, "at p=0.6 the price drifts up ~2% per step — not a martingale"
assert np.isclose(call_price, 7.475), "the call is worth 7.475 at zero rates"
# one-step drift at p=0.6, for the record
drift = 0.6 * u + 0.4 * d
assert np.isclose(drift, 1.02)
print(f"Task 7 OK — p* = {p_star:.4f}; at p = 0.6 the gross drift is {drift:.2f} per step; "
      f"call = {call_price:.4f}.")'''))

# ---- Task 8: leakage ----
cells.append(md(
r"""### Task 8 — Leakage, as a measurability violation

**Goal:** build a "strategy" that decides at time 1 using the *final* payoff (a variable that is
$\mathcal F_3$- but not $\mathcal F_1$-measurable), and compare its expected P&L to the honest
version that may only use $\mathcal F_1$. Show the cheat is *detected* by `is_measurable`.

**Why:** this is the whole of Q1 in one cell. Leakage is not a bug you spot by staring at a backtest —
it is conditioning on a $\sigma$-algebra bigger than the one you had, and it *always* looks profitable.

**Hint boundary:** the cheating rule is `np.where(V > 0, 1.0, -1.0)`; the honest rule is a function of
time-1 information only, e.g. `np.where(S[:,1] > S0, 1.0, -1.0)`. P&L: `rule * (S[:,3] - S[:,1])`."""))

cells.append(code(
'''# TODO — the leak, and the test that catches it.
cheat_rule = ____                       # np.where(V > 0, 1.0, -1.0)   <- uses the FINAL payoff
honest_rule = np.where(S[:, 1] > S0, 1.0, -1.0)

pnl_cheat = E(cheat_rule * (S[:, 3] - S[:, 1]))
pnl_honest = E(honest_rule * (S[:, 3] - S[:, 1]))
print(f"cheating rule : F_1-measurable? {is_measurable(cheat_rule, 1)}   E[P&L] = {pnl_cheat:+.4f}")
print(f"honest rule   : F_1-measurable? {is_measurable(honest_rule, 1)}   E[P&L] = {pnl_honest:+.4f}")'''))

cells.append(code(
'''# CHECK — do not edit
assert not is_measurable(cheat_rule, 1), "the cheating rule peeks at F_3 — that is the leak"
assert is_measurable(honest_rule, 1), "the honest rule may only use time-1 information"
assert pnl_cheat > pnl_honest, "leakage always flatters the backtest"
assert abs(pnl_honest) < 1e-9, "under the martingale measure no adapted rule has an edge"
print(f"Task 8 OK — the leak earns {pnl_cheat:+.3f} out of thin air; the adapted rule earns "
      f"{pnl_honest:+.3f}. Under a martingale, no adapted strategy has an edge.")'''))

# ---- EXIT ----
cells.append(code(
'''# EXIT TICKET — paste this output to your teacher.
print("=== Lab 011: conditional expectation on a tree ===")
print(f"Filtration        : |atoms of F_t| = {[len(atoms(t)) for t in range(N+1)]}, "
      f"|F_t| = {[2 ** (2 ** t) for t in range(N+1)]}")
print(f"Adapted?          : S_t adapted = {all(is_measurable(S[:,t], t) for t in range(N+1))}, "
      f"V measurable only at t = {min(t for t in range(N+1) if is_measurable(V, t))}")
for t in range(N + 1):
    vals = np.round([cond_exp(V, t)[c[0]] for c in atoms(t)], 4).tolist()
    print(f"E[V | F_{t}]        : {vals}")
print(f"Partial averaging : worst gap over ALL events = {max(partial_averaging_gap(V,t) for t in range(N+1)):.1e}")
print(f"Tower property    : worst gap over all s<=t   = {tower_max_gap:.1e}")
print(f"Projection        : min E[(V-Y)^2] = {E((V-cond_exp(V,1))**2):.4f} at Y = E[V|F_1]; "
      f"residual orthogonal = {np.allclose(ortho, 0, atol=1e-9)}")
print(f"Variance split    : Var(V) {E((V-E(V))**2):.4f} = {E((V-cond_exp(V,1))**2):.4f} (unexplained) "
      f"+ {E((cond_exp(V,1)-E(V))**2):.4f} (explained by flip 1)")
print(f"Martingale        : p* = {p_star:.4f}; gap {martingale_gap(p_star):.1e}; "
      f"at p=0.6 gap {martingale_gap(0.6):.3f}")
print(f"Call price        : E*[V] = {call_price:.4f}  (zero rates)")
print(f"Leakage           : F_3 rule earns {pnl_cheat:+.3f} vs adapted {pnl_honest:+.3f}")
print()
print("One-sentence takeaway (edit me):")
print("E[X|F_t] is the F_t-measurable random variable that averages X within each cell of my")
print("information - equivalently the least-squares projection of X onto what I know - so a forecast")
print("is a projection, its residual is unpredictable by construction, and leakage is nothing but")
print("conditioning on a bigger sigma-algebra than I actually had.")'''))

# ---- Stretch ----
cells.append(md(
r"""### Stretch (optional, ungraded)

- **Coarser information.** Build the atoms of $\sigma(S_2)$ (group by the *price* at $t=2$, not the
  path) and confirm there are only 3 cells because `HT` and `TH` fuse. Compute $E[V|\sigma(S_2)]$ and
  compare with $E[V|\mathcal F_2]$ — which is larger on the fused cell, and why? (This is why order
  flow beats price alone: Year 2 Q3.)
- **Path-dependent payoff.** Replace $V$ with a lookback, $\max_t S_t - 100$, and redo Tasks 3–6.
  Nothing in your code should need to change — that is the point of building the filtration properly.
- **Conditional Jensen.** Verify $E[(S_3-K)^+|\mathcal F_2]\ge (E[S_3|\mathcal F_2]-K)^+$ cell by cell
  and find the cell with the biggest gap. That gap is option value from uncertainty (units 016–017).
- **More periods.** Set `N = 6` (64 outcomes) and re-run everything except the $2^{2^t}$ event
  enumeration in Task 4 (which explodes — think about why, and check partial averaging on the atoms
  plus a random sample of unions instead).
- **Non-martingale measure.** Under $p=0.6$, find an adapted rule with positive expected P&L, and
  state in one sentence why no such rule exists under $p^\*$."""))

nb = {"cells": cells,
      "metadata": {"kernelspec": {"display_name": "Financial Eng Labs (.venv)",
                                   "language": "python", "name": "feq-labs"},
                   "language_info": {"name": "python", "version": "3.12"}},
      "nbformat": 4, "nbformat_minor": 5}

lab_path = "labs/0011-conditional-expectation-tree.ipynb"
with open(lab_path, "w") as f:
    json.dump(nb, f, indent=1)
    f.write("\n")
print("wrote", lab_path)

# ---- Build the filled SOLUTION by replacing the ____ blanks with the hinted answers ----
answers = {
    "key = ____": "key = omega[i][:t]",
    "return all(____ for c in atoms(t))": "return all(np.allclose(X[c], X[c][0], atol=tol) for c in atoms(t))",
    "val = ____": "val = np.dot(P[c], X[c]) / P[c].sum()",
    "gap = abs(____)": "gap = abs(E(Y * ind) - E(X * ind))",
    "inner = ____": "inner = cond_exp(cond_exp(V, t), s)",
    "takeout_rhs = ____": "takeout_rhs = S[:, 1] * cond_exp(V, 1)",
    "resid = ____": "resid = V - cond_exp(V, 1)",
    "mse = ____": "mse = E((V - Y) ** 2)",
    "p_star = ____": "p_star = (1 - d) / (u - d)",
    "call_price = ____": "call_price = cond_exp_p(V, 0, p_star)[0]",
    "cheat_rule = ____": "cheat_rule = np.where(V > 0, 1.0, -1.0)",
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
sol_path = "solutions/0011-conditional-expectation-tree.ipynb"
with open(sol_path, "w") as f:
    json.dump(sol, f, indent=1)
    f.write("\n")
print("wrote", sol_path)
