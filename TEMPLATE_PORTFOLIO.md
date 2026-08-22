# Template: build a portfolio the Lab 010.2 way

Use this when you have real data and want to mirror the Q1 synthesis lab
(`labs/0010-2-q1-synthesis-walkthrough.ipynb`).

**Assumed inputs:** daily history for ~100 stocks over ~10 years (prices or returns).

**Goal:** build a stock-picking portfolio whose edge is “who beats whom,” then decide
if it is real after honest statistics and after trading costs.

---

## Words (plain language)

| Word | Meaning here |
|------|----------------|
| **Signal** | A number per stock today: how much you like it vs the others. |
| **Book / portfolio** | The positions you actually hold (buys and sells). |
| **Long** | Buy it; you win if it rises. |
| **Short** | Sell borrowed shares; you win if it falls. |
| **Weight** | Size of that name as a fraction of the book. |
| **The market** | The shared tide that moves most stocks together. |
| **Beta** | How hard a stock rides that tide. |
| **Dollar-neutral** | Dollars long ≈ dollars short; little net bet on “market up/down.” |
| **Gross** | Total size: sum of absolute weights (usually set to 1). |
| **Alpha (here)** | Profit from picking winners vs losers, not from riding the market. |

If the broker **forbids shorts**, you cannot build the dollar-neutral book below.
Use a long-only variant (top-N names, or overweight vs a benchmark) and judge success
as “beat the benchmark after costs,” not “market-neutral alpha.”

That long-only job, on a **weeks-to-months** clock, is the monthly book
(units 131–170). The same job on an **hours-to-days** clock — this template's
daily recipe, with the shorts removed and an ADV cap added — is units 171–210.
Both: ML scores in, constrained optimizer out, **information ratio vs a named
benchmark**. The store you must build first is Year 4 Q1 (121–130). Maps:
`reference/long-only-mid-horizon.html` and `reference/long-only-mid-frequency.html`.
What each unit must teach: `reference/year-4-lessons.html`,
`reference/year-5-lessons.html`, `reference/year-6-lessons.html`.
Do not skip there from Year 1.

---

## 0. Fix the rules up front

Decide **before** looking at results:

1. **Universe** — the N stocks. Handle IPOs, delistings, missing days; do not silently
   drop only the losers.
2. **Mandate** — relative value (who beats whom), not market direction.
3. **Holding style** — e.g. signal at today’s close → hold through tomorrow (daily
   rebalance), or weekly if you want lower turnover.
4. **Cost model** — half-spread + impact (or broker fees + estimated slippage).
   Without this, skip capacity later.

---

## 1. Build clean returns

For each stock, each day:

- Compute **log returns** for time-series work; use **simple returns** when combining
  names into a portfolio return.
- Align calendars (holidays, early closes).
- Flag bad prints (zero price, impossible jumps that are data errors).

Result: a panel `T days × N names`.

---

## 2. Make a signal (the opinion)

Example (lab’s `rev5`): **5-day cross-sectional reversal**

- For each stock today: score related to −(return over the last 5 days).
- Or any rule computable from data available **at that day’s close only**
  (no look-ahead).

Output each day: N numbers = “how much I like each name.”

---

## 3. Turn signal → portfolio weights (the book)

**Every day, in this order:**

### A. Relative views (strip the average)

```text
score_i − mean(score across names)
```

You are ranking stocks against each other, not calling the market up or down.

### B. Estimate beta (trailing, causal)

For each name, using the **past ~252 trading days only**:

- Regress stock return on a market proxy (equal-weight of your universe, or an index).
- Save \(\hat\beta_i\).

Do not use future data in the beta window.

### C. Neutralize market exposure

Remove the part of the score that lines up with beta, while keeping dollar-neutrality.

- Geometry: project onto the plane of `[ones, beta]`; keep the residual.
- Regression: residual of regressing scores on `[1, beta]`.

**Trap:** neutralizing beta alone can break dollar-neutrality if betas do not average
to zero in the right sense. Remove **both** exposures together, then **verify**:

- `sum(w) ≈ 0` (dollar-neutral)
- `sum(w × beta) ≈ 0` (beta-neutral)

### D. Scale size (gross = 1)

```text
w_i = residual_i / sum(|residual|)
```

- **gross** = sum(|w|) = 1  
- **net** = sum(w) ≈ 0  

### E. Dollars and trade

```text
dollars_i = w_i × capital
```

- Positive → buy (long)  
- Negative → short  

### F. One P&L number per day

Hold for the chosen horizon. Approximate:

```text
portfolio return_t = sum_i ( w_{i,t} × r_{i,t+1} )
```

That daily series is the research object — not a pooled name-day regression with
tens of thousands of fake independent rows.

---

## 4. Horse-race several candidates (multiple testing)

Do not trust one signal. Build a short list (e.g. 5–15): reversal, momentum, low-vol,
value if you have fundamentals, etc.

For each: repeat Steps 3A–F → one daily P&L series each.

Then:

1. Uncorrected screen: which look “significant”?  
2. Correct for searching M ideas: Bonferroni, Benjamini–Hochberg, and/or a
   best-of-M null (how often noise alone produces a winner this good).  
3. Keep only what survives the correction you would use to **commit capital**
   (usually the conservative bar).

---

## 5. Measure the survivor honestly

On the winner’s daily P&L:

- Annualized return, volatility, **Sharpe ratio**
- **Confidence interval** on Sharpe (block bootstrap if dependence matters)
- Residual market beta: regress book returns on the market; report it even if small
- Daily turnover → drives trading costs

Report the interval, not only the point estimate.

---

## 6. Subtract costs and find capacity

Each day, cost ≈ function of dollars traded vs ADV (average daily dollar volume).

Plot **net Sharpe vs AUM**. Ask: at *your* size, is net Sharpe still above zero
(or above your hurdle)?

If costs kill the edge, the answer is “not tradable,” even if gross looked good.

---

## 7. Write the decision (memo)

One page covering:

1. Question (universe, horizon, mandate)  
2. Why a naïve pooled screen would lie (dependence / overlap / search)  
3. Method (how weights were built; what was neutralized)  
4. Result (gross Sharpe, CI, HAC t, turnover)  
5. Multiple-testing correction and survivors  
6. Net of costs and capacity  
7. Recommendation (proceed / paper-trade small / kill)  
8. What would change your mind  

---

## Minimal checklist

| Step | You do |
|------|--------|
| Data | Clean daily returns for N × ~10 years |
| Risk | Market proxy (EW index / PC1); neutralize beta |
| Signal | Compute with no look-ahead |
| Book | Demean → beta-neutral → gross = 1 → trade |
| Evidence | One daily return; CI; multiple-testing |
| Reality | Costs + capacity |
| Output | Proceed / paper-trade / kill |

---

## Concrete first recipe (closest to Lab 010.2)

1. Universe = your ~100 stocks.  
2. Signal = 5-day cross-sectional reversal.  
3. Market proxy = equal-weight of the universe.  
4. Trailing 252-day beta → neutralize with `[1, beta]` → gross-1 dollar-neutral.  
5. Rebalance daily; record one P&L per day.  
6. Also run ~10 alternate or decoy signals; apply multiple-testing.  
7. Apply cost model with ADV; size the book from the capacity curve.  

---

## Flow (same arc as the lab)

```text
Job
  → how to hold it (long/short, dollar-neutral)
  → what it costs
  → clean data + reality of returns
  → what risk to remove (market / beta)
  → fake discoveries from a lazy screen
  → fix the unit of observation (daily book P&L)
  → size of edge + uncertainty
  → pay for searching many signals
  → after costs / capacity
  → write the decision
```

---

## Power reminder

~100 names and ~10 years still may not prove a *tiny* edge. This template is how you
avoid fooling yourself; it does not guarantee a live edge. Power (years of data vs
true Sharpe) is often the binding constraint.

---

## Related

- Worked teaching case: `labs/0010-2-q1-synthesis-walkthrough.ipynb`
- Year 4 mandate (long-only, weeks–months, ML + optimizer): `reference/long-only-mid-horizon.html`
- Year 5 mandate (long-only, hours–days, ML + optimizer): `reference/long-only-mid-frequency.html`
- Year 4 teaching plan (what each lesson must teach): `reference/year-4-lessons.html`
- Year 5 teaching plan: `reference/year-5-lessons.html`
- Year 6 teaching plan (data kit + going live): `reference/year-6-lessons.html`
- Plain-language teaching decision: `NOTES.md` (2026-07-27)
- Q1 checkpoint (spurious signal): `labs/0010-checkpoint-spurious-signal.ipynb`
