"""One-off builder for Lab 016 (Black–Scholes PDE & Feynman–Kac). Produces the
student notebook and the filled solution notebook from a single source of truth.
Run once, then keep (matches the _gen_lab_XXXX.py convention)."""
import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

CELLS = []

def md(text):
    CELLS.append(("md", text, None))

def code(sol, student=None):
    CELLS.append(("code", sol, student))

md(r"""# Lab 016 — The Black–Scholes PDE: recover it, break it, and meet Feynman–Kac

**Lesson:** [`0016-black-scholes-pde-feynman-kac.html`](../lessons/0016-black-scholes-pde-feynman-kac.html)
· **Reference:** [`feynman-kac.html`](../reference/feynman-kac.html)

**The one skill:** derive the Black–Scholes PDE from Itô plus no-arbitrage, then state
**Feynman–Kac** as the theorem that this PDE and yesterday's discounted $Q$-expectation are the
*same object*. By the end you will have checked, with numbers, that (1) Itô on $V(t,S)$ under $Q$
splits into a predictable piece and a $\Delta$-multiple of $d\widetilde W$, (2) the discounted
process $e^{-rt}V$ is a martingale exactly when the PDE holds, (3) the closed-form call has
**machine-zero residual** on a grid, (4) three damaged equations leave the residuals the lesson
named (drop curvature $\to -3.752$, put $\mu$ in $\to +6.368$, drop funding $\to +0.523$),
(5) a Monte-Carlo under $Q$ lands on $10.4506$, and (6) a one-step local $p^*$-average — the PDE
as a tiny tree — recovers today's value.

**Exit criteria:** every CHECK passes and the EXIT TICKET prints cleanly.

**How this notebook works**

| Cell tag | You do |
|----------|--------|
| **PROVIDED** | Run it. Imports, parameters, the pricing scaffolds. |
| **TODO** | Fill the `____` blanks. This is where the learning is. |
| **CHECK** | Run it — immediate assertions. Don't edit. |
| **EXIT TICKET** | Final deliverable. Prints your summary. |

**Environment:** Python 3 + `numpy` + `scipy` (only for the normal PDF/CDF). Fully self-contained
(no network, runs in seconds). See [`labs/README.md`](./README.md).""")

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

A price is a surface $V(t,s)$ over the clock and the current share price. Under $Q$,
$dS = rS\,dt + \sigma S\,d\widetilde W$. Itô on that surface is

$$dV = \big(V_t + r S V_s + \tfrac12\sigma^2 S^2 V_{ss}\big)dt + \sigma S V_s\,d\widetilde W.$$

Short $\Delta = V_s$ shares and the $d\widetilde W$ cancels. The leftover book is riskless, so it
must earn $r$:

$$V_t + r S V_s + \tfrac12\sigma^2 S^2 V_{ss} - r V = 0, \qquad V(T,s)=(s-K)^+.$$

That is the **Black–Scholes PDE**. **Feynman–Kac** says the solution is yesterday's expectation:

$$V(t,s) = E_Q\big[e^{-r(T-t)}(S_T-K)^+ \,\big|\, S_t = s\big].$$

| Object | Formula | Meaning |
|--------|---------|---------|
| Delta | $V_s = N(d_1)$ | shares that cancel $d\widetilde W$ |
| Gamma | $V_{ss} = n(d_1)/(S\sigma\sqrt{\tau})$ | curvature; the Itô leftover |
| Theta | $V_t = -S n(d_1)\sigma/(2\sqrt{\tau}) - rKe^{-r\tau}N(d_2)$ | time slope |
| PDE residual | $V_t + rSV_s + \tfrac12\sigma^2 S^2 V_{ss} - rV$ | zero iff the surface solves the PDE |
| Four-term budget at $(0,100)$ | $-6.414 + 3.184 + 3.752 - 0.523$ | sums to $0.000$ |

with $\tau = T-t$, $d_1 = \big(\ln(S/K)+(r+\tfrac12\sigma^2)\tau\big)/(\sigma\sqrt{\tau})$,
$d_2 = d_1 - \sigma\sqrt{\tau}$.""")

code(r"""# PROVIDED — market, closed-form call, analytic Greeks. Run it.
import numpy as np
from scipy.stats import norm

rng = np.random.default_rng(20160816)

S0    = 100.0
K     = 100.0
R_F   = 0.05     # cash rate r (continuously compounded)
SIGMA = 0.20
MU    = 0.15     # REAL-WORLD drift — used only where it is a bug
T     = 1.0

def bs_call(S, tau, r=R_F, sigma=SIGMA, K_=K):
    S = np.asarray(S, dtype=float)
    tau = np.asarray(tau, dtype=float)
    out = np.maximum(S - K_, 0.0)
    live = tau > 1e-14
    if not np.any(live):
        return out
    vol = sigma * np.sqrt(tau)
    d1 = (np.log(S / K_) + (r + 0.5 * sigma**2) * tau) / vol
    d2 = d1 - vol
    price = S * norm.cdf(d1) - K_ * np.exp(-r * tau) * norm.cdf(d2)
    return np.where(live, price, out)

def greeks(S, tau, r=R_F, sigma=SIGMA, K_=K):
    # Analytic V, V_t (theta), V_s (delta), V_ss (gamma) for a European call.
    vol = sigma * np.sqrt(tau)
    d1 = (np.log(S / K_) + (r + 0.5 * sigma**2) * tau) / vol
    d2 = d1 - vol
    V = S * norm.cdf(d1) - K_ * np.exp(-r * tau) * norm.cdf(d2)
    delta = norm.cdf(d1)
    gamma = norm.pdf(d1) / (S * vol)
    theta = (-S * norm.pdf(d1) * sigma / (2.0 * np.sqrt(tau))
             - r * K_ * np.exp(-r * tau) * norm.cdf(d2))
    return V, theta, delta, gamma

V0, THETA, DELTA, GAMMA = greeks(S0, T)
print(f"market  : S0={S0}, K={K}, r={R_F}, sigma={SIGMA}, mu={MU}, T={T}")
print(f"call    : V = {V0:.6f}")
print(f"greeks  : theta={THETA:.6f},  delta={DELTA:.6f},  gamma={GAMMA:.6f}")""")

# ---- Task 1 ----
md(r"""### Task 1 — Itô on $V(t,S)$ under $Q$: name the two shove sizes

**Goal:** fill the drift $a$ and the diffusion $b$ of the stock under $Q$, then the predictable
piece of $dV$.

**Why:** the whole PDE is Itô plus a cancellation. You need the three $dt$ pieces in your hands
before you cancel anything. Under $Q$ the stock is $dS = rS\,dt + \sigma S\,d\widetilde W$, so
$a = rS$ and $b = \sigma S$, and

$$\text{drift of }V = V_t + a\,V_s + \tfrac12 b^2 V_{ss}.$$

**Hint boundary:** `R_F * S0` and `SIGMA * S0`.""")

code(r"""# TODO — the stock's drift and diffusion under Q, then the dt piece of dV.
a = R_F * S0                                          # <- fill: r * S
b = SIGMA * S0                                        # <- fill: sigma * S
drift_V = THETA + a * DELTA + 0.5 * b**2 * GAMMA      # <- Itô: V_t + a V_s + (1/2) b^2 V_ss

print(f"a = r S     = {a:.3f}")
print(f"b = sigma S = {b:.3f}")
print(f"drift of V  = theta + a*delta + 0.5*b^2*gamma = {drift_V:.6f}")
print(f"r * V       = {R_F * V0:.6f}   <- hold this; Task 2 says they match")""",
r"""# TODO — the stock's drift and diffusion under Q, then the dt piece of dV.
a = ____                                              # r * S
b = ____                                              # sigma * S
drift_V = THETA + a * DELTA + 0.5 * b**2 * GAMMA      # provided: Itô's dt piece

print(f"a = r S     = {a:.3f}")
print(f"b = sigma S = {b:.3f}")
print(f"drift of V  = theta + a*delta + 0.5*b^2*gamma = {drift_V:.6f}")
print(f"r * V       = {R_F * V0:.6f}   <- hold this; Task 2 says they match")""")

code(r"""# CHECK — do not edit
assert abs(a - 5.0) < 1e-12, "under Q the stock's drift is r S = 0.05 * 100 = 5"
assert abs(b - 20.0) < 1e-12, "the diffusion is sigma S = 0.20 * 100 = 20"
assert abs(drift_V - R_F * V0) < 1e-10, "Itô's dt piece must equal r V — that IS the PDE at this point"
print("Task 1 OK -- a=5, b=20, and the predictable piece of dV is rV = 0.5225.")""")

# ---- Task 2 ----
md(r"""### Task 2 — Discounted price is a martingale $\Leftrightarrow$ the PDE

**Goal:** form the $dt$ coefficient of $d(e^{-rt}V)$ and set it to zero. That coefficient is the
**PDE residual**.

**Why:** Lesson 015 said discounted prices are $Q$-martingales, i.e. they have no $dt$ term.
Itô on the product $e^{-rt}V$ (linear in $V$, so no extra correction on the discount) gives

$$d(e^{-rt}V) = e^{-rt}\big(V_t + rSV_s + \tfrac12\sigma^2 S^2 V_{ss} - rV\big)dt + \cdots\,d\widetilde W.$$

The thing in parentheses is the residual. For a true price it is zero.

**Hint boundary:** `drift_V - R_F * V0`.""")

code(r"""# TODO — the PDE residual at (t=0, S=100).
resid = drift_V - R_F * V0                            # <- fill: dt coeff of d(e^{-rt} V), up to e^{-rt}

print(f"PDE residual at (0, 100) = {resid:.3e}")
print(f"four-term budget         = {THETA:.4f} + {R_F*S0*DELTA:.4f} + {0.5*SIGMA**2*S0**2*GAMMA:.4f} + {-R_F*V0:.4f}")""",
r"""# TODO — the PDE residual at (t=0, S=100).
resid = ____                                          # drift_V - r * V

print(f"PDE residual at (0, 100) = {resid:.3e}")
print(f"four-term budget         = {THETA:.4f} + {R_F*S0*DELTA:.4f} + {0.5*SIGMA**2*S0**2*GAMMA:.4f} + {-R_F*V0:.4f}")""")

code(r"""# CHECK — do not edit
assert abs(resid) < 1e-12, "the closed form is an exact solution, so the residual is machine zero"
# name the four pieces so a broken budget is obvious
carry = R_F * S0 * DELTA
convex = 0.5 * SIGMA**2 * S0**2 * GAMMA
fund = R_F * V0
assert abs(THETA + carry + convex - fund) < 1e-12
assert abs(THETA + 6.4140) < 5e-4
assert abs(carry - 3.1842) < 5e-4
assert abs(convex - 3.7524) < 5e-4
assert abs(fund - 0.5225) < 5e-4
print("Task 2 OK -- residual is 0. The budget is -6.414 + 3.184 + 3.752 - 0.523 = 0.")""")

# ---- Task 3 ----
md(r"""### Task 3 — The residual is zero on a grid, not just at one point

**Goal:** fill the residual function $V_t + r s V_s + \tfrac12\sigma^2 s^2 V_{ss} - r V$ and
evaluate it on a small grid of times and spots.

**Why:** a solution of a PDE is a solution *everywhere*, not at the one point we like. If the
residual is machine-zero on a grid, you have earned the right to trust the formula as a PDE
solution, not just as an average.

**Hint boundary:** `Vt + R_F*S*Vs + 0.5*SIGMA**2*S**2*Vss - R_F*V`.""")

code(r"""# TODO — the PDE residual as a function of (S, tau).
def pde_resid(S, tau):
    V, Vt, Vs, Vss = greeks(S, tau)
    return Vt + R_F * S * Vs + 0.5 * SIGMA**2 * S**2 * Vss - R_F * V   # <- fill

spots = np.array([80.0, 100.0, 120.0])
taus  = np.array([0.25, 0.50, 1.00])
grid = np.array([[pde_resid(s, tau) for s in spots] for tau in taus])
print("residual grid (rows = tau 0.25/0.50/1.00, cols = S 80/100/120):")
print(np.array2string(grid, formatter={"float_kind": lambda x: f"{x: .2e}"}))
print(f"max |residual| = {np.max(np.abs(grid)):.3e}")""",
r"""# TODO — the PDE residual as a function of (S, tau).
def pde_resid(S, tau):
    V, Vt, Vs, Vss = greeks(S, tau)
    return ____                                       # V_t + r S V_s + 0.5 sigma^2 S^2 V_ss - r V

spots = np.array([80.0, 100.0, 120.0])
taus  = np.array([0.25, 0.50, 1.00])
grid = np.array([[pde_resid(s, tau) for s in spots] for tau in taus])
print("residual grid (rows = tau 0.25/0.50/1.00, cols = S 80/100/120):")
print(np.array2string(grid, formatter={"float_kind": lambda x: f"{x: .2e}"}))
print(f"max |residual| = {np.max(np.abs(grid)):.3e}")""")

code(r"""# CHECK — do not edit
assert np.max(np.abs(grid)) < 1e-11, "analytic Greeks make the residual machine-zero on the whole grid"
assert abs(pde_resid(S0, T)) < 1e-12
print("Task 3 OK -- the formula solves the PDE at every (S, tau) we checked, not just ATM 1y.")""")

# ---- Task 4 ----
md(r"""### Task 4 — Put $\mu$ in the PDE on purpose

**Goal:** evaluate the *damaged* residual that uses $\mu$ on the slope instead of $r$.

**Why:** this is the continuous-time face of Lesson 015's "simulate with $\mu$" bug. The leftover
equals $(\mu-r)S V_s$ — the risk premium on the delta, counted twice. If your PDE mentions the
real-world drift, it is not a pricing equation.

**Hint boundary:** `THETA + MU*S0*DELTA + 0.5*SIGMA**2*S0**2*GAMMA - R_F*V0`.""")

code(r"""# TODO — residual of the mu-PDE (wrong slope coefficient).
resid_mu = THETA + MU * S0 * DELTA + 0.5 * SIGMA**2 * S0**2 * GAMMA - R_F * V0  # <- fill
print(f"mu-PDE residual     = {resid_mu:.4f}")
print(f"(mu - r) * S * Δ    = {(MU - R_F) * S0 * DELTA:.4f}   <- they must match")""",
r"""# TODO — residual of the mu-PDE (wrong slope coefficient).
resid_mu = ____                                       # theta + mu*S*delta + 0.5*sig^2*S^2*gamma - r*V
print(f"mu-PDE residual     = {resid_mu:.4f}")
print(f"(mu - r) * S * Δ    = {(MU - R_F) * S0 * DELTA:.4f}   <- they must match")""")

code(r"""# CHECK — do not edit
assert abs(resid_mu - (MU - R_F) * S0 * DELTA) < 1e-12, "the leftover must be exactly (mu-r) S delta"
assert abs(resid_mu - 6.3683) < 5e-4, "at these numbers that leftover is 6.368"
print("Task 4 OK -- putting mu in the PDE leaves +6.368, the risk premium on 0.64 shares.")""")

# ---- Task 5 ----
md(r"""### Task 5 — Drop the Itô correction, and drop the funding term

**Goal:** form the two other damaged residuals from the lesson: ordinary calculus (no
$\tfrac12\sigma^2 S^2 V_{ss}$) and a book that funds the option for free (no $-rV$).

**Why:** each leftover equals the term you dropped. The residual is a unit test that names the
bug, not just a red flag.

**Hint boundary:** `THETA + R_F*S0*DELTA - R_F*V0` and `THETA + R_F*S0*DELTA + 0.5*SIGMA**2*S0**2*GAMMA`.""")

code(r"""# TODO — two more damaged residuals.
resid_no_gamma = THETA + R_F * S0 * DELTA - R_F * V0                          # <- drop curvature
resid_no_fund = THETA + R_F * S0 * DELTA + 0.5 * SIGMA**2 * S0**2 * GAMMA  # <- drop -rV

print(f"drop curvature : residual = {resid_no_gamma:.4f}   (should be -3.752)")
print(f"drop funding   : residual = {resid_no_fund:.4f}   (should be +0.523)")""",
r"""# TODO — two more damaged residuals.
resid_no_gamma = ____                                 # theta + r*S*delta - r*V   (no curvature)
resid_no_fund = ____                                 # theta + r*S*delta + 0.5*sig^2*S^2*gamma

print(f"drop curvature : residual = {resid_no_gamma:.4f}   (should be -3.752)")
print(f"drop funding   : residual = {resid_no_fund:.4f}   (should be +0.523)")""")

code(r"""# CHECK — do not edit
convex = 0.5 * SIGMA**2 * S0**2 * GAMMA
assert abs(resid_no_gamma + convex) < 1e-12, "dropping curvature leaves residual = -convex"
assert abs(resid_no_fund - R_F * V0) < 1e-12, "dropping -rV leaves residual = +rV"
assert abs(resid_no_gamma + 3.7524) < 5e-4
assert abs(resid_no_fund - 0.5225) < 5e-4
print("Task 5 OK -- drop curvature -> -3.752; drop funding -> +0.523. The residual names the missing term.")""")

# ---- Task 6 ----
md(r"""### Task 6 — Feynman–Kac, the expectation machine

**Goal:** fill the $Q$-terminal stock $S_T = S_0\exp\big((r-\tfrac12\sigma^2)T + \sigma\sqrt{T}\,Z\big)$
and the discounted-payoff Monte-Carlo.

**Why:** Feynman–Kac says this average *is* the PDE solution. Landing on $10.4506$ is the
landing the lesson drew as red dots on a green curve.

**Hint boundary:** `(R_F - 0.5*SIGMA**2)*T + SIGMA*np.sqrt(T)*Z`.""")

code(r"""# TODO — terminal stock under Q, then the discounted-payoff average.
n_mc = 80_000
Z = rng.standard_normal(n_mc // 2)
Z = np.concatenate([Z, -Z])                   # provided: antithetic pair, tighter average
S_T = S0 * np.exp((R_F - 0.5 * SIGMA**2) * T + SIGMA * np.sqrt(T) * Z)   # <- fill the exponent
payoff = np.maximum(S_T - K, 0.0)
mc_price = np.exp(-R_F * T) * payoff.mean()                               # provided: discount the average

print(f"Monte-Carlo under Q : {mc_price:.4f}")
print(f"closed form         : {V0:.4f}")
print(f"gap                 : {mc_price - V0:+.4f}")""",
r"""# TODO — terminal stock under Q, then the discounted-payoff average.
n_mc = 80_000
Z = rng.standard_normal(n_mc // 2)
Z = np.concatenate([Z, -Z])                   # provided: antithetic pair, tighter average
S_T = S0 * np.exp(____)                               # (r - 0.5*sigma^2)*T + sigma*sqrt(T)*Z
payoff = np.maximum(S_T - K, 0.0)
mc_price = np.exp(-R_F * T) * payoff.mean()           # provided: discount the average

print(f"Monte-Carlo under Q : {mc_price:.4f}")
print(f"closed form         : {V0:.4f}")
print(f"gap                 : {mc_price - V0:+.4f}")""")

code(r"""# CHECK — do not edit
assert abs(mc_price - V0) < 0.12, "80k antithetic Q-paths must land within 0.12 of 10.4506"
# the usual bug: drifting at mu instead of r inflates the price
S_T_mu = S0 * np.exp((MU - 0.5 * SIGMA**2) * T + SIGMA * np.sqrt(T) * Z)
mc_wrong = np.exp(-R_F * T) * np.maximum(S_T_mu - K, 0.0).mean()
assert mc_wrong - V0 > 4.0, "drifting at mu=15% must inflate the 'price' by several dollars"
print(f"Task 6 OK -- MC under Q = {mc_price:.4f} (gap {mc_price-V0:+.4f}). "
      f"Drifting at mu prints {mc_wrong:.2f}, the 015 bug again.")""")

# ---- Task 7 ----
md(r"""### Task 7 — Feynman–Kac, the one-step tree (the PDE as a local average)

**Goal:** fill the one-step CRR weights and the discounted two-child average of *tomorrow's*
closed-form value. That local average must recover *today's* value.

**Why:** this is Feynman–Kac at the smallest scale. The PDE *is* the statement that today's
$V$ equals a discounted $p^*$-average of $V$ an instant later. A binomial node is that
statement, discretised. The 2,000-step tree of Lab 015 was this node, repeated.

**Hint boundary:** `p_star = (R - d) / (u - d)`, then `np.exp(-R_F*dt)*(p_star*V_u + (1-p_star)*V_d)`.""")

code(r"""# TODO — one-step local expectation at (t=0, S=100).
dt = 1.0 / 252.0                                      # one trading day
u = np.exp(SIGMA * np.sqrt(dt))
d = 1.0 / u
R = np.exp(R_F * dt)
p_star = (R - d) / (u - d)                            # <- fill

V_u = float(bs_call(S0 * u, T - dt))                  # provided: tomorrow's value if up
V_d = float(bs_call(S0 * d, T - dt))                  # provided: tomorrow's value if down
V_local = np.exp(-R_F * dt) * (p_star * V_u + (1.0 - p_star) * V_d)  # <- fill

print(f"u, d, p*   : {u:.6f}, {d:.6f}, {p_star:.6f}")
print(f"V_u, V_d   : {V_u:.4f}, {V_d:.4f}")
print(f"local avg  : {V_local:.6f}")
print(f"today's V  : {V0:.6f}")
print(f"gap        : {V_local - V0:+.2e}")""",
r"""# TODO — one-step local expectation at (t=0, S=100).
dt = 1.0 / 252.0                                      # one trading day
u = np.exp(SIGMA * np.sqrt(dt))
d = 1.0 / u
R = np.exp(R_F * dt)
p_star = ____                                         # (R - d) / (u - d)

V_u = float(bs_call(S0 * u, T - dt))                  # provided: tomorrow's value if up
V_d = float(bs_call(S0 * d, T - dt))                  # provided: tomorrow's value if down
V_local = ____                                        # e^{-r dt} * (p* V_u + (1-p*) V_d)

print(f"u, d, p*   : {u:.6f}, {d:.6f}, {p_star:.6f}")
print(f"V_u, V_d   : {V_u:.4f}, {V_d:.4f}")
print(f"local avg  : {V_local:.6f}")
print(f"today's V  : {V0:.6f}")
print(f"gap        : {V_local - V0:+.2e}")""")

code(r"""# CHECK — do not edit
assert 0.0 < p_star < 1.0, "p* is a probability: the no-arbitrage window d < R < u"
assert abs(p_star - (R - d) / (u - d)) < 1e-12
assert abs(V_local - V0) < 5e-4, "a one-day node must recover today's 10.4506 to a few hundredths of a cent"
print("Task 7 OK -- the one-step p*-average recovers today's price. That node IS the PDE.")""")

# ---- EXIT ----
code(r"""# EXIT TICKET — paste this output to your teacher.
print("=== Lab 016: the Black-Scholes PDE and Feynman-Kac ===")
print(f"Itô under Q      : a=rS={a:.1f}, b=sigma S={b:.1f}, drift of V={drift_V:.4f} (= rV)")
print(f"PDE residual     : {resid:.2e} at (0,100); max on the 3x3 grid {np.max(np.abs(grid)):.2e}")
print(f"Four-term budget : {THETA:.3f} + {R_F*S0*DELTA:.3f} + {0.5*SIGMA**2*S0**2*GAMMA:.3f} - {R_F*V0:.3f} = 0")
print(f"Damaged residuals: mu-in={resid_mu:.3f}, no-gamma={resid_no_gamma:.3f}, no-fund={resid_no_fund:.3f}")
print(f"Feynman-Kac MC   : {mc_price:.4f} vs closed form {V0:.4f} (gap {mc_price-V0:+.4f})")
print(f"One-step tree    : p*={p_star:.4f}, local {V_local:.6f} vs {V0:.6f} (gap {V_local-V0:+.2e})")
print()
print("One-sentence takeaway (edit me):")
print("The Black-Scholes PDE is the no-arbitrage balance after a delta hedge kills dW; Feynman-Kac")
print("says that PDE plus the payoff is the same object as the discounted Q-expectation.")""")

md(r"""### Stretch (optional, ungraded)

- **Put PDE.** Repeat Tasks 1–3 for the put $P = Ke^{-rT}N(-d_2) - S N(-d_1)$. Same residual
  identity, opposite delta, still machine-zero. Then check put-call parity
  $C-P = S - Ke^{-rT}$ survives as an identity of two PDE solutions.
- **Finite-difference solver.** Implement one backward explicit step on a log-$S$ grid and
  march from $\tau=0$ to $\tau=1$. Compare the ATM node to $10.4506$. Stability of the
  explicit scheme is a preview of Lesson 019's numerical track.
- **The heat kernel.** Change variables to $x=\ln(S/K)$, $\tau=T-t$, and confirm numerically
  that the transformed $u$ satisfies $u_\tau = \tfrac12\sigma^2 u_{xx}$ at a handful of
  interior points. That is why $N(d_1)$ is in the formula.
- **American preview.** At each node of a small CRR tree take
  $\max(\text{continuation},\,S-K)$ instead of continuation alone. For this *call* (no
  dividends) the extra $\max$ never triggers — European and American coincide. For the
  corresponding *put* they do not. Lesson 017 will not need this; a later pricing unit will.""")

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

import os
os.makedirs("labs", exist_ok=True)
os.makedirs("solutions", exist_ok=True)
nbf.write(build(student=True),  "labs/0016-black-scholes-pde.ipynb")
nbf.write(build(student=False), "solutions/0016-black-scholes-pde.ipynb")
print("wrote labs/0016-black-scholes-pde.ipynb and solutions/0016-black-scholes-pde.ipynb")
