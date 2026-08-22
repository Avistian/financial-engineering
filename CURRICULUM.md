# Expert Curriculum — Quantitative Research (Systematic Trading)

Agent-facing plan for lesson sequencing. The student-facing version is
[reference/curriculum.html](./reference/curriculum.html).

**Pace:** ~1.5–2 hours/day **baseline** · ~600–700 hours/year · **~4,000 hours over 6 years.**
Years 1–3 are the original systematic-alpha QR track (unchanged). **Years 4–6 are extra
calendar, not a swap.** Unit numbers now match study order: the **data kit** (Year 4 Q1),
then the **monthly** long-only book, then the **daily** long-only book, then the desk
(paper and a tiny live book). QT and QD stay in Years 1–3 at awareness depth.

**Lesson-by-lesson teaching plans** (what each unit must teach, in order; labs not written yet):
[Year 4](./reference/year-4-lessons.html) ·
[Year 5](./reference/year-5-lessons.html) ·
[Year 6](./reference/year-6-lessons.html).

**Study order is the unit numbers:** Years 1–3 → 121–240. Do not skip the store
(121–130) before a long-only backtest.

### Why 240 units take 6 years (read this if the math looks off)

A common, correct objection: *240 lessons ÷ 365 days ≈ 8 months — so at one lesson/day this is
a one-year plan, not six.* That objection is right about **reading** and wrong about
**mastery**. Stop treating a numbered row as "one day." Years 1–3 are still the original
~2,000-hour QR track; Years 4–6 add three ~650-hour specializations and do not shorten them.

**A unit ≠ a day.** Each numbered row below is a **unit** = one concept *plus its lab/reproduction
work plus its quiz/checkpoint*. Units are not uniform:

| Unit type | Sessions to finish | Where |
|-----------|--------------------|-------|
| Concept lesson (read + quiz) | 1–3 sessions | dense in Y1 |
| Derivation / math unit (prove it, then code it) | 2–5 sessions | Y1 Q2, interview prep |
| Lab / reproduction unit (build, tune, debug, re-run) | 4–12 sessions | dominant Y2–Y5 |
| Checkpoint / exit exam | 3–6 sessions | end of each quarter/year |
| Capstone (project + write-up + defense) | 20–40+ sessions | Y3 Q4, Y4 Q4, Y5 Q4, Y6 Q4 |

**Where the ~4,000 hours actually go** (lessons are a small slice of the clock):

| Activity | ≈ hours | Share |
|----------|---------|-------|
| Lesson content itself (240 × ~0.75h) | ~180 | ~5% |
| Deep primary-source reading (books + ~65 core papers) | ~520 | ~13% |
| **Hands-on labs & reproduction** (pricing, ML pipelines, LOB, backtests, long-only books, desk loop) | ~1,650 | ~41% |
| Checkpoints + year exit exams | ~300 | ~8% |
| Spaced retrieval / review | ~260 | ~7% |
| **Interview drilling** (mental math, brainteasers, LeetCode) — runs *throughout*, concentrated in Y3 Q4 | ~200 | ~5% |
| **Year-3 capstone** (general systematic-alpha defense) | ~200 | ~5% |
| **Year-4 exit** (honest store + monthly book through the optimizer) | ~150 | ~4% |
| **Year-5 capstones** (monthly book defended + daily book through the optimizer) | ~150 | ~4% |
| **Year-6 capstones** (daily book defended + paper/live desk) | ~150 | ~4% |

**Density curve (front-loaded learning, back-loaded building, then a mandate year):**
- **Year 1** — concept- and derivation-dense. Units arrive ~2–3/week. This is the only phase where "lessons/week" is the right mental model. You are buying vocabulary, the stochastic-calculus toolkit, and *evaluation discipline*.
- **Year 2** — reproduction-heavy. ~1 unit/week; each is days of feature engineering, model fitting, and — above all — validation. This is the heart of the QR craft.
- **Year 3** — build- and interview-dominated. Portfolio construction, execution, systems awareness, then the interview gauntlet and a capstone whose calendar is set by experiments and writing, not reading.
- **Year 4** — the store first (as-of keys, no leaked joins), then the **monthly** long-only book through the optimizer. Same validation bar as Year 2.
- **Year 5** — run and defend that monthly book, then the same job on a **hours-to-days** clock (this course's mid-frequency) through the daily optimizer. Costs and ADV are first-order.
- **Year 6** — defend the daily book, then the desk: backtest=live code path, paper loop, reconcile, kill switch, small live. Do **not** skip here from Year 1.

**Unit numbering:** Year N → units `(N-1)*40 + 001` … `(N-1)*40 + 040`.
**Rule:** finish each quarter's checkpoint before advancing. A unit is "done" when its lab runs
and its quiz/checkpoint passes — not when the reading is skimmed.

> **Critical framing (read first).** Two truths must coexist the whole way:
> 1. **Markets are adversarial and low-signal.** Most "edges" are overfit noise. The single most valuable thing this curriculum teaches is not a model — it is the discipline to *not fool yourself*: leakage-free pipelines, purged/embargoed CV, CPCV, PBO, and the deflated Sharpe ratio. A QR who can kill their own bad backtest is worth more than one who can train a fancier net.
> 2. **Simple, well-validated beats complex and leaky.** As of 2024–2026, tuned gradient-boosted trees + strong-default MLPs still win most *tabular* alpha problems; deep sequence models earn their keep mainly on microstructure/LOB and text. Every model below is taught **with its failure mode**, not as hype.
>
> A model, method, or paper earns a unit only if it set SOTA, exposed a real limitation, or is a baseline you must beat. See [RESOURCES.md](./RESOURCES.md).

### Core (★) vs optional (◆) sources

- **★ Core** — required. Read deeply and either reproduce it or use it as a baseline. Exit exams test these.
- **◆ Optional / time-permitting** — read *only after* the quarter's core work is done, and *never* by cutting a lab or exit-exam prep. A ◆ source is a ~2 h skim with a one-paragraph "when it wins / when it breaks" note in [NOTES.md](./NOTES.md).

---

## Year 1 — Foundations: Markets, the Math Bridge, and Honest ML (Units 001–040)

**Goal:** Speak markets fluently from zero, rebuild the probability/statistics a quant needs,
acquire the stochastic-calculus toolkit, and internalize the leakage/labeling discipline that
separates real research from data-mined nonsense. You cannot argue you found alpha until you can
prove you did not just overfit.

### Q1 · Markets & the quant landscape + statistical foundations (Units 001–010)
| # | Unit topic | Primary source | Lab / deliverable |
|---|-----------|----------------|-------------------|
| 001 | The quant landscape: buy vs sell side, QR/QT/QD, HFT vs mid vs low frequency, what "alpha" means | Bouchaud *Trades, Quotes & Prices* Ch.1; firm blogs | Map 6 firms to strategy styles |
| 002 | Instruments & mechanics: equities, futures, options, ETFs; how an order becomes a trade | Hull Ch.1–2 | Glossary of 20 instruments/terms |
| 003 | Market structure & the limit order book (intro): exchanges, matching, price-time priority (FIFO) | Bouchaud Ch.3 | Trace an order through a toy LOB |
| 004 | Returns, prices & stylized facts: log returns, fat tails, vol clustering, autocorrelation of \|r\| | Cont 2001 (stylized facts) ★ | **Lab:** measure 5 stylized facts on real data |
| 005 | Probability refresher: RVs, moments, normal/lognormal/Student-t/Poisson | Wasserman *All of Statistics* Ch.1–5 | Fit & compare tail distributions |
| 006 | Estimation & inference: bias/variance, MLE, confidence intervals, the bootstrap | Wasserman Ch.6–9 | Bootstrap a Sharpe-ratio CI |
| 007 | Hypothesis testing & multiple-testing traps: t-stats, p-values, why finance breaks classical testing | Harvey-Liu-Zhu 2016 ★ | Simulate false discoveries under many trials |
| 008 | Linear algebra for quants: covariance, eigendecomposition, PCA (geometry, not recipe) | Strang *Linear Algebra* (PCA); Axler | PCA of a returns panel by hand |
| 009 | Regression done right: OLS, heteroskedasticity, Newey-West, when regression lies | Wooldridge (intro); Newey-West 1987 | Robust vs naïve standard errors |
| 010 | **Q1 checkpoint** — statistical hygiene | — | Reproduce a returns-analysis notebook; detect a planted spurious signal |

### Q2 · Stochastic calculus & derivatives pricing (Units 011–020) — the math bridge
| # | Unit topic | Primary source | Lab / deliverable |
|---|-----------|----------------|-------------------|
| 011 | Measure-theoretic probability (lite): spaces, filtrations, conditional expectation as projection | Shreve II Ch.1–2 ★ | Compute E[·\|filtration] on a tree |
| 012 | Random walks → Brownian motion: construction, properties, quadratic variation | Shreve II Ch.3 ★ | Simulate BM; verify [W]_t = t |
| 013 | The Itô integral & Itô's lemma | Shreve II Ch.4 ★ | Apply Itô to d(log S), d(S²) |
| 014 | SDEs: GBM, Ornstein-Uhlenbeck, existence/uniqueness intuition | Shreve II Ch.4–5 | Simulate & fit an OU process |
| 015 | Risk-neutral pricing & the Girsanov theorem: measure change, market price of risk | Shreve II Ch.5 ★ | Change measure on a binomial → BS limit |
| 016 | The Black-Scholes PDE & Feynman-Kac: PDEs ↔ expectations | Shreve II Ch.6 ★ | Derive BS PDE; state Feynman-Kac |
| 017 | Greeks & dynamic hedging: delta/gamma/vega/theta; the P&L of a hedged option | Hull Ch.19; Wilmott | Simulate delta-hedging P&L & slippage |
| 018 | Jump-diffusion & Poisson processes: Merton model, compound Poisson | Merton 1976; Cont-Tankov | Add jumps to a price simulator |
| 019 | Numerical methods: Monte Carlo, finite differences, variance reduction | Glasserman *Monte Carlo Methods* | MC pricer w/ antithetic + control variates |
| 020 | **Q2 checkpoint** — price & hedge a European option **three ways** | Shreve II | Closed form vs MC vs PDE; reconcile to tolerance |

### Q3 · Financial time series & volatility (Units 021–030)
| # | Unit topic | Primary source | Lab / deliverable |
|---|-----------|----------------|-------------------|
| 021 | Stationarity & unit roots: why prices aren't stationary but returns (almost) are | Tsay Ch.2 ★ | ADF test; difference a price series |
| 022 | ARMA/ARIMA and the limits of linear models on returns | Tsay Ch.2 | Fit ARMA; show near-zero return predictability |
| 023 | Volatility I — ARCH/GARCH: conditional heteroskedasticity, persistence, forecasting | Tsay Ch.3 ★ | Fit GARCH(1,1); forecast vol |
| 024 | Realized volatility & quadratic variation theory: tick data → daily RV | Andersen-Bollerslev-Diebold-Labys 2003 ★ | Compute RV from intraday returns |
| 025 | The HAR-RV model: heterogeneous autoregression, long memory | Corsi 2009 ★ | **Lab:** HAR-RV forecaster |
| 026 | Jumps & the leverage effect: bipower variation, jump detection, asymmetric vol | Barndorff-Nielsen-Shephard 2004 | Detect jumps; split RV = C + J |
| 027 | Cointegration & pairs: Engle-Granger, Johansen, spurious regression | Tsay Ch.8; Engle-Granger 1987 ★ | Find & test a cointegrated pair |
| 028 | Statistical arbitrage: mean reversion, OU signals, half-life, trade lifecycle | Avellaneda-Lee 2010 ★ | Build a pairs signal w/ entry/exit |
| 029 | Multivariate volatility & covariance: DCC, EWMA, the dimensionality curse (preview RMT; dependence beyond ρ → Y3 copulas) | Tsay Ch.10 | EWMA cov of a small panel |
| 030 | **Q3 checkpoint** — HAR-RV vs GARCH | Corsi 2009 | Validate a vol forecaster out-of-sample; honest error metrics |

### Q4 · Financial ML foundations I — data & labeling (Units 031–040) — AFML core
| # | Unit topic | Primary source | Lab / deliverable |
|---|-----------|----------------|-------------------|
| 031 | Why standard ML fails on finance: non-IID, low SNR, regime change, adversaries | López de Prado *AFML* Ch.1 ★ | Break an IID assumption on real data |
| 032 | Financial data structures: the bar zoo — time, tick, volume, dollar bars | AFML Ch.2 ★ | Build tick/volume/dollar bars |
| 033 | Information-driven bars: imbalance & run bars; sample by information, not clock | AFML Ch.2 | Implement imbalance bars |
| 034 | The CUSUM filter & event-based sampling | AFML Ch.2 §2.5.2 | CUSUM event timestamps |
| 035 | The triple-barrier labeling method: path-dependent labels that match trading | AFML Ch.3 §3.4 ★ | **Lab:** triple-barrier labeler |
| 036 | Meta-labeling: separating side from size; precision boosting | AFML Ch.3 §3.6 ★ | Add a meta-label model |
| 037 | Fractional differentiation: stationarity while preserving memory | AFML Ch.5 ★ | Frac-diff a price series; ADF vs memory |
| 038 | Sample weights & overlapping outcomes: label uniqueness, why IID breaks | AFML Ch.4 ★ | Compute average uniqueness |
| 039 | Sequential bootstrap: sampling toward uniqueness | AFML Ch.4 §4.5 | Implement sequential bootstrap |
| 040 | **Q4 / Year-1 exit exam** — end-to-end data→label pipeline | AFML Ch.2–5 | Bars → frac-diff features → triple-barrier labels → weighted sample, **zero leakage**, defended |

**Year 1 exit criterion:** you can (a) price/hedge an option three ways, (b) build the AFML
data→label pipeline with no leakage, (c) forecast volatility with a validated HAR-RV, and
(d) explain, cold, why a naïve backtest lies.

**◆ Optional (Year 1):** Baxter-Rennie *Financial Calculus* (gentler than Shreve) · Sinclair
*Volatility Trading* · Cont-Tankov *Financial Modelling with Jump Processes* (advanced).

---

## Year 2 — The Researcher's Craft: ML That Survives Markets (Units 041–080)

**Goal:** master the modeling, **validation**, and microstructure toolkit that generates and
*defends* alpha. Year 2 is the difference between "I got a great backtest" and "I have an edge I
can stake capital and my reputation on."

### Q1 · Financial ML II — features & ensembles (Units 041–050)
| # | Unit topic | Primary source | Lab / deliverable |
|---|-----------|----------------|-------------------|
| 041 | Feature importance done right: MDI, MDA, and their finance-specific failure modes | AFML Ch.8 ★ | MDI vs MDA on labeled data |
| 042 | Orthogonal features & clustered feature importance (Cluster MDI/MDA) | AFML Ch.8; *ML for Asset Managers* Ch.6 ★ | Cluster features; clustered importance |
| 043 | Entropy features: information content as signal (Shannon, Kontoyiannis) | AFML Ch.18 | Entropy-rate feature on returns |
| 044 | Structural break tests: CUSUM, SADF/explosive tests, regime & bubble detection | AFML Ch.17 ★ | SADF bubble detector |
| 045 | Bagging vs boosting in finance: variance vs bias; why bagging is safer on noisy labels | AFML Ch.6; ESL Ch.15–16 ★ | Bagging vs boosting under label noise |
| 046 | Random forests for finance: OOB, feature sampling, pitfalls under low uniqueness | Breiman 2001; AFML Ch.6 | RF w/ sample weights |
| 047 | Gradient boosting (XGBoost/LightGBM/CatBoost) for tabular alpha | Chen-Guestrin 2016; Ke 2017 ★ | Tune a GBDT signal model |
| 048 | Hyperparameter search without leaking: nested CV, the true cost of tuning | AFML Ch.9 ★ | Nested CV w/ purging |
| 049 | Ensemble stacking & model diversity for robustness | Wolpert 1992 (skim) | Blend diverse signal models |
| 050 | **Q1 checkpoint** — feature-importance study | AFML Ch.8 | Separate real from noise features; defend which to keep |

### Q2 · Backtesting & the war on overfitting (Units 051–060) — the differentiator
| # | Unit topic | Primary source | Lab / deliverable |
|---|-----------|----------------|-------------------|
| 051 | Why backtesting is hard: selection bias under multiple testing; the overfitting epidemic | Bailey-López de Prado 2014 ★ | Reproduce a "too good" backtest |
| 052 | Purged K-Fold CV: purging train/test contamination from overlapping labels | AFML Ch.7 §7.4 ★ | Implement PurgedKFold |
| 053 | The embargo mechanism: leakage across the serial-correlation horizon | AFML Ch.7 ★ | Add embargo; measure leak reduction |
| 054 | Combinatorial Purged Cross-Validation (CPCV): many backtest paths from one history | AFML Ch.12 §12.4 ★ | **Lab:** CPCV path generator |
| 055 | The Deflated & Probabilistic Sharpe Ratio: adjust for skew, kurtosis, track length | Bailey-López de Prado 2012/2014 ★ | Deflated Sharpe on a strategy |
| 056 | Probability of Backtest Overfitting (PBO): combinatorially-symmetric CV | Bailey et al. 2015 ★ | Compute PBO for a strategy family |
| 057 | Minimum backtest length & "how many trials until a false discovery" | Bailey-López de Prado 2014 | Compute min length for a target Sharpe |
| 058 | Walk-forward vs CPCV vs cross-sectional: what each can and can't tell you | AFML Ch.11–12 | Compare all three on one strategy |
| 059 | Strategy risk & bet sizing: Kelly, drawdown control, stop-outs | AFML Ch.10; Thorp on Kelly ★ | Bet-sizing from meta-label probabilities |
| 060 | **Q2 checkpoint** — kill or confirm | AFML Ch.11–12 | Take a "great" backtest; prove/debunk it with CPCV + PBO + deflated Sharpe |

### Q3 · Market microstructure & LOB dynamics (Units 061–070)
| # | Unit topic | Primary source | Lab / deliverable |
|---|-----------|----------------|-------------------|
| 061 | LOB mechanics in depth: order types, queue position, price-time priority revisited | Bouchaud Ch.3–4 ★ | Simulate queue-position dynamics |
| 062 | Order Flow Imbalance (OFI) & price impact | Cont-Kukanov-Stoikov 2014 ★ | **Lab:** fit OFI→return impact |
| 063 | Multi-Level OFI & integrated OFI; cross-impact | Cont-Cucuringu-Zhang 2023 ★ | MLOFI via PCA; cross-impact LASSO |
| 064 | Price impact models: linear, square-root law, permanent vs temporary | Bouchaud Ch.11; Almgren et al. 2005 ★ | Fit the square-root impact law |
| 065 | Hawkes processes I: self-exciting point processes, intensity, branching ratio | Bacry-Mastromatteo-Muzy 2015 ★ | Simulate & fit a univariate Hawkes |
| 066 | Hawkes processes II: state-dependent & multivariate order arrivals | Bacry et al. 2015 | Multivariate Hawkes on order events |
| 067 | Adverse selection & information asymmetry: Glosten-Milgrom, Kyle's lambda | Kyle 1985; Glosten-Milgrom 1985 ★ | Estimate Kyle's lambda |
| 068 | Bid-ask spread decomposition: inventory vs adverse selection vs processing | O'Hara *Market Microstructure Theory* | Decompose a spread |
| 069 | Agent-based models & LOB simulators: building a synthetic book | Byrd et al. *ABIDES* | Run an ABM LOB simulation |
| 070 | **Q3 checkpoint** — microstructure reproduction | Cont-Kukanov-Stoikov | Fit OFI→impact **and** a Hawkes intensity on LOB data; interpret honestly |

### Q4 · Modern deep learning & NLP for markets (Units 071–080)
| # | Unit topic | Primary source | Lab / deliverable |
|---|-----------|----------------|-------------------|
| 071 | Sequence models: RNN/LSTM/GRU and the vanishing-gradient reality | Goodfellow *Deep Learning* Ch.10 | LSTM on a sequence task |
| 072 | Attention & transformers: self-attention, positional encoding | Vaswani et al. 2017 ★ | Implement scaled-dot-product attention |
| 073 | Deep LOB models: DeepLOB (CNN+LSTM) — what deep nets extract from the book | Zhang-Zohren-Roberts 2019 ★ | **Lab:** reproduce a DeepLOB predictor |
| 074 | Autoregressive & generative sequence models: forecasting vs generation | — | AR forecaster; discuss generation |
| 075 | NLP for finance I: text as data — earnings calls, 10-K/10-Q, news | Loughran-McDonald 2011 ★ | LM sentiment on filings |
| 076 | NLP for finance II: embeddings, transformer sentiment, event extraction, LLMs as feature extractors | FinBERT (Araci 2019); Loughran-McDonald | Embeddings → signal features |
| 077 | Tabular deep learning: FT-Transformer, and where deep nets lose to GBDTs on tabular | Gorishniy et al. 2021; Grinsztajn et al. 2022 ★ | FT-Transformer vs GBDT, fair split |
| 078 | Tabular foundation models: TabPFN, TabDPT, in-context learning & zero-shot transfer | Hollmann et al. 2023 (TabPFN); Ma et al. 2024 (TabDPT) ★ | Zero-shot TFM vs tuned GBDT |
| 079 | Practical DL: regularization, early stopping, and not fooling yourself on noisy data | Goodfellow Ch.7–8 | Overfit-then-regularize demo |
| 080 | **Q4 / Year-2 exit exam** — deep model, honest eval | Zhang-Zohren-Roberts 2019 | Reproduce a DeepLOB-style predictor with correct temporal splits; match/beat a GBDT baseline honestly |

**Year 2 exit criterion:** you can build a leakage-free, sample-weighted signal model; **validate
it with CPCV/PBO/deflated Sharpe**; reproduce a microstructure result; and know when a deep model
is worth it vs a GBDT. You can look at someone else's backtest and find the leak.

**◆ Optional (Year 2):** *ML for Asset Managers* (full) · Dixon-Halperin-Bilokon *Machine Learning
in Finance* · Prado's *Causal Factor Investing* · TabReD / TabArena benchmark papers.

---

## Year 3 — Alpha, Execution, Systems & the Interview (Units 081–120)

**Goal:** turn signals into a deployable, capacity-aware strategy; understand execution and the
systems that run it; then convert everything into offer-getting interview performance and a
defended capstone.

### Q1 · Portfolio construction & risk (Units 081–090)
| # | Unit topic | Primary source | Lab / deliverable |
|---|-----------|----------------|-------------------|
| 081 | Mean-variance optimization & its instability | Markowitz 1952; Grinold-Kahn Ch.2 ★ | MVO and its blow-ups |
| 082 | Covariance cleaning: RMT (Marčenko-Pastur) + Ledoit-Wolf shrinkage & denoising | Laloux et al. 1999; Ledoit-Wolf 2004 ★; *ML for Asset Managers* Ch.2 | **Lab:** MP fit + shrink & denoise a cov matrix |
| 083 | Factor models & risk decomposition: Barra-style, PCA factors, idiosyncratic risk | Grinold-Kahn Ch.3 ★ | Decompose portfolio risk |
| 084 | The Fundamental Law & signal combination: IC, breadth, transfer coefficient, alpha blending | Grinold-Kahn Ch.6, 11–14 ★ | Compute IC/IR; combine 3 signals; measure lift |
| 085 | Copulas I — dependence beyond correlation: Sklar's theorem, margins vs copula, Gaussian & Student-t, Spearman/Kendall | McNeil-Frey-Embrechts Ch.5–7 ★; Embrechts-McNeil-Straumann 2002 ★ | Fit Gaussian & t-copulas to a returns pair; compare to linear ρ |
| 086 | Copulas II — tails, families & risk: tail dependence, Archimedean (Clayton/Gumbel/Frank), simulation; why the Gaussian copula fails in crashes | McNeil-Frey-Embrechts ★; Li 2000 (cautionary) | **Lab:** simulate joint losses via copula; compare VaR/ES vs Gaussian; document the failure mode |
| 087 | Hierarchical Risk Parity (HRP) & robust allocation | López de Prado 2016 ★ | HRP vs MVO out-of-sample |
| 088 | Transaction costs & capacity: turnover, slippage, alpha decay, strategy capacity | Grinold-Kahn; Kyle/impact | Net-of-cost Sharpe & capacity curve |
| 089 | Risk management & drawdown: VaR/ES caveats, copula-aware aggregation, stress, regime-aware sizing | Hull Risk Mgmt; McNeil-Frey-Embrechts ★ | Backtest a drawdown-control overlay; stress with fitted copula |
| 090 | **Q1 checkpoint** — build a portfolio | Grinold-Kahn; LdP; MFE | Denoised, cost-aware portfolio from multiple signals; report net Sharpe, capacity, and a copula-based stress of joint losses |

### Q2 · Optimal execution, market making & RL (Units 091–100)
| # | Unit topic | Primary source | Lab / deliverable |
|---|-----------|----------------|-------------------|
| 091 | The execution problem: implementation shortfall, arrival price, benchmarks | Cartea-Jaimungal-Penalva Ch.1 ★ | Define IS & benchmarks on fills |
| 092 | The Almgren-Chriss framework: permanent vs temporary impact; the execution frontier | Almgren-Chriss 2000 ★ | **Lab:** Almgren-Chriss optimal schedule |
| 093 | Scheduling algorithms: TWAP, VWAP, POV, IS algos | Cartea et al. Ch.7 ★ | Implement TWAP/VWAP; compare cost |
| 094 | Market making & inventory control: the Avellaneda-Stoikov model | Avellaneda-Stoikov 2008 ★ | Quote w/ inventory skew |
| 095 | Markov Decision Processes for trading: states, actions, rewards | Sutton-Barto Ch.3 ★ | Frame execution as an MDP |
| 096 | Value-based RL: Q-learning, DQN, Double DQN for execution | Sutton-Barto Ch.6; Mnih 2015; van Hasselt 2016 ★ | Double-DQN execution agent |
| 097 | Policy-gradient & actor-critic: PPO for trading agents | Schulman et al. 2017 (PPO) ★ | PPO agent on the sim |
| 098 | RL pitfalls in finance: reward hacking, non-stationarity, sim-to-real, why RL rarely ships naïvely | Cartea et al.; survey | Break your own RL agent; document |
| 099 | Backtesting execution & MM agents against a LOB simulator | Byrd et al. *ABIDES* | Agent vs TWAP/VWAP in sim |
| 100 | **Q2 checkpoint** — execution head-to-head | Almgren-Chriss; Sutton-Barto | Almgren-Chriss schedule **vs** RL agent **vs** TWAP/VWAP; explain the winner |

### Q3 · Research infrastructure & low-latency awareness (Units 101–110) — Python-first; C++/Rust here
| # | Unit topic | Primary source | Lab / deliverable |
|---|-----------|----------------|-------------------|
| 101 | The research stack: market-data engineering, point-in-time correctness, survivorship bias | Data-eng notes; López de Prado | Build a point-in-time data loader |
| 102 | Building a backtest engine: event-driven vs vectorized, fills, costs, look-ahead safety | *Advances in Financial ML*; QuantConnect/Zipline docs | **Lab:** leakage-safe event-driven backtester |
| 103 | Performance in Python: vectorization, numba, memory, profiling; when Python is enough | High-Performance Python (Gorelick-Ozsvald) | Profile & 10× a hot loop |
| 104 | The tick-to-trade loop & latency budget: where microseconds go (systems awareness) | Firm talks; NASDAQ/Databento docs | Draw a latency budget diagram |
| 105 | C++ for quants I: memory model, RAII, value semantics, compile-time dispatch | Stroustrup; *Effective Modern C++* | Port a hot function to C++ |
| 106 | C++/Rust for quants II: cache locality, lock-free queues, the LMAX Disruptor pattern | LMAX Disruptor paper; Rust book | Ring-buffer queue benchmark |
| 107 | Kernel bypass & networking: DPDK, zero-copy, RDMA — concepts and when they matter | DPDK docs (concepts) | One-page "when do we need this?" memo |
| 108 | Determinism & tail latency: P99, jitter, measuring it | Dean-Barroso "The Tail at Scale" | Measure latency distribution & P99 |
| 109 | Reproducible research: experiment tracking, config, seeds, the "did it really work?" audit | MLflow/W&B docs | Reproduce a past result from config alone |
| 110 | **Q3 checkpoint** — infra you can trust | — | Build a leakage-safe event-driven backtester; profile & optimize a hot path |

### Q4 · Interview mastery & capstone (Units 111–120)
| # | Unit topic | Primary source | Lab / deliverable |
|---|-----------|----------------|-------------------|
| 111 | Mental math & rapid estimation under pressure | Zhou *A Practical Guide to Quant Finance Interviews* ("Green Book") ★ | Timed arithmetic & Fermi drills |
| 112 | Probability brainteasers: expectation, conditioning, symmetry | Green Book; *Heard on the Street* ★ | 30 timed probability puzzles |
| 113 | Market-making & betting games: EV, variance, adverse selection in games | Optiver/IMC practice; Green Book | Play & analyze a market-making game |
| 114 | Stochastic-calculus & pricing derivations for interviews | Shreve II; Green Book ★ | Derive BS & 10 SDE facts from memory |
| 115 | Statistics/ML interview questions & "why" reasoning | Green Book; *Hundred-Page ML Book* | Explain 20 ML concepts cold |
| 116 | Coding interviews I: arrays, hashing, two-pointer, DP | *Elements of Programming Interviews*; LeetCode ★ | 25 DP/array problems |
| 117 | Coding interviews II: graphs, trees, quant-flavored problems | EPI; LeetCode ★ | 25 graph/tree problems |
| 118 | System design for trading: data → signal → execution → risk, end to end | Firm eng blogs; DDIA (Kleppmann) | Whiteboard a trading-system design |
| 119 | Behavioral, research presentation, "walk me through a project" | — | Rehearse the capstone pitch |
| 120 | **Q4 / Year-3 exit — Capstone** | everything | **End-to-end research project**: data → signal → CPCV-validated backtest → cost/capacity-aware sizing → write-up, presented as if defending it to a PM |

**Year 3 exit criterion (the mission):** you can stand in front of a skeptical PM and defend an
original, leakage-free, capacity-aware strategy — including an honest account of joint-loss
dependence (copulas, not just correlation) — and you can pass the mental-math, probability,
derivation, and coding gauntlet that gets the offer.

**◆ Optional (Year 3):** Narang *Inside the Black Box* · Chan *Quantitative Trading* / *Algorithmic
Trading* · Cartea-Jaimungal-Penalva full text · *Designing Data-Intensive Applications* (systems depth).

---

## Year 4 — Honest store, then the monthly long-only book (Units 121–160)

**What each lesson must teach:** [reference/year-4-lessons.html](./reference/year-4-lessons.html)
(one skill, ordered beats, the trap). Labs are specified later; they are not written yet.

**This year is extra time, not a replacement.** Years 1–3 stay required. Year 4
starts with the **data kit** — a store of facts that could have been known that
morning — then aims that store at one mandate:

> Own stocks for **weeks to a few months**. Do not borrow shares to bet they fall
> (**long-only**). Beat a **stated benchmark** after costs. Turn a machine-learning
> *score* (a number per stock: how much you like it versus the others) into holdings
> with an optimizer that respects real constraints (no shorts, sector caps, name caps,
> turnover, a risk model).

Everyday picture: first you refuse a join without an as-of key. Then each month you
rank a list of stocks, the optimizer decides *how much* of the ones you like you can
actually own, you hold until the next rebalance, and you are judged on **how much
you beat the index**, not on a market-neutral Sharpe. Lesson 001 called this bucket
**low frequency / factor investing**. Running and defending this book is Year 5 Q1.
Year 5 Q2 onward is the faster clock.

**Prerequisite:** Year 3 Q1 (units 081–090) and Year 2 Q2 (units 051–060) in particular.
Unit 084's Fundamental Law and unit 047's GBDT are the on-ramps, not substitutes.

**Goal:** ship a point-in-time store *and* a walk-forward, cost-aware monthly
long-only book whose scores come from ML and whose holdings come from a constrained
optimizer. The full PM defense of that book is unit 170 (Year 5 Q1).

### Q1 · The data kit (Units 121–130)
| # | Unit topic | Primary source | Lab / deliverable |
|---|-----------|----------------|-------------------|
| 121 | What a desk data set is: tables + as-of keys | vendor docs; unit 101 | Name the six tables; refuse a join without an as-of key |
| 122 | Price panel: splits, dividends, delist returns | Bali-Engle-Murray; CRSP notes | Adjuster; price-only lie vs total return |
| 123 | Point-in-time membership: IPO, add/drop, delist | unit 132 | Survivors-only vs PIT; fake premium |
| 124 | Point-in-time fundamentals (vintages / as-of join) | Bali-Engle-Murray | Restated leak vs vintage join |
| 125 | Earnings/event calendar: timestamp, timezone, surprise | Bernard-Thomas | After-close vs before-open leak test |
| 126 | Daily bars: open, close, auction, VWAP, volume, spread | Heston-Korajczyk-Sadka | Auction ≠ last trade |
| 127 | Liquidity history: trailing ADV, spread, days-to-trade | Amihud 2002 | Causal ADV; days-to-trade at stated AUM |
| 128 | Benchmark reconstitution as data | unit 139 | Frozen starting list vs true membership |
| 129 | Feature store: (name, as-of morning), no future joins | AFML point-in-time | Illegal-join unit tests |
| 130 | **Q1 checkpoint** — one store that serves monthly and daily | 122–129 | Both panels pass the leak tests |

### Q2 · The mandate and the classic baselines (Units 131–140)
| # | Unit topic | Primary source | Lab / deliverable |
|---|-----------|----------------|-------------------|
| 131 | The long-only mid-horizon mandate: benchmark, active return, tracking error, information ratio vs Sharpe | Grinold-Kahn Ch.1–2, 4–5 ★; Qian-Hua-Sorensen Ch.1–2 ★ | Compute Sharpe *and* IR on a toy long-only book vs an equal-weight and a cap-weight benchmark |
| 132 | Universe construction: point-in-time membership, IPOs, delistings, survivorship bias | Bali-Engle-Murray Ch.1–2 ★; López de Prado (data pitfalls) | Rebuild a 20-year universe two ways (survivors-only vs point-in-time); show the fake premium |
| 133 | Corporate actions & the return you actually earn: splits, dividends, spinoffs, total return | Bali-Engle-Murray; CRSP methodology notes | Reconstruct total-return series; show a price-only backtest lie |
| 134 | The cross-section as the unit of observation: characteristics today, residual return next month | Fama-MacBeth 1973 ★; Cochrane *Asset Pricing* Ch.12 | Fama–MacBeth on one toy characteristic; report the average slope and its t |
| 135 | Classic factor I — momentum: 12-1 cross-section and time-series trend | Jegadeesh-Titman 1993 ★; Moskowitz-Ooi-Pedersen 2012; Asness-Moskowitz-Pedersen 2013 ★ | 12-1 long-only deciles vs long-short; report IR vs Sharpe; skip-last-month ablation |
| 136 | Classic factor II — value (book/price, earnings/price) and value+momentum | Fama-French 1992/1993/2015 ★; Asness-Moskowitz-Pedersen 2013 ★ | Value long-only; 50/50 and IC-weighted blend with momentum |
| 137 | Classic factor III — quality / profitability, investment, low-volatility | Novy-Marx 2013 ★; Fama-French 2015; Ang-Hodrick-Xing-Zhang 2006 ★ | Quality and low-vol long-only; show low-vol is a beta bet unless you neutralize |
| 138 | The factor zoo and publication decay: which characteristics survive honest tests | Harvey-Liu-Zhu 2016 (re-warm); McLean-Pontiff 2016 ★; Hou-Xue-Zhang 2020 ★ | Screen ~20 characteristics; Bonferroni / BH; measure post-publication fade |
| 139 | Building the benchmark you claim to beat: cap-weight vs equal-weight, reconstitution, float | Sharpe 1991 ◆; index methodology notes; Qian-Hua-Sorensen | Same book vs EW and vs cap-weight: show why "beat EW" is the easier exam |
| 140 | **Q1 checkpoint** — honest long-only factor notebook | JT 1993; FF; AMP 2013 | Point-in-time universe + total returns + 12-1 and value, IR vs a named benchmark, multiple-testing note |

### Q3 · Cross-sectional ML for ranking stocks (Units 141–150)
| # | Unit topic | Primary source | Lab / deliverable |
|---|-----------|----------------|-------------------|
| 141 | The prediction target at a monthly horizon: next-month residual, rank, or excess vs the benchmark | Gu-Kelly-Xiu 2020 ★; AFML Ch.3 (contrast with triple-barrier) | Three targets on the same features; compare IC and long-only IR |
| 142 | Point-in-time features: lagged returns, fundamentals, revisions, industry — no restated numbers | Green-Hand-Zhang 2017 ★; Gu-Kelly-Xiu 2020 ★; Bali-Engle-Murray | Build a PIT feature panel; plant a restated-earnings leak and catch it |
| 143 | Information coefficient, IC decay, and matching the rebalance to the decay | Grinold-Kahn Ch.6 ★; Qian-Hua-Sorensen | IC by holding week 1…8; pick a rebalance that matches the decay |
| 144 | Linear cross-sectional models: WLS, industry neutralization, residualizing size and beta | Fama-MacBeth 1973; Gu-Kelly-Xiu linear baseline ★ | Residualize features on industry + size + beta; measure IC lift |
| 145 | Tree models on the cross-section: GBDT as a regressor vs a ranker | Gu-Kelly-Xiu 2020 ★; Chen-Guestrin / Ke (re-warm 047) | LightGBM on next-month residual vs a linear model; purged walk-forward |
| 146 | Learning-to-rank for portfolios: pairwise / listwise losses that match "who beats whom" | Burges LambdaMART ◆; Liu LTR survey ◆ | LambdaMART (or LightGBM rank) vs MSE on the same panel; compare top-decile IR |
| 147 | Cross-sectional CV that respects time *and* names: year-blocks, purging, no future firm | AFML Ch.7 ★; Gu-Kelly-Xiu appendix | i.i.d. K-fold (leaks) vs walk-forward year-blocks; document the fake lift |
| 148 | Combining ML scores with classic factors: stacking, IC-weighting, orthogonalization | Grinold-Kahn Ch.11–14 ★; unit 049 | Blend linear + GBDT + 12-1; measure *incremental* IR, not just raw IR |
| 149 | When ML adds nothing: small monthly samples, regime breaks, feature death | Gu-Kelly-Xiu 2020 (what actually worked); McLean-Pontiff 2016 | Kill your own model on a 2015–2020 holdout; write the autopsy |
| 150 | **Q2 checkpoint** — leakage-free monthly ranker | Gu-Kelly-Xiu; AFML 7 | Features → GBDT → walk-forward IC/IR vs linear and 12-1; defend or kill |

### Q4 · Optimization: turning a score into a long-only book (Units 151–160)
| # | Unit topic | Primary source | Lab / deliverable |
|---|-----------|----------------|-------------------|
| 151 | From score to weight *without* an optimizer: top-N, quantile tilts, rank-weighted | Grinold-Kahn; Qian-Hua-Sorensen; `TEMPLATE_PORTFOLIO.md` | Top-50 vs rank-weight vs z-score tilt vs the same-score long-short; IR and turnover |
| 152 | Active weights and the one-period utility: more of what you like, minus risk, minus costs | Grinold-Kahn Ch.2, 14 ★; Markowitz (re-warm 081) | Solve a 10-name toy by hand, then as a quadratic program |
| 153 | Long-only as a constraint: why the optimizer clips, and what you lose vs long-short | Grinold-Kahn Ch.14–15 ★; Jacobs-Levy 140/30 ◆ | Same alpha, long-only vs long-short vs 140/30; measure the transfer coefficient |
| 154 | Risk models the optimizer trusts: fundamental (Barra-style) vs statistical vs shrinkage | Grinold-Kahn Ch.3 ★; units 082–083 | Plug three risk models into the same QP; compare active risk vs realized tracking error |
| 155 | Linear constraints real books have: sector, name, beta, turnover, number of names | Grinold-Kahn; Boyd-Vandenberghe (selected) ★; CVXPY | Add constraints one by one; watch tracking error and IR move |
| 156 | Cost-aware optimization: spread + impact, a turnover penalty, the capacity curve | Grinold-Kahn; Boyd et al. 2017 ★; unit 088 | Net IR vs turnover penalty; AUM at which monthly long-only IR hits your hurdle |
| 157 | Multi-period rebalancing: when *not* to trade (decaying alpha, today's cost) | Boyd et al. 2017 ★; Gârleanu-Pedersen 2013 ★ | Myopic vs multi-period with decaying alpha; count the skipped trades |
| 158 | Convex optimization toolkit: QP / SOCP, what stays convex, what a solver can promise | Boyd-Vandenberghe ★; OSQP / Clarabel docs | Formulate the book as a QP; show a non-convex variant that the solver cannot certify |
| 159 | Robust / resampled optimization: inputs are noisy, naïve MVO is brittle | Michaud; Ledoit-Wolf (re-warm); Fabozzi *Robust PO* ◆ | Perturb alphas; compare naïve MVO vs shrinkage vs resampled vs a simple tilt |
| 160 | **Q4 / Year-4 exit** — scores → constrained long-only book | Grinold-Kahn; Boyd 2017 | Optimizer takes Q2 scores + a risk model + costs + long-only/sector/beta constraints; defend *net* IR |

**Year 4 exit criterion:** you have a store that passes the leak tests (130) and
you can turn walk-forward scores into a constrained long-only book whose *net*
information ratio you can defend (160). You have not yet run the book through
drift, shortfall, and a crash — that is Year 5 Q1.

**◆ Optional (Year 4):** Cochrane *Asset Pricing* (full) · Fabozzi *Robust Portfolio
Optimization and Management* · Israel-Kelly-Moskowitz AQR practitioner papers.

---

## Year 5 — Defend the monthly book; research the daily book (Units 161–200)

**What each lesson must teach:** [reference/year-5-lessons.html](./reference/year-5-lessons.html).
Labs are not written yet.

**This year is extra time, not a replacement.** Q1 finishes the monthly book.
Q2–Q4 take the same long-only + ML + optimizer job and move the clock from
**weeks** to **hours and days** — what Lesson 001 called **mid-frequency**.

> Own stocks for **hours to a few days**. Do not borrow shares to bet they fall
> (**long-only**). Beat a **stated benchmark** after costs. Trading costs are the
> same order as the edge (the Q1 lab already showed this at a one-day hold).

**Prerequisite:** Year 4 (the store 121–130, the mandate 131, the optimizer 151–160)
plus Year 2 Q2 (validation), Year 2 Q3 (impact / ADV), and Year 3 Q2 (execution).

**Goal:** defend the monthly book to a PM who forbids shorts (170), then ship a
liquid, cost-first daily book through the optimizer (200). The full daily PM
defense is unit 210 (Year 6 Q1).

### Q1 · Run the monthly book and defend it (Units 161–170)
| # | Unit topic | Primary source | Lab / deliverable |
|---|-----------|----------------|-------------------|
| 161 | Between rebalances: weight drift, dividends, cash, corporate actions mid-month | Bali-Engle-Murray; CRSP notes | Simulate drift between monthly rebalances; split P&L into selection vs interaction |
| 162 | Getting into the names: implementation shortfall at a monthly horizon | Perold 1988 ★; Almgren-Chriss (re-warm 091–093) | TWAP the monthly trade list; paper IR vs net IR after shortfall |
| 163 | Index-futures overlay: long-only stocks + a short index future to control beta | Hull (futures mechanics); Grinold-Kahn | Same stock book, unhedged vs futures-hedged; report Sharpe *and* IR |
| 164 | Drawdowns you will eat: a long-only book rides market crashes | units 085–089; McNeil-Frey-Embrechts | 2008 and 2020 on long-only vs hedged; write the one-page client memo |
| 165 | Attribution: Brinson–Fachler, factor, and "what the optimizer actually bet" | Brinson-Hood-Beebower 1986 ★; Brinson-Fachler 1985 ★; Grinold-Kahn | Attribute a year of active return to allocation, selection, interaction, and beta |
| 166 | Capacity, crowding, and the live-vs-paper gap for slow equity | Korajczyk-Sadka; McLean-Pontiff; unit 088 | Scale AUM; find where net IR hits the hurdle; document crowding |
| 167 | Pre-register the research: write the kill criteria *before* you look | AFML research process; `TEMPLATE_PORTFOLIO.md` | One-page pre-registration of the capstone (universe, target, constraints, kill rules) |
| 168 | Failure modes specific to this mandate: leaked fundamentals, index-hugging, hidden beta, overfit optimizer | synthesis of 131–167 | Plant four bugs in a notebook; find them unaided |
| 169 | Overlays a real book meets: 140/30, restricted lists, tax-aware, ESG screens | Jacobs-Levy ◆; tax-aware / restricted-list notes | Add a restricted list and a 140/30 sleeve; measure IR and turnover change |
| 170 | **Q1 checkpoint — Monthly long-only capstone** | everything in 121–169; Y2 validation; Y3 Q1 | **End-to-end long-only book**: PIT universe → features → walk-forward ML ranker → constrained optimizer (risk + costs + no shorts) → net IR vs a named benchmark → capacity + attribution + proceed/kill memo, defended as to a PM who only allows longs |

### Q2 · The faster mandate and short-horizon baselines (Units 171–180)
| # | Unit topic | Primary source | Lab / deliverable |
|---|-----------|----------------|-------------------|
| 171 | Mid-frequency vs mid-horizon: same long-only rules, different clock; costs as a first-order term | Lesson 001; Grinold-Kahn (turnover); `TEMPLATE_PORTFOLIO.md` | Same scores, daily vs monthly rebalance; *net* IR after costs |
| 172 | The clock of a trading day: open, continuous session, close auction, overnight — which return you earn | Heston-Korajczyk-Sadka 2010 ★; Lou-Polk-Skouras 2019 ★ | Split open-to-close vs close-to-open P&L on a long-only book |
| 173 | Liquidity as a membership rule: ADV, spread, days-to-trade — who you are allowed to own | Amihud 2002 ★; Korajczyk-Sadka | Same signal, liquid-only vs all names; show the fake IR from illiquids |
| 174 | Short-horizon baseline I — cross-sectional reversal (1–5 day), long-only | Jegadeesh 1990 ★; Lehmann 1990 ★; Q1 lab `rev5` | Long-only top-decile reversal vs long-short; net of costs |
| 175 | Short-horizon baseline II — residual / industry-neutral reversal and residual momentum | Blitz-Huij-Martens ◆; Da-Qian-Warachka ◆ | Raw vs residual reversal; long-only IR |
| 176 | Event baseline — post-earnings announcement drift (PEAD), revisions, upgrades | Bernard-Thomas 1989/1990 ★; Livnat-Mendenhall | Long-only PEAD on a point-in-time earnings calendar; skip the timestamp leak |
| 177 | Overnight and close-auction effects: who you hold through the close | Lou-Polk-Skouras 2019 ★; Bogousslavsky ◆ | Hold-through-close vs flatten-at-close; net IR |
| 178 | News and text at a daily horizon (re-warm 075–076 as a ranker, not sentiment theater) | Loughran-McDonald; Tetlock 2007 ◆ | Next-day residual from a filing/news feature; long-only top-N |
| 179 | Combining short-horizon baselines; multiple testing when you have more trials | Harvey-Liu-Zhu (re-warm); unit 138 | Screen ~15 daily signals; BH; keep only what survives |
| 180 | **Q1 checkpoint** — daily long-only from reversal + PEAD | JT-short; Bernard-Thomas | Liquid PIT universe, net IR vs a named benchmark, costs first, multiple-testing note |

### Q3 · Daily / multi-day ML ranking (Units 181–190)
| # | Unit topic | Primary source | Lab / deliverable |
|---|-----------|----------------|-------------------|
| 181 | The prediction target at 1–5 days: next-day residual, open-to-close, or a short triple-barrier | AFML Ch.3 ★; contrast with unit 141 | Three daily targets on the same features; compare IC and long-only IR |
| 182 | Point-in-time daily features: lagged residuals, volume shocks, range, overnight gap — no same-day close in a close-to-close score | AFML Ch.2 ★; unit 142 | Plant a same-day-close leak; catch it |
| 183 | IC decay over hours and days: when a daily score dies | Grinold-Kahn Ch.6 ★; unit 143 | IC at close+1h, +1d, +5d; pick a hold that matches the decay |
| 184 | Overlapping daily labels and uniqueness (re-warm 038–039) | AFML Ch.4 ★ | Uniqueness weights on 5-day labels; unweighted vs weighted IC |
| 185 | Tree models on the daily cross-section: GBDT as regressor vs ranker | Gu-Kelly-Xiu methods ★; unit 145 | Daily LightGBM vs linear vs 5-day reversal; purged walk-forward |
| 186 | Short return-*paths* as features without becoming DeepLOB: aggregates vs a 20-day sequence | units 071–072; keep tabular unless sequence wins honestly | Path features vs aggregates; honest temporal split |
| 187 | Event-aware ML: flag earnings/news days so the model does not treat them as ordinary Tuesdays | Bernard-Thomas; AFML Ch.17 | Model with/without event flags; leftover PEAD |
| 188 | Two clocks, one research book: combining daily ML with Year-4 monthly scores | Grinold-Kahn Ch.11–14 ★ | Daily sleeve + monthly sleeve, both long-only; incremental IR |
| 189 | When daily ML is just reversal in costume | synthesis of 174–185 | Residualize the ML score on 5-day reversal; leftover IR |
| 190 | **Q2 checkpoint** — leakage-free daily ranker | AFML 3–4, 7; unit 185 | Features → GBDT → walk-forward IC/IR vs reversal and PEAD; defend or kill |

### Q4 · Optimization when you trade every day (Units 191–200)
| # | Unit topic | Primary source | Lab / deliverable |
|---|-----------|----------------|-------------------|
| 191 | Turnover is the strategy: why the Year-4 optimizer, run daily, goes broke | Boyd et al. 2017 ★; unit 156 | Monthly-tuned QP run every day; show cost death |
| 192 | Daily utility with a hard participation cap: do not take more than X% of ADV | Almgren; Grinold-Kahn; unit 064 | Participation constraint; names you wanted but could not buy |
| 193 | Intraday vs close-only rebalance: two optimizations per day or one | Cartea et al.; Boyd 2017 | Close-only vs open+close rebalance; net IR |
| 194 | Temporary impact on a daily trade list: the square-root law at this size | Almgren et al. 2005 ★; unit 064 | Paper vs impact-adjusted IR as AUM grows |
| 195 | Liquidity-aware risk: names that look diversifying until you have to exit | Amihud 2002; Kyle (re-warm 067) | Stressed 5-day liquidation of the long-only book |
| 196 | Beta control without shorts: a daily index-futures overlay on a high-turnover stock book | unit 163; Hull | Unhedged vs daily-hedged; Sharpe vs IR; futures roll cost |
| 197 | Multi-period daily: Gârleanu–Pedersen with a 1–5 day half-life | Gârleanu-Pedersen 2013 ★; Boyd 2017 ★ | Myopic daily vs smoothed; count the turnover you skipped |
| 198 | Auction-aware execution: how much of the trade list goes to the close | Perold 1988; Kissell ◆ | Close-auction vs TWAP the list; implementation shortfall |
| 199 | Capacity is smaller than Year 4: the AUM curve at daily turnover | unit 166; Korajczyk-Sadka | Capacity curve, daily long-only vs monthly long-only, same capital |
| 200 | **Q4 / Year-5 exit** — daily scores → ADV-capped, impact-aware, optionally futures-hedged book | Boyd; Almgren | Defend *net* IR; show the AUM where it dies |

**Year 5 exit criterion:** the monthly book is defended (170), and you can turn
daily scores into an ADV-capped, impact-aware book whose *net* IR you can
defend (200). Overnight-gap autopsy and the two-sleeve NAV come in Year 6 Q1.

**◆ Optional (Year 5):** Kissell *The Science of Algorithmic Trading* · full Tetlock /
news-alpha literature after the PEAD baseline is honest · overnight-only or
open-to-close-only specialist sleeves (only after the close-to-close capstone is honest).

---

## Year 6 — Defend the daily book; paper and live (Units 201–240)

**What each lesson must teach:** [reference/year-6-lessons.html](./reference/year-6-lessons.html).
Labs are not written yet. This year is extra time.

Q1 finishes the faster book. Q2–Q4 are the desk: the same functions live as in
the backtest, a paper loop, a kill switch, a tiny live book.

> A loop that turns the store into orders, a ledger that adds up, and a button
> that stops you.

**Study order is the unit numbers.** Do not skip 121–130. Do not paper-trade
before 210 is honest.

### Q1 · Run the daily book and defend it (Units 201–210)
| # | Unit topic | Primary source | Lab / deliverable |
|---|-----------|----------------|-------------------|
| 201 | Overnight gap risk: you are long into the open | Lou-Polk-Skouras 2019; unit 164 | Overnight vs intraday contribution; a gap-day autopsy |
| 202 | Corporate actions and dividends on a daily book (more events per hold) | unit 161; Bali-Engle-Murray | Miss a split; show the P&L lie |
| 203 | Live-vs-paper at this clock: stale scores, late features, dropped prints | unit 101; AFML point-in-time | Delay features by one bar; measure IR death |
| 204 | Attribution for a daily long-only: selection vs timing vs cost vs beta | Brinson 1985/86; Grinold-Kahn | Attribute a quarter of daily active return |
| 205 | Crowding and the reversal crowded-trade: when everyone fades yesterday | Lou-Polk; McLean-Pontiff | Post-2009 reversal fade; write the memo |
| 206 | Pre-register the daily capstone: kill criteria before you look | unit 167; `TEMPLATE_PORTFOLIO.md` | One-page pre-registration (universe, hold, ADV cap, kill rules) |
| 207 | Failure modes: same-day leak, ADV-blind optimizer, closet indexer, cost-free Sharpe | synthesis of 171–206 | Plant four bugs in a notebook; find them unaided |
| 208 | Two-sleeve NAV: Year-4 monthly + Year-5 daily, one long-only book | Grinold-Kahn blend | Combine sleeves; joint IR, correlation of actives, capacity |
| 209 | Overlays: 140/30 or futures-hedged "synthetic market-neutral" while cash stays long-only | Jacobs-Levy ◆; unit 163 | Same names, three mandates; what IR and Sharpe each claim |
| 210 | **Q1 checkpoint — Daily long-only capstone** | everything in 121–209; Y2 validation | **End-to-end daily long-only book**: liquid PIT universe → 1–5 day ML ranker → ADV-and-cost-aware optimizer (no shorts) → net IR vs a named benchmark → capacity vs the Year-4 book → attribution + proceed/kill memo, defended as to a PM who only allows longs and rebalances often |

### Q2 · Research/prod parity (Units 211–220)
| # | Unit topic | Primary source | Lab / deliverable |
|---|-----------|----------------|-------------------|
| 211 | One code path: backtest calls the same functions as live | unit 109 | Plant a private backtest score; catch it |
| 212 | Score job: scheduled, logged, replayable | — | Same inputs ⇒ same scores |
| 213 | Optimizer job: constraints as dated config | units 155, 192 | Config mismatch backtest vs live |
| 214 | Order list a broker accepts: name, side, qty, type | Hull; broker docs | Weights → share orders, long-only |
| 215 | Fill model vs live fills as a standing table | Perold 1988 | Predicted vs realized shortfall |
| 216 | Position and cash ledger: cash + stock = NAV | — | Broken identity is a halt |
| 217 | Corporate actions on the live book (not only the panel) | unit 122 | Missed overnight split |
| 218 | Calendar: holidays, half-days, auction times | exchange calendars | Job on a closed day |
| 219 | Replay from config + store revision + git hash | unit 109 | Rebuild Tuesday's book |
| 220 | **Q2 checkpoint** — backtest and live agree on one morning | 211–219 | Same scores, weights, orders |

### Q3 · Broker, paper, risk (Units 221–230)
| # | Unit topic | Primary source | Lab / deliverable |
|---|-----------|----------------|-------------------|
| 221 | Broker mechanics: account, cash, buying power, rejects | broker docs | Cash-only long-only; why orders still reject |
| 222 | Order types: MKT, LMT, MOC, LOC | unit 093; exchange docs | Which type each clock uses |
| 223 | Close auction operationally: imbalance, cutoffs | unit 198 | Late MOC is a missed trade |
| 224 | Paper-trading loop: store → score → orders → fills → ledger | synthesis | The loop in objects, not a backtest relabel |
| 225 | Reconciliation: ledger vs broker vs fills | — | Daily match; break ⇒ no new orders |
| 226 | Kill switch and risk limits on the order path | unit 089 | Planted breach must refuse or flatten |
| 227 | Slippage tracking: predicted vs realized | units 215, 162 | Weekly read of the gap |
| 228 | Restricted lists and compliance holds | unit 169 | Hard zero in optimizer *and* broker |
| 229 | Shape of the trading day: cutoffs for each clock | — | Written clock: T1…T5 |
| 230 | **Q3 checkpoint** — a reconciled week of paper | 224–227 | Five days, one kill test, not five backtest days |

### Q4 · Small live and the ops capstone (Units 231–240)
| # | Unit topic | Primary source | Lab / deliverable |
|---|-----------|----------------|-------------------|
| 231 | Going live small: tiny AUM, one sleeve, written abort | — | First-week rules |
| 232 | Monitoring: expected vs realized IR, turnover, rejects | — | Dashboard as a list of comparisons |
| 233 | Incident log: missed auction, stale feature, wrong split | — | Cause, P&amp;L, fix, test |
| 234 | Two-frequency ops on one NAV | unit 208 | Shared ADV and cash |
| 235 | Vendor outage and fallback | — | Skip / flatten / labeled stale — never a silent guess |
| 236 | Tax lots / after-tax as an overlay (awareness) | — | Do not rewrite the pre-tax book |
| 237 | Pre-register the live trial | units 167, 206 | Duration, AUM, abort, 'paper was a lie' |
| 238 | Failure modes of going live | synthesis | Four planted operational bugs |
| 239 | The runbook | — | Times, halt, who to call |
| 240 | **Q4 / Year-6 exit — Capstone** | 121–239; Y4; Y5 | 20 paper (or tiny live) days: store + replay + reconcile + kill test + proceed/kill |

**Year 6 exit criterion:** you can answer a PM who asks "can we turn this on Monday?"
with a daily book you have already defended (210), a morning where backtest=live,
a reconciled paper stretch, a tested kill switch, and a runbook — for a long-only
book on either clock.

**◆ Optional (Year 6):** a specific broker's API (IBKR paper, etc.) only after the
objects in 221–226 are solid without brand names · after-tax lots only after 240 is
honest pre-tax.

---

## Interview prep runs the WHOLE way, not just Y3 Q4

Y3 Q4 is the *concentration*, not the start. From Year 1, keep a standing weekly habit
(≈2–3 h/week, drawn from strong days — never from a lab or checkpoint):
- **Weekly:** 10 mental-math drills + 5 probability brainteasers (Green Book / Heard on the Street).
- **Weekly from Y1 Q1:** 3–5 LeetCode problems (easy→medium), rotating arrays → DP → graphs → trees. You are a strong programmer already; keep the muscle warm and quant-flavored.
- **After each math/pricing unit:** add one derivation you can now do from memory to a running "derivations I own" list in NOTES.md.

This spacing is deliberate (see the `teach` skill's storage-strength note): distributed practice
beats a Year-3 cram.

## Currency rule (quarterly)

At the **start of each quarter**, spend one session checking whether the *frontier* units
(tabular foundation models, deep LOB, RL for execution, backtest-overfitting tooling,
cross-sectional ML for monthly *and* daily equity) have a new SOTA or a newly-exposed
failure mode. Update [RESOURCES.md](./RESOURCES.md) and the affected unit rows. The
**core canon** (Shreve, AFML, Grinold-Kahn, Qian-Hua-Sorensen, Almgren-Chriss, Cont
microstructure, Gu-Kelly-Xiu as the monthly ML baseline, Jegadeesh/Lehmann +
Bernard-Thomas as the daily baselines) is stable — do not churn it. Only promote a new
paper to ★ if it sets SOTA, exposes a real failure mode, or is a baseline you will be
measured against.
