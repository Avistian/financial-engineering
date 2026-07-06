# Expert Curriculum — Quantitative Research (Systematic Trading)

Agent-facing plan for lesson sequencing. The student-facing version is
[reference/curriculum.html](./reference/curriculum.html).

**Pace:** ~1.5–2 hours/day **baseline** · ~600–700 hours/year · **~2,000 hours over 3 years.**
Center of gravity: **Quant Researcher / systematic alpha** (stats, ML, signals, validation,
backtesting). QT (pricing, microstructure) and QD (systems, latency) are covered to the depth a
top QR needs to collaborate and interview — not as separate careers.

### Why 120 units take 3 years (read this if the math looks off)

A common, correct objection: *120 lessons ÷ 365 days ≈ 4 months — so at one lesson/day this is
a one-year plan, not three.* That objection is right about **reading** and wrong about
**mastery**. Stop treating a numbered row as "one day."

**A unit ≠ a day.** Each numbered row below is a **unit** = one concept *plus its lab/reproduction
work plus its quiz/checkpoint*. Units are not uniform:

| Unit type | Sessions to finish | Where |
|-----------|--------------------|-------|
| Concept lesson (read + quiz) | 1–3 sessions | dense in Y1 |
| Derivation / math unit (prove it, then code it) | 2–5 sessions | Y1 Q2, interview prep |
| Lab / reproduction unit (build, tune, debug, re-run) | 4–12 sessions | dominant Y2–Y3 |
| Checkpoint / exit exam | 3–6 sessions | end of each quarter/year |
| Capstone (project + write-up + defense) | 20–40+ sessions | Y3 Q4 |

**Where the ~2,000 hours actually go** (lessons are a small slice of the clock):

| Activity | ≈ hours | Share |
|----------|---------|-------|
| Lesson content itself (120 × ~0.75h) | ~90 | ~5% |
| Deep primary-source reading (books + ~40 core papers) | ~350 | ~18% |
| **Hands-on labs & reproduction** (pricing, ML pipelines, LOB, backtests) | ~850 | ~43% |
| Checkpoints + year exit exams | ~160 | ~8% |
| Spaced retrieval / review | ~150 | ~7% |
| **Interview drilling** (mental math, brainteasers, LeetCode) — runs *throughout*, concentrated in Y3 Q4 | ~200 | ~10% |
| **Year-3 capstone** (project + write-up + defense) | ~200 | ~10% |

**Density curve (front-loaded learning, back-loaded building):**
- **Year 1** — concept- and derivation-dense. Units arrive ~2–3/week. This is the only phase where "lessons/week" is the right mental model. You are buying vocabulary, the stochastic-calculus toolkit, and *evaluation discipline*.
- **Year 2** — reproduction-heavy. ~1 unit/week; each is days of feature engineering, model fitting, and — above all — validation. This is the heart of the QR craft.
- **Year 3** — build- and interview-dominated. Portfolio construction, execution, systems awareness, then the interview gauntlet and a capstone whose calendar is set by experiments and writing, not reading.

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
| 029 | Multivariate volatility & covariance: DCC, EWMA, the dimensionality curse (preview RMT) | Tsay Ch.10 | EWMA cov of a small panel |
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
| 082 | Random Matrix Theory: the Marčenko-Pastur law, eigenvalue cleaning | Laloux et al. 1999; Bouchaud-Potters ★ | MP fit; separate signal eigenvalues |
| 083 | Ledoit-Wolf covariance shrinkage & denoising | Ledoit-Wolf 2004 ★; *ML for Asset Managers* Ch.2 | **Lab:** shrink & denoise a cov matrix |
| 084 | Factor models & risk decomposition: Barra-style, PCA factors, idiosyncratic risk | Grinold-Kahn Ch.3 ★ | Decompose portfolio risk |
| 085 | The Fundamental Law of Active Management: IC, breadth, transfer coefficient | Grinold-Kahn Ch.6 ★ | Compute IC & IR of a signal |
| 086 | Signal combination & alpha blending: ensembling signals vs models | Grinold-Kahn Ch.11–14 | Combine 3 signals; measure lift |
| 087 | Hierarchical Risk Parity (HRP) & robust allocation | López de Prado 2016 ★ | HRP vs MVO out-of-sample |
| 088 | Transaction costs & capacity: turnover, slippage, alpha decay, strategy capacity | Grinold-Kahn; Kyle/impact | Net-of-cost Sharpe & capacity curve |
| 089 | Risk management & drawdown: VaR/ES caveats, stress, regime-aware sizing | Hull Risk Mgmt; McNeil-Frey-Embrechts | Backtest a drawdown-control overlay |
| 090 | **Q1 checkpoint** — build a portfolio | Grinold-Kahn; LdP | Denoised, cost-aware portfolio from multiple signals; report net Sharpe & capacity |

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
original, leakage-free, capacity-aware strategy — and you can pass the mental-math, probability,
derivation, and coding gauntlet that gets the offer.

**◆ Optional (Year 3):** Narang *Inside the Black Box* · Chan *Quantitative Trading* / *Algorithmic
Trading* · Cartea-Jaimungal-Penalva full text · *Designing Data-Intensive Applications* (systems depth).

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
(tabular foundation models, deep LOB, RL for execution, backtest-overfitting tooling) have a new
SOTA or a newly-exposed failure mode. Update [RESOURCES.md](./RESOURCES.md) and the affected unit
rows. The **core canon** (Shreve, AFML, Grinold-Kahn, Almgren-Chriss, Cont microstructure) is
stable — do not churn it. Only promote a new paper to ★ if it sets SOTA, exposes a real failure
mode, or is a baseline you will be measured against.
