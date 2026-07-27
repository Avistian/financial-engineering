"""Generate labs/0010-2-q1-synthesis-walkthrough.ipynb — the Unit 001–009 worked example.

Unlike the exit-ticket labs this notebook has NO blanks: it is a narrated, end-to-end
research project that applies every concept from Units 001–009 to one realistic case,
and verifies each claim it makes with a CHECK cell.

This notebook is COMMITTED WITH ITS OUTPUTS so it reads end-to-end on the web without
being run. This script writes cells with empty outputs, so regenerating always needs the
execute step after it, or the committed results are lost:

    ./.venv/bin/python scripts/_gen_lab_0010_2.py
    ./.venv/bin/python -m jupyter nbconvert --to notebook --execute --inplace \
        --ExecutePreprocessor.kernel_name=python3 \
        labs/0010-2-q1-synthesis-walkthrough.ipynb
    bash scripts/render_notebooks.sh

The execute step is also the test suite: 22 CHECK cells assert every numeric claim the
narrative makes, so a non-zero exit means the prose and the data have drifted apart.
"""
import json

CELLS = []


def md(src):
    CELLS.append({"cell_type": "markdown", "metadata": {},
                  "source": src.strip("\n").splitlines(keepends=True)})


def code(src):
    CELLS.append({"cell_type": "code", "metadata": {}, "execution_count": None,
                  "outputs": [], "source": src.strip("\n").splitlines(keepends=True)})


# ======================================================================== header
md(r"""
# Lab 010.2 — One real research project, from mandate to memo (Units 001–009)

**Lesson:** the Q1 arc, [`0001`](../lessons/0001-quant-landscape.html) →
[`0010`](../lessons/0010-q1-checkpoint.html)

Lab 010 handed you a *single* claim and asked you to kill it. This notebook is the other half
of the same skill: it walks a **complete research project** — the kind that fills a quant
researcher's first month on a desk — and shows **every concept from Units 001–009 doing real
work at the exact moment a decision depends on it.**

The story: you are a new QR on a mid-frequency equity desk. A PM hands you 12 stocks, ten years
of daily prices, and 12 candidate signals, and asks one question: **is there anything tradable
here?** By the end you will have a defensible answer, a number for how much capital it holds,
and a memo you could actually send.

**What makes this different from Lab 010.** There, everything was noise and the right answer was
"kill it." Here **one signal is genuinely real** and eleven are not. That is much harder and much
more realistic: a discipline that kills *everything* is as useless as one that kills nothing. You
will watch a naïve screen crown five "winners" — four of them pure noise — and then watch the Q1
toolkit strip that down to
the one that is actually there — without also destroying it.

**How this notebook works**

| Cell tag | You do |
|----------|--------|
| **SETUP** | Run it. Imports, constants, the simulated market. |
| **WORKED** | **Read the code, then run it, then read the output.** There are no blanks — the code is the explanation. |
| **CHECK** | Assertions that prove the claim the section just made. If one fails, the narrative is wrong, not you. |
| **MEMO** | The deliverable: the research note this whole notebook exists to produce. |

**How to actually learn from it.** Before running each WORKED cell, cover the output and predict
the sign and rough size of what will print. Every section ends with a **takeaway** line naming the
decision that concept just made. If you can reconstruct the twelve takeaways from memory, you own
Q1.

**Where each unit shows up**

| Unit | Concept | Section |
|------|---------|---------|
| 001 | Alpha, buy-side, QR/QT/QD, frequency, alpha decay, the research lifecycle | §1, §12 |
| 002 | Instruments, long/short, gross vs net, leverage, margin, option payoffs | §2, §12 |
| 003 | Limit order book, spread, tick, FIFO, mid vs micro-price, market impact | §3, §12 |
| 004 | Log returns, fat tails, vol clustering, long memory, leverage effect, √h scaling | §4, §5 |
| 005 | Moments, Student-t, covariance vs correlation, uncorrelated ≠ independent, CLT, Bayes | §6 |
| 006 | Estimand/estimator, bias–variance, standard error, MLE, confidence intervals, bootstrap | §10 |
| 007 | t-stats, p-values, power, FWER, Bonferroni, Benjamini–Hochberg, the haircut | §11 |
| 008 | Covariance matrix, eigendecomposition, PCA, scree, market factor, projection | §7 |
| 009 | OLS, projection, R², heteroskedasticity, White, Newey–West, when regression lies | §8, §9 |

**Environment:** Python 3 + `numpy`, `pandas`, `scipy`, `statsmodels`. Fully self-contained
(simulated market — no network). Runs end-to-end in well under a minute. See
[`labs/README.md`](./README.md).
""")

# ======================================================================== colab
md(r"""
### Running on Google Colab?

Colab opens only this single file, so the lab dependencies (numpy, pandas, scipy, statsmodels, …)
and the course repo are **not** guaranteed to be present. The cell below fixes that: on Colab it
shallow-clones the course repo, installs `requirements-labs.txt`, and switches into `labs/` so
relative paths resolve. **On a local venv or Binder it does nothing — just run it and continue.**
""")

code(r"""
# @colab-bootstrap — PROVIDED. Makes the lab self-sufficient on Google Colab; a no-op elsewhere.
import os, sys

if "google.colab" in sys.modules:
    if not os.path.isdir("/content/financial-engineering"):
        !git clone --depth 1 https://github.com/Avistian/financial-engineering.git /content/financial-engineering
    %pip install -q -r /content/financial-engineering/requirements-labs.txt
    os.chdir("/content/financial-engineering/labs")
    print("Colab ready — working dir:", os.getcwd())
else:
    print("Not on Colab — using the local environment as-is.")
""")

# ======================================================================== §1 mandate
md(r"""
## §1 · The mandate — what you were actually asked (Unit 001)

Before a single line of code, be precise about the job. Unit 001 gave you three axes to locate
any quant role, and all three change what counts as a correct answer here.

**Axis 1 — buy side, not sell side.** A sell-side desk makes money on *flow*: it quotes, it
hedges, it earns the spread, and its core risk question is "am I hedged?" You are **buy side**:
you make money only if your *forecast* is right. Nobody pays you for volume. That means your
deliverable is not a model — it is a **decision about whether to risk the firm's capital**, and
the honest answer is often no.

**Axis 2 — QR, not QT or QD.** As the **researcher** you own the question *is this edge real?*
The trader (QT) owns *what do I quote right now* and the developer (QD) owns *does it run in
40 microseconds*. So the burden of proof lives with you. If you hand a PM a leaky backtest, no
one downstream will catch it.

**Axis 3 — mid frequency.** You will hold positions for about a day. This is the crucial
scoping decision, because it fixes what can possibly work:

| Frequency | Holding period | Where the edge comes from | Capacity |
|-----------|----------------|---------------------------|----------|
| HFT | microseconds → minutes | queue position, order flow, latency | tiny |
| **Mid (you)** | **hours → days** | **short-horizon statistical relationships** | **small–moderate** |
| Low | weeks → years | risk premia, fundamentals, slow flows | large |

At one-day holding you are in the regime where **transaction costs are the same order of
magnitude as the signal**. That is why §3 and §12 spend real effort on the order book: for this
mandate, costs are not an afterthought, they are half the answer.

### What "alpha" has to mean here

Unit 001 defined alpha as **return not explained by known risk exposures**. Take that literally,
because it dictates the whole analysis:

- If a strategy makes money simply by being long the market, that is **beta**, not alpha. The PM
  can buy an index fund for free. So the book must be **market-neutral** (§9), and demonstrating
  the neutrality is part of the deliverable.
- Alpha must be **measured net of costs** (§12). A gross edge smaller than the spread you must
  cross does not exist as a business.
- Alpha **decays**. Anything you find is already being competed away, which makes the *capacity*
  question ("how many dollars does this hold?") as important as the *significance* question.

### The research lifecycle — the map for the rest of this notebook

Unit 001 laid out the arc every project follows. This notebook is one full lap:

```
   idea  →  data  →  signal  →  validation  →  costs  →  sizing  →  decision
   (§1)     (§4–6)    (§7)      (§8–11)        (§12)     (§12)      (MEMO)
```

The single most common way this lap fails is that **validation is done last and briefly**, after
the researcher has fallen in love with the signal. Notice how much of this notebook lives in
§8–§11. That ratio *is* the lesson.

### Ground truth (so you can grade the method, not guess the answer)

Real research never tells you the answer. But a *teaching* notebook must, or you cannot tell a
good method from a lucky one. So, disclosed up front — and never used by any analysis cell:

> The market below is simulated. **Exactly one** of the 12 candidate signals — `rev5`, a 5-day
> cross-sectional reversal — carries a true edge, and that edge is **purely relative-value**:
> it predicts which names beat *the others*, not which way the market goes. The other **11 signals
> are pure noise**, deliberately given the names of real factors so they look respectable. Returns
> are fat-tailed, volatility-clustered, and driven by a common market factor.
>
> The test of the Q1 toolkit is whether it can find that one signal, reject the other eleven, and
> report an *honest* effect size for the survivor — all without being told any of this.
""")

code(r"""
# SETUP — imports, constants, and the display helpers used throughout.
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats, integrate

TRADING_DAYS = 252          # Unit 004: the annualization constant for the sqrt-h vol rule
N_DAYS       = 2520         # 10 years of daily data
WIN          = 252          # 1-year trailing window for estimating betas (Unit 009)
H_NAIVE      = 5            # the naive analyst's forward horizon, in days
SEED         = 14

# 12 fictional large caps in 3 sectors. Unit 002: these are cash equities - we can go long or
# short, they pay no coupon, and their price is what we model.
TICKERS   = ["ALFA", "BRVO", "CHRL", "DLTA", "ECHO", "FXTR",
             "GOLF", "HTEL", "INDA", "JULT", "KILO", "LIMA"]
SECTOR_OF = np.array([0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2])
SECTORS   = ["Tech", "Energy", "Financials"]
N_NAMES   = len(TICKERS)

def rule(title=""):
    print(("-- " + title + " ").ljust(78, "-") if title else "-" * 78)

def show(df, n=None):
    '''Print a DataFrame without pandas truncating it.'''
    with pd.option_context("display.width", 130, "display.max_columns", 40,
                           "display.float_format", lambda v: f"{v:>9.4f}"):
        print(df if n is None else df.head(n))

print(f"{N_NAMES} names, {N_DAYS} trading days (~{N_DAYS/TRADING_DAYS:.0f} years), "
      f"seed={SEED}")
print("sectors:", {s: [TICKERS[i] for i in range(N_NAMES) if SECTOR_OF[i] == k]
                   for k, s in enumerate(SECTORS)})
""")

# ======================================================================== §2 instruments
md(r"""
## §2 · The instrument and the book you will actually hold (Unit 002)

Unit 002 insisted that you cannot reason about a strategy until you can state, mechanically, what
position it puts on. So let us state it.

**The instrument: cash equity.** Of the four core instruments, we use the simplest. A share is a
claim on a company; its payoff is whatever the price does. Compare it to the others, because the
contrast is the point:

| Instrument | Payoff | What it costs to hold |
|------------|--------|-----------------------|
| **Equity (ours)** | linear in price: $S_T - S_0$ per share | financing on the long, borrow fee on the short |
| Futures | linear, but on a *forward* price, marked daily | margin only — no upfront principal |
| Option | **non-linear**: $\max(S_T-K,0)$ for a call | the premium, paid up front |
| ETF | linear, in a basket | the fund's expense ratio |

We hold equity because the mandate is a *forecast* of relative prices, and a linear instrument
turns a correct forecast directly into P&L with no extra moving parts. (In §12 we will bolt on one
option to see the non-linearity earn its keep.)

**The book: dollar-neutral long/short.** Recall from §1 that alpha must exclude market direction.
Unit 002's mechanics give the construction:

- **Long** name $i$ with weight $w_i>0$: you buy it and profit if it rises.
- **Short** name $i$ with weight $w_i<0$: you borrow the share, sell it, and profit if it falls.
  A short is *not* symmetric in practice — you pay a borrow fee, you can be recalled, and your
  loss is unbounded above.
- **Dollar-neutral** means $\sum_i w_i = 0$: the dollars long equal the dollars short. Whatever
  the market does, it moves both sides and largely cancels.

Two exposure numbers describe any such book, and confusing them is a classic beginner error:

$$\text{gross} = \sum_i |w_i| \qquad\qquad \text{net} = \sum_i w_i$$

**Gross** is how much risk you have on; **net** is how much market direction you carry. We will
always run gross $=1$ (so every P&L number is *per dollar of gross exposure* and comparisons are
apples-to-apples) and net $=0$.

**Leverage and margin.** Because long and short partly finance each other, a prime broker lets
you hold gross exposure larger than your capital. Gross $=2\times$ your equity means **2× leverage**:
it multiplies both your alpha *and* your drawdown, and it never improves your Sharpe ratio. That
last point is worth pausing on — leverage is a *sizing* decision, not a *research* decision, which
is exactly why we do the research at 1× and discuss sizing separately in §12.
""")

code(r"""
# WORKED — the mechanics of a dollar-neutral long/short book, on one day, in dollars.
capital = 10_000_000.0                       # $10M of equity
target_gross = 1.0                           # gross exposure = 1x capital (no leverage yet)

# A signal is just a number per name: positive = we expect out-performance.
raw_view = pd.Series([1.8, 0.9, 0.4, -0.2, 1.1, -0.6,
                      -1.3, 0.2, -0.9, -1.5, 0.7, -0.6], index=TICKERS)

# Step 1: strip the average view. What is left is a purely RELATIVE opinion, which is the only
# kind that can be market-neutral (Unit 001: the average view IS a market call).
relative = raw_view - raw_view.mean()

# Step 2: scale so that gross exposure = 1. Now weights are comparable across days and signals.
w = relative / relative.abs().sum()

book = pd.DataFrame({
    "view": raw_view, "relative": relative, "weight": w,
    "dollars": w * capital * target_gross,
    "side": np.where(w > 0, "LONG", "SHORT"),
})
show(book)

gross, net = w.abs().sum(), w.sum()
rule("exposures")
print(f"gross = sum|w| = {gross:.4f}  ->  ${gross*capital:,.0f} of stock at risk")
print(f"net   = sum w  = {net:+.2e}  ->  ${net*capital:+,.0f} of market exposure  (dollar-neutral)")
print(f"long  ${book.dollars[book.dollars > 0].sum():>12,.0f}   "
      f"short ${book.dollars[book.dollars < 0].sum():>12,.0f}")

# What this book earns on a day, decomposed. Note the market move cancels because net = 0.
rule("one day's P&L, decomposed")
market_move   = 0.0120                                     # the whole market is up 1.2%
idio          = np.array([0.004, -0.002, 0.001, 0.000, 0.003, -0.005,
                          -0.002, 0.001, -0.004, -0.006, 0.002, -0.001])
name_returns  = market_move + idio                          # every name gets the market move
pnl_total     = float((w.values * name_returns).sum() * capital)
pnl_from_mkt  = float(net * market_move * capital)
pnl_from_idio = float((w.values * idio).sum() * capital)
print(f"every name moved +{market_move:.2%} with the market, plus its own idiosyncratic move")
print(f"P&L from the market move  = ${pnl_from_mkt:>10,.2f}   <- zero BY CONSTRUCTION (net = 0)")
print(f"P&L from stock selection  = ${pnl_from_idio:>10,.2f}   <- this is the only thing we get paid for")
print(f"total P&L                 = ${pnl_total:>10,.2f}  = {pnl_total/capital:+.3%} of capital")

rule("leverage (a sizing choice, not a research result)")
for L in (1.0, 2.0, 4.0):
    print(f"  gross {L:>3.1f}x -> ${L*capital:>12,.0f} of stock, "
          f"P&L {L*pnl_total/capital:+.3%} of capital, "
          f"margin posted at 50% Reg-T = ${L*capital*0.5:,.0f}")
""")

code(r"""
# CHECK — the book really is dollar-neutral and really is market-immune.
assert abs(net) < 1e-12, "dollar-neutral means the weights sum to zero"
assert abs(gross - 1.0) < 1e-12, "we normalized gross exposure to exactly 1"
assert abs(pnl_from_mkt) < 1e-6, "with net = 0 a common move contributes nothing"
assert abs(pnl_total - pnl_from_idio) < 1e-6, "so ALL the P&L is stock selection"
# Leverage scales return and risk identically -> it cannot change a Sharpe ratio.
assert np.isclose((2 * pnl_total) / (2 * abs(pnl_total)), pnl_total / abs(pnl_total))
print("§2 OK — gross 1.0, net 0.0, and every dollar of P&L came from relative views.")
print("TAKEAWAY: subtracting the average view is what converts a market call into alpha.")
""")

# ======================================================================== §3 LOB
md(r"""
## §3 · The venue — what it costs to put that book on (Unit 003)

The §2 P&L assumed you traded at "the price." There is no such thing. Unit 003 replaced that
fiction with the **limit order book**: a queue of resting buy orders (bids) below a queue of
resting sell orders (asks). Two facts from that lesson decide this project.

**Fact 1: there are two prices, and you always get the worse one.** The **best bid** is the most
anyone will currently pay; the **best ask** is the least anyone will currently accept. The gap is
the **spread**. A market buy pays the ask; a market sell receives the bid. So a round trip costs
you the spread before you have been right about anything. The **mid price** $(\text{bid}+\text{ask})/2$
is a convenient fiction for marking positions, not a price you can trade.

The spread is quoted in **ticks** — the minimum price increment, one cent for US equities. For a
liquid $50 stock the spread is usually *exactly one tick*, because competition to be at the front
of the queue drives it to the smallest legal value.

**Fact 2: your own order moves the price.** The book has finite depth. A large market order eats
the best level, then the next, then the next, each worse than the last — that is **slippage**, and
it is why cost grows with size. Priority within a level is **price-time (FIFO)**: better price
first, and at equal price, whoever arrived first.

**The micro-price — a free forecast hiding in the book.** If the bid has 1,200 shares behind it
and the ask only 800, the book *leans*: there is more eagerness to buy than to sell, and the next
move is a little more likely to be up. Size-weighting the two quotes captures that lean,

$$P_\text{micro} = \frac{P_\text{ask}\,Q_\text{bid} + P_\text{bid}\,Q_\text{ask}}{Q_\text{bid}+Q_\text{ask}},$$

and note the *crossed* pairing: the **bid** size multiplies the **ask** price. That looks wrong
until you check the limiting case — if all the size is on the bid ($Q_\text{ask}\to 0$) the
micro-price goes to the *ask*, which is right, because a book that badly imbalanced is about to
trade up through the offer. The imbalance $\;(Q_\text{bid}-Q_\text{ask})/(Q_\text{bid}+Q_\text{ask})$
is the ancestor of the order-flow-imbalance signals of Year 2 Q3.
""")

code(r"""
# WORKED — a toy book for ALFA at $50. Walk an order through it and pay the real price.
bids = [(49.99, 1200), (49.98, 3000), (49.97, 5000)]   # price, shares - best first
asks = [(50.00,  800), (50.01, 2500), (50.02, 6000)]

best_bid, bid_qty = bids[0]
best_ask, ask_qty = asks[0]
mid      = 0.5 * (best_bid + best_ask)
spread   = best_ask - best_bid
micro    = (best_ask * bid_qty + best_bid * ask_qty) / (bid_qty + ask_qty)
imbalance = (bid_qty - ask_qty) / (bid_qty + ask_qty)

rule("the book")
for px, sz in reversed(asks):
    print(f"      ASK {px:>7.2f}  {'#' * (sz // 400):<16} {sz:>6,}")
print(f"      --- spread = ${spread:.2f} = {spread/mid*1e4:.1f} bp = "
      f"{round(spread/0.01)} tick ---")
for px, sz in bids:
    print(f"      BID {px:>7.2f}  {'#' * (sz // 400):<16} {sz:>6,}")

rule("the three 'prices'")
print(f"mid         = {mid:.4f}   <- for marking the book, NOT tradable")
print(f"micro-price = {micro:.4f}   <- leans {'UP' if micro > mid else 'DOWN'}: "
      f"imbalance = {imbalance:+.1%} (more size on the {'bid' if imbalance > 0 else 'ask'})")
print(f"you buy at  = {best_ask:.4f}   you sell at = {best_bid:.4f}")

rule("walking a 2,500-share market buy through the book (price-time priority)")
order, remaining, spent, fills = 2500, 2500, 0.0, []
for px, sz in asks:
    take = min(remaining, sz)
    spent += take * px
    fills.append((px, take))
    remaining -= take
    print(f"  filled {take:>6,} @ {px:.2f}  (level had {sz:,})"
          + ("  <- level exhausted, walk up" if take == sz and remaining else ""))
    if remaining == 0:
        break
vwap = spent / order
print(f"\naverage fill (VWAP) = {vwap:.4f}")
print(f"cost vs mid       = {(vwap-mid)/mid*1e4:>6.2f} bp   <- what you actually paid to trade")
print(f"  of which spread = {(best_ask-mid)/mid*1e4:>6.2f} bp   (half the spread, unavoidable)")
print(f"  of which impact = {(vwap-best_ask)/mid*1e4:>6.2f} bp   (slippage from walking the book)")
""")

code(r"""
# CHECK — the book mechanics behave as Unit 003 says they must.
assert best_ask > best_bid, "a sane book has ask above bid"
assert round(spread / 0.01) == 1, "a liquid $50 name trades at a one-tick spread"
assert best_bid < mid < best_ask, "the mid sits strictly between the quotes"
assert micro > mid, "more size on the bid => the book leans up => micro-price above mid"
assert best_bid <= micro <= best_ask, "the micro-price is still a price inside the book"
assert vwap > best_ask, "a 2,500-share order eats past the 800 at the touch, so it pays worse"
assert sum(q for _, q in fills) == order and fills[0][0] < fills[1][0], "FIFO: best price fills first"
print(f"§3 OK — a 2,500-share order cost {(vwap-mid)/mid*1e4:.2f} bp, not 0 bp.")
print("TAKEAWAY: 'the price' is a fiction; size determines what you actually pay.")
""")

md(r"""
### From one order to a cost function: the square-root law

Walking a hand-drawn book does not scale to ten years of trading. Unit 003 gave the empirical
regularity that does — the **square-root law of market impact**. Trading a quantity $Q$ against
a stock with daily volume $V$ and daily volatility $\sigma$ costs, in relative terms,

$$\text{impact} \;\approx\; Y\,\sigma\,\sqrt{\frac{Q}{V}}, \qquad Y \approx 0.4\text{–}1.$$

Read the three ingredients as claims about the world:

- **$\sqrt{Q/V}$, not $Q/V$.** Cost per share grows with size, but *sublinearly* — doubling your
  order raises the average cost per share by only $\sqrt2 \approx 1.41$, not 2. This is one of the
  most robust empirical facts in all of microstructure, and it holds across venues, asset classes
  and decades. It is also merciful: it means capacity degrades gracefully rather than falling off
  a cliff.
- **$Q/V$, a *fraction* of volume.** Only relative size matters. $10M in a stock that trades $1B
  a day is nothing; the same $10M in a stock that trades $20M a day is a disaster.
- **$\sigma$.** Impact is measured in units of the stock's own volatility. Volatile names are
  expensive to trade — the same participation rate moves them further.

Total cost per trade is then the unavoidable half-spread plus this impact. That single function
is what §12 will use to convert a gross edge into a business, so build it now and keep it.
""")

code(r"""
# WORKED — the cost model this project will live and die by.
HALF_SPREAD_BP = 1.0      # half of a 2 bp spread: the floor on any trade
Y_IMPACT       = 0.4      # conservative end of the empirical range
ADV_DOLLARS    = 500e6    # $500M/day: a genuinely liquid large cap
SIGMA_DAILY    = 0.011    # ~17% annualized (we verify this against the panel in Section 4)

def trade_cost_bp(dollars, adv=ADV_DOLLARS, sigma=SIGMA_DAILY, Y=Y_IMPACT):
    '''One-way cost of trading `dollars` of one name, in basis points of notional.'''
    participation = dollars / adv
    impact_bp = Y * sigma * np.sqrt(participation) * 1e4
    return HALF_SPREAD_BP + impact_bp, impact_bp, participation

rule("cost of one trade vs its size  (ADV = $500M/day)")
print(f"{'trade size':>12} {'% of ADV':>10} {'impact':>9} {'+ spread':>10} {'total':>8}")
for d in (0.1e6, 1e6, 5e6, 25e6, 100e6, 400e6):
    tot, imp, part = trade_cost_bp(d)
    print(f"${d/1e6:>10.1f}M {part:>9.2%} {imp:>8.2f}bp {HALF_SPREAD_BP:>8.2f}bp {tot:>6.2f}bp")

rule("the sublinear scaling, checked")
a, _, _ = trade_cost_bp(10e6)
b, _, _ = trade_cost_bp(40e6)
_, ia, _ = trade_cost_bp(10e6)
_, ib, _ = trade_cost_bp(40e6)
print(f"4x the size multiplies IMPACT by {ib/ia:.3f}  (sqrt(4) = 2.000)")
print(f"...so cost per share rose 2x while the dollars traded rose 4x: "
      f"total cost paid rose {4*ib/ia:.1f}x")
print(f"\nSanity vs the hand-walked book: our 2,500-share order was "
      f"${2500*50/1e6:.3f}M = {2500*50/ADV_DOLLARS:.4%} of ADV")
print(f"  square-root law says {trade_cost_bp(2500*50)[0]:.2f} bp; "
      f"the toy book charged {(vwap-mid)/mid*1e4:.2f} bp -- same order of magnitude.")
""")

code(r"""
# CHECK — the cost model has the shape the square-root law requires.
_, imp_1, _ = trade_cost_bp(1e6)
_, imp_4, _ = trade_cost_bp(4e6)
assert np.isclose(imp_4 / imp_1, 2.0, rtol=1e-9), "4x size must be exactly 2x impact"
assert trade_cost_bp(0.0)[0] == HALF_SPREAD_BP, "at zero size you still cross the spread"
assert trade_cost_bp(1e6)[0] < trade_cost_bp(10e6)[0] < trade_cost_bp(100e6)[0], "cost rises with size"
assert trade_cost_bp(1e6, adv=50e6)[0] > trade_cost_bp(1e6, adv=500e6)[0], "illiquid names cost more"
print("§3b OK — cost(size) is increasing, sublinear, and floored at the half-spread.")
print("TAKEAWAY: capacity is a property of the cost curve, so it must be modelled, not assumed.")
""")

# ======================================================================== §4 the data
md(r"""
## §4 · The data — ten years of prices, and what returns to compute (Unit 004)

Now the market. It is simulated, which is a feature for teaching: we know the truth, so we can
check whether the method finds it. But it is not *convenient* — it is built to have the same
pathologies real equity data has, because those pathologies are what break naïve analysis:

| Ingredient | Why it is there | Which unit it makes relevant |
|------------|-----------------|------------------------------|
| A common **market factor** all 12 names load on | real panels are dominated by one factor | 008 (PC1), 009 (why pooled $n$ lies) |
| **Sector** factors | correlation has structure beyond the market | 008 (PC2, PC3) |
| **Student-$t$** shocks | returns have fat tails | 004, 005 |
| **Two-scale stochastic volatility** | volatility clusters *and* has long memory | 004 |
| A **leverage effect** (down days raise tomorrow's vol) | equity vol is asymmetric | 004 |
| One **true cross-sectional edge**, tiny | so the exercise has a right answer | 007–012 |

The volatility deserves a word, because it is the engine behind three of the five stylized facts.
Log-volatility is the sum of two AR(1) pieces: a **slow** one ($\phi = 0.996$, a memory measured
in years) and a **fast** one ($\phi = 0.92$, a memory of days) that also responds *negatively* to
the day's return. The slow piece produces long memory; the fast piece produces the leverage
effect; together they produce clustering. One process, three facts — which is a hint that in real
markets these "separate" stylized facts may also be one mechanism seen from three angles.
""")

code(r"""
# SETUP — the simulated market. Read it: every line maps to a stylized fact.
PHI_S, ETA_S = 0.996, 0.038          # slow log-vol component  -> long memory in |r|
PHI_F, ETA_F = 0.920, 0.025          # fast log-vol component  -> clustering
GAMMA, DELTA = -0.12, 0.06           # GAMMA < 0 -> the leverage effect; DELTA -> vol-of-vol
E_ABS_Z, KAPPA = 0.75, 0.00055       # E|z|; KAPPA = the size of the ONE true edge
LV_CAP, CLIP_Z = 1.00, 4.0            # cap vol excursions & shock size: keeps tails realistic

def std_t(rng, df, size):
    '''Student-t draws rescaled to unit variance, so df controls tails and NOT scale.'''
    return rng.standard_t(df, size=size) / np.sqrt(df / (df - 2.0))

def simulate_market(seed=SEED, n_days=N_DAYS, kappa=KAPPA, burn=800):
    rng = np.random.default_rng(seed)
    n, T = N_NAMES, n_days + burn
    v_lv = (ETA_S**2 / (1 - PHI_S**2)
            + (GAMMA**2 + DELTA**2 * 0.45 + ETA_F**2) / (1 - PHI_F**2))   # keeps E[sigma^2] on target

    beta_true = rng.uniform(0.75, 1.35, size=n)     # each name's market sensitivity
    sec_load  = rng.uniform(0.50, 1.00, size=n)     # ...and sector sensitivity
    idio_bar  = rng.uniform(0.0090, 0.0140, size=n) # ...and baseline idiosyncratic vol

    slow_m = fast_m = 0.0
    slow_i = np.zeros(n); fast_i = np.zeros(n)
    R = np.zeros((T, n)); rm = np.zeros(T); rev = np.zeros((T, n))
    alpha_today = np.zeros(n)

    for t in range(T):
        # --- the market factor: stochastic vol x fat-tailed shock ---
        sig_m  = 0.0105 * np.exp(min(slow_m + fast_m - v_lv, LV_CAP))
        zm     = float(np.clip(std_t(rng, 6, 1)[0], -CLIP_Z, CLIP_Z))
        rm[t]  = 0.05 / TRADING_DAYS + sig_m * zm        # ~5%/yr equity risk premium

        # --- sector factors and idiosyncratic shocks ---
        f     = std_t(rng, 6, 3) * 0.004
        sig_i = idio_bar * np.exp(np.minimum(slow_i + fast_i - v_lv, LV_CAP))
        ei    = np.clip(std_t(rng, 5, n), -CLIP_Z, CLIP_Z)

        # --- the return of each name: factors + idio + (the tiny true alpha) ---
        R[t] = beta_true * rm[t] + sec_load * f[SECTOR_OF] + sig_i * ei + alpha_today

        # --- the signal, computable from data available at the CLOSE of day t (no look-ahead) ---
        if t >= 4:
            rev[t] = -R[t-4:t+1].sum(axis=0) / (np.sqrt(5.0) * idio_bar * 1.9)
        # THE ONLY TRUE EDGE, and it acts on tomorrow. Cross-sectionally demeaned => pure
        # relative value: it says who beats whom, never which way the market goes.
        alpha_today = kappa * (rev[t] - rev[t].mean())

        # --- volatility updates: slow (memory) + fast (clustering, leverage via GAMMA*z) ---
        slow_m = PHI_S * slow_m + ETA_S * rng.normal()
        fast_m = PHI_F * fast_m + GAMMA * zm + DELTA * (abs(zm) - E_ABS_Z) + ETA_F * rng.normal()
        slow_i = PHI_S * slow_i + ETA_S * rng.normal(size=n)
        fast_i = PHI_F * fast_i + GAMMA * ei + DELTA * (np.abs(ei) - E_ABS_Z) + ETA_F * rng.normal(size=n)

    s = slice(burn, None)
    return R[s], rev[s], rm[s], beta_true

R, REV_TRUE, r_market_factor, beta_true = simulate_market()
dates = pd.bdate_range("2016-01-04", periods=N_DAYS)
rets  = pd.DataFrame(R, index=dates, columns=TICKERS)      # LOG returns, by construction
prices = 50.0 * np.exp(rets.cumsum())                      # so prices are exp of cumulative sums

rule("the panel")
print(f"log-return panel: {rets.shape[0]} days x {rets.shape[1]} names, "
      f"{dates[0].date()} -> {dates[-1].date()}")
show(pd.DataFrame({
    "start px":  prices.iloc[0], "end px": prices.iloc[-1],
    "ann ret":   rets.mean() * TRADING_DAYS,
    "ann vol":   rets.std() * np.sqrt(TRADING_DAYS),
    "true beta": beta_true,
}))
print(f"\nequal-weight index: ann vol {rets.mean(axis=1).std()*np.sqrt(TRADING_DAYS):>6.1%}   "
      f"vs our assumed SIGMA_DAILY {SIGMA_DAILY*np.sqrt(TRADING_DAYS):.1%} annualized")
_idx_ret = rets.mean(axis=1).mean() * TRADING_DAYS
print(f"equal-weight index: ann RETURN {_idx_ret:+.1%}, though the simulator was given a "
      f"+5.0% drift.")
_se_mu = (rets.mean(axis=1).std() * np.sqrt(TRADING_DAYS)
          / np.sqrt(N_DAYS / TRADING_DAYS))          # SE of an annualized mean return
print("That gap is not a bug - it is Unit 006 arriving early. The standard error on an annualized")
print(f"mean return estimated from {N_DAYS/TRADING_DAYS:.0f} years is about {_se_mu:.1%}, so the "
      f"realized {_idx_ret:+.1%} sits")
print(f"{abs(_idx_ret - 0.05)/_se_mu:.1f} standard errors from the +5.0% we built in: on the unlucky "
      f"side, but well inside")
print("the range a decade cannot distinguish. A 10-year sample simply cannot measure an equity")
print("premium. Good thing our book will not bet on one: everything from Section 10 on is")
print("market-NEUTRAL, so whatever the market did washes out of the P&L entirely.")
""")

code(r"""
# CHECK — the simulated market is in a realistic range (a bad simulator teaches bad lessons).
ann_vol    = rets.std() * np.sqrt(TRADING_DAYS)
idx_vol    = rets.mean(axis=1).std() * np.sqrt(TRADING_DAYS)
years_data = N_DAYS / TRADING_DAYS
assert rets.shape == (N_DAYS, N_NAMES)
assert (ann_vol > 0.15).all() and (ann_vol < 0.45).all(), f"implausible name vols:\n{ann_vol}"
assert 0.10 < idx_vol < 0.30, "index vol should be ~10-30% for a large-cap panel"
assert (prices > 0).all().all(), "prices modelled as exp(cumulative log returns) can never go <= 0"
assert not rets.isna().any().any()
# a simulator can be "fat-tailed" and still be absurd. These bound it to large-cap behaviour:
assert np.expm1(rets.abs().values.max()) < 0.20, \
    "no single-day move above 20% - these are meant to be large caps, not meme stocks"
assert (prices.iloc[-1] / prices.iloc[0]).max() < 10, \
    "no name 10x's over the decade; that would make the 'boring large cap' framing a lie"
assert abs(idx_vol - SIGMA_DAILY * np.sqrt(TRADING_DAYS)) < 0.05, \
    "the panel's realized vol must match the SIGMA_DAILY the Section 3 cost model assumes"
print(f"§4 OK — {years_data:.0f} years, {N_NAMES} names, name vols "
      f"{ann_vol.min():.0%}-{ann_vol.max():.0%}, index vol {idx_vol:.0%}. Plausible market.")
""")

md(r"""
### Simple returns or log returns? (and why the answer is not stylistic)

Unit 004 gave two definitions of "the return" over one period:

$$R_t = \frac{P_t}{P_{t-1}} - 1 \qquad\text{(simple)} \qquad\qquad
  r_t = \ln\frac{P_t}{P_{t-1}} \qquad\text{(log)}$$

They agree to first order for small moves — the Taylor expansion is
$\ln(1+R) = R - R^2/2 + \dots$, so at $R = 1\%$ they differ by about $0.005\%$. Which is why
people are sloppy about them, and why the sloppiness is invisible until it is expensive. Each has
exactly one property the other lacks:

- **Log returns add across time.** $r_{1\to3} = r_1 + r_2 + r_3$, because logs turn the product of
  gross returns into a sum. Simple returns *compound* instead: $(1+R_1)(1+R_2)-1$. Anything
  involving multiple periods — aggregating to weekly, the $\sqrt{h}$ vol rule, a sum in a CLT — is
  cleaner in logs. That is why the panel above is log returns.
- **Simple returns add across assets.** A portfolio's simple return is $\sum_i w_i R_i$ exactly;
  the log return of a portfolio is *not* $\sum_i w_i r_i$, because the log of a sum is not the sum
  of logs. So portfolio arithmetic — §2's book, §9's P&L — wants simple returns.

The practical rule: **logs for time, simple for cross-section.** On a typical day the two agree to
well under a basis point, so mixing them costs a rounding error — and this notebook accepts that.
But check the printed maximum below: on the wildest day of the decade the gap is around a full
percent, because the error term is $R^2/2$ and $R^2$ grows fast. The approximation is worst exactly
on the days that decide your year, which is the general shape of this whole subject.

There is a third consequence, and it is the one that matters for §5. If log returns are roughly
normal, then prices are **lognormal**: $P_T = P_0 e^{\sum r_t}$ with a sum in the exponent. This
is exactly why the lognormal shows up everywhere in pricing (Q2's Black–Scholes) and why prices
have a floor at zero while returns have no floor.
""")

code(r"""
# WORKED — the two definitions, and the two additivity properties, checked numerically.
simple = prices.pct_change().dropna()
log_r  = np.log(prices / prices.shift(1)).dropna()

rule("how different are they, day to day?")
d = pd.DataFrame({"simple": simple["ALFA"], "log": log_r["ALFA"]})
d["difference"] = d.simple - d.log
d["~ R^2/2"] = d.simple ** 2 / 2                     # the leading Taylor term
show(d.iloc[:5])
print(f"max |simple - log| over 10y = {d.difference.abs().max():.5f} "
      f"(on a day when |R| = {d.simple.abs().max():.3%})")
print(f"correlation between the two definitions = {d.simple.corr(d.log):.6f}")

rule("logs add across TIME")
p0, p5 = prices['ALFA'].iloc[0], prices['ALFA'].iloc[5]
print(f"sum of 5 daily log returns   = {log_r['ALFA'].iloc[:5].sum():+.6f}")
print(f"log(P5 / P0) computed direct = {np.log(p5 / p0):+.6f}   <- identical")
print(f"sum of 5 daily SIMPLE returns= {simple['ALFA'].iloc[:5].sum():+.6f}")
print(f"correct compounding          = {np.prod(1 + simple['ALFA'].iloc[:5]) - 1:+.6f}   <- NOT the sum")

rule("simple returns add across ASSETS")
w_eq = np.full(N_NAMES, 1 / N_NAMES)
port_simple = float((w_eq * simple.iloc[0]).sum())
port_log_wrong = float((w_eq * log_r.iloc[0]).sum())
port_log_right = float(np.log1p(port_simple))
print(f"portfolio simple return  sum w_i R_i = {port_simple:+.6f}   <- exact")
print(f"naive  sum w_i r_i                   = {port_log_wrong:+.6f}   <- WRONG (log of a sum)")
print(f"log of the true portfolio return     = {port_log_right:+.6f}")

rule("prices are lognormal because log returns add")
print(f"P_T = P_0 * exp(sum of log returns): "
      f"{prices['ALFA'].iloc[0]:.2f} * exp({log_r['ALFA'].sum():+.4f}) = "
      f"{prices['ALFA'].iloc[0]*np.exp(log_r['ALFA'].sum()):.2f}  "
      f"(actual {prices['ALFA'].iloc[-1]:.2f})")
""")

code(r"""
# CHECK — the two additivity identities, exactly.
assert np.isclose(log_r["ALFA"].iloc[:5].sum(), np.log(p5 / p0)), "logs must add across time"
assert np.isclose(np.prod(1 + simple["ALFA"].iloc[:5]) - 1,
                  np.expm1(log_r["ALFA"].iloc[:5].sum())), "simple returns compound"
assert np.isclose(port_simple, float((w_eq * simple.iloc[0]).sum())), "simple returns add across assets"
assert abs(port_log_wrong - port_simple) > 1e-9, "sum w_i r_i is NOT the portfolio return"
assert d.difference.abs().median() < 5e-5, "on a TYPICAL day the gap is under half a basis point"
assert np.allclose(d.difference, d["~ R^2/2"], atol=3e-3), "the gap IS the leading Taylor term R^2/2"
assert d.simple.corr(d.log) > 0.999, "so the two series carry essentially the same information"
print("§4b OK — logs add over time, simple returns add over assets; at daily size both are fine.")
print("TAKEAWAY: logs for time, simple for cross-section. Know which error you are making.")
""")

# ======================================================================== §5 stylized facts
md(r"""
## §5 · Diagnose before you model — the five stylized facts (Unit 004)

A researcher who fits a model before looking at the data is guessing. Unit 004's stylized facts
are the standard diagnostic pass, and each one **invalidates a specific default assumption** that
some tool you are about to use makes silently.

| # | Stylized fact | Which default it kills | Where it bites in this notebook |
|---|----------------|------------------------|--------------------------------|
| 1 | Returns are **fat-tailed** (excess kurtosis $\gg 0$) | "normal enough" | Sharpe CIs (§10), risk of ruin (§12) |
| 2 | Returns are **~linearly unpredictable** ($\rho(r_t,r_{t+1})\approx0$) | easy money | any edge must be small (§9) |
| 3 | **Volatility clusters** ($\rho(|r_t|,|r_{t+1}|)>0$) | homoskedastic errors | White SEs (§8) |
| 4 | Volatility has **long memory** | "yesterday's vol is enough" | HAC lag choice (§8) |
| 5 | The **leverage effect**: down days raise tomorrow's vol | symmetric risk | drawdowns cluster (§12) |

Facts 2 and 3 together are the single most important sentence in Q1: **returns are unpredictable
in their sign but highly predictable in their magnitude.** Direction is nearly a martingale;
risk is forecastable. Everything about how quant funds actually make money — sizing, vol
targeting, risk models — descends from that asymmetry.

**One methodological note that matters more than it looks.** A single 2,520-day series gives a
noisy autocorrelation estimate: the standard error of a correlation on $n$ points is roughly
$1/\sqrt n \approx 0.02$, so a lone reading of $0.03$ is not evidence of anything. We have 12
names, so we average each statistic **across names**, cutting the noise by about $\sqrt{12}$.
Pooling independent estimates to see a small effect is the same $1/\sqrt n$ logic that Unit 006
builds standard errors from — and it is the honest alternative to squinting at one chart.
""")

code(r"""
# WORKED — measure all five facts, averaging across the 12 names to beat estimation noise.
def acf(x, lag):
    x = np.asarray(x)
    return float(np.corrcoef(x[:-lag], x[lag:])[0, 1])

facts = pd.DataFrame(index=TICKERS)
facts["kurtosis"]   = [stats.kurtosis(rets[c], fisher=True) for c in TICKERS]        # fact 1
facts["acf1(r)"]    = [acf(rets[c], 1) for c in TICKERS]                             # fact 2
facts["acf1(|r|)"]  = [acf(rets[c].abs(), 1) for c in TICKERS]                       # fact 3
facts["acf22(|r|)"] = [acf(rets[c].abs(), 22) for c in TICKERS]                      # fact 4
facts["leverage"]   = [float(np.corrcoef(rets[c][:-1], rets[c].abs()[1:])[0, 1])     # fact 5
                       for c in TICKERS]
show(facts)
avg = facts.mean()

rule("fact 1 - fat tails: how often does a '4-sigma' day happen?")
z_all = ((rets - rets.mean()) / rets.std()).values.ravel()
for k in (3, 4, 5):
    emp, norm = np.mean(np.abs(z_all) > k), 2 * stats.norm.sf(k)
    print(f"  |z| > {k}:  observed {emp:.5f}  vs Gaussian {norm:.7f}   "
          f"-> {emp/norm:>6.1f}x too often")
print(f"  mean excess kurtosis = {avg['kurtosis']:.2f}  (a Gaussian scores 0)")

rule("facts 2-4 - the sign is unpredictable, the SIZE is not")
print(f"{'lag':>5} {'mean acf(r)':>14} {'mean acf(|r|)':>15}")
for lag in (1, 5, 22, 66):
    ar  = np.mean([acf(rets[c], lag) for c in TICKERS])
    aar = np.mean([acf(rets[c].abs(), lag) for c in TICKERS])
    bar = "#" * int(max(aar, 0) * 100)
    print(f"{lag:>5} {ar:>+14.4f} {aar:>+15.4f}  {bar}")
print(f"  ~2 SE band on a single-name acf estimate = +/-{2/np.sqrt(N_DAYS):.4f}")

rule("fact 5 - the leverage effect")
print(f"  mean corr(r_t, |r_t+1|) = {avg['leverage']:+.4f}   (negative: bad days beget wild days)")

rule("bonus - aggregational gaussianity and the sqrt-h rule")
def agg_kurt_and_vol(h):
    '''Average excess kurtosis and the vol-scaling ratio across all 12 names at horizon h.'''
    ks, ratios = [], []
    for c in TICKERS:
        v = rets[c].values
        a = v[:len(v) // h * h].reshape(-1, h).sum(1)
        ks.append(stats.kurtosis(a))
        ratios.append(a.std() / (np.sqrt(h) * v.std()))
    return float(np.mean(ks)), float(np.mean(ratios))

print(f"{'horizon':>9} {'mean excess kurtosis':>22} {'vol(h) / (sqrt(h) x vol(1))':>29}")
agg_kurt = {}
for h in (1, 5, 21, 63):
    k_h, ratio_h = agg_kurt_and_vol(h)
    agg_kurt[h] = k_h
    print(f"{h:>9} {k_h:>22.2f} {ratio_h:>28.3f}x")
print("  tails thin out as you aggregate (a CLT effect, Section 6) while vol scales ~ sqrt(h).")
print("  averaged across all 12 names, because a single name's monthly kurtosis (only "
      f"{N_DAYS//21} points) is far too noisy to read.")
""")

code(r"""
# CHECK — all five stylized facts are present, and the key contrast holds.
assert avg["kurtosis"] > 2.0, "returns must be clearly fat-tailed vs a Gaussian's 0"
assert np.mean(np.abs(z_all) > 4) > 5 * 2 * stats.norm.sf(4), "4-sigma days far too common for a normal"
assert abs(avg["acf1(r)"]) < 0.05, "fact 2: almost no linear predictability in the SIGN"
assert avg["acf1(|r|)"] > 0.10, "fact 3: clear clustering in the MAGNITUDE"
assert avg["acf1(|r|)"] > 5 * abs(avg["acf1(r)"]), "the headline contrast: |r| is far more predictable than r"
assert avg["acf22(|r|)"] > 0.02, "fact 4: vol memory still positive a month out"
assert avg["leverage"] < -0.03, "fact 5: the leverage effect is negative"
assert agg_kurt[21] < agg_kurt[1], \
    "aggregational gaussianity: monthly returns are less fat-tailed than daily (mean over names)"
print(f"§5 OK — kurtosis {avg['kurtosis']:.1f}, acf1(r) {avg['acf1(r)']:+.3f}, "
      f"acf1(|r|) {avg['acf1(|r|)']:+.3f}, leverage {avg['leverage']:+.3f}.")
print("TAKEAWAY: sign unpredictable + magnitude predictable. Every later choice follows from this.")
""")

# ======================================================================== §6 probability
md(r"""
## §6 · The probability toolkit, pointed at this data (Unit 005)

Unit 005 was abstract on purpose. Here is each piece doing a concrete job.

### The four moments, and what each one costs you

Mean, variance, skewness, kurtosis. Two are about *reward and risk*; two are about **how wrong
your risk number is**:

- **Mean** — the edge. For daily equities it is a rounding error next to the noise, which is the
  whole difficulty of the field.
- **Variance / standard deviation** — the risk. Its square root is volatility.
- **Skewness** — asymmetry. Negative skew means the left tail is longer: many small gains, rare
  large losses. A strategy can manufacture a lovely Sharpe ratio by selling insurance and hiding
  its risk in negative skew.
- **Kurtosis** — tail weight. High kurtosis means extreme moves of *either* sign are far more
  likely than a normal implies, so a variance-based risk estimate understates what can happen.

### The distributions to know cold

**Normal.** The CLT's attractor, and the reason it is everywhere. But it assigns essentially zero
probability to the days that actually hurt: a 5-sigma move is a 1-in-1.7-million event under a
normal, and §5 just measured them happening far more often.

**Student-$t$.** A normal with a randomized variance — which is *mechanically* what stochastic
volatility produces, so it is not a curve-fitting hack but the right functional form for this
data. Its degrees of freedom $\nu$ parameterize the tails: $\nu\to\infty$ recovers the normal,
$\nu \le 4$ means infinite kurtosis, $\nu \le 2$ means infinite variance. Fitted $\nu$ on real
daily equity returns is typically **3 to 5**, so the *fourth* moment barely exists.

**Lognormal.** What prices are if log returns are normal (§4). Positive by construction.

**Poisson.** Counts of rare events in a window — trades arriving, jumps, defaults. We do not use
it here; it returns in Unit 018 for jump-diffusions.

We fit the $t$ by **maximum likelihood** (Unit 006's workhorse): choose the parameters under which
the data we actually saw is most probable.
""")

code(r"""
# WORKED — the four moments, then a normal vs Student-t fit by maximum likelihood.
idx = rets.mean(axis=1).rename("EW index")          # the equal-weight index: our market proxy

rule("the four moments")
mom = pd.DataFrame({
    "mean (daily)":  [idx.mean()] + [rets[c].mean() for c in TICKERS[:3]],
    "std (daily)":   [idx.std()] + [rets[c].std() for c in TICKERS[:3]],
    "skew":          [stats.skew(idx)] + [stats.skew(rets[c]) for c in TICKERS[:3]],
    "excess kurt":   [stats.kurtosis(idx)] + [stats.kurtosis(rets[c]) for c in TICKERS[:3]],
}, index=["EW index"] + TICKERS[:3]).T
show(mom)
print(f"\nannualized: the index earns {idx.mean()*TRADING_DAYS:.2%} with "
      f"{idx.std()*np.sqrt(TRADING_DAYS):.2%} vol  ->  Sharpe {idx.mean()/idx.std()*np.sqrt(252):.2f}")
print(f"the daily MEAN is {idx.mean():.6f} and the daily SD is {idx.std():.4f}: "
      f"noise is {idx.std()/abs(idx.mean()):.0f}x the signal.")

rule("MLE: which distribution actually generated this?")
mu_n, sd_n = stats.norm.fit(idx)
df_t, loc_t, sc_t = stats.t.fit(idx)
ll_n = stats.norm.logpdf(idx, mu_n, sd_n).sum()
ll_t = stats.t.logpdf(idx, df_t, loc_t, sc_t).sum()
print(f"  normal    MLE: mu={mu_n:+.5f} sigma={sd_n:.5f}          log-likelihood {ll_n:>9.1f}")
print(f"  Student-t MLE: df={df_t:.2f} loc={loc_t:+.5f} scale={sc_t:.5f}  log-likelihood {ll_t:>9.1f}")
print(f"  the t is exp({ll_t-ll_n:.1f}) times more likely to have produced this data")
print(f"  df = {df_t:.1f}  ->  the 4th moment is barely finite; the 5th does not exist")

rule("tail probabilities: the cost of assuming normality")
print(f"{'threshold':>10} {'observed':>10} {'Student-t':>11} {'normal':>11} {'normal is off by':>18}")
for k in (2, 3, 4, 5):
    thr = k * idx.std()
    emp = float(np.mean(np.abs(idx - idx.mean()) > thr))
    p_t = 2 * stats.t.sf(thr / sc_t, df_t)
    p_n = 2 * stats.norm.sf(k)
    print(f"{k:>9}sd {emp:>10.5f} {p_t:>11.5f} {p_n:>11.5f} {emp/max(p_n,1e-12):>16.0f}x")

rule("what a Gaussian assumption implies about the worst day in 10 years")
print(f"  observed worst day        : {idx.min():.2%}")
print(f"  Gaussian 1-in-2520 quantile: {stats.norm.ppf(1/N_DAYS, idx.mean(), idx.std()):.2%}")
print(f"  Student-t 1-in-2520 quantile: {stats.t.ppf(1/N_DAYS, df_t, loc_t, sc_t):.2%}")
""")

code(r"""
# CHECK — the t beats the normal, and the normal underestimates tails.
assert ll_t > ll_n, "on fat-tailed data the Student-t must fit better by likelihood"
assert 2.0 < df_t < 8.0, f"fitted df={df_t:.2f} should land in the realistic 2-8 band"
emp4 = float(np.mean(np.abs(idx - idx.mean()) > 4 * idx.std()))
assert emp4 > 10 * 2 * stats.norm.sf(4), "4-sigma days must be >>10x more common than Gaussian"
assert idx.min() < stats.norm.ppf(1 / N_DAYS, idx.mean(), idx.std()), \
    "the realized worst day should be worse than the Gaussian 1-in-10-year day"
assert idx.std() / abs(idx.mean()) > 20, "daily noise dwarfs the daily mean - the core difficulty"
print(f"§6 OK — Student-t(df={df_t:.1f}) beats the normal by {ll_t-ll_n:.0f} log-likelihood units.")
print("TAKEAWAY: 'approximately normal' is the assumption that makes risk models lie.")
""")

md(r"""
### Uncorrelated is not independent — the confusion that costs the most money

Unit 005 called this a costly confusion. Here is the bill.

- **Uncorrelated** means one specific thing: $\text{Cov}(X,Y) = 0$, i.e. no *linear* relationship.
- **Independent** means everything: no relationship of any kind. $P(X,Y) = P(X)P(Y)$.

Independence implies uncorrelatedness. **The converse is false**, and returns are the textbook
counterexample: $r_t$ and $r_{t+1}$ are essentially uncorrelated (§5, fact 2), while $|r_t|$ and
$|r_{t+1}|$ are strongly correlated (fact 3). Consecutive returns are *linearly* unrelated and
*emphatically* dependent.

Why that is expensive: almost every classical formula you know assumes **independent**
observations, but people check for **uncorrelated**, see a clean result, and proceed. The
$1/\sqrt{n}$ standard error, the $t$-test, the i.i.d. bootstrap — all of them count observations
as if each brought fresh information. When observations are dependent, $n$ observations carry
less than $n$ observations' worth of evidence, so the standard error is too small and every
$t$-statistic is too big. §8 measures exactly that gap, and §10 pays for it in a wider confidence
interval.

### Covariance, correlation, and the matrix that organizes them

For a panel you need the whole **covariance matrix** $\Sigma$, with $\Sigma_{ij} =
\text{Cov}(r_i,r_j)$. It carries variances on its diagonal and co-movement off it, but in units of
return-squared, so a volatile name dominates it for reasons that have nothing to do with
co-movement. The **correlation matrix** $C$ standardizes that away,

$$C = D^{-1}\Sigma D^{-1}, \qquad D = \text{diag}(\sigma_1,\dots,\sigma_N),$$

so every diagonal entry is 1 and every off-diagonal is a unitless number in $[-1,1]$. This is the
object §7 decomposes.
""")

code(r"""
# WORKED — the counterexample that makes 'uncorrelated != independent' concrete.
rule("linearly unrelated, yet strongly dependent")
print(f"{'name':>6} {'corr(r_t, r_t+1)':>18} {'corr(|r_t|, |r_t+1|)':>22}")
for c in TICKERS[:5]:
    print(f"{c:>6} {acf(rets[c], 1):>+18.4f} {acf(rets[c].abs(), 1):>+22.4f}")
print(f"{'MEAN':>6} {avg['acf1(r)']:>+18.4f} {avg['acf1(|r|)']:>+22.4f}")

# If consecutive returns were independent, knowing today would tell you nothing about the SIZE
# of tomorrow. Condition on today and look.
rule("conditioning: sort days by today's move, then look at tomorrow")
x = rets["ALFA"]
q = pd.qcut(x[:-1], 5, labels=["most negative", "down", "flat", "up", "most positive"])
tomorrow = pd.DataFrame({"bucket": q.values,
                         "next_r": x.values[1:],
                         "next_abs": np.abs(x.values[1:])})
g = tomorrow.groupby("bucket", observed=True).agg(
    next_mean_return=("next_r", "mean"), next_mean_abs=("next_abs", "mean"),
    next_volatility=("next_r", "std"), days=("next_r", "size"))
show(g)
spread_dir = g.next_mean_return.max() - g.next_mean_return.min()
spread_vol = g.next_volatility.max() / g.next_volatility.min()
print(f"\ntomorrow's mean RETURN varies by only {spread_dir:.4f} across buckets  (no direction edge)")
print(f"tomorrow's VOLATILITY varies by {spread_vol:.2f}x across buckets      (a large risk edge)")

rule("covariance vs correlation, and C = D^-1 Sigma D^-1")
Sigma = rets.cov().values
D = np.diag(rets.std().values)
C = np.linalg.inv(D) @ Sigma @ np.linalg.inv(D)
print("correlation matrix (first 6 names):")
show(pd.DataFrame(C[:6, :6], index=TICKERS[:6], columns=TICKERS[:6]))
off = C[~np.eye(N_NAMES, dtype=bool)]
print(f"\naverage pairwise correlation = {off.mean():.3f}  (range {off.min():.3f} to {off.max():.3f})")
print(f"pandas .corr() agrees with D^-1 Sigma D^-1: {np.allclose(C, rets.corr().values)}")
""")

code(r"""
# CHECK — the counterexample, and the matrix identity.
assert abs(avg["acf1(r)"]) < 0.05 and avg["acf1(|r|)"] > 0.10, "uncorrelated in sign, dependent in size"
assert spread_dir < 0.004, "conditioning on today gives almost no edge on tomorrow's DIRECTION"
assert spread_vol > 1.3, "...but a big edge on tomorrow's VOLATILITY - hence dependence"
assert np.allclose(C, rets.corr().values), "C = D^-1 Sigma D^-1 is the correlation matrix"
assert np.allclose(np.diag(C), 1.0), "a correlation matrix has ones on the diagonal"
assert np.all(np.linalg.eigvalsh(Sigma) > 0), "a covariance matrix must be positive definite"
assert 0.15 < off.mean() < 0.60, "realistic average equity pairwise correlation"
print(f"§6b OK — returns are uncorrelated (acf1 {avg['acf1(r)']:+.3f}) yet dependent "
      f"(vol varies {spread_vol:.1f}x by bucket).")
print("TAKEAWAY: your n observations are worth fewer than n. Section 8 puts a number on it.")
""")

md(r"""
### LLN vs CLT, and the Bayes calculation that should govern your priors

Two theorems, constantly conflated. Unit 005's distinction:

- The **law of large numbers** says the sample mean *converges* to the true mean. It promises a
  destination and says nothing about the journey.
- The **central limit theorem** says how far you still are: the error
  $\bar X_n - \mu$ is approximately normal with standard deviation $\sigma/\sqrt n$. It gives you
  the **rate** — and therefore the error bar.

The $\sqrt n$ is the tyrant of this entire field. To halve your uncertainty you need **four times**
the data. Since you cannot buy more history, the only lever left is reducing $\sigma$ — which is
why hedging out the market (§9) is not cosmetic, it is how you buy statistical power.

The CLT also explains a fact from §5: aggregating fat-tailed daily returns into monthly ones made
them *less* fat-tailed. A sum of many independent draws drifts toward normality no matter how ugly
each draw is. The catch — and it is a big one — is that the convergence is slow **in the tails**,
which is precisely where risk lives.

**Bayes' rule: the number that should scare you.** Unit 005 gave the update

$$P(H \mid E) = \frac{P(E \mid H)\,P(H)}{P(E)}.$$

Apply it to the only question that matters. You have a significant backtest. What is the
probability the edge is real? That depends on your **prior** — how many of the strategies people
try are genuinely good — and on the **power** of your test. Real research priors are brutally
low: most ideas do not work. Run the arithmetic before you trust a $p$-value.
""")

code(r"""
# WORKED — the sqrt(n) rate, then the Bayes calculation on 'my backtest is significant'.
rule("CLT: the error bar on the mean shrinks like 1/sqrt(n)")
print(f"{'n days':>8} {'SE of mean':>13} {'SE as % of a 5bp/day edge':>28}")
edge = 0.0005
for n in (63, 252, 1260, 2520, 10080):
    se = idx.std() / np.sqrt(n)
    print(f"{n:>8} {se:>13.6f} {se/edge*100:>27.0f}%")
print("to halve the error bar you need 4x the data. You cannot buy more history.")

rule("the CLT actually working - and how noisy the evidence for it is")
print(f"{'horizon':>8} {'n obs':>7} {'excess kurt (index)':>21} {'mean over 12 names':>20}")
for n in (1, 5, 21, 63):
    agg = idx.values[:len(idx) // n * n].reshape(-1, n).mean(axis=1)
    per_name = [stats.kurtosis(rets[c].values[:N_DAYS // n * n].reshape(-1, n).mean(axis=1))
                for c in TICKERS]
    print(f"{n:>8} {len(agg):>7} {stats.kurtosis(agg):>21.2f} {np.mean(per_name):>20.2f}")
print("  The 12-name average declines cleanly. The single index series does NOT decline")
print("  monotonically - and that is the lesson, not an inconvenience: at a 63-day horizon")
print(f"  ONE series gives only {N_DAYS//63} observations, and a kurtosis estimated from "
      f"{N_DAYS//63} points")
print("  is almost pure noise. The CLT is a statement about the limit, not a promise that")
print("  every finite sample walks toward it in a straight line. Averaging across names is")
print("  how we got a readable answer in Section 5 - more data, same question.")

rule("LLN vs CLT stated precisely")
print("  LLN: sample mean -> true mean.                 (a promise with no timetable)")
print("  CLT: (sample mean - true mean) ~ N(0, sigma/sqrt(n)).  (the timetable)")

rule("BAYES - given a significant backtest, is the edge real?")
print(f"{'prior P(real)':>14} {'power':>8} {'alpha':>8} {'P(real | significant)':>24}")
for prior in (0.50, 0.20, 0.05, 0.01):
    for power, alpha_lvl in ((0.80, 0.05), (0.50, 0.05)):
        post = prior * power / (prior * power + (1 - prior) * alpha_lvl)
        print(f"{prior:>13.0%} {power:>8.0%} {alpha_lvl:>8.0%} {post:>23.1%}")
prior, power, alpha_lvl = 0.05, 0.50, 0.05
posterior = prior * power / (prior * power + (1 - prior) * alpha_lvl)
print(f"\nRealistic quant research: a {prior:.0%} prior and {power:.0%} power.")
print(f"A p < 0.05 result is then real with probability {posterior:.0%} "
      f"- so {1-posterior:.0%} of 'discoveries' are false.")
print("This is why Section 11 corrects for multiple testing instead of trusting p < 0.05.")
""")

code(r"""
# CHECK — the sqrt(n) law and the Bayes arithmetic.
se_252, se_1008 = idx.std() / np.sqrt(252), idx.std() / np.sqrt(1008)
assert np.isclose(se_252 / se_1008, 2.0, rtol=1e-9), "4x the data must halve the standard error"
assert stats.kurtosis(idx.values[:2520].reshape(-1, 63).mean(axis=1)) < stats.kurtosis(idx), \
    "the CLT should pull aggregated returns toward normality"
assert posterior < 0.5, "with a low prior, a p<0.05 result is more likely false than true"
assert (0.5 * 0.5 / (0.5 * 0.5 + 0.5 * 0.05)) > posterior, "a better prior raises the posterior"
print(f"§6c OK — SE ~ 1/sqrt(n) confirmed; P(real | p<0.05) = {posterior:.0%} at a 5% prior.")
print("TAKEAWAY: a p-value is not P(the edge is real). Your prior does most of the work.")
""")

# ======================================================================== §7 PCA
md(r"""
## §7 · The risk structure of the panel (Unit 008)

We now know each name's behaviour. The next question is **how they move together**, because §1
said alpha is what remains after known exposures are removed — and you cannot remove an exposure
you have not found.

### The panel is a matrix, and $\Sigma$ is where the structure hides

Our data is a $2520 \times 12$ matrix. The covariance matrix $\Sigma$ (or its standardized
sibling $C$) compresses that into $12\times12$ numbers describing co-movement. But 66 distinct
correlations is still too many to reason about, and they are not independent of one another — they
have *structure*. Eigendecomposition finds it.

### Eigenvectors: the directions a matrix does not rotate

Re-warming Unit 008 in one paragraph. A matrix is a transformation of space. Most input vectors
come out pointing somewhere new. An **eigenvector** $v$ is a rare direction that comes out
pointing the same way, only rescaled:

$$\Sigma v = \lambda v.$$

The **eigenvalue** $\lambda$ is the stretch factor. For a covariance matrix, whose job is to
describe a cloud of points, this has a directly physical meaning: eigenvectors are the **axes of
the data cloud's ellipsoid**, and each eigenvalue is the **variance along that axis**. Because
$\Sigma$ is symmetric and positive semi-definite, we are guaranteed real, non-negative eigenvalues
and orthogonal eigenvectors — a full set of perpendicular axes.

**PCA is nothing more than that decomposition, read as a story about portfolios.** Each
eigenvector is a set of weights, i.e. a portfolio; its eigenvalue is that portfolio's variance.
The first principal component is the single portfolio with the most variance in the panel.

Two identities make this checkable rather than mystical:

$$\sum_i \lambda_i = \text{trace}(C) = N \qquad\text{and}\qquad
  \text{variance explained by } i = \frac{\lambda_i}{N}.$$

The first says the decomposition conserves total variance — it only *redistributes* it into
independent directions. (For a correlation matrix the trace is exactly $N$, since every diagonal
entry is 1. A useful arithmetic check: with $N = 12$, if PC1's eigenvalue is 6 then it accounts
for 6/12 = 50% of the panel's variance — which is close to what we are about to find.)

**PC1 is the market.** For any equity panel, the first eigenvector comes out with **all weights of
the same sign** — a portfolio that is long everything. That is not a coincidence to be admired; it
is the market factor, discovered from the correlation matrix alone with no index data. It is the
exposure §9 must remove.
""")

code(r"""
# WORKED — eigendecompose the correlation matrix and read the structure off it.
C = rets.corr().values
evals, evecs = np.linalg.eigh(C)                 # eigh: symmetric matrices, ascending order
order = np.argsort(evals)[::-1]                  # re-sort descending: PC1 first
evals, evecs = evals[order], evecs[:, order]
if evecs[:, 0].mean() < 0:                       # an eigenvector's sign is arbitrary; fix it
    evecs[:, 0] *= -1

rule("the identities that must hold")
print(f"sum of eigenvalues = {evals.sum():.6f}   trace(C) = {np.trace(C):.6f}   N = {N_NAMES}")
print(f"largest eigenvalue = {evals[0]:.4f}  ->  {evals[0]/N_NAMES:.1%} of panel variance")
print(f"C v1 = lambda1 v1 ?  max error = {np.abs(C @ evecs[:,0] - evals[0]*evecs[:,0]).max():.2e}")
print(f"eigenvectors orthonormal? V'V = I to {np.abs(evecs.T @ evecs - np.eye(N_NAMES)).max():.2e}")

rule("scree plot - how many independent risks are there really?")
cum = np.cumsum(evals) / N_NAMES
for i in range(N_NAMES):
    print(f"  PC{i+1:<2} lambda={evals[i]:>6.3f}  {evals[i]/N_NAMES:>6.1%}  "
          f"cumulative {cum[i]:>6.1%}  {'#' * int(evals[i]/N_NAMES*100)}")
k90 = int(np.searchsorted(cum, 0.90) + 1)
print(f"\n{k90} of {N_NAMES} components are needed for 90% of the variance.")

rule("PC1 is the market factor - look at the signs")
pc1 = pd.Series(evecs[:, 0], index=TICKERS)
show(pd.DataFrame({"PC1 loading": pc1, "PC2 loading": evecs[:, 1],
                   "sector": [SECTORS[s] for s in SECTOR_OF], "true beta": beta_true}))
print(f"\nall PC1 loadings the same sign? {bool(np.all(pc1 > 0) or np.all(pc1 < 0))}"
      f"  -> PC1 is 'long everything' = THE MARKET")
pc1_returns = rets.values @ evecs[:, 0]
print(f"corr(PC1 portfolio, equal-weight index) = {np.corrcoef(pc1_returns, idx)[0,1]:.4f}")
print(f"PC2 loadings by sector: " + ", ".join(
    f"{SECTORS[s]} {evecs[SECTOR_OF == s, 1].mean():+.3f}" for s in range(3))
    + "   -> PC2 separates sectors")

rule("the theory link to Unit 009: PC1 loadings are proportional to beta_i / sigma_i")
sd = rets.std().values
print(f"corr(PC1 loading, true beta)             = {np.corrcoef(pc1, beta_true)[0,1]:+.3f}")
print(f"corr(PC1 loading, true beta / sigma_i)   = {np.corrcoef(pc1, beta_true/sd)[0,1]:+.3f}  <- near 1")
print("because we decomposed the CORRELATION matrix, each name was pre-divided by its own vol.")
""")

code(r"""
# CHECK — the eigendecomposition identities and the market-factor claim.
assert np.isclose(evals.sum(), N_NAMES), "trace of a correlation matrix = N (variance is conserved)"
assert np.allclose(C @ evecs[:, 0], evals[0] * evecs[:, 0]), "the eigenvector equation itself"
assert np.allclose(evecs.T @ evecs, np.eye(N_NAMES), atol=1e-10), "eigenvectors are orthonormal"
assert np.all(evals > 0) and np.all(np.diff(evals) <= 1e-12), "positive definite, sorted descending"
assert np.all(pc1 > 0), "PC1 must be long every name - it is the market"
assert evals[0] / N_NAMES > 3 * evals[1] / N_NAMES, "PC1 should dwarf PC2"
assert abs(np.corrcoef(pc1_returns, idx)[0, 1]) > 0.95, "the PC1 portfolio IS the index, found blind"
assert np.corrcoef(pc1, beta_true / sd)[0, 1] > 0.90, "PC1 loading ~ beta_i/sigma_i, as theory says"
print(f"§7 OK — PC1 = {evals[0]/N_NAMES:.0%} of risk, all-positive loadings, "
      f"corr {np.corrcoef(pc1_returns, idx)[0,1]:.3f} with the index.")
print("TAKEAWAY: one factor dominates the panel. Any 'edge' that is really that factor is not alpha.")
""")

md(r"""
### Projection — the operation that removes an exposure (and secretly is OLS)

We have found the market direction. Now remove it. Unit 008's tool is **projection**, and it is
worth seeing that projection and regression are the same act, because that identity is the bridge
between Units 008 and 009.

Take a vector $z$ (a set of signal values across names) and a direction $b$ (each name's beta).
Split $z$ into the part that lies **along** $b$ and the part **perpendicular** to it:

$$\underbrace{z}_{\text{signal}} \;=\; \underbrace{\frac{z^\top b}{b^\top b}\,b}_{\text{the part explained by }b}
\;+\; \underbrace{z - \frac{z^\top b}{b^\top b}\,b}_{\text{the residual, } \perp\, b}$$

Every piece has a job. $z^\top b$ measures how much $z$ points along $b$; dividing by $b^\top b$
converts that into "how many copies of $b$"; multiplying by $b$ rebuilds it as a vector. Subtract,
and what is left is guaranteed orthogonal to $b$ — verify it by taking the inner product, which
gives $z^\top b - (z^\top b / b^\top b)(b^\top b) = 0$ exactly.

**The residual is the neutralized signal.** A book built from it has zero net beta, so market
moves cannot touch it.

Now the punchline: that coefficient $z^\top b / b^\top b$ **is** the OLS slope from regressing $z$
on $b$ with no intercept. Projection and least squares are one operation. So when §8 says "OLS is
projection", it is not an analogy — the neutralization we just did is a regression, and the
regressions §8 runs are projections. Two units, one piece of geometry.

#### The trap: two neutralities at once

We now want the book to be neutral on **two** axes simultaneously — dollar-neutral ($\sum_i w_i=0$,
§2) *and* beta-neutral ($\sum_i w_i \hat\beta_i = 0$). The obvious move is to do them in sequence:
demean, then project out $\beta$. **That does not work,** and the reason is pure geometry.

Projecting out $b$ subtracts a multiple of $b$. If $\bar b \neq 0$ — and betas average about 1, so
it certainly is not zero — then subtracting $c\,b$ shifts the sum of the weights by $-c\sum_i b_i
\neq 0$. Fixing the second exposure **re-broke the first**. Sequential projections only compose when
the directions are orthogonal, and $\mathbf{1}$ and $\beta$ are emphatically not.

The fix is to remove both at once, which means projecting onto the orthogonal complement of the
*plane* spanned by $\mathbf{1}$ and $\beta$ — and that is just OLS with **two** regressors:

$$z \;=\; a\,\mathbf{1} \;+\; c\,\beta \;+\; \varepsilon, \qquad w \propto \hat\varepsilon$$

The residual of *that* regression is orthogonal to both columns, so it is dollar-neutral and
beta-neutral simultaneously. Equivalently — and this is the form we will code — project $z$ onto the
**demeaned** beta vector $\beta - \bar\beta$, which is already perpendicular to $\mathbf{1}$. Having
made the two directions orthogonal, the sequential recipe works again.

This is the single most common way a "market-neutral" book quietly is not, so we verify both
exposures rather than assuming them.
""")

code(r"""
# WORKED — project a signal onto beta, then prove the projection IS an OLS regression.
z_demo = np.array([1.8, 0.9, 0.4, -0.2, 1.1, -0.6, -1.3, 0.2, -0.9, -1.5, 0.7, -0.6])
z_demo = z_demo - z_demo.mean()                 # dollar-neutral first (Section 2)
b = beta_true

coef = (z_demo @ b) / (b @ b)                   # "how many copies of b are in z"
z_neutral = z_demo - coef * b                   # the residual: perpendicular to b

rule("splitting the signal into 'market bet' + 'relative value'")
show(pd.DataFrame({"signal z": z_demo, "beta b": b,
                   "along b (market bet)": coef * b,
                   "residual (alpha)": z_neutral}, index=TICKERS))
print(f"\nprojection coefficient = z.b / b.b = {z_demo @ b:+.4f} / {b @ b:.4f} = {coef:+.6f}")
print(f"residual . b = {z_neutral @ b:+.2e}   <- orthogonal by construction")
print(f"norms: |z|^2 = {z_demo @ z_demo:.4f} = |along|^2 {coef**2*(b@b):.4f} "
      f"+ |residual|^2 {z_neutral @ z_neutral:.4f}   (Pythagoras)")

rule("the identity: projection == OLS with no intercept")
ols_no_int = sm.OLS(z_demo, b).fit()
print(f"  projection coefficient : {coef:.10f}")
print(f"  OLS slope of z on b    : {ols_no_int.params[0]:.10f}")
print(f"  max |residual difference| = {np.abs(ols_no_int.resid - z_neutral).max():.2e}")
print("  => 'neutralize an exposure' and 'regress it out' are the same instruction.")

rule("the trap - fixing beta-neutrality BREAKS dollar-neutrality")
print(f"  before projecting: sum(z) = {z_demo.sum():+.2e}  (dollar-neutral)   "
      f"z.b = {z_demo @ b:+.4f}  (NOT beta-neutral)")
print(f"  after  projecting: sum(z) = {z_neutral.sum():+.4f}  <- BROKEN        "
      f"z.b = {z_neutral @ b:+.2e}  (beta-neutral)")
print(f"  the damage is exactly -coef * sum(b) = {-coef * b.sum():+.4f}, because mean(b) = "
      f"{b.mean():.3f} != 0")
print("  a book like this is short (or long) the market in DOLLARS while claiming neutrality.")

rule("the fix - remove both exposures at once == OLS on [1, beta]")
b_c   = b - b.mean()                            # demeaned beta: now perpendicular to the 1-vector
z_both = z_demo - ((z_demo @ b_c) / (b_c @ b_c)) * b_c
ols_two = sm.OLS(z_demo, sm.add_constant(b)).fit()   # the same thing, stated as a regression
print(f"  sum(z) = {z_both.sum():+.2e}   z.b = {z_both @ b:+.2e}   <- BOTH zero, together")
print(f"  identical to the 2-regressor OLS residual? max diff = "
      f"{np.abs(ols_two.resid - z_both).max():.2e}")
show(pd.DataFrame({"signal z": z_demo, "beta b": b,
                   "1-axis fix only": z_neutral, "both axes (used later)": z_both}, index=TICKERS))
print("This is the neutralization build_book() uses in Section 10.")

rule("PCA as compression: rebuild the panel from k components")
scores = rets.values @ evecs                     # the panel in PC coordinates
for k in (1, 2, 3, 6, 12):
    approx = scores[:, :k] @ evecs[:, :k].T
    kept = 1 - ((rets.values - approx) ** 2).sum() / (rets.values ** 2).sum()
    print(f"  k={k:>2} components: {kept:>6.1%} of the panel's squared variation reproduced "
          f"(theory: {np.cumsum(evals)[k-1]/N_NAMES:.1%})")
""")

code(r"""
# CHECK — projection geometry, the OLS identity, and PCA reconstruction.
assert abs(z_neutral @ b) < 1e-12, "the residual must be exactly orthogonal to beta"
assert np.isclose(z_demo @ z_demo, coef**2 * (b @ b) + z_neutral @ z_neutral), "Pythagoras"
assert np.isclose(coef, ols_no_int.params[0]), "projection coefficient == OLS slope"
assert np.allclose(ols_no_int.resid, z_neutral), "projection residual == OLS residual"
full = scores @ evecs.T
assert np.allclose(full, rets.values, atol=1e-10), "all 12 components reconstruct the panel exactly"
assert abs(z_neutral.sum()) > 0.01, "projecting out raw beta really does break dollar-neutrality"
assert np.isclose(z_neutral.sum(), -coef * b.sum()), "and the damage is exactly -coef * sum(b)"
assert abs(z_both.sum()) < 1e-12, "the two-axis fix is dollar-neutral..."
assert abs(z_both @ b) < 1e-12, "...and beta-neutral, at the same time"
assert np.allclose(ols_two.resid, z_both), "the two-axis fix IS the residual of OLS on [1, beta]"
print("§7b OK — projection removes an exposure exactly, and it is literally an OLS regression.")
print("TAKEAWAY: Units 008 and 009 are one idea: least squares = orthogonal projection.")
print("TAKEAWAY: neutralities do not compose. Remove correlated exposures together, then VERIFY.")
""")

# ======================================================================== §8 the signals
md(r"""
## §8 · The twelve candidates, and the screen that fools you

Time to test signals. The PM's research folder has 12 candidates with respectable factor names.
Each is a number per name per day, computable from information available at that day's close.
One of them is `rev5` — the 5-day reversal from §4's simulator. The other eleven are noise
wearing a good suit. **Nothing below knows which is which.**

### The naïve screen — and why it is so persuasive

A reasonable-looking first pass, and the one a smart, untrained analyst writes on day one:

> Stack every name and every day into one big regression of the next 5 days' return on today's
> signal. With 12 names $\times$ 2,515 days we get **over 30,000 observations** — a huge sample.
> Read off the $t$-statistic. Keep whatever clears $|t| > 2$.

Every step feels defensible. The horizon matches the intended holding period. Pooling across names
is standard panel practice. 30,000 observations sounds like overwhelming evidence. And the code is
four lines.

It is nonetheless **wrong in three independent ways**, and each one inflates the $t$-statistic:

1. **The 5-day windows overlap.** Sampling daily but measuring 5-day forward returns means
   consecutive observations share 4 of their 5 days. They are near-copies. (Unit 009 → §9)
2. **The 12 names are not 12 independent observations.** §7 measured $\approx 42\%$ of panel
   variance in one factor: on any given day all 12 names largely move *together*. (Unit 005 → §9)
3. **We are running 12 tests and will report the best one.** (Unit 007 → §11)

Run it, and watch it produce a list of "discoveries."
""")

code(r"""
# WORKED — build the 12 candidate signals, then run the naive screen on all of them.
DECOY_NAMES = ["mom12m", "value", "quality", "lowvol", "size", "growth",
               "sentiment", "accruals", "carry", "beta_arb", "analyst_rev"]

def zscore_time(a):
    '''Standardize each name's signal over TIME, so signals are comparable to each other.'''
    return (a - a.mean(0)) / a.std(0)

def simulate_decoy_signals(seed=23, n_days=N_DAYS, burn=500):
    '''11 persistent signals built with NO knowledge of returns. Every one is pure noise.
    Each has a common component, so - like real factors - it is partly a disguised market bet.'''
    rng = np.random.default_rng(seed)
    out = {}
    for name in DECOY_NAMES:
        T = n_days + burn
        common, idio_s = np.zeros(T), np.zeros((T, N_NAMES))
        a = rng.uniform(0.6, 2.2)                       # how market-like this signal is
        for t in range(1, T):
            common[t] = 0.985 * common[t-1] + rng.normal()
            idio_s[t] = 0.970 * idio_s[t-1] + rng.normal(size=N_NAMES)
        out[name] = zscore_time((a * common[:, None] + idio_s)[burn:])
    return out

signals = {"rev5": zscore_time(REV_TRUE)}
signals.update(simulate_decoy_signals())
SIGNAL_NAMES = list(signals)
M = len(SIGNAL_NAMES)

rule(f"{M} candidate signals")
print(pd.DataFrame({
    "autocorr(1)":  [acf(signals[s][:, 0], 1) for s in SIGNAL_NAMES],
    "cross-sec sd": [signals[s].std(1).mean() for s in SIGNAL_NAMES],
    "corr w/ market-wide avg": [np.corrcoef(signals[s].mean(1), idx)[0, 1] for s in SIGNAL_NAMES],
}, index=SIGNAL_NAMES).round(4).to_string())

# The naive screen: overlapping H-day forward returns, all names stacked, classical SEs.
fwd = np.array([R[t+1:t+1+H_NAIVE].sum(0) for t in range(N_DAYS - H_NAIVE)])
screen = []
for s in SIGNAL_NAMES:
    x = signals[s][:N_DAYS - H_NAIVE].ravel()
    fit = sm.OLS(fwd.ravel(), sm.add_constant(x)).fit()
    screen.append({"signal": s, "beta": fit.params[1], "t_naive": fit.tvalues[1],
                   "p_naive": fit.pvalues[1], "R2": fit.rsquared, "n_obs": int(fit.nobs)})
screen = pd.DataFrame(screen).set_index("signal").reindex(
    pd.Series([abs(r) for r in pd.DataFrame(screen).set_index("signal").t_naive]
              ).values.argsort()[::-1].tolist()) if False else pd.DataFrame(screen).set_index("signal")
screen = screen.reindex(screen.t_naive.abs().sort_values(ascending=False).index)

rule(f"THE NAIVE SCREEN: {H_NAIVE}-day fwd return ~ signal, {int(screen.n_obs.iloc[0]):,} pooled obs")
print(screen.assign(verdict=np.where(screen.p_naive < 0.05, "*** SIGNIFICANT ***", "-"))
            .to_string(float_format=lambda v: f"{v:>10.4f}"))
n_sig = int((screen.p_naive < 0.05).sum())
print(f"\n{n_sig} of {M} signals are 'significant' at p < 0.05.")
print(f"Best: {screen.index[0]} with t = {screen.t_naive.iloc[0]:.2f}, "
      f"p = {screen.p_naive.iloc[0]:.2e}.")
print("If you stopped here you would report a research pipeline with a "
      f"{n_sig/M:.0%} hit rate. Ground truth: 1 of 12 is real.")
""")

code(r"""
# CHECK — the naive screen really does manufacture a pile of false discoveries.
assert screen.n_obs.iloc[0] > 30000, "the naive screen brags about >30,000 observations"
assert abs(screen.t_naive.iloc[0]) > 8, "the headline t should look overwhelming"
assert n_sig >= 4, "several signals should clear p<0.05, though only ONE is real by construction"
decoy_hits = [s for s in screen.index if s != "rev5" and screen.p_naive[s] < 0.05]
assert len(decoy_hits) >= 3, f"pure noise should sail through the naive screen: {decoy_hits}"
assert screen.R2.max() < 0.02, "note how tiny R^2 is even for the 'best' signal - low SNR is normal"
print(f"§8 OK — the naive screen flagged {n_sig} signals; "
      f"{len(decoy_hits)} of them ({', '.join(decoy_hits)}) are pure noise.")
print("TAKEAWAY: 30,000 rows is not 30,000 observations. The rest of the notebook is the fix.")
""")

# ======================================================================== §9 regression
md(r"""
## §9 · Regression done right — dismantling the headline (Unit 009)

The screen's $t$-statistic is a ratio. Unit 009's central lesson is that the numerator is usually
fine and **the denominator is the liar**:

$$t = \frac{\hat\beta}{\text{SE}(\hat\beta)}.$$

$\hat\beta$ is a sample average, so it is consistent under weak assumptions. $\text{SE}(\hat\beta)$
is where the assumptions hide, and each violated one shrinks it and inflates $t$. We will fix them
one at a time. First, though, make sure OLS itself is not a black box.

### OLS from first principles, and the identity you should be able to derive

Model, estimator, and the three facts worth owning. With one regressor plus an intercept, OLS
picks the line minimizing the sum of squared vertical misses, and the solution is

$$\hat\beta_1 = \frac{\text{Cov}(x,y)}{\text{Var}(x)}
             = \rho_{xy}\,\frac{\sigma_y}{\sigma_x}.$$

Read the second form: **a regression slope is a correlation, rescaled by the ratio of the two
standard deviations.** A slope of 0.003 is not "small" — it is a correlation dressed in the units
of $y$ per unit of $x$, and it is why §8's $R^2$ can be 0.004 while its $t$ is enormous.

Three properties, all verified numerically below:

1. **The residuals are orthogonal to the regressors** — $\hat\varepsilon^\top x = 0$ and
   $\sum\hat\varepsilon = 0$. This is not a coincidence, it is the first-order condition: if the
   residual had any component along $x$, you could reduce the squared error by moving $\hat\beta$.
   This is §7's projection again — fitted values are the projection of $y$ onto the column space
   of $X$, and the residual is what is perpendicular to it.
2. **$R^2 = 1 - \text{SSR}/\text{SST}$**, the fraction of variation explained — which for a single
   regressor is exactly $\rho_{xy}^2$.
3. **The classical standard error**
   $\text{SE}(\hat\beta_1) = \sqrt{\hat\sigma^2_\varepsilon / \sum_i (x_i-\bar x)^2}$.
   Stare at that denominator, because it is the source of every problem to come: it counts
   observations as though each contributed independent information. Nothing in the formula knows
   that our rows overlap in time and cluster across names.
""")

code(r"""
# WORKED — reproduce statsmodels' OLS by hand on the winning signal, to prove nothing is magic.
best_signal = screen.index[0]
x_pool = signals[best_signal][:N_DAYS - H_NAIVE].ravel()
y_pool = fwd.ravel()
fit_ols = sm.OLS(y_pool, sm.add_constant(x_pool)).fit()
resid = fit_ols.resid
n_pool = len(y_pool)

beta_hand = np.cov(x_pool, y_pool, ddof=1)[0, 1] / np.var(x_pool, ddof=1)
rho = np.corrcoef(x_pool, y_pool)[0, 1]
beta_via_rho = rho * y_pool.std(ddof=1) / x_pool.std(ddof=1)
se_hand = np.sqrt((resid @ resid / (n_pool - 2)) / ((x_pool - x_pool.mean()) ** 2).sum())

rule(f"OLS by hand vs statsmodels  (signal = {best_signal})")
print(f"  slope   statsmodels {fit_ols.params[1]:.8f}   Cov/Var {beta_hand:.8f}   "
      f"rho*sy/sx {beta_via_rho:.8f}")
print(f"  SE      statsmodels {fit_ols.bse[1]:.8f}   by hand {se_hand:.8f}")
print(f"  t       statsmodels {fit_ols.tvalues[1]:.4f}       by hand "
      f"{fit_ols.params[1]/se_hand:.4f}")
print(f"  correlation rho = {rho:+.5f}  ->  a {abs(rho):.1%} correlation, nothing more")

rule("property 1 - OLS is projection: residuals are orthogonal to the regressors")
print(f"  residual . x     = {resid @ x_pool:+.3e}   (exactly zero up to floating point)")
print(f"  sum of residuals = {resid.sum():+.3e}   (the intercept guarantees this)")
print(f"  corr(residual, x) = {np.corrcoef(resid, x_pool)[0,1]:+.3e}")

rule("property 2 - R^2 three ways")
sst = ((y_pool - y_pool.mean()) ** 2).sum()
print(f"  1 - SSR/SST = {1 - (resid**2).sum()/sst:.8f}")
print(f"  statsmodels = {fit_ols.rsquared:.8f}")
print(f"  rho^2       = {rho**2:.8f}")
print(f"  -> the signal explains {fit_ols.rsquared:.2%} of 5-day return variation. "
      f"That is NORMAL for real alpha, and it is why t-stats matter more than R^2.")

rule("property 3 - where the classical SE comes from, and what it assumes")
print(f"  SE = sqrt( sigma_eps^2 / sum (x - xbar)^2 )")
print(f"     = sqrt( {resid @ resid / (n_pool-2):.3e} / {((x_pool-x_pool.mean())**2).sum():.1f} )"
      f" = {se_hand:.3e}")
print(f"  it treats all {n_pool:,} rows as independent. They are not, in TWO ways. -> below.")
""")

code(r"""
# CHECK — the three OLS properties, exactly.
assert np.isclose(fit_ols.params[1], beta_hand), "beta_hat = Cov(x,y)/Var(x)"
assert np.isclose(fit_ols.params[1], beta_via_rho), "beta_hat = rho * sy / sx"
assert abs(resid @ x_pool) < 1e-8 * abs(y_pool).sum(), "residuals orthogonal to x (projection)"
assert abs(resid.sum()) < 1e-8 * abs(y_pool).sum(), "residuals sum to zero when an intercept is fitted"
assert np.isclose(fit_ols.rsquared, rho ** 2), "for one regressor, R^2 = rho^2"
assert np.isclose(fit_ols.rsquared, 1 - (resid ** 2).sum() / sst), "R^2 = 1 - SSR/SST"
assert np.isclose(fit_ols.bse[1], se_hand, rtol=1e-8), "the classical SE formula, reproduced"
assert fit_ols.rsquared < 0.02, "real signals explain almost none of the variance"
print(f"§9 OK — OLS reproduced by hand; R^2 = {fit_ols.rsquared:.4f} = rho^2, residuals ⟂ x.")
print("TAKEAWAY: beta_hat is a rescaled correlation. The SE is the part that assumes independence.")
""")

md(r"""
### Failure 1 — heteroskedasticity (and why White barely helps here)

The classical SE assumes **homoskedasticity**: every observation's error has the same variance.
§5 destroyed that assumption — volatility clusters, so errors are small in calm months and large
in turbulent ones.

**White (HC) standard errors** fix it by refusing to pool one $\hat\sigma^2_\varepsilon$ across all
observations. Instead of assuming a common error variance, they use each observation's own squared
residual, so noisy observations are automatically down-weighted.

Now predict before you look: how much will White move the $t$-statistic? Unit 010's answer, which
surprises people: **usually not much.** Heteroskedasticity generally inflates $t$ by tens of
percent, not multiples. And here that small change is *itself diagnostic information* — if fixing
the variance assumption barely moves the number, then variance is not what is broken. Dependence
is. Which is the next section.
""")

code(r"""
# WORKED — White HC1 robust standard errors, and evidence they are needed.
fit_white = fit_ols.get_robustcov_results(cov_type="HC1")
se_classical, t_classical = fit_ols.bse[1], fit_ols.tvalues[1]
se_white, t_white = fit_white.bse[1], fit_white.tvalues[1]

rule("is there heteroskedasticity? sort by fitted value and look at residual size")
bucket = pd.qcut(fit_ols.fittedvalues, 5, labels=["Q1", "Q2", "Q3", "Q4", "Q5"])
hsk = pd.DataFrame({"bucket": bucket, "abs_resid": np.abs(resid),
                    "resid_var": resid ** 2}).groupby("bucket", observed=True).mean()
show(hsk)
print(f"residual variance varies {hsk.resid_var.max()/hsk.resid_var.min():.2f}x across buckets "
      f"-> errors are NOT identically scaled")
bp = sm.stats.diagnostic.het_breuschpagan(resid, sm.add_constant(x_pool))
print(f"Breusch-Pagan test: LM = {bp[0]:.1f}, p = {bp[1]:.2e}  "
      f"-> {'reject' if bp[1] < 0.05 else 'cannot reject'} homoskedasticity")

rule("what White does to the t-statistic")
print(f"  classical : SE = {se_classical:.6f}   t = {t_classical:+.2f}")
print(f"  White HC1 : SE = {se_white:.6f}   t = {t_white:+.2f}")
print(f"  SE ratio White/classical = {se_white/se_classical:.3f}  "
      f"({se_white/se_classical-1:+.1%})")
print(f"\nHeteroskedasticity is REAL (p = {bp[1]:.1e}) but costs only "
      f"{abs(t_classical)-abs(t_white):+.2f} of t.")
print("That near-miss is the clue: the problem is not the variance, it is the DEPENDENCE.")
""")

code(r"""
# CHECK — heteroskedasticity exists, White is the right tool, and it is not the main problem.
assert bp[1] < 0.05, "the Breusch-Pagan test should detect heteroskedasticity in return data"
assert hsk.resid_var.max() / hsk.resid_var.min() > 1.2, "residual variance is visibly non-constant"
assert se_white > 0 and np.isfinite(t_white)
assert abs(se_white / se_classical - 1) < 0.5, "White typically moves the SE by tens of %, not multiples"
assert abs(t_white) > 4, "after White alone the headline still looks impressive - we are not done"
print(f"§9b OK — heteroskedasticity confirmed (p={bp[1]:.0e}) but White only took t "
      f"from {t_classical:.1f} to {t_white:.1f}.")
print("TAKEAWAY: use White always; expect it to be a small correction. A small change is a clue.")
""")

md(r"""
### Failure 2 — overlapping windows, Newey–West, and the effective sample size

Here is the big one. We sampled **daily** but measured **5-day forward** returns. So the
observation at day $t$ and the observation at day $t+1$ share four of their five days. They are not
two pieces of evidence; they are one piece of evidence, counted twice.

The regression errors therefore inherit strong positive autocorrelation, and positively correlated
errors make the classical SE far too small. **Newey–West (HAC)** standard errors fix it by
estimating the error covariance out to a chosen lag — you must include at least the overlap
horizon, so `maxlags = 5` here — and letting nearby observations partially cancel.

The most useful way to report the damage is not the new $t$ but an **effective sample size**. If
$\text{SE}$ inflates by a factor $\phi$, then since $\text{SE}\propto 1/\sqrt n$, you really had

$$n_\text{eff} \;=\; \frac{n}{\phi^2}$$

independent observations. This converts an abstract statistical correction into the sentence a PM
actually needs: *"you claimed 30,000 observations; you had this many."*
""")

code(r"""
# WORKED — Newey-West HAC standard errors and the effective sample size.
fit_nw = fit_ols.get_robustcov_results(cov_type="HAC", maxlags=H_NAIVE, use_correction=True)
se_nw, t_nw_pool = fit_nw.bse[1], fit_nw.tvalues[1]
inflation = se_nw / se_classical
n_eff_time = n_pool / inflation ** 2

rule("proof the errors are autocorrelated (they must be - the windows overlap)")
res_by_day = resid.reshape(N_DAYS - H_NAIVE, N_NAMES).mean(1)   # average residual per day
print(f"{'lag':>5} {'autocorr of daily residual':>28}")
for lag in (1, 2, 3, 4, 5, 6, 10):
    flag = "  <- inside the 5-day overlap" if lag <= H_NAIVE else ""
    print(f"{lag:>5} {acf(res_by_day, lag):>+28.4f}{flag}")

rule("the same regression, three standard errors")
tbl = pd.DataFrame({
    "SE": [se_classical, se_white, se_nw],
    "t": [t_classical, t_white, t_nw_pool],
    "vs classical": [1.0, se_white / se_classical, inflation],
}, index=["classical (iid)", "White HC1 (heterosk.)", f"Newey-West (HAC, {H_NAIVE} lags)"])
show(tbl)

rule("translating the SE inflation into an honest sample size")
print(f"  SE inflated {inflation:.2f}x  ->  n_eff = n / inflation^2 = "
      f"{n_pool:,} / {inflation**2:.2f} = {n_eff_time:,.0f}")
print(f"  the analyst claimed {n_pool:,} observations; the time overlap alone cuts that to "
      f"~{n_eff_time:,.0f}")
print(f"  headline t {t_classical:+.2f}  ->  HAC t {t_nw_pool:+.2f}")
print(f"\nStill {'above' if abs(t_nw_pool) > 1.96 else 'below'} the naive 1.96 bar. "
      "And that is the trap: HAC fixed TIME, not the cross-section. Read on.")
""")

code(r"""
# CHECK — the overlap shows up as residual autocorrelation and HAC deflates the t.
assert acf(res_by_day, 1) > 0.15, "with 5-day overlap, adjacent daily residuals must be correlated"
assert acf(res_by_day, 1) > acf(res_by_day, 10), "autocorrelation should decay with lag"
assert se_nw > se_classical, "HAC must widen the standard error when errors are autocorrelated"
assert inflation > 1.2, "the widening should be substantial, not cosmetic"
assert abs(t_nw_pool) < abs(t_classical), "so the headline t must deflate"
assert n_eff_time < n_pool, "and the effective sample size must fall below the row count"
print(f"§9c OK — HAC inflated the SE {inflation:.2f}x, cutting t from {t_classical:.1f} "
      f"to {t_nw_pool:.1f} and n from {n_pool:,} to ~{n_eff_time:,.0f}.")
print("TAKEAWAY: overlapping windows duplicate evidence. Always report n_eff, not n.")
""")

md(r"""
### Failure 3 — the one no standard error can fix: cross-sectional dependence

We have handled non-constant variance and time dependence. The $t$-statistic is still wrong, and
this failure is the most instructive of the three because **the fix is not a better standard
error.**

The pooled regression treated 12 names on the same day as 12 observations. §7 showed that
$\approx 42\%$ of panel variance is one common factor: on a day the market falls 2%, essentially
all 12 residuals are negative together. Twelve names on one day therefore carry far less than
twelve observations' worth of information about a common effect.

Standard theory quantifies it. If $n$ observations each have pairwise correlation $\rho$, the
variance of their mean is inflated by $1+(n-1)\rho$, so the effective count is

$$n_\text{eff} = \frac{n}{1 + (n-1)\rho}.$$

With $N = 12$ and $\rho \approx 0.5$, twelve names collapse to about **two** independent
observations. Combine that with the time overlap and the analyst's 30,000 rows are worth a few
hundred.

**Why Newey–West cannot rescue this.** HAC models correlation *along the time axis*. This
correlation is *across names at the same instant* — a direction HAC never looks in. Applying a
more sophisticated time-series correction to a cross-sectional problem is precision aimed at the
wrong dimension, and you can watch it fail below.

The real fix is to change **the unit of observation**. If the dependence is *within* a day, then
stop pretending a name-day is an observation and make **the day** the observation: collapse the
12 names into the one number you actually care about — the return of the portfolio the signal
implies. That is a research decision, not an econometric patch, and it is what §10 does.
""")

code(r"""
# WORKED — measure the cross-sectional dependence, then watch HAC fail to fix it.
resid_mat = resid.reshape(N_DAYS - H_NAIVE, N_NAMES)
rc = np.corrcoef(resid_mat.T)
rho_bar = float(rc[~np.eye(N_NAMES, dtype=bool)].mean())

rule("residual correlation ACROSS names on the SAME day")
show(pd.DataFrame(rc[:6, :6], index=TICKERS[:6], columns=TICKERS[:6]))
print(f"\naverage pairwise residual correlation rho = {rho_bar:.3f}")
n_eff_cs = N_NAMES / (1 + (N_NAMES - 1) * rho_bar)
print(f"12 names with rho = {rho_bar:.2f}  ->  n_eff = N / (1 + (N-1)rho) = {n_eff_cs:.2f} "
      f"independent observations per day")

rule("the honest arithmetic on the analyst's '30,000 observations'")
n_days_eff = (N_DAYS - H_NAIVE) / inflation ** 2
print(f"  rows in the regression                       {n_pool:>10,}")
print(f"  ...but only {N_DAYS-H_NAIVE:,} distinct days      {N_DAYS-H_NAIVE:>10,}")
print(f"  ...and 5-day overlap cuts days by {inflation**2:.1f}x     {n_days_eff:>10,.0f}")
print(f"  ...and 12 names are worth {n_eff_cs:.1f}              "
      f"{n_days_eff*n_eff_cs:>10,.0f}   <- the real evidence")
print(f"  overstatement factor: {n_pool/(n_days_eff*n_eff_cs):>.0f}x")

rule("cluster-by-day SEs vs HAC: which axis is the problem?")
day_id = np.repeat(np.arange(N_DAYS - H_NAIVE), N_NAMES)
fit_cl = sm.OLS(y_pool, sm.add_constant(x_pool)).fit(cov_type="cluster",
                                                     cov_kwds={"groups": day_id})
comp = pd.DataFrame({
    "SE": [se_classical, se_white, se_nw, fit_cl.bse[1]],
    "t": [t_classical, t_white, t_nw_pool, fit_cl.tvalues[1]],
    "x classical": [1.0, se_white/se_classical, inflation, fit_cl.bse[1]/se_classical],
    "fixes": ["nothing", "unequal variance", "time dependence", "same-day dependence"],
}, index=["classical", "White HC1", f"Newey-West({H_NAIVE})", "cluster by day"])
show(comp)
print("\nEach correction targets a different assumption, and none of them targets ALL of them.")
print("Note especially: HAC and clustering disagree, because they look along different axes.")
""")

code(r"""
# CHECK — cross-sectional dependence is large and is a different axis from HAC's.
assert rho_bar > 0.15, f"residuals must be correlated across names on the same day (got {rho_bar:.3f})"
assert n_eff_cs < 4, f"12 correlated names are worth <4 independent obs (got {n_eff_cs:.2f})"
assert fit_cl.bse[1] > se_classical, "clustering by day must widen the SE"
assert n_pool / (n_days_eff * n_eff_cs) > 20, "the naive row count overstates evidence by >20x"
assert not np.isclose(fit_cl.bse[1], se_nw, rtol=0.05), \
    "HAC and day-clustering must differ - they correct different dependence axes"
print(f"§9d OK — rho={rho_bar:.2f} across names, so 12 names ≈ {n_eff_cs:.1f} observations. "
      f"The 30,000 rows are worth ~{n_days_eff*n_eff_cs:,.0f}.")
print("TAKEAWAY: when dependence is within a day, fix the UNIT OF OBSERVATION, not the SE formula.")
""")

# ======================================================================== §10 the portfolio
md(r"""
## §10 · The right unit of observation — build the portfolio (Units 008 + 009)

The fix follows from the diagnosis. The dependence lives *within* each day, so make **the day**
the observation. For each day, turn the 12 signal values into the book §2 defined and record the
one number that follows: the return that book earned. Twelve years of name-days becomes one clean
daily P&L series.

This is better on three counts, and only the first is statistical:

1. **The dependence is gone by construction.** One observation per day, so no same-day
   correlation to correct.
2. **It measures what we would actually earn.** A pooled slope of 0.0032 is not a business. A
   daily return series has a Sharpe ratio, a drawdown, and a turnover.
3. **It forces the neutrality question into the open.** Building a book makes you decide, in code,
   what exposures you are removing.

### Estimating beta — and being honest that it is estimated

To neutralize the market we need each name's beta. In §4 the simulator *knew* the true betas; a
researcher does not. So we estimate them the way Unit 009 says: regress each name's return on the
market proxy over a **trailing 252-day window**, using only data available at the time.

$$\hat\beta_{i,t} \;=\; \frac{\widehat{\text{Cov}}_t(r_i,\,r_\text{mkt})}{\widehat{\text{Var}}_t(r_\text{mkt})}$$

Then neutralize with §7's projection, using $\hat\beta$ in place of $b$.

And here is the second-order consequence that separates a careful researcher from a careless one.
$\hat\beta$ is an **estimator**, so it carries error (Unit 006). Neutralizing against an estimate
makes the book *neutral in expectation*, not neutral in realization. Below we will find a small
but **statistically significant residual market exposure** — an exposure we explicitly tried to
remove and did not fully. It survives because estimation error does not vanish just because you
took the right action. Anyone who claims their book is exactly market-neutral has not measured it.

Note also the cost of estimation: the first year of data is consumed producing the first
$\hat\beta$, so the tradable record is nine years, not ten. That is Unit 006's bias–variance
trade-off in calendar form — a longer window gives a steadier beta but a staler one, and burns
more history.
""")

code(r"""
# WORKED — causal rolling betas, then the neutralized dollar-neutral book for each signal.
market_proxy = rets.mean(axis=1)                                  # the equal-weight index (Section 7: ~PC1)
cov_roll = rets.rolling(WIN).cov(market_proxy)
var_roll = market_proxy.rolling(WIN).var()
beta_hat = cov_roll.div(var_roll, axis=0)                    # uses data up to and including day t

rule(f"estimated betas ({WIN}-day trailing window) vs the truth the simulator used")
show(pd.DataFrame({
    "true beta": beta_true,
    "mean beta_hat": beta_hat.mean().values,
    "sd of beta_hat over time": beta_hat.std().values,
    "mean abs error": (beta_hat - beta_true).abs().mean().values,
}, index=TICKERS))
print(f"\nfirst usable day = index {int(beta_hat.notna().all(axis=1).values.argmax())} "
      f"-> we sacrifice year 1 to estimate betas, leaving "
      f"{(N_DAYS-WIN)/TRADING_DAYS:.1f} tradable years")
print(f"typical |beta_hat - beta| = {(beta_hat - beta_true).abs().mean().mean():.3f} "
      f"-> neutralization will be imperfect. That is Unit 006, not a bug.")

def build_book(sig, start=WIN):
    '''signal -> dollar-neutral, beta-neutral, gross-1 weights -> next-day book return.'''
    z   = sig - sig.mean(axis=1, keepdims=True)               # Section 2: strip the market call
    b   = np.nan_to_num(beta_hat.values, nan=1.0)
    bc  = b - b.mean(axis=1, keepdims=True)                   # Section 7: demean beta FIRST, so
    den = np.sum(bc * bc, axis=1)                             # that this keeps BOTH neutralities
    den = np.where(den > 0, den, 1.0)     # days before beta exists have bc == 0; we drop them below
    z   = z - (np.sum(z * bc, axis=1) / den)[:, None] * bc
    w = z / np.abs(z).sum(1, keepdims=True)                   # Section 2: gross = 1
    return (w[start:-1] * R[start+1:]).sum(1), w[start:]

pnl, weights = build_book(signals["rev5"])
pnl = pd.Series(pnl, index=dates[WIN+1:], name="rev5")
turnover = float(np.abs(np.diff(weights, axis=0)).sum(1).mean())

rule("the book's exposures, verified rather than asserted")
gross_v, net_v = np.abs(weights).sum(1), weights.sum(1)
book_beta_true = weights @ beta_true
print(f"gross exposure : mean {gross_v.mean():.6f}  (target 1)")
print(f"net exposure   : mean {net_v.mean():+.2e}   max |net| {np.abs(net_v).max():.2e}   (target 0)")
print(f"beta vs beta_HAT: mean {np.nanmean(np.sum(weights*np.nan_to_num(beta_hat.values[WIN:],nan=1.0),1)):+.2e}"
      f"   <- zero by construction")
print(f"beta vs TRUE beta: mean {book_beta_true.mean():+.4f}  sd {book_beta_true.std():.4f}"
      f"   <- NOT zero: beta_hat has error")

rule("did we actually hedge the market? (regress the book on the market)")
fb = sm.OLS(pnl.values, sm.add_constant(market_proxy.values[WIN+1:])).fit()
fb_hac = fb.get_robustcov_results(cov_type="HAC", maxlags=10, use_correction=True)
print(f"  book return = alpha + beta * market")
print(f"  residual market beta = {fb.params[1]:+.4f}  (HAC t = {fb_hac.tvalues[1]:+.2f})")
print(f"  corr(book, market)   = {np.corrcoef(pnl.values, market_proxy.values[WIN+1:])[0,1]:+.3f}")
print(f"  corr(book, TRUE market factor) = "
      f"{np.corrcoef(pnl.values, r_market_factor[WIN+1:])[0,1]:+.3f}   <- near zero: the hedge works")
print(f"  R^2 of the market on our book = {fb.rsquared:.4f} -> "
      f"{fb.rsquared:.1%} of book variance is market. Small, real, and worth reporting.")

rule("the book, described")
print(f"  observations   : {len(pnl):,} days ({len(pnl)/TRADING_DAYS:.1f} years), one per day")
print(f"  daily mean     : {pnl.mean()*1e4:+.2f} bp     annualized {pnl.mean()*TRADING_DAYS:+.2%}")
print(f"  daily vol      : {pnl.std()*1e4:.2f} bp      annualized {pnl.std()*np.sqrt(252):.2%}")
print(f"  daily turnover : {turnover:.1%} of gross  -> we replace the book every "
      f"{1/turnover:.1f} days")
print(f"  autocorr(1) of the P&L = {acf(pnl.values,1):+.4f}  <- near zero, unlike the pooled residuals")
""")

code(r"""
# CHECK — the book is what we said it is, including the honest caveat about beta_hat.
assert len(pnl) == N_DAYS - WIN - 1, "we lose the first year to beta estimation"
assert np.allclose(gross_v, 1.0), "gross exposure is exactly 1 every day"
assert np.abs(net_v).max() < 1e-12, "dollar-neutral every day"
assert abs(np.corrcoef(pnl.values, r_market_factor[WIN+1:])[0, 1]) < 0.12, \
    "exposure to the TRUE market factor should be nearly eliminated"
assert abs(fb.params[1]) < 0.30, "residual beta on the observable proxy is small..."
assert abs(fb_hac.tvalues[1]) > 2, "...but statistically real, because beta_hat is an estimate"
assert abs(acf(pnl.values, 1)) < 0.10, "the daily P&L has little autocorrelation - one obs per day"
assert turnover > 0.30, "a 5-day reversal signal must trade a lot; this drives Section 12"
print(f"§10 OK — {len(pnl):,} daily observations, gross 1.00, net 0.00, "
      f"residual market beta {fb.params[1]:+.3f} (t={fb_hac.tvalues[1]:+.1f}).")
print("TAKEAWAY: neutral-in-expectation is not neutral-in-realization. Measure the hedge; report it.")
""")

# ======================================================================== §11 estimation
md(r"""
## §11 · How good is it, and how sure are we? (Unit 006)

We have a nine-year daily P&L. Now Unit 006's vocabulary, which exists precisely to stop you from
confusing a number with the truth:

- The **estimand** is what we want to know: the strategy's *true* long-run Sharpe ratio. We will
  never observe it.
- The **estimator** is the recipe: $\widehat{SR} = \bar r / s_r \times \sqrt{252}$.
- The **estimate** is the number this particular history produced. A different decade gives a
  different number.

The gap between the second and third is the entire subject. A Sharpe ratio without an error bar is
not a result, it is a rumour.

**Why $\sqrt{252}$?** The Sharpe ratio is quoted annually by convention. Mean return scales with
$h$; volatility scales with $\sqrt h$ (Unit 004, verified in §5). So the ratio scales with
$h/\sqrt h = \sqrt h$. This rests on returns being serially uncorrelated — which §10 checked
before using the rule, rather than after.

**Three error bars, deliberately.** Unit 006 gave a formula and a computational alternative, and
comparing them is how you find out whether your assumptions matter:

1. **The Lo (2002) analytic SE**, which corrects for the skew and kurtosis §5 found:
   $\text{SE}(\widehat{SR}) \approx \sqrt{\big(1 + \tfrac12 SR^2 - \gamma_1 SR + \tfrac{\gamma_2-3}{4}SR^2\big)/n}$.
   Note it *needs* the higher moments — the naïve $\sqrt{(1+SR^2/2)/n}$ assumes normality and is
   therefore optimistic on fat-tailed data.
2. **The i.i.d. bootstrap.** Resample days with replacement, recompute the Sharpe thousands of
   times, and read the percentiles off the resulting distribution. No formula, no distributional
   assumption — but it *does* assume independence, since it shuffles days freely.
3. **The block bootstrap.** Resample contiguous 21-day *blocks* instead of individual days, which
   preserves volatility clustering. This is the honest version whenever observations are dependent.

If the block interval is much wider than the i.i.d. one, dependence is materially hurting your
precision. If they agree, you have *earned* the right to use the simple version — and it is worth
noticing that we would not know which case we were in without checking.
""")

code(r"""
# WORKED — the Sharpe ratio as an estimator, with three independent error bars.
n_obs = len(pnl)
sr_daily = pnl.mean() / pnl.std()
sr_ann = sr_daily * np.sqrt(TRADING_DAYS)
skew_p, kurt_p = stats.skew(pnl), stats.kurtosis(pnl, fisher=False)

rule("estimand, estimator, estimate")
print(f"  estimand : the TRUE long-run Sharpe ratio of this strategy   (unobservable)")
print(f"  estimator: mean/sd * sqrt(252)")
print(f"  estimate : {sr_ann:.3f}   from {n_obs:,} days = {n_obs/TRADING_DAYS:.1f} years")
print(f"\n  ann return {pnl.mean()*TRADING_DAYS:+.2%}  /  ann vol "
      f"{pnl.std()*np.sqrt(TRADING_DAYS):.2%}  =  {sr_ann:.2f}")
print(f"  the sqrt(252) rule is legitimate here because autocorr(P&L) = {acf(pnl.values,1):+.3f} ~ 0")

rule("error bar 1 - the Lo (2002) analytic SE, with and without the fat-tail correction")
se_naive = np.sqrt((1 + 0.5 * sr_daily**2) / n_obs) * np.sqrt(TRADING_DAYS)
se_lo = np.sqrt((1 + 0.5*sr_daily**2 - skew_p*sr_daily
                 + (kurt_p - 3)/4 * sr_daily**2) / n_obs) * np.sqrt(TRADING_DAYS)
print(f"  skew = {skew_p:+.3f}, kurtosis = {kurt_p:.2f} (normal = 3)")
print(f"  SE assuming normality : {se_naive:.4f}  ->  95% CI "
      f"[{sr_ann-1.96*se_naive:.2f}, {sr_ann+1.96*se_naive:.2f}]")
print(f"  SE with Lo correction : {se_lo:.4f}  ->  95% CI "
      f"[{sr_ann-1.96*se_lo:.2f}, {sr_ann+1.96*se_lo:.2f}]")

rule("error bars 2 & 3 - i.i.d. bootstrap vs block bootstrap (4,000 resamples each)")
rng = np.random.default_rng(7)
v = pnl.values
B, BLOCK = 4000, 21
boot_iid = np.empty(B); boot_blk = np.empty(B)
n_blocks = n_obs // BLOCK
for i in range(B):
    s1 = v[rng.integers(0, n_obs, n_obs)]                       # shuffle days: assumes independence
    boot_iid[i] = s1.mean() / s1.std() * np.sqrt(TRADING_DAYS)
    starts = rng.integers(0, n_obs - BLOCK, n_blocks)           # keep 21-day blocks intact
    s2 = np.concatenate([v[j:j+BLOCK] for j in starts])
    boot_blk[i] = s2.mean() / s2.std() * np.sqrt(TRADING_DAYS)

ci = pd.DataFrame({
    "SE": [se_naive, se_lo, boot_iid.std(), boot_blk.std()],
    "CI low":  [sr_ann-1.96*se_naive, sr_ann-1.96*se_lo,
                np.quantile(boot_iid, .025), np.quantile(boot_blk, .025)],
    "CI high": [sr_ann+1.96*se_naive, sr_ann+1.96*se_lo,
                np.quantile(boot_iid, .975), np.quantile(boot_blk, .975)],
    "assumes": ["normal iid returns", "iid returns, any moments",
                "independence (shuffles days)", f"only {BLOCK}-day local dependence"],
}, index=["analytic (normal)", "analytic (Lo)", "bootstrap iid", f"bootstrap block({BLOCK})"])
ci["width"] = ci["CI high"] - ci["CI low"]
show(ci)
print(f"\nblock CI is {ci.width.iloc[3]/ci.width.iloc[2]:.2f}x the width of the i.i.d. CI.")
print("They nearly agree - which is EVIDENCE, not luck: Section 10 built a book whose daily P&L")
print("is close to serially independent, so shuffling days is defensible HERE. On the overlapping")
print("pooled regression of Section 9 it would not have been.")

rule("what the interval means for the decision")
lo_b, hi_b = np.quantile(boot_blk, .025), np.quantile(boot_blk, .975)
print(f"  point estimate {sr_ann:.2f}, but the data only pins it to [{lo_b:.2f}, {hi_b:.2f}]")
print(f"  P(true Sharpe < 0.5 | this sample) ~ {np.mean(boot_blk < 0.5):.1%}")
print(f"  the CI excludes zero -> there IS something here (Section 12 asks if it survives costs)")
print(f"  reporting '{sr_ann:.2f}' with no interval would overstate what 9 years can establish.")
""")

code(r"""
# CHECK — the Sharpe estimate, its error bars, and the agreement between methods.
assert 0.6 < sr_ann < 1.8, f"gross Sharpe should be plausible for a real edge (got {sr_ann:.2f})"
assert se_lo > 0 and se_naive > 0
assert np.isclose(boot_iid.mean(), sr_ann, atol=4 * boot_iid.std()), "bootstrap should centre on the estimate"
assert abs(boot_iid.std() - se_lo) < 0.5 * se_lo, "bootstrap SE and the Lo formula should broadly agree"
assert ci.width.iloc[3] > 0.9 * ci.width.iloc[2], "the block CI must not be NARROWER than iid by much"
assert lo_b > 0, "the 95% interval should exclude zero - this signal is not nothing"
assert hi_b - lo_b > 0.4, "9 years cannot pin a Sharpe ratio tightly; the interval must be wide"
print(f"§11 OK — Sharpe {sr_ann:.2f}, 95% block-bootstrap CI [{lo_b:.2f}, {hi_b:.2f}].")
print("TAKEAWAY: report the interval. 9 years of daily data locates a Sharpe to about +/-0.4.")
""")

# ======================================================================== §12 multiple testing
md(r"""
## §12 · But we tested twelve — the multiple-testing correction (Unit 007)

One thing remains, and it is the step that separates research from data mining. The Sharpe ratio
and its interval in §11 are the right answer to the question *"given that I test this one signal,
is it real?"* That is not the question. We tested **twelve**, and we are talking about the winner.

### The $t$-statistic *is* the Sharpe ratio

First, a connection worth internalizing. For a mean-zero null,
$t = \bar r/(s_r/\sqrt n) = \widehat{SR}_\text{daily}\sqrt{n}$, and since
$\widehat{SR}_\text{ann} = \widehat{SR}_\text{daily}\sqrt{252}$,

$$t \;=\; \widehat{SR}_\text{ann}\,\sqrt{\text{years}}.$$

A Sharpe of 1.0 over 4 years is $t = 2$. A Sharpe of 0.5 needs **16 years** to reach the same
$t$. This one identity explains why long track records are worth so much and why a two-year
backtest establishes almost nothing.

### Why finance breaks classical testing

A 5% significance level means a 5% chance of a false positive *per test*. Run $M$ independent
tests on pure noise and the probability of at least one false positive — the **family-wise error
rate** — is $1-(1-\alpha)^M$. At $M=12$ that is already 46%. At $M=100$ it is 99.4%. Since a real
desk tries hundreds of variations, "we found something significant" is the *expected* outcome of
searching, whether or not anything is there.

Three responses, and it matters that they answer different questions:

- **Bonferroni** controls the FWER by testing each signal at $\alpha/M$. It answers "am I sure
  about *every* rejection?" It is conservative by design, and on correlated tests it is
  over-conservative.
- **Benjamini–Hochberg** controls the **false discovery rate** — the expected *share* of your
  rejections that are wrong. It answers "of the signals I take forward, what fraction are junk?",
  which is the more natural question for a research pipeline that can afford some misses. Because
  it buys power by tolerating some false positives, BH is **always at least as permissive as
  Bonferroni**: its survivor set is a superset.
- **The empirical best-of-$M$ null** is the most honest and the least clever: simulate the entire
  search under no edge, and ask how often pure noise produces a winner as good as ours. It needs
  no distributional assumption and automatically accounts for the *whole procedure*.

**Expect the two corrections to disagree here, and do not treat that as a bug.** Our best decoy
lands just under the Bonferroni bar, so Bonferroni kills it and BH lets it through. That is not one
method being wrong; it is the two methods answering different questions. "5% FDR" *means* roughly
one in twenty of your discoveries is false — so BH admitting a decoy is BH working as designed. Which
one you should use depends on the cost of being wrong, and for committing capital to a strategy we
want the conservative answer.

One subtlety on the last one. The expected maximum of $M$ standard normals is about 1.63 for
$M=12$ — but we are running **two-sided** tests, so the relevant bar is the expected maximum of
$M$ *absolute* values, which is higher. Getting this wrong understates the bar you must clear, so
we compute both.
""")

code(r"""
# WORKED — run the honest portfolio test on ALL twelve, then correct for having run twelve.
rule("every candidate, evaluated the Section-10 way (one observation per day)")
rows = []
for s in SIGNAL_NAMES:
    p_s, w_s = build_book(signals[s])
    f_s = sm.OLS(p_s, np.ones(len(p_s))).fit()
    f_hac = f_s.get_robustcov_results(cov_type="HAC", maxlags=10, use_correction=True)
    rows.append({"signal": s,
                 "SR": p_s.mean() / p_s.std() * np.sqrt(TRADING_DAYS),
                 "t_HAC": f_hac.tvalues[0],
                 "turnover": float(np.abs(np.diff(w_s, axis=0)).sum(1).mean()),
                 "t_naive_pooled": screen.t_naive[s]})
res = pd.DataFrame(rows).set_index("signal")
res["p_two_sided"] = 2 * stats.norm.sf(res.t_HAC.abs())
res = res.reindex(res.t_HAC.abs().sort_values(ascending=False).index)
show(res)

alpha_lvl = 0.05
bonf_p = alpha_lvl / M
bonf_t = stats.norm.isf(bonf_p / 2)
print(f"\nuncorrected bar |t| > {stats.norm.isf(alpha_lvl/2):.2f}: "
      f"{int((res.p_two_sided < alpha_lvl).sum())} signals pass "
      f"-> {', '.join(res.index[res.p_two_sided < alpha_lvl])}")
print(f"FWER if we ignore the search: 1 - 0.95^{M} = {1-(1-alpha_lvl)**M:.1%} chance of >=1 false find")

rule("correction I - Bonferroni (controls the family-wise error rate)")
print(f"  per-test level alpha/M = {alpha_lvl}/{M} = {bonf_p:.5f}  ->  bar |t| > {bonf_t:.2f}")
surv_bonf = list(res.index[res.p_two_sided < bonf_p])
for s in res.index[:5]:
    print(f"    {s:12s} |t| = {abs(res.t_HAC[s]):>5.2f}  p = {res.p_two_sided[s]:.2e}  "
          f"{'SURVIVES' if res.p_two_sided[s] < bonf_p else 'rejected'}")
print(f"  survivors: {surv_bonf}")

rule("correction II - Benjamini-Hochberg (controls the false discovery rate)")
p_sorted = res.p_two_sided.sort_values()
bh = pd.DataFrame({"p": p_sorted,
                   "rank": np.arange(1, M + 1),
                   "BH threshold": np.arange(1, M + 1) / M * alpha_lvl})
bh["passes"] = bh.p <= bh["BH threshold"]
show(bh)
k_bh = int(np.where(bh.passes.values)[0].max() + 1) if bh.passes.any() else 0
surv_bh = list(bh.index[:k_bh])
print(f"  largest rank with p <= (rank/M)*alpha is {k_bh}  ->  survivors: {surv_bh}")
bh_extra = [s for s in surv_bh if s not in surv_bonf]
if bh_extra:
    print(f"  NOTE: BH also admits {bh_extra} — which we know are decoys. This is not a failure of")
    print(f"  BH; controlling FDR at {alpha_lvl:.0%} MEANS accepting that ~1 in 20 discoveries is")
    print(f"  false. BH bought power (a lower bar) by selling certainty. Bonferroni made the")
    print(f"  opposite trade and got the right answer here.")
    print(f"  Decision rule: to COMMIT CAPITAL, use the conservative bar. To pick what to RESEARCH")
    print(f"  next, BH's list is the more useful one.")

rule("correction III - the empirical best-of-M null (the decisive test)")
def expected_max_abs_normal(m):
    f = lambda z: z * m * 2 * stats.norm.pdf(z) * (2 * stats.norm.cdf(z) - 1) ** (m - 1)
    return integrate.quad(f, 0, 12, limit=300)[0]

emax_signed = integrate.quad(
    lambda z: z * M * stats.norm.pdf(z) * stats.norm.cdf(z) ** (M - 1), -8, 10)[0]
emax_abs = expected_max_abs_normal(M)
print(f"  E[max of {M} signed z] = {emax_signed:.2f}   (the wrong bar for a two-sided test)")
print(f"  E[max of {M} |z|]      = {emax_abs:.2f}   (the right one)")
print(f"  (Yes, {emax_abs:.2f} is almost exactly the familiar 1.96. That is a COINCIDENCE at M={M},")
print(f"   not the same quantity: 1.96 is a 5% critical value for ONE test, while {emax_abs:.2f} is the")
print(f"   AVERAGE best-of-{M} score under no edge. They part company fast - see M=200 below.)")

rng2 = np.random.default_rng(5)
NREP = 3000
best_null = np.empty(NREP)
for i in range(NREP):                       # M zero-edge books of the same length and vol
    draws = rng2.normal(0, pnl.std(), size=(M, n_obs))
    t_null = draws.mean(1) / (draws.std(1) / np.sqrt(n_obs))
    best_null[i] = np.abs(t_null).max()
t_win = abs(res.t_HAC.iloc[0])
p_mc = (np.sum(best_null >= t_win) + 1) / (NREP + 1)
print(f"  simulated null best-of-{M} |t|: mean {best_null.mean():.2f}, "
      f"95th pct {np.quantile(best_null,0.95):.2f}, max {best_null.max():.2f}")
print(f"  our winner ({res.index[0]}) scored |t| = {t_win:.2f}")
print(f"  empirical p-value for the WHOLE SEARCH = {p_mc:.4f}")
print(f"  -> a search over 12 zero-edge signals produces a winner this good "
      f"{p_mc:.1%} of the time.")

rule("the haircut: what is left after paying for the search")
sr_haircut = res.SR.iloc[0] * max(t_win - emax_abs, 0) / t_win
print(f"  reported Sharpe                          {res.SR.iloc[0]:.2f}")
print(f"  t after the best-of-M bar: {t_win:.2f} - {emax_abs:.2f} = {t_win-emax_abs:.2f}")
print(f"  haircut Sharpe (scaled by the surviving t) {sr_haircut:.2f}")
print(f"  Harvey-Liu-Zhu: with hundreds of trials the bar rises further - "
      f"E[max of 200 |z|] = {expected_max_abs_normal(200):.2f}")
""")

code(r"""
# CHECK — the correction admits exactly the real signal and rejects the eleven decoys.
uncorrected = list(res.index[res.p_two_sided < alpha_lvl])
assert len(uncorrected) >= 2, "at |t|>1.96 some noise sneaks through - that is the whole problem"
assert "rev5" == res.index[0], "the honest test should rank the genuinely real signal first"
assert surv_bonf == ["rev5"], f"Bonferroni must leave exactly the real signal, got {surv_bonf}"
assert "rev5" in surv_bh, "BH must also find the real signal"
assert set(surv_bonf) <= set(surv_bh), "BH is always at least as permissive as Bonferroni"
assert len(surv_bh) > len(surv_bonf), \
    "here BH admits a decoy too - that is FDR control working as designed, not a bug"
assert t_win > bonf_t, "rev5 clears even the conservative Bonferroni bar"
assert p_mc < 0.05, f"the empirical best-of-M p-value must reject the null (got {p_mc:.4f})"
assert emax_abs > emax_signed, "the two-sided bar is strictly higher than the one-sided one"
assert 0 < sr_haircut < res.SR.iloc[0], "the haircut must reduce, but not erase, the Sharpe"
# and the decoys that looked good in the naive screen are now dead
assert all(abs(res.t_HAC[s]) < bonf_t for s in res.index if s != "rev5"), \
    "no decoy may clear the corrected bar"
print(f"§12 OK — of {M} candidates and {len(uncorrected)} nominally significant ones, "
      f"{surv_bonf} survives correction (best-of-M p = {p_mc:.4f}).")
print("TAKEAWAY: t = SR x sqrt(years), and the bar is E[max of M], never 1.96.")
""")

md(r"""
### Power, and the minimum track length you need

The mirror image of a false positive is a false negative, and Unit 007's **power** is the
probability of detecting an edge that is genuinely there. Inverting $t = SR\sqrt{\text{years}}$
gives the most useful back-of-envelope in quantitative finance:

$$\text{years needed for } t = 2 \;=\; \left(\frac{2}{SR}\right)^2.$$

Read the consequences and let them recalibrate your expectations:

- $SR = 2.0$ → 1 year. (If you see this claimed, suspect leakage first.)
- $SR = 1.0$ → 4 years.
- $SR = 0.5$ → **16 years** — longer than most datasets and most careers.
- And with a Bonferroni bar of $t > 2.87$ instead of 2, multiply all of it by $(2.87/2)^2 \approx 2$.

Two conclusions follow. First, **most true edges are undetectable** with available history; the
field is not short of ideas, it is short of statistical power. Second — the reason §10 mattered —
the only lever you control is $\sigma$. Hedging out the market raised $SR$ by shrinking the
denominator, which bought years of equivalent data for free. That is why neutralization is
statistical machinery, not window dressing.
""")

code(r"""
# WORKED — power, minimum track length, and where our result sits.
rule("years of daily data needed to reach a given t, by true Sharpe")
print(f"{'true SR':>9} {'t=1.96 (naive)':>16} {'t=2.87 (Bonferroni, M=12)':>28}")
for target in (0.25, 0.5, 0.8, 1.0, 1.5, 2.0):
    print(f"{target:>9.2f} {(1.96/target)**2:>15.1f}y {(bonf_t/target)**2:>27.1f}y")

rule("power: if the true Sharpe really is what we measured, how often would we catch it?")
years = n_obs / TRADING_DAYS
for true_sr in (0.3, 0.5, sr_ann, 1.5):
    ncp = true_sr * np.sqrt(years)                       # non-centrality = expected t
    pw_naive = stats.norm.sf(1.96 - ncp) + stats.norm.cdf(-1.96 - ncp)
    pw_bonf = stats.norm.sf(bonf_t - ncp) + stats.norm.cdf(-bonf_t - ncp)
    print(f"  true SR {true_sr:>4.2f} over {years:.1f}y -> expected t = {ncp:>4.2f}, "
          f"power {pw_naive:>5.1%} at 1.96, {pw_bonf:>5.1%} at {bonf_t:.2f}")

rule("where our winner sits")
print(f"  measured SR {sr_ann:.2f} over {years:.1f} years  ->  t = SR*sqrt(years) = "
      f"{sr_ann*np.sqrt(years):.2f}  (HAC t was {t_win:.2f})")
print(f"  minimum track length for this SR at the Bonferroni bar: "
      f"{(bonf_t/sr_ann)**2:.1f} years; we have {years:.1f}. Enough, but not comfortably.")
print(f"\n  Had the true Sharpe been 0.5, this same 9-year sample would have found it only "
      f"{stats.norm.sf(bonf_t - 0.5*np.sqrt(years)):.0%} of the time.")
print("  Most real edges are simply too small to prove. That is the honest state of the field.")
""")

code(r"""
# CHECK — the power arithmetic and the t = SR*sqrt(years) identity.
assert np.isclose(sr_ann * np.sqrt(years), pnl.mean() / (pnl.std() / np.sqrt(n_obs)), rtol=0.02), \
    "t = SR_annual * sqrt(years) is an identity, not an approximation"
assert (1.96 / 0.5) ** 2 > 15, "a Sharpe of 0.5 needs >15 years to reach t=2"
assert (bonf_t / sr_ann) ** 2 < years, "our sample IS long enough for the Sharpe we measured"
assert stats.norm.sf(bonf_t - 0.5 * np.sqrt(years)) < 0.5, \
    "a Sharpe-0.5 edge would be missed more often than caught in 9 years"
print(f"§12b OK — t = {sr_ann:.2f} x sqrt({years:.1f}) = {sr_ann*np.sqrt(years):.2f}; "
      f"a Sharpe of 0.5 would need {(bonf_t/0.5)**2:.0f} years.")
print("TAKEAWAY: power, not ideas, is the binding constraint. Reduce sigma to buy years.")
""")

# ======================================================================== §13 costs
md(r"""
## §13 · Net of costs — does it survive contact with the market? (Units 003 + 001)

The signal is real and we have measured it honestly. That is *still* not a business, because
everything so far assumed free trading. §3 built the cost function; now spend it.

The arithmetic is short and brutal. §10's book has a daily turnover around two-thirds of gross, so
we replace essentially the whole portfolio every 1.5 days — which is inherent to a 5-day reversal
signal, not a flaw in the implementation. Each unit of turnover pays the half-spread plus impact,
so daily cost as a fraction of capital is

$$\text{cost}_\text{daily} = \text{turnover} \times \big(\text{half-spread} + Y\sigma\sqrt{Q/V}\big).$$

Two things follow, and together they are Unit 001's alpha-decay lesson made quantitative.

**Costs subtract from the numerator only.** Trading costs reduce return without reducing
volatility, so the Sharpe ratio falls linearly in cost: $SR_\text{net} = (\mu - c)/\sigma$. There
is no diversification benefit to costs.

**Capacity is where the curve crosses zero.** The half-spread is fixed per unit turnover, but
impact grows with $\sqrt{\text{AUM}}$. So net Sharpe declines monotonically with size and
eventually goes negative. The AUM at which that happens is the strategy's **capacity**, and it is
as much a part of the result as the Sharpe ratio. A Sharpe of 1.2 that holds \$10M and a Sharpe of
0.4 that holds \$2B are not comparable products.

This is also the mechanism behind alpha decay. As capital crowds into a known signal, the marginal
dollar pays more impact and earns less edge, until net alpha is competed to zero. Nothing needs to
"stop working" for a strategy to die — enough people finding it is sufficient.
""")

code(r"""
# WORKED — the capacity curve: net Sharpe as a function of AUM.
rule("cost per unit of turnover, and the resulting capacity curve")
print(f"turnover = {turnover:.1%} of gross per day  ->  full portfolio replaced every "
      f"{1/turnover:.1f} days")
print(f"gross (pre-cost) Sharpe = {sr_ann:.2f}, gross ann return = {pnl.mean()*TRADING_DAYS:.2%}\n")

cap = []
for aum in (2e6, 5e6, 10e6, 25e6, 50e6, 100e6, 250e6, 500e6, 1e9):
    per_name_trade = turnover * aum / N_NAMES            # gross = 1x AUM, spread over 12 names
    cost_bp, impact_bp, part = trade_cost_bp(per_name_trade)
    daily_cost = turnover * cost_bp / 1e4
    net_sr = (pnl.mean() - daily_cost) / pnl.std() * np.sqrt(TRADING_DAYS)
    cap.append({"AUM $M": aum/1e6, "traded/day $M": turnover*aum/1e6,
                "% of ADV": part, "impact bp": impact_bp, "cost bp": cost_bp,
                "cost %/yr": daily_cost * TRADING_DAYS,
                "net ann ret": (pnl.mean()-daily_cost)*TRADING_DAYS, "net SR": net_sr})
cap = pd.DataFrame(cap).set_index("AUM $M")
show(cap)

viable = cap[cap["net SR"] > 0.5]
breakeven = cap[cap["net SR"] > 0]
rule("reading the curve")
print(f"gross Sharpe                       {sr_ann:.2f}")
print(f"net Sharpe at $25M                 {cap.loc[25.0, 'net SR']:.2f}   "
      f"(costs eat {1 - cap.loc[25.0,'net SR']/sr_ann:.0%} of it)")
print(f"largest AUM with net Sharpe > 0.5  ${viable.index.max():.0f}M   <- the practical capacity")
print(f"largest AUM with net Sharpe > 0    ${breakeven.index.max():.0f}M   <- where the edge dies")
print(f"\nCosts do not scale the Sharpe down uniformly: they subtract from the NUMERATOR, so")
print(f"the decay accelerates as impact grows with sqrt(AUM).")

rule("the honest equity curve at $25M, net of all costs")
aum_run = 25e6
c_bp, _, _ = trade_cost_bp(turnover * aum_run / N_NAMES)
net_daily = pnl - turnover * c_bp / 1e4
equity = (1 + net_daily).cumprod()
dd = equity / equity.cummax() - 1
print(f"  total net return  {equity.iloc[-1]-1:+.1%} over {years:.1f} years  "
      f"(CAGR {equity.iloc[-1]**(1/years)-1:+.2%})")
print(f"  net Sharpe        {net_daily.mean()/net_daily.std()*np.sqrt(252):.2f}")
print(f"  max drawdown      {dd.min():.1%}   ({int((dd < -0.05).sum())} of {len(dd):,} days spent "
      f"more than 5% below the previous peak)")
print(f"  worst single day  {net_daily.min():.2%}   best {net_daily.max():+.2%}")
print(f"  % of days positive {(net_daily > 0).mean():.1%}   <- alpha is a thin, noisy edge")
by_year = net_daily.groupby(net_daily.index.year)
yearly = pd.DataFrame({"days": by_year.size(),
                       "ret": by_year.apply(lambda s: (1 + s).prod() - 1),
                       "vol": by_year.std() * np.sqrt(TRADING_DAYS),
                       "SR":  by_year.apply(lambda s: s.mean() / s.std()
                                            * np.sqrt(TRADING_DAYS))})
yearly.index.name = "year"
yearly = yearly[yearly.days >= 150]   # drop stub years: an annualized SR from a few days is noise
print("\nby calendar year (note how much a single year's Sharpe varies - that is Section 11's CI):")
show(yearly)
""")

code(r"""
# CHECK — costs bite, monotonically, and capacity is finite.
assert cap["net SR"].is_monotonic_decreasing, "net Sharpe must fall as AUM rises (impact grows)"
assert cap["net SR"].iloc[0] < sr_ann, "even the smallest book pays the spread"
assert cap["net SR"].iloc[-1] < 0, "at some size the edge must die - capacity is finite"
assert breakeven.index.max() < 1000, "breakeven capacity should be inside the range we scanned"
assert net_daily.mean() > 0, "at $25M the strategy is still net profitable"
assert dd.min() < -0.05, "a real 9-year equity curve has meaningful drawdowns"
assert 0.45 < (net_daily > 0).mean() < 0.60, "a genuine edge wins barely more than half the days"
assert yearly["SR"].std() > 0.3, "single-year Sharpes scatter widely - hence long samples matter"
print(f"§13 OK — gross SR {sr_ann:.2f} -> net {cap.loc[25.0,'net SR']:.2f} at $25M; "
      f"capacity ~${breakeven.index.max():.0f}M; max DD {dd.min():.0%}.")
print("TAKEAWAY: an edge is not a business until it is net of costs and sized to its capacity.")
""")

md(r"""
### One option, to see non-linearity earn its keep (Unit 002 + Unit 004)

The drawdown above is the fat tail from §5 arriving in P&L form. §2 promised one look at a
non-linear instrument, and this is the natural place: a **protective put** on the market as a tail
hedge.

A put with strike $K$ pays $\max(K - S_T,\,0)$ at expiry — nothing if the market holds up, and
dollar-for-dollar below $K$. Combined with a long position it produces the payoff shape that
defines the instrument's usefulness: **losses are floored, upside is intact, and you pay a premium
for the privilege.** That asymmetry is impossible to build from stock alone at any weight, which
is precisely why options exist.

We only compute the **payoff at expiry**, which needs no theory. What the premium *should* be is a
pricing question, and pricing it is Q2's entire job: Units 011–016 build the machinery (Brownian
motion, Itô, risk-neutral measure) that turns this payoff diagram into the Black–Scholes formula,
and Unit 017 makes it dynamic with the Greeks.
""")

code(r"""
# WORKED — the payoff of a protective put, and what it does to the book's worst days.
S0, K, premium, notional = 100.0, 90.0, 2.40, 1_000_000   # index at 100, 10% OTM put, 2.4% premium
rule("payoff at expiry: long index + long put (strike 90, premium 2.40)")
print(f"{'S_T':>7} {'index P&L':>13} {'put payoff':>13} {'premium':>10} {'net':>13} {'unhedged':>13}")
for ST in (120, 110, 100, 90, 80, 70, 50):
    idx_pnl = (ST - S0) / S0 * notional
    put_pay = max(K - ST, 0.0) / S0 * notional
    net = idx_pnl + put_pay - premium / S0 * notional
    print(f"{ST:>7} {idx_pnl:>13,.0f} {put_pay:>13,.0f} "
          f"{-premium/S0*notional:>10,.0f} {net:>13,.0f} {idx_pnl:>13,.0f}")
floor = (K - S0 - premium) / S0
print(f"\nthe floor: no matter how far the market falls, you lose at most "
      f"(K - S0 - premium)/S0 = {floor:.1%}")
print(f"the cost : you give up {premium/S0:.1%} of every upside scenario")
print("this kink is what a linear instrument cannot reproduce at ANY weight - Q2 prices it.")

rule("why our book might want one: the tail we measured in Section 5")
print(f"  book's worst day        {net_daily.min():.2%}")
print(f"  book's excess kurtosis  {stats.kurtosis(net_daily):.2f}  (Gaussian = 0)")
print(f"  Gaussian 1-in-10y day   {stats.norm.ppf(1/2520, net_daily.mean(), net_daily.std()):.2%}"
      f"  <- what a normal model would have told you to expect")
print(f"  max drawdown            {dd.min():.1%}")
print("  fat tails are not a curiosity; they are the thing that ends funds.")
""")

code(r"""
# CHECK — the put payoff has the shape that defines a non-linear instrument.
assert max(K - 120, 0) == 0 and max(K - 70, 0) == 20, "a put pays only below its strike"
worst_hedged = min((ST - S0 + max(K - ST, 0) - premium) / S0 for ST in range(1, 200))
assert np.isclose(worst_hedged, floor, atol=1e-9), "losses are floored at (K - S0 - premium)/S0"
assert (120 - S0 + 0 - premium) / S0 < (120 - S0) / S0, "the premium costs you upside"
assert floor > -0.20, "a 10% OTM put caps the loss well short of a total wipeout"
assert stats.kurtosis(net_daily) > 0, "the book's own P&L is fat-tailed too"
print(f"§13b OK — the put floors losses at {floor:.1%} in exchange for {premium/S0:.1%} of upside.")
print("TAKEAWAY: non-linear payoffs buy shapes stock cannot. Q2 works out what they should cost.")
""")

# ======================================================================== the memo
md(r"""
## The deliverable — the memo

Research that is not written down did not happen. This is the artefact the whole notebook exists to
produce: what you found, how confident you are, what it holds, and — most importantly — **what
would change your mind.**

Notice what the memo does *not* say. It does not say "we found alpha." It reports an effect with an
interval, a capacity limit, and a list of ways it could still be wrong. That register — confident
about the method, humble about the number — is what a PM is actually buying from a researcher.
""")

code(r"""
# MEMO — the research note. Paste this to your teacher as the exit ticket.
line = "=" * 78
print(line)
print("RESEARCH MEMO - Q1 signal review".center(78))
print(f"universe: {N_NAMES} US large caps | sample: {dates[0].date()} to {dates[-1].date()} "
      f"| author: you".center(78))
print(line)

print("\n1. QUESTION")
print(f"   Is any of {M} candidate signals a tradable, market-neutral edge at ~1-day holding?")

print("\n2. WHAT THE NAIVE SCREEN SAID  (and why we did not believe it)")
print(f"   Pooled OLS, {H_NAIVE}-day overlapping forward returns, {n_pool:,} name-day rows:")
print(f"     {int((screen.p_naive < 0.05).sum())} of {M} signals significant at p<0.05; "
      f"best |t| = {abs(screen.t_naive.iloc[0]):.1f}")
print(f"   Three independent inflations, each measured:")
print(f"     heteroskedasticity  White SE x{se_white/se_classical:.2f}  "
      f"(t {t_classical:+.1f} -> {t_white:+.1f})")
print(f"     {H_NAIVE}-day overlap        HAC SE  x{inflation:.2f}  "
      f"(t {t_white:+.1f} -> {t_nw_pool:+.1f})")
print(f"     cross-sec. dependence  rho={rho_bar:.2f} => 12 names ~ {n_eff_cs:.1f} obs "
      f"(no SE fixes this)")
print(f"   Honest evidence: ~{n_days_eff*n_eff_cs:,.0f} observations, not {n_pool:,} "
      f"({n_pool/(n_days_eff*n_eff_cs):.0f}x overstated).")

print("\n3. METHOD USED INSTEAD")
print(f"   Signal -> cross-sectionally demeaned -> beta-neutralized against a causal {WIN}-day")
print(f"   rolling beta -> gross-1 dollar-neutral book -> ONE daily return per day.")
print(f"   Verified: gross {gross_v.mean():.2f}, net {abs(net_v).max():.0e}, "
      f"corr with true market factor "
      f"{np.corrcoef(pnl.values, r_market_factor[WIN+1:])[0,1]:+.2f}.")
print(f"   Caveat reported, not hidden: residual beta on the observable proxy is "
      f"{fb.params[1]:+.3f} (t={fb_hac.tvalues[1]:+.1f})")
print(f"   because beta_hat is estimated (mean abs error "
      f"{(beta_hat - beta_true).abs().mean().mean():.2f}).")

print("\n4. RESULT")
print(f"   Winner: '{res.index[0]}' - {H_NAIVE}-day cross-sectional reversal.")
print(f"     gross Sharpe        {sr_ann:.2f}   over {years:.1f} years ({n_obs:,} obs)")
print(f"     95% CI (block boot) [{lo_b:.2f}, {hi_b:.2f}]   <- what 9 years can actually pin down")
print(f"     HAC t               {t_win:.2f}")
print(f"     ann return / vol    {pnl.mean()*TRADING_DAYS:.1%} / {pnl.std()*np.sqrt(252):.1%}")
print(f"     daily turnover      {turnover:.0%}")

print("\n5. MULTIPLE-TESTING CORRECTION  (we tested 12; the bar is not 1.96)")
print(f"     uncorrected |t|>1.96      {len(uncorrected)} pass: {', '.join(uncorrected)}")
print(f"     Bonferroni  |t|>{bonf_t:.2f}      {surv_bonf}")
print(f"     Benjamini-Hochberg        {surv_bh}"
      + (f"  <- admits {bh_extra}; FDR trades certainty for power" if bh_extra else ""))
print(f"     empirical best-of-{M} null  p = {p_mc:.4f}  "
      f"(vs E[max|z|] bar of {emax_abs:.2f})")
print(f"     haircut Sharpe            {sr_haircut:.2f}  (after paying for the search)")

print("\n6. NET OF COSTS AND CAPACITY")
print(f"     cost model: {HALF_SPREAD_BP:.0f}bp half-spread + {Y_IMPACT}*sigma*sqrt(Q/ADV), "
      f"ADV ${ADV_DOLLARS/1e6:.0f}M")
print(f"     net Sharpe at  $25M   {cap.loc[25.0,'net SR']:.2f}")
print(f"     net Sharpe at $100M   {cap.loc[100.0,'net SR']:.2f}")
print(f"     capacity (net SR>0.5) ~${viable.index.max():.0f}M     "
      f"breakeven ~${breakeven.index.max():.0f}M")
print(f"     at $25M: net {equity.iloc[-1]-1:+.0%} total, max drawdown {dd.min():.0%}, "
      f"{(net_daily>0).mean():.0%} of days positive")

print("\n7. RECOMMENDATION")
verdict = ("PROCEED TO PAPER TRADING, sized small"
           if (surv_bonf == ["rev5"] and p_mc < 0.05 and cap.loc[25.0, "net SR"] > 0.3)
           else "DO NOT ALLOCATE")
print(f"     {verdict}")
print(f"     One real edge out of {M} candidates. It survives every correction we know how to")
print(f"     apply, but it is capacity-limited and turnover-heavy: this is a "
      f"${viable.index.max():.0f}M sleeve,")
print(f"     not a flagship. The other {M-1} candidates are indistinguishable from noise.")

print("\n8. WHAT WOULD CHANGE MY MIND  (the section that makes this defensible)")
print("     - the CI includes Sharpes near "
      f"{lo_b:.1f}; a bad year is fully consistent with the edge being real")
print("     - costs are modelled, not measured: real fills would settle this")
print("     - 12 names is a thin cross-section; the same test on 500 names is the real test")
print("     - purged/embargoed CV and a deflated Sharpe are NOT yet applied (Year 2 Q2)")
print("     - the residual market beta above says the hedge is imperfect out of sample")
print(line)
""")

# ======================================================================== ledger
md(r"""
## The concept ledger — what each unit actually decided

The point of the walkthrough is that none of these were recited; each one **changed a number or a
decision**. If you can reproduce this table from memory, you own Q1.

| Unit | Concept | The decision it made here |
|------|---------|---------------------------|
| 001 | Alpha ≠ beta | forced the book to be market-neutral, so §10 exists at all |
| 001 | Frequency & capacity | 1-day holding ⇒ costs are half the answer ⇒ §13 |
| 001 | Alpha decay | reframed "capacity" from a footnote into part of the result |
| 002 | Long/short, gross vs net | gave the exact weight construction; net = 0 killed market P&L |
| 002 | Leverage | separated *sizing* from *research* — leverage cannot change a Sharpe |
| 002 | Option payoffs | showed the floored-loss shape stock cannot replicate |
| 003 | Spread, mid, FIFO | established that a round trip costs money before you are right |
| 003 | Micro-price | revealed a forecast hiding in queue imbalance (Year 2's OFI) |
| 003 | Square-root impact | became the cost function that produced the capacity curve |
| 004 | Log vs simple returns | logs for aggregation, simple for portfolios; lognormal prices |
| 004 | Fat tails | invalidated normal-based risk numbers and Sharpe CIs |
| 004 | Vol clustering | predicted the heteroskedasticity White had to correct |
| 004 | Long memory | set the HAC lag choice |
| 004 | Leverage effect | explained why drawdowns cluster instead of arriving evenly |
| 004 | √h scaling | licensed the √252 annualization — after we checked autocorrelation |
| 005 | Four moments | skew/kurtosis entered the Lo standard error directly |
| 005 | Student-$t$ | fit the returns far better than the normal (df ≈ 3–4) |
| 005 | Uncorrelated ≠ independent | the reason 30,000 rows were not 30,000 observations |
| 005 | Covariance vs correlation | gave §7 the right matrix to decompose |
| 005 | CLT & √n | fixed the price of precision: 4× data to halve the error bar |
| 005 | Bayes | showed p < 0.05 means ~35% real at a realistic prior |
| 006 | Estimand/estimator/estimate | separated "the Sharpe" from "our Sharpe" |
| 006 | Standard error | turned one number into an interval |
| 006 | MLE | fitted the Student-$t$ degrees of freedom |
| 006 | Bootstrap (i.i.d. & block) | error bar with no formula; the block version tested independence |
| 006 | Estimation error | explained the residual beta the hedge could not remove |
| 007 | $t$ = SR × √years | converted every Sharpe claim into a required track length |
| 007 | FWER | 12 tests ⇒ 46% chance of a false find before we started |
| 007 | Bonferroni / BH | raised the bar to \|t\| > 2.87 and killed two surviving decoys |
| 007 | Power | showed a Sharpe-0.5 edge would be undetectable in 9 years |
| 007 | Best-of-$M$ null & haircut | priced the search itself; gave the decisive p-value |
| 008 | Covariance matrix | organized 12 names into one object |
| 008 | Eigendecomposition | found the axes of risk; trace identity checked the arithmetic |
| 008 | PCA & scree | PC1 ≈ 51% of variance, discovered without any index data |
| 008 | Market factor | named the exposure that had to be hedged |
| 008 | Projection | performed the hedge — and turned out to *be* OLS |
| 009 | OLS = projection | unified §7 and §9; residuals ⟂ regressors is the first-order condition |
| 009 | β̂ = Cov/Var = ρ·σy/σx | showed a slope is a rescaled correlation |
| 009 | R² | 0.004 for a real signal — normal, and why t-stats matter more |
| 009 | White (HC) SE | corrected real heteroskedasticity, and moved t barely — a clue |
| 009 | Newey–West (HAC) | corrected the 5-day overlap; gave n_eff |
| 009 | When regression lies | the deepest lesson: no SE fixes the wrong unit of observation |

### The one sentence

A naïve screen turned pure noise into five discoveries with 30,000 "observations." The Q1
toolkit reduced that to one real edge with a Sharpe of about 1.4, an honest confidence interval
more than a full Sharpe wide, and a capacity of roughly $100M — and the single step that
mattered most was not a fancier standard error, it was **changing what counts as an observation.**
""")

md(r"""
## Your turn (ungraded, in rough order of value)

1. **Break the neutralization.** In `build_book`, delete the beta-projection line and keep only
   the cross-sectional demeaning. Re-run §10–§12. How much does the residual market beta rise,
   and what happens to the Sharpe *interval*? (You are measuring what §11 called buying power by
   reducing σ.)
2. **Trade the naïve winner.** Take the decoy that looked best in §8's pooled screen and run it
   through §10–§13 as though you believed it. Watch a $t$ over 4 become a Sharpe near zero. This
   is the single most useful exercise here: it is what a leaked backtest feels like from the inside.
3. **Vary $M$.** Add 88 more decoys (`simulate_decoy_signals` takes a seed) for $M = 100$. The
   uncorrected screen will find far more "signals" while the best-of-$M$ null stays calm. Confirm
   `rev5` still survives Bonferroni at the higher bar — and note how much thinner its margin gets.
4. **Kill the edge with costs.** Lower `ADV_DOLLARS` to \$50M (mid caps) and re-run §13. At what
   AUM does a genuinely real edge become untradable? This is why capacity belongs in the memo.
5. **Set `KAPPA = 0`** in `simulate_market` and re-run the whole notebook. *Every* signal is now
   noise. A trustworthy pipeline must return nothing — verify that yours does. A method that only
   ever confirms is worthless.
6. **Halve the sample.** Re-run on the first five years only and compare the confidence interval.
   Feel the $\sqrt n$ in your hands rather than in a formula.
7. **Non-overlapping windows.** Rebuild §8's screen sampling every 5th day instead of daily. HAC
   and classical SEs should converge, because you removed the overlap instead of correcting for it.
   The cleanest fix is usually not to create the problem.

## Where this goes next

Everything above validated a signal *in sample* with careful standard errors. That is Q1's ceiling,
and it is not enough — three known holes remain, and each has a quarter devoted to it:

- **Q2 (Units 011–020) — the math bridge.** We wrote down an option payoff and refused to price it.
  Measure-theoretic probability, Brownian motion, Itô's lemma, risk-neutral pricing and the
  Black–Scholes PDE are what turn that payoff into a price and a hedge.
- **Q3 (Units 021–030) — time series & volatility.** §5 measured volatility clustering and long
  memory; Q3 *forecasts* them (GARCH, realized vol, HAR-RV) and formalizes the stationarity we
  assumed. Unit 027's cointegration is the rigorous version of the relative-value bet we traded.
- **Q4 and Year 2 — honest validation.** The memo's own caveats name the gap: no purged or
  embargoed cross-validation, no deflated Sharpe ratio, no probability of backtest overfitting.
  Our best-of-$M$ null is the *idea* of those tools, hand-rolled. Year 2 Q2 makes it rigorous.

One habit to carry forward: **the analysis that changes the answer is usually the one that changes
the unit of observation, not the one that changes the formula.**
""")

# ======================================================================== write
nb = {
    "cells": CELLS,
    "metadata": {
        "kernelspec": {"display_name": "Financial Eng Labs (.venv)",
                       "language": "python", "name": "feq-labs"},
        "language_info": {"name": "python", "version": "3.12"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

OUT = "labs/0010-2-q1-synthesis-walkthrough.ipynb"
with open(OUT, "w") as f:
    json.dump(nb, f, indent=1)
    f.write("\n")
n_md = sum(1 for c in CELLS if c["cell_type"] == "markdown")
print(f"wrote {OUT}: {len(CELLS)} cells ({n_md} markdown, {len(CELLS)-n_md} code)")
