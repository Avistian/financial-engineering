"""One-off builder for Lab 015 (risk-neutral pricing & Girsanov). Produces the student
notebook and the filled solution notebook from a single source of truth. Run once, then delete."""
import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

# Each code cell is (solution_source, student_source). If student is None, they are identical.
CELLS = []

def md(text):
    CELLS.append(("md", text, None))

def code(sol, student=None):
    CELLS.append(("code", sol, student))

md(r"""# Lab 015 — Risk-neutral pricing: replicate, change measure, and reach Black–Scholes

**Lesson:** [`0015-risk-neutral-pricing-girsanov.html`](../lessons/0015-risk-neutral-pricing-girsanov.html)
· **Reference:** [`girsanov.html`](../reference/girsanov.html)

**The one skill:** price a derivative by *replication*, then show that the same number is a discounted
expectation under a **different probability measure** — and do that measure change explicitly, with
Girsanov weights, on real-world paths. By the end you will have checked, with numbers, that (1) the
replication price ignores the real-world probability `p`, (2) the risk-neutral weight
`p* = (R−d)/(u−d)` makes the discounted stock a martingale, (3) a three-period tree reproduces Lesson
011's `7.475`, (4) the Black–Scholes formula prices a one-year at-the-money call at `10.4506`, (5) the
CRR tree converges to exactly that, (6) Monte-Carlo under `Q` agrees — and drifting at `μ` instead of
`r` inflates the price by ~73%, (7) re-weighting *real-world* paths by `Z = e^{−θW_T−½θ²T}` gives the
identical price, and (8) `N(d₂)` is **not** the real-world probability of exercise.

**Exit criteria:** every CHECK passes and the EXIT TICKET prints cleanly.

**How this notebook works**

| Cell tag | You do |
|----------|--------|
| **PROVIDED** | Run it. Imports, parameters, the pricing scaffolds. |
| **TODO** | Fill the `____` blanks. This is where the learning is. |
| **CHECK** | Run it — immediate assertions. Don't edit. |
| **EXIT TICKET** | Final deliverable. Prints your summary. |

**Environment:** Python 3 + `numpy` + `scipy` (only for the normal CDF). Fully self-contained (no
network, runs in seconds). See [`labs/README.md`](./README.md).""")

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

**A price is a hedging cost.** On a one-period tree the stock goes from $S_0$ to $uS_0$ or $dS_0$, and
cash multiplies by $R = e^{r\Delta t}$. A portfolio of $\Delta$ shares and $B$ cash that matches the
derivative's payoff in *both* states costs the same as the derivative:

$$\Delta = \frac{C_u - C_d}{S_u - S_d},\qquad B = \frac{C_d - \Delta S_d}{R},\qquad
\text{price} = \Delta S_0 + B$$

The real-world probability $p$ never appears. Rearranging that cost gives an expectation under
*manufactured* weights:

$$\text{price} = \frac{1}{R}\big[p^\ast C_u + (1-p^\ast) C_d\big],\qquad
p^\ast = \frac{R-d}{u-d}$$

| Object | Formula | Meaning |
|--------|---------|---------|
| Risk-neutral weight | $p^\ast = (R-d)/(u-d)$ | the weight that makes the *discounted stock* a martingale |
| Market price of risk | $\theta = (\mu - r)/\sigma$ | reward per unit of risk = the size of the Brownian shift |
| Girsanov weight | $Z_T = e^{-\theta W_T - \frac12\theta^2 T}$ | how much more (less) $Q$ counts a path than $P$ does |
| Stock under $Q$ | $S_T = S_0 e^{(r-\frac12\sigma^2)T + \sigma \tilde W_T}$ | drift is $r$, **not** $\mu$; $\sigma$ unchanged |
| Pricing formula | $V_0 = E_Q[e^{-rT} V_T]$ | discounted expected payoff **under $Q$** |
| Black–Scholes call | $S_0 N(d_1) - Ke^{-rT}N(d_2)$ | that expectation, evaluated |

with $d_1 = \dfrac{\ln(S_0/K) + (r + \frac12\sigma^2)T}{\sigma\sqrt T}$ and $d_2 = d_1 - \sigma\sqrt T$.

**The identity this lab is built around:** $E_Q[X] = E_P[Z\,X]$. You can either simulate under $Q$
directly, or simulate under the *real world* $P$ and re-weight — and both must give the same price.""")

# ---- PROVIDED params ----
code(r"""# PROVIDED — RNG, market parameters, and the normal CDF. Run it.
import numpy as np
from scipy.stats import norm

rng = np.random.default_rng(20150815)

# --- one-period tree (matches Lesson 011's tree and the lesson's worked example)
S0_T, U, D, K_T = 100.0, 1.1, 0.9, 100.0

# --- continuous-time market for the Black-Scholes half
S0    = 100.0   # spot price today
K     = 100.0   # strike
R_F   = 0.05    # risk-free rate r (continuously compounded)
SIGMA = 0.20    # volatility
MU    = 0.15    # REAL-WORLD expected return (used only where it belongs!)
T     = 1.0     # one year

THETA = (MU - R_F) / SIGMA          # market price of risk = the Sharpe ratio

print(f"tree     : S0={S0_T}, u={U}, d={D}, K={K_T}")
print(f"market   : S0={S0}, K={K}, r={R_F}, sigma={SIGMA}, mu={MU}, T={T}")
print(f"theta    : (mu - r)/sigma = {THETA:.3f}   <- the Brownian shift Girsanov applies")""")

# ---- Task 1 ----
md(r"""### Task 1 — Replicate the option, and watch the price ignore `p`

**Goal:** fill the hedge ratio $\Delta = (C_u - C_d)/(S_u - S_d)$. Everything else is provided: the cash
leg, the replication cost, and a sweep over real-world probabilities.

**Why:** this is the whole foundation. A price is what it costs to *manufacture* the payoff out of stock
and cash — so it cannot depend on anybody's forecast. The sweep makes that concrete: the replication
cost is flat across every `p`, while "discounted expected payoff" is a straight line through it.

**Hint boundary:** `(C_u - C_d) / (S_u - S_d)`.""")

code(r"""# TODO — the hedge ratio (shares per option).
def replicate(S0_, u, d, K_, R=1.0):
    S_u, S_d = S0_ * u, S0_ * d
    C_u, C_d = max(S_u - K_, 0.0), max(S_d - K_, 0.0)
    delta = (C_u - C_d) / (S_u - S_d)         # <- fill this
    bond = (C_d - delta * S_d) / R            # provided: cash leg, discounted
    return delta, bond, delta * S0_ + bond, C_u, C_d

delta, bond, price_rep, C_u, C_d = replicate(S0_T, U, D, K_T, R=1.0)
print(f"payoffs      : up {C_u:.1f}, down {C_d:.1f}")
print(f"hedge ratio  : delta = {delta:.3f} shares")
print(f"cash leg     : B = {bond:.2f}   (negative = borrow)")
print(f"replication  : price = {price_rep:.3f}")

# provided: the portfolio really does pay the option in BOTH states
pay_up   = delta * S0_T * U + bond
pay_down = delta * S0_T * D + bond
print(f"portfolio pays: up {pay_up:.3f} (option {C_u:.1f}), down {pay_down:.3f} (option {C_d:.1f})")

# provided: the forecast-based 'price' moves with p; the replication price does not
ps = np.linspace(0.0, 1.0, 11)
exp_prices = ps * C_u + (1 - ps) * C_d
print("\np      :", " ".join(f"{p:5.2f}" for p in ps))
print("E_p[C] :", " ".join(f"{e:5.2f}" for e in exp_prices))
print("replic.:", " ".join(f"{price_rep:5.2f}" for _ in ps), " <- flat")""",
r"""# TODO — the hedge ratio (shares per option).
def replicate(S0_, u, d, K_, R=1.0):
    S_u, S_d = S0_ * u, S0_ * d
    C_u, C_d = max(S_u - K_, 0.0), max(S_d - K_, 0.0)
    delta = ____                              # (C_u - C_d) / (S_u - S_d)
    bond = (C_d - delta * S_d) / R            # provided: cash leg, discounted
    return delta, bond, delta * S0_ + bond, C_u, C_d

delta, bond, price_rep, C_u, C_d = replicate(S0_T, U, D, K_T, R=1.0)
print(f"payoffs      : up {C_u:.1f}, down {C_d:.1f}")
print(f"hedge ratio  : delta = {delta:.3f} shares")
print(f"cash leg     : B = {bond:.2f}   (negative = borrow)")
print(f"replication  : price = {price_rep:.3f}")

# provided: the portfolio really does pay the option in BOTH states
pay_up   = delta * S0_T * U + bond
pay_down = delta * S0_T * D + bond
print(f"portfolio pays: up {pay_up:.3f} (option {C_u:.1f}), down {pay_down:.3f} (option {C_d:.1f})")

# provided: the forecast-based 'price' moves with p; the replication price does not
ps = np.linspace(0.0, 1.0, 11)
exp_prices = ps * C_u + (1 - ps) * C_d
print("\np      :", " ".join(f"{p:5.2f}" for p in ps))
print("E_p[C] :", " ".join(f"{e:5.2f}" for e in exp_prices))
print("replic.:", " ".join(f"{price_rep:5.2f}" for _ in ps), " <- flat")""")

code(r"""# CHECK — do not edit
assert abs(delta - 0.5) < 1e-12, "delta = (10-0)/(110-90) = 0.5"
assert abs(bond + 45.0) < 1e-12, "the cash leg is -45 (you borrow 45)"
assert abs(price_rep - 5.0) < 1e-12, "the replicating portfolio costs 5 today"
assert abs(pay_up - C_u) < 1e-12 and abs(pay_down - C_d) < 1e-12, "it must match the option in BOTH states"
# selling at the 'expected payoff' price of 7 would hand a buyer 2 units of free money
assert abs((0.7 * C_u + 0.3 * C_d) - 7.0) < 1e-12, "E_p[C] at p=0.7 is 7 -- an arbitrage against 5"
print("Task 1 OK -- price = replication cost = 5, whatever p is. The forecast never enters.")""")

# ---- Task 2 ----
md(r"""### Task 2 — The risk-neutral weight `p*`, and the martingale it creates

**Goal:** fill $p^\ast = (R-d)/(u-d)$, then confirm two things: the discounted $p^\ast$-average of the
**stock** is today's stock price (a martingale), and the discounted $p^\ast$-average of the **option**
payoff is the replication price from Task 1.

**Why:** this is the bridge from hedging to expectation. The weights are manufactured from `u`, `d` and
the interest rate — nobody's beliefs — and they are the *only* weights that reprice the stock correctly.

**Hint boundary:** `(R - d) / (u - d)`.""")

code(r"""# TODO — the risk-neutral probability.
def p_star(u, d, R):
    return (R - d) / (u - d)                  # <- fill this

# zero rates first (R = 1), matching Task 1
R0 = 1.0
ps0 = p_star(U, D, R0)
stock_repriced = (ps0 * S0_T * U + (1 - ps0) * S0_T * D) / R0
option_priced  = (ps0 * C_u + (1 - ps0) * C_d) / R0
print(f"R = {R0}:  p* = {ps0:.4f}")
print(f"   discounted p*-average of the STOCK  = {stock_repriced:.4f}  (S0 = {S0_T})")
print(f"   discounted p*-average of the OPTION = {option_priced:.4f}  (replication {price_rep:.4f})")

# now with 2% interest -- beliefs unchanged, yet p* moves
R2 = 1.02
ps2 = p_star(U, D, R2)
delta2, bond2, price2, _, _ = replicate(S0_T, U, D, K_T, R=R2)
print(f"\nR = {R2}: p* = {ps2:.4f}   (moved with the RATE, not with sentiment)")
print(f"   replication price = {price2:.4f}, discounted p*-average = {(ps2*C_u + (1-ps2)*C_d)/R2:.4f}")""",
r"""# TODO — the risk-neutral probability.
def p_star(u, d, R):
    return ____                               # (R - d) / (u - d)

# zero rates first (R = 1), matching Task 1
R0 = 1.0
ps0 = p_star(U, D, R0)
stock_repriced = (ps0 * S0_T * U + (1 - ps0) * S0_T * D) / R0
option_priced  = (ps0 * C_u + (1 - ps0) * C_d) / R0
print(f"R = {R0}:  p* = {ps0:.4f}")
print(f"   discounted p*-average of the STOCK  = {stock_repriced:.4f}  (S0 = {S0_T})")
print(f"   discounted p*-average of the OPTION = {option_priced:.4f}  (replication {price_rep:.4f})")

# now with 2% interest -- beliefs unchanged, yet p* moves
R2 = 1.02
ps2 = p_star(U, D, R2)
delta2, bond2, price2, _, _ = replicate(S0_T, U, D, K_T, R=R2)
print(f"\nR = {R2}: p* = {ps2:.4f}   (moved with the RATE, not with sentiment)")
print(f"   replication price = {price2:.4f}, discounted p*-average = {(ps2*C_u + (1-ps2)*C_d)/R2:.4f}")""")

code(r"""# CHECK — do not edit
assert abs(ps0 - 0.5) < 1e-12, "p* = (1-0.9)/(1.1-0.9) = 0.5 at zero rates"
assert abs(stock_repriced - S0_T) < 1e-12, "under p* the DISCOUNTED stock is a martingale: it reprices S0"
assert abs(option_priced - price_rep) < 1e-12, "the discounted p*-average must equal the replication price"
assert abs(ps2 - 0.6) < 1e-12, "p* = (1.02-0.9)/0.2 = 0.6 with 2% interest"
assert abs(price2 - 6.0/1.02) < 1e-12, "with R=1.02 the price is 6/1.02 = 5.882"
# the real-world probability does NOT reprice the stock
assert abs((0.7*S0_T*U + 0.3*S0_T*D)/R2 - S0_T) > 1e-3, "p = 0.7 must NOT reproduce today's stock price"
print(f"Task 2 OK -- p* is the unique weight that makes the discounted stock a fair game.")""")

# ---- Task 3 ----
md(r"""### Task 3 — A three-period tree: reproduce Lesson 011's `7.475`

**Goal:** fill the **backward step** — the one-period risk-neutral pricing formula, applied at every
node: a node's value is the $p^\ast$-weighted average of its two children, discounted by $R$.

**Why:** in Lesson 011 you computed `7.475` by backward averaging with `½` and were told the `½` would
be explained later. This is later: `½ = (R−d)/(u−d)` for `u=1.1, d=0.9, r=0`. Rolling the tree backwards
is just Task 1's replication repeated at every node.

**Hint boundary:** `(q * V[1:] + (1 - q) * V[:-1]) / R` — `V[1:]` are the up-children, `V[:-1]` the down.""")

code(r"""# TODO — the backward step: a node is the discounted p*-average of its two children.
def tree_price(S0_, u, d, K_, r, T_, n):
    dt = T_ / n
    R = np.exp(r * dt)
    q = p_star(u, d, R)
    j = np.arange(n + 1)                                   # number of up-moves at expiry
    S_terminal = S0_ * u**j * d**(n - j)
    V = np.maximum(S_terminal - K_, 0.0)                   # provided: the call payoff at expiry
    for _ in range(n):                                     # roll the tree backwards, one date at a time
        V = (q * V[1:] + (1 - q) * V[:-1]) / R             # <- fill this
    return V[0]

price_3 = tree_price(S0_T, U, D, K_T, r=0.0, T_=3.0, n=3)
print(f"three-period tree (u=1.1, d=0.9, r=0, K=100): {price_3:.4f}")
print(f"Lesson 011 computed by backward averaging     : 7.4750")
print(f"one-period tree, same machinery               : {tree_price(S0_T, U, D, K_T, 0.0, 1.0, 1):.4f}")""",
r"""# TODO — the backward step: a node is the discounted p*-average of its two children.
def tree_price(S0_, u, d, K_, r, T_, n):
    dt = T_ / n
    R = np.exp(r * dt)
    q = p_star(u, d, R)
    j = np.arange(n + 1)                                   # number of up-moves at expiry
    S_terminal = S0_ * u**j * d**(n - j)
    V = np.maximum(S_terminal - K_, 0.0)                   # provided: the call payoff at expiry
    for _ in range(n):                                     # roll the tree backwards, one date at a time
        V = ____                                           # (q*V[1:] + (1-q)*V[:-1]) / R
    return V[0]

price_3 = tree_price(S0_T, U, D, K_T, r=0.0, T_=3.0, n=3)
print(f"three-period tree (u=1.1, d=0.9, r=0, K=100): {price_3:.4f}")
print(f"Lesson 011 computed by backward averaging     : 7.4750")
print(f"one-period tree, same machinery               : {tree_price(S0_T, U, D, K_T, 0.0, 1.0, 1):.4f}")""")

code(r"""# CHECK — do not edit
assert abs(price_3 - 7.475) < 1e-9, "the three-period tree must reproduce Lesson 011's 7.475"
assert abs(tree_price(S0_T, U, D, K_T, 0.0, 1.0, 1) - 5.0) < 1e-9, "one step must give back Task 1's 5.0"
print("Task 3 OK -- the 1/2 in Lesson 011 was p* = (R-d)/(u-d) all along.")""")

# ---- Task 4 ----
md(r"""### Task 4 — Black–Scholes: the risk-neutral expectation, evaluated

**Goal:** fill $d_1$ and $d_2$ and the call formula $C = S_0N(d_1) - Ke^{-rT}N(d_2)$.

**Why:** this is not a new theory — it is $E_Q[e^{-rT}(S_T-K)^+]$ written out, because under $Q$ the
log of $S_T$ is normal. Everything else in the quarter (the PDE in Lesson 016, Monte-Carlo in 019) is
another route to this same number.

**Hint boundary:** `d1 = (np.log(S_/K_) + (r + 0.5*sig**2)*T_) / (sig*np.sqrt(T_))`; `d2 = d1 - sig*np.sqrt(T_)`.""")

code(r"""# TODO — the Black-Scholes call price.
def bs_call(S_, K_, r, sig, T_):
    d1 = (np.log(S_ / K_) + (r + 0.5 * sig**2) * T_) / (sig * np.sqrt(T_))   # <- fill this
    d2 = d1 - sig * np.sqrt(T_)                                              # <- fill this
    return S_ * norm.cdf(d1) - K_ * np.exp(-r * T_) * norm.cdf(d2), d1, d2

bs_price, d1, d2 = bs_call(S0, K, R_F, SIGMA, T)
print(f"d1 = {d1:.4f},  d2 = {d2:.4f}")
print(f"N(d1) = {norm.cdf(d1):.4f},  N(d2) = {norm.cdf(d2):.4f}")
print(f"call  = {S0:.0f}*{norm.cdf(d1):.4f} - {K:.0f}*{np.exp(-R_F*T):.4f}*{norm.cdf(d2):.4f} = {bs_price:.4f}")""",
r"""# TODO — the Black-Scholes call price.
def bs_call(S_, K_, r, sig, T_):
    d1 = ____                                # (ln(S/K) + (r + sig^2/2)T) / (sig*sqrt(T))
    d2 = ____                                # d1 - sig*sqrt(T)
    return S_ * norm.cdf(d1) - K_ * np.exp(-r * T_) * norm.cdf(d2), d1, d2

bs_price, d1, d2 = bs_call(S0, K, R_F, SIGMA, T)
print(f"d1 = {d1:.4f},  d2 = {d2:.4f}")
print(f"N(d1) = {norm.cdf(d1):.4f},  N(d2) = {norm.cdf(d2):.4f}")
print(f"call  = {S0:.0f}*{norm.cdf(d1):.4f} - {K:.0f}*{np.exp(-R_F*T):.4f}*{norm.cdf(d2):.4f} = {bs_price:.4f}")""")

code(r"""# CHECK — do not edit
assert abs(d1 - 0.35) < 1e-12 and abs(d2 - 0.15) < 1e-12, "for S=K=100, r=5%, sigma=20%, T=1: d1=0.35, d2=0.15"
assert abs(bs_price - 10.4506) < 1e-3, "the call must price at ~10.4506"
# sanity: no-arbitrage bounds -- a call is worth at least S - K e^{-rT} and never more than S
assert max(S0 - K*np.exp(-R_F*T), 0) <= bs_price <= S0, "the price must sit inside the no-arbitrage bounds"
print(f"Task 4 OK -- a one-year at-the-money call on a 20%-vol stock costs {bs_price:.4f} (~10% of spot).")""")

# ---- Task 5 ----
md(r"""### Task 5 — The tree becomes the formula (CRR limit)

**Goal:** fill the CRR up-factor $u = e^{\sigma\sqrt{\Delta t}}$ (and $d = 1/u$), then price the same
call on trees of growing size and watch the gap to Black–Scholes close.

**Why:** Black–Scholes is not an extra assumption bolted onto the tree — it *is* the tree, at infinite
resolution. Choosing `u = exp(sigma*sqrt(dt))` is what gives the tree the right volatility.

**Hint boundary:** `u = np.exp(sig * np.sqrt(dt))`.""")

code(r"""# TODO — the CRR up-factor.
def crr_price(S_, K_, r, sig, T_, n):
    dt = T_ / n
    u = np.exp(sig * np.sqrt(dt))             # <- fill this
    d = 1.0 / u                               # provided
    return tree_price(S_, u, d, K_, r, T_, n)

print(f"Black-Scholes                : {bs_price:.4f}")
for n in [1, 2, 4, 8, 16, 32, 64, 128, 512, 2000]:
    p_n = crr_price(S0, K, R_F, SIGMA, T, n)
    print(f"  {n:5d}-step CRR tree        : {p_n:8.4f}   gap {p_n - bs_price:+.4f}")

crr_2000 = crr_price(S0, K, R_F, SIGMA, T, 2000)""",
r"""# TODO — the CRR up-factor.
def crr_price(S_, K_, r, sig, T_, n):
    dt = T_ / n
    u = ____                                  # np.exp(sig * np.sqrt(dt))
    d = 1.0 / u                               # provided
    return tree_price(S_, u, d, K_, r, T_, n)

print(f"Black-Scholes                : {bs_price:.4f}")
for n in [1, 2, 4, 8, 16, 32, 64, 128, 512, 2000]:
    p_n = crr_price(S0, K, R_F, SIGMA, T, n)
    print(f"  {n:5d}-step CRR tree        : {p_n:8.4f}   gap {p_n - bs_price:+.4f}")

crr_2000 = crr_price(S0, K, R_F, SIGMA, T, 2000)""")

code(r"""# CHECK — do not edit
assert abs(crr_2000 - bs_price) < 0.01, "a 2000-step CRR tree must land within a cent of Black-Scholes"
assert abs(crr_price(S0, K, R_F, SIGMA, T, 1) - bs_price) > 1.0, "a 1-step tree is a crude caricature"
# the gap shrinks along a fixed parity (the odd/even zig-zag)
gaps = [abs(crr_price(S0, K, R_F, SIGMA, T, n) - bs_price) for n in [32, 64, 128, 256]]
assert all(gaps[i] > gaps[i+1] for i in range(len(gaps)-1)), "doubling the steps must halve the gap"
print("Task 5 OK -- same risk-neutral logic, finer grid: the tree converges to Black-Scholes.")""")

# ---- Task 6 ----
md(r"""### Task 6 — Monte-Carlo under `Q` (and the classic bug)

**Goal:** fill the risk-neutral terminal price
$S_T = S_0\exp\big((r - \tfrac12\sigma^2)T + \sigma\sqrt{T}Z\big)$ — note the drift is **`r`**, not
`μ` — then average the discounted payoff. Then run it again with `μ` on purpose and measure the damage.

**Why:** every Monte-Carlo pricer you write is this cell. Feeding it the real-world drift is the single
most common pricing bug in the wild, and it does not fail loudly — it just returns a confidently wrong
number.

**Hint boundary:** `S0 * np.exp((drift - 0.5*SIGMA**2)*T + SIGMA*np.sqrt(T)*Z)` with `drift = R_F`.""")

code(r"""# TODO — simulate the terminal price under Q (drift r) and price by Monte-Carlo.
N_MC = 400_000
z = rng.standard_normal(N_MC // 2)
Z = np.concatenate([z, -z])                    # provided: antithetic pairs (variance reduction)

def mc_price(drift):
    S_T = S0 * np.exp((drift - 0.5 * SIGMA**2) * T + SIGMA * np.sqrt(T) * Z)   # <- fill this
    return np.exp(-R_F * T) * np.maximum(S_T - K, 0.0).mean(), S_T

mc_q, S_T_Q = mc_price(R_F)                    # correct: risk-neutral drift
mc_wrong, _ = mc_price(MU)                     # WRONG on purpose: real-world drift

print(f"Black-Scholes                     : {bs_price:.4f}")
print(f"Monte-Carlo under Q (drift r=5%)  : {mc_q:.4f}   gap {mc_q - bs_price:+.4f}")
print(f"Monte-Carlo with mu=15% (the bug) : {mc_wrong:.4f}   {100*(mc_wrong/bs_price - 1):+.1f}% too high")""",
r"""# TODO — simulate the terminal price under Q (drift r) and price by Monte-Carlo.
N_MC = 400_000
z = rng.standard_normal(N_MC // 2)
Z = np.concatenate([z, -z])                    # provided: antithetic pairs (variance reduction)

def mc_price(drift):
    S_T = ____                                 # S0*exp((drift - sigma^2/2)T + sigma*sqrt(T)*Z)
    return np.exp(-R_F * T) * np.maximum(S_T - K, 0.0).mean(), S_T

mc_q, S_T_Q = mc_price(R_F)                    # correct: risk-neutral drift
mc_wrong, _ = mc_price(MU)                     # WRONG on purpose: real-world drift

print(f"Black-Scholes                     : {bs_price:.4f}")
print(f"Monte-Carlo under Q (drift r=5%)  : {mc_q:.4f}   gap {mc_q - bs_price:+.4f}")
print(f"Monte-Carlo with mu=15% (the bug) : {mc_wrong:.4f}   {100*(mc_wrong/bs_price - 1):+.1f}% too high")""")

code(r"""# CHECK — do not edit
assert abs(mc_q - bs_price) < 0.06, "Monte-Carlo under Q must match Black-Scholes to Monte-Carlo error"
assert abs(np.exp(-R_F*T) * S_T_Q.mean() - S0) < 0.05, "under Q the DISCOUNTED stock must average back to S0"
assert mc_wrong > bs_price * 1.5, "drifting at mu instead of r inflates the price badly (~+73%)"
print(f"Task 6 OK -- Q prices at {mc_q:.4f}; the mu bug prints {mc_wrong:.4f}, a {100*(mc_wrong/bs_price-1):.0f}% error with no error message.")""")

# ---- Task 7 ----
md(r"""### Task 7 — Do the measure change explicitly: Girsanov weights

**Goal:** fill the Radon–Nikodym weight $Z_T = \exp(-\theta W_T - \tfrac12\theta^2 T)$. Then, using
paths simulated in the **real world** (drift `μ`), check three things: the weights average to 1, the
re-weighted stock averages to $S_0e^{rT}$, and the re-weighted discounted payoff is the Black–Scholes
price.

**Why:** Task 6 short-circuited the measure change by simulating under `Q` directly. This task performs
it, on real-world paths — the identity $E_Q[X] = E_P[Z X]$ made numeric. Nothing about the paths
changes; only how much each one counts.

**Hint boundary:** `np.exp(-THETA * W_T - 0.5 * THETA**2 * T)`.""")

code(r"""# TODO — the Girsanov (Radon-Nikodym) weight of each path.
W_T = np.sqrt(T) * Z                            # provided: terminal Brownian value of each path
S_T_P = S0 * np.exp((MU - 0.5 * SIGMA**2) * T + SIGMA * W_T)      # REAL-WORLD paths (drift mu)

Zw = np.exp(-THETA * W_T - 0.5 * THETA**2 * T)  # <- fill this

mean_weight   = Zw.mean()                       # must be 1: Q is a probability
stock_under_Q = (Zw * S_T_P).mean()             # must be S0 e^{rT}: the drift was re-weighted away
price_girsanov = np.exp(-R_F * T) * (Zw * np.maximum(S_T_P - K, 0.0)).mean()

print(f"E_P[Z]                       = {mean_weight:.4f}   (must be 1.0)")
print(f"E_P[Z*S_T] (real-world paths)= {stock_under_Q:.3f}   vs S0*e^(rT) = {S0*np.exp(R_F*T):.3f}")
print(f"E_P[S_T]   (unweighted)      = {S_T_P.mean():.3f}   vs S0*e^(muT) = {S0*np.exp(MU*T):.3f}")
print(f"price via Girsanov weights   = {price_girsanov:.4f}   vs Black-Scholes {bs_price:.4f}")
print(f"weight of a path that ended W_T=+1: {np.exp(-THETA*1 - 0.5*THETA**2*T):.3f}  (counts less under Q)")
print(f"weight of a path that ended W_T=-1: {np.exp(THETA*1 - 0.5*THETA**2*T):.3f}  (counts more under Q)")""",
r"""# TODO — the Girsanov (Radon-Nikodym) weight of each path.
W_T = np.sqrt(T) * Z                            # provided: terminal Brownian value of each path
S_T_P = S0 * np.exp((MU - 0.5 * SIGMA**2) * T + SIGMA * W_T)      # REAL-WORLD paths (drift mu)

Zw = ____                                       # exp(-theta*W_T - 0.5*theta^2*T)

mean_weight   = Zw.mean()                       # must be 1: Q is a probability
stock_under_Q = (Zw * S_T_P).mean()             # must be S0 e^{rT}: the drift was re-weighted away
price_girsanov = np.exp(-R_F * T) * (Zw * np.maximum(S_T_P - K, 0.0)).mean()

print(f"E_P[Z]                       = {mean_weight:.4f}   (must be 1.0)")
print(f"E_P[Z*S_T] (real-world paths)= {stock_under_Q:.3f}   vs S0*e^(rT) = {S0*np.exp(R_F*T):.3f}")
print(f"E_P[S_T]   (unweighted)      = {S_T_P.mean():.3f}   vs S0*e^(muT) = {S0*np.exp(MU*T):.3f}")
print(f"price via Girsanov weights   = {price_girsanov:.4f}   vs Black-Scholes {bs_price:.4f}")
print(f"weight of a path that ended W_T=+1: {np.exp(-THETA*1 - 0.5*THETA**2*T):.3f}  (counts less under Q)")
print(f"weight of a path that ended W_T=-1: {np.exp(THETA*1 - 0.5*THETA**2*T):.3f}  (counts more under Q)")""")

code(r"""# CHECK — do not edit
assert abs(mean_weight - 1.0) < 0.01, "E_P[Z] must be 1 -- that is the job of the -0.5*theta^2*T term"
assert (Zw > 0).all(), "equivalence: every weight is strictly positive (no outcome is created or destroyed)"
assert abs(stock_under_Q - S0*np.exp(R_F*T)) < 0.3, "re-weighted, the stock grows at r, not mu"
assert abs(S_T_P.mean() - S0*np.exp(MU*T)) < 0.3, "unweighted, the same paths still grow at mu"
assert abs(price_girsanov - bs_price) < 0.06, "E_P[Z * discounted payoff] must equal the Q-price"
print("Task 7 OK -- same paths, re-weighted by Z: the drift moved to r and the price came out identical.")""")

# ---- Task 8 ----
md(r"""### Task 8 — `N(d₂)` is not a forecast

**Goal:** fill the **real-world** probability that the call finishes in the money. Under $P$,
$S_T > K$ exactly when $Z > -\big(\ln(S_0/K) + (\mu - \tfrac12\sigma^2)T\big)/(\sigma\sqrt T)$, so that
probability is $N\big((\ln(S_0/K) + (\mu - \tfrac12\sigma^2)T)/(\sigma\sqrt T)\big)$ — the same
expression as $d_2$ with $\mu$ in place of $r$.

**Why:** this is the failure mode of the whole lesson. $N(d_2)$ is a *pricing* weight, not a forecast,
and the two differ by a lot. Reporting a risk-neutral probability as a real-world one — "the market
says there is a 56% chance" — is a professional-grade error, and it happens most often with
risk-neutral default probabilities.

**Hint boundary:** `d2_real = (np.log(S0/K) + (MU - 0.5*SIGMA**2)*T) / (SIGMA*np.sqrt(T))`, then `norm.cdf(d2_real)`.""")

code(r"""# TODO — the REAL-WORLD probability of exercise.
d2_real = (np.log(S0 / K) + (MU - 0.5 * SIGMA**2) * T) / (SIGMA * np.sqrt(T))   # <- fill this
prob_real = norm.cdf(d2_real)

prob_q = norm.cdf(d2)                                     # provided: N(d2), the Q-probability
emp_q = (S_T_Q > K).mean()                                # provided: measured on the Q-paths of Task 6
emp_p = (S_T_P > K).mean()                                # provided: measured on the P-paths of Task 7

print(f"risk-neutral P(S_T > K) = N(d2)      = {prob_q:.4f}   (simulated under Q: {emp_q:.4f})")
print(f"real-world   P(S_T > K) with mu=15%  = {prob_real:.4f}   (simulated under P: {emp_p:.4f})")
print(f"difference                            = {prob_real - prob_q:+.4f}  <- the same option, two questions")""",
r"""# TODO — the REAL-WORLD probability of exercise.
d2_real = ____                                            # (ln(S0/K) + (mu - sigma^2/2)T)/(sigma*sqrt(T))
prob_real = norm.cdf(d2_real)

prob_q = norm.cdf(d2)                                     # provided: N(d2), the Q-probability
emp_q = (S_T_Q > K).mean()                                # provided: measured on the Q-paths of Task 6
emp_p = (S_T_P > K).mean()                                # provided: measured on the P-paths of Task 7

print(f"risk-neutral P(S_T > K) = N(d2)      = {prob_q:.4f}   (simulated under Q: {emp_q:.4f})")
print(f"real-world   P(S_T > K) with mu=15%  = {prob_real:.4f}   (simulated under P: {emp_p:.4f})")
print(f"difference                            = {prob_real - prob_q:+.4f}  <- the same option, two questions")""")

code(r"""# CHECK — do not edit
assert abs(prob_q - 0.5596) < 1e-3, "N(d2) = N(0.15) = 0.5596 -- the risk-neutral exercise probability"
assert abs(prob_real - 0.7422) < 1e-3, "the real-world probability uses mu: N(0.65) = 0.7422"
assert prob_real - prob_q > 0.15, "the two must differ substantially -- that is the whole point"
assert abs(emp_q - prob_q) < 0.01 and abs(emp_p - prob_real) < 0.01, "simulations must confirm both"
print("Task 8 OK -- 56% is what the PRICE implies; 74% is what the model FORECASTS. Never quote one for the other.")""")

# ---- EXIT ----
code(r"""# EXIT TICKET — paste this output to your teacher.
print("=== Lab 015: risk-neutral pricing, the measure change, and Black-Scholes ===")
print(f"Replication      : delta={delta:.2f}, B={bond:.1f}, price={price_rep:.3f} -- unchanged for every p")
print(f"Risk-neutral wt  : p*={ps0:.3f} at r=0 (reprices the stock exactly); p*={ps2:.3f} at R=1.02")
print(f"Three-step tree  : {price_3:.4f} == Lesson 011's 7.475 (the 1/2 was p* all along)")
print(f"Market price risk: theta=(mu-r)/sigma=({MU}-{R_F})/{SIGMA}={THETA:.2f}")
print(f"Black-Scholes    : d1={d1:.3f}, d2={d2:.3f}, call={bs_price:.4f}")
print(f"CRR limit        : 2000-step tree {crr_2000:.4f} (gap {crr_2000-bs_price:+.4f})")
print(f"Monte-Carlo (Q)  : {mc_q:.4f}; with mu instead of r: {mc_wrong:.4f} ({100*(mc_wrong/bs_price-1):+.0f}% error)")
print(f"Girsanov weights : E_P[Z]={mean_weight:.4f}, E_P[Z*S_T]={stock_under_Q:.2f} (=S0e^rT), price={price_girsanov:.4f}")
print(f"Exercise prob.   : Q says {prob_q:.3f}, the real world says {prob_real:.3f}")
print()
print("One-sentence takeaway (edit me):")
print("A price is the cost of replication, which equals a discounted expectation under Q; Girsanov builds")
print("Q by re-weighting paths with Z=exp(-theta W_T - theta^2 T/2), moving the drift to r and leaving sigma alone.")""")

md(r"""### Stretch (optional, ungraded)

- **Put-call parity.** Price the put by the same risk-neutral expectation and verify
  `C - P = S0 - K e^{-rT}` to machine precision. Then check the parity holds on the tree too — it is a
  pure no-arbitrage statement, so it must hold at every `n`.
- **Delta from the hedge.** `N(d1)` is the Black-Scholes hedge ratio. Compute it by bumping the spot
  (`(C(S+h) - C(S-h)) / 2h`) and confirm it matches `norm.cdf(d1)` — a preview of Lesson 017's Greeks.
- **Importance sampling for real.** The Girsanov weights of Task 7 are exactly the machinery behind
  importance sampling. Price a *deep out-of-the-money* call (`K = 160`) under `Q` directly and again by
  simulating with a large positive drift and re-weighting; compare the standard errors. This is how
  practitioners price rare events (Lesson 019).
- **Incompleteness.** Add a third state to the one-period tree (up / flat / down) and try to solve for
  `Δ` and `B`. Two instruments, three equations: no solution. Then find the *range* of `p*` weights that
  keep the discounted stock a martingale — that range is FTAP 2 in action.
- **Implied volatility.** Invert `bs_call` numerically: given a market price of `12.0`, solve for the
  `sigma` that reproduces it. That number is what options markets actually quote.""")

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

nbf.write(build(student=True),  "labs/0015-risk-neutral-pricing.ipynb")
nbf.write(build(student=False), "solutions/0015-risk-neutral-pricing.ipynb")
print("wrote labs/0015-risk-neutral-pricing.ipynb and solutions/0015-risk-neutral-pricing.ipynb")
