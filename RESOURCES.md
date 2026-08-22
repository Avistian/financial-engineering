# Quantitative Research Resources

The curated, high-trust source set for this mission. Knowledge for lessons is drawn from here —
not from parametric guesses. Wisdom (judgment, taste, war stories) comes from the communities at
the bottom. Annotate every entry: what it covers, when to reach for it.

Tiers match [CURRICULUM.md](./CURRICULUM.md): **★ Core** (required, reproduce or beat) ·
**◆ Optional** (skim after core work).

---

## Knowledge — Books (the canon)

### Math foundations (linear algebra, statistics)
- ★ **Strang — *Introduction to Linear Algebra*** (Wellesley-Cambridge). Eigen-thinking as geometry; symmetric matrices, the spectral theorem, and PCA. His MIT **18.06** lectures cover the same ground free online. Use for: Year 1 Q1 (unit 008) and every covariance/PCA/risk-model unit after.
- ◆ **Axler — *Linear Algebra Done Right***. Clean, proof-first treatment of the spectral theorem (symmetric ⇒ real eigenvalues + orthogonal eigenvectors). Reach for when you want the theorem stated and proved, not just applied.
- ★ **Wasserman — *All of Statistics*** (Springer). Fast, rigorous coverage of probability, estimation, inference, and hypothesis testing. Use for: Year 1 Q1 (units 005–007).
- ★ **Wooldridge — *Introductory Econometrics: A Modern Approach*** (Cengage). The standard, readable regression text: simple/multiple OLS, the Gauss–Markov assumptions, and — foregrounded — heteroskedasticity and robust standard errors. Use for: Year 1 Q1 (unit 009) and every signal/factor regression after.

### Stochastic calculus & pricing
- ★ **Shreve — *Stochastic Calculus for Finance II: Continuous-Time Models*** (Springer, 2004).
  The standard bridge for a strong-math student new to SDEs. Use for: Brownian motion, Itô, Girsanov, BS PDE, Feynman-Kac (Year 1 Q2). **Ch. 5 is the primary source for unit 015**: the Radon–Nikodym derivative process (§5.2), the **Girsanov theorem** (§5.2.2), the **martingale representation theorem** (§5.3 — the continuous-time guarantee that a replicating strategy exists), and risk-neutral pricing with the **market price of risk** `θ = (μ−r)/σ` (§5.4). **Ch. 6 is the primary source for unit 016**: the Black–Scholes PDE from the discounted-martingale argument (§6.2–6.3) and the **Feynman–Kac theorem** (§6.4) that identifies the PDE solution with the discounted $Q$-expectation. The hedge-and-no-arbitrage derivation is the same algebra in a different order.
- ◆ **Shreve — *Volume I: The Binomial Asset Pricing Model***. Discrete warm-up; read first if Vol II feels abrupt. Ch. 2 covers information, conditional expectation and martingales in pure discrete time — the gentler entrance to unit 011. **Ch. 1–2** is also the discrete warm-up for unit 015: replication on a one-period tree, the risk-neutral probability `p* = (R−d)/(u−d)`, and the change of measure with everything visible on paper before Girsanov generalises it.
- ◆ **Baxter & Rennie — *Financial Calculus***. Gentler, intuition-first companion to Shreve. §3.1–3.3 for filtrations/measure change with minimal formalism; **Ch. 3** gives the Itô calculus (the lemma and the stock model) with far less measure-theoretic scaffolding than Shreve — the softer on-ramp to unit 013.
- ◆ **Wilmott — *Paul Wilmott Introduces Quantitative Finance*** (Wiley). The most hand-holding, picture-heavy derivation of Itô's lemma and the Black–Scholes argument in print; light on rigor, heavy on intuition. Reach for it if Shreve II Ch.4 feels abstract (unit 013). Shreve II **Ch.4 §4.2–4.4** is the primary source for unit 013 (the Itô integral as a martingale, the Itô–Doeblin formula, and the `d(log S)` / GBM example).
- ◆ **Williams — *Probability with Martingales*** (CUP, 1991). The compact, rigorous treatment of measure-theoretic probability built around martingales: σ-algebras, conditional expectation as an L² projection, and the convergence theorems. Reach for it when you want a *proof* rather than Shreve's finance-first exposition (units 011–012).
- ◆ **Mörters & Peres — *Brownian Motion*** (CUP, 2010; draft free online). The modern, rigorous-but-readable reference on Brownian motion itself: construction, path properties (continuity, nowhere-differentiability), quadratic variation, the strong Markov property and the reflection principle. Reach for it when Shreve Ch.3 feels too terse (unit 012). Shreve II **Ch.3 §3.2–3.4** is the primary source for unit 012 (scaled random walk → BM, the martingale property, and `[W]_t = t`).
- ★ **Øksendal — *Stochastic Differential Equations: An Introduction with Applications*** (Springer, 6th ed.). The cleanest standalone treatment of SDEs: what an SDE means, the **existence & uniqueness theorem** (Ch. 5 §5.2 — the Lipschitz + linear-growth conditions), and the GBM/Ornstein–Uhlenbeck examples solved by integrating factor. Primary source for unit 014 (**§5.1–5.2**); Shreve II **§4.4–4.5** is the finance-flavoured companion (GBM solve; the Vasicek/OU rate model appears later in Shreve Ch.6).
- ★ **Hull — *Options, Futures, and Other Derivatives***. The market-mechanics + Greeks reference. Use for: instruments, hedging, risk (Y1 Q1, Q2).
- ◆ **Glasserman — *Monte Carlo Methods in Financial Engineering***. Use for: variance reduction, MC pricing (unit 019).
- ◆ **Cont & Tankov — *Financial Modelling with Jump Processes***. Advanced jumps (unit 018).

### Financial ML & validation (the heart of the QR job)
- ★ **López de Prado — *Advances in Financial Machine Learning* (AFML)** (Wiley, 2018). The single most important book here. Bars (Ch.2), triple-barrier + meta-labeling (Ch.3), sample weights (Ch.4), fractional differentiation (Ch.5), ensembles (Ch.6), **purged/embargoed CV (Ch.7)**, feature importance (Ch.8), hyper-tuning (Ch.9), bet sizing (Ch.10), backtesting + **CPCV (Ch.11–12)**, structural breaks (Ch.17), entropy (Ch.18). Use it all Year 1 Q4 → Year 2 Q2.
- ★ **López de Prado — *Machine Learning for Asset Managers*** (CUP, 2020). Denoising/detoning covariance (Ch.2), clustered feature importance (Ch.6). Use for: Y2 Q1 and Y3 Q1 (RMT/shrinkage).
- ◆ **Dixon, Halperin & Bilokon — *Machine Learning in Finance***. Broader ML-in-finance reference, incl. RL.

### Time series & volatility
- ★ **Tsay — *Analysis of Financial Time Series*** (Wiley). Stationarity, ARMA, GARCH, cointegration, multivariate vol. Year 1 Q3.

### Microstructure
- ★ **Bouchaud, Bonart, Donier & Gould — *Trades, Quotes and Prices*** (CUP, 2018). The modern microstructure/LOB bible: book mechanics, impact, the square-root law. Year 2 Q3.
- ◆ **O'Hara — *Market Microstructure Theory***. Classic theory: adverse selection, spread decomposition.

### Portfolio construction & risk
- ★ **Grinold & Kahn — *Active Portfolio Management*** (2nd ed.). The Fundamental Law, IC/breadth, factor risk, alpha combination. Year 3 Q1 and the on-ramp to Year 4 (units 121, 133, 142–146, 155).
- ★ **Qian, Hua & Sorensen — *Quantitative Equity Portfolio Management*** (Chapman & Hall). The practitioner book for **long-only, benchmark-relative** equity: active return, tracking error, information ratio, IC decay, and turning a score into a constrained book. Primary Year-4 companion (units 121, 129, 133, 141).
- ★ **Boyd & Vandenberghe — *Convex Optimization*** (CUP; free online). What a quadratic / second-order-cone program *is*, why convexity lets a solver certify a solution, and how to write constraints so they stay convex. Use selected chapters for Year 4 Q3 (units 145, 148).
- ★ **Boyd, Busseti, Diamond, Kahn, Koh, Nystrup & Speth — *Multi-Period Trading via Convex Optimization*** (Foundations & Trends in Optimization, 2017; free preprint). The clean modern statement of “maximize expected return − risk − costs” over several rebalances, including when *not* to trade. Primary source for units 146–147.
- ★ **Bali, Engle & Murray — *Empirical Asset Pricing: The Cross Section of Stock Returns*** (Wiley). The handbook for building a point-in-time stock universe, total returns, and characteristic-sorted portfolios without the usual CRSP traps. Year 4 Q1 (units 122–124, 132).
- ◆ **Cochrane — *Asset Pricing*** (Princeton, revised). Discount-factor view of the cross-section; Ch.12 is the Fama–MacBeth companion (unit 124).
- ◆ **Fabozzi, Kolm, Pachamanova & Focardi — *Robust Portfolio Optimization and Management***. When Markowitz inputs are noisy (they always are). Unit 149.
- ◆ **Bouchaud & Potters — *Theory of Financial Risk and Derivative Pricing***. RMT for covariance cleaning.
- ★ **McNeil, Frey & Embrechts — *Quantitative Risk Management*** (Princeton). Copulas (Ch.5–7), VaR/ES, risk aggregation. Core for units 085–086 and 089.
- ◆ **Nelsen — *An Introduction to Copulas*** (Springer). Gentler mathematical companion to MFE when Sklar/margins need a slower pass.

### Execution, market making & RL
- ★ **Cartea, Jaimungal & Penalva — *Algorithmic and High-Frequency Trading*** (CUP). Execution, impact, market making, the math of Year 3 Q2.
- ★ **Sutton & Barto — *Reinforcement Learning: An Introduction* (2nd ed.)**. Free online. MDPs, Q-learning, policy gradients. Year 3 Q2.

### Deep learning
- ★ **Goodfellow, Bengio & Courville — *Deep Learning*** (free online). Sequence models, regularization. Year 2 Q4.

### Systems & performance (awareness track)
- ◆ **Gorelick & Ozsvald — *High Performance Python***. Profiling, numba, vectorization. Unit 103.
- ◆ **Meyers — *Effective Modern C++*** / **the Rust Book**. For the C++/Rust units 105–106.
- ◆ **Kleppmann — *Designing Data-Intensive Applications*** (DDIA). Data systems for the system-design interview.

### Interview prep
- ★ **Zhou — *A Practical Guide to Quant Finance Interviews* ("the Green Book")**. The canonical drill book: brainteasers, probability, stochastic calc, coding. Year 3 Q4 + weekly throughout.
- ★ **Crack — *Heard on the Street: Quantitative Questions from Wall Street Job Interviews***. Companion puzzle bank.
- ★ **Aziz — *Elements of Programming Interviews (EPI)*** (Python edition) + **LeetCode**. Coding gauntlet.

---

## Knowledge — Papers (★ core, ◆ optional). Read in the year they appear.

### Statistics of markets / overfitting
- ★ Cont (2001), *Empirical properties of asset returns: stylized facts and statistical issues.* — the 5 stylized facts (unit 004).
- ★ Harvey, Liu & Zhu (2016), *…and the Cross-Section of Expected Returns.* — multiple-testing in finance (unit 007).
- ★ Newey & West (1987), *A Simple, Positive Semi-Definite, Heteroskedasticity and Autocorrelation Consistent Covariance Matrix*, Econometrica 55(3):703–708. — HAC standard errors for regressions with serially correlated / overlapping-return errors (unit 009). Companion: White (1980), *A Heteroskedasticity-Consistent Covariance Matrix Estimator*, Econometrica 48(4):817–838.
- ★ Bailey & López de Prado (2014), *The Deflated Sharpe Ratio.* — unit 055.
- ★ Bailey, Borwein, López de Prado & Zhu (2014/2015), *The Probability of Backtest Overfitting.* — unit 056.

### Volatility & time series
- ★ Andersen, Bollerslev, Diebold & Labys (2003), *Modeling and Forecasting Realized Volatility.* — unit 024.
- ★ Corsi (2009), *A Simple Approximate Long-Memory Model of Realized Volatility (HAR-RV).* — unit 025.
- ★ Engle & Granger (1987), *Co-integration and Error Correction.* — unit 027.
- ★ Avellaneda & Lee (2010), *Statistical Arbitrage in the U.S. Equities Market.* — unit 028.
- ◆ Barndorff-Nielsen & Shephard (2004), bipower variation / jump detection — unit 026.

### Microstructure
- ★ Cont, Kukanov & Stoikov (2014), *The Price Impact of Order Book Events.* — OFI (unit 062).
- ★ Cont, Cucuringu & Zhang (2023), *Cross-impact of order flow imbalance in equity markets* (arXiv **2112.13213**; Quant. Finance 2023). — MLOFI / integrated OFI via PCA (unit 063).
- ★ Almgren, Thum, Hauptmann & Li (2005), *Direct Estimation of Equity Market Impact.* — square-root law (unit 064).
- ★ Bacry, Mastromatteo & Muzy (2015), *Hawkes Processes in Finance.* — units 065–066.
- ★ Kyle (1985), *Continuous Auctions and Insider Trading*; Glosten & Milgrom (1985), *Bid, Ask and Transaction Prices…* — adverse selection (unit 067).
- ◆ Byrd, Hybinette & Balch, *ABIDES: Agent-Based Interactive Discrete Event Simulation* — LOB simulator (units 069, 099).

### Machine learning / deep learning
- ★ Chen & Guestrin (2016), *XGBoost*; Ke et al. (2017), *LightGBM.* — unit 047.
- ★ Breiman (2001), *Random Forests.* — unit 046.
- ★ Vaswani et al. (2017), *Attention Is All You Need.* — unit 072.
- ★ Zhang, Zohren & Roberts (2019), *DeepLOB: Deep Convolutional Neural Networks for Limit Order Books*, IEEE TSP 67(11):3001–3012 (SSRN 3519855). — units 073, 080.
- ★ Grinsztajn, Oyallon & Varoquaux (2022), *Why do tree-based models still outperform deep learning on tabular data?* — unit 077.
- ★ Gorishniy et al. (2021), *Revisiting Deep Learning Models for Tabular Data* (FT-Transformer). — unit 077.
- ★ Hollmann et al. (2023), *TabPFN.* — unit 078.
- ★ Ma et al. (2024), *TabDPT: Scaling Tabular Foundation Models on Real Data* (arXiv **2410.18164**; NeurIPS 2025). — unit 078.
- ★ Loughran & McDonald (2011), *When Is a Liability Not a Liability? Textual Analysis, Dictionaries, and 10-Ks.* — finance NLP (unit 075).
- ◆ Araci (2019), *FinBERT.* — unit 076.

### Portfolio / risk
- ★ Markowitz (1952), *Portfolio Selection.* — unit 081.
- ★ Laloux, Cizeau, Bouchaud & Potters (1999), *Noise Dressing of the Financial Correlation Matrix* (RMT). — unit 082.
- ★ Ledoit & Wolf (2004), *A well-conditioned estimator for large-dimensional covariance matrices.* — unit 082.
- ★ Embrechts, McNeil & Straumann (2002), *Correlation and Dependence in Risk Management: Properties and Pitfalls.* — why linear correlation is not enough (unit 085).
- ★ López de Prado (2016), *Building Diversified Portfolios that Outperform Out of Sample* (HRP). — unit 087.
- ◆ Li (2000), *On Default Correlation: A Copula Function Approach.* — the Gaussian-copula CDO formula; taught as a **failure-mode case study**, not a method to copy (unit 086).

### Empirical asset pricing / long-only mid-horizon equity (Year 4)
- ★ Fama & MacBeth (1973), *Risk, Return, and Equilibrium: Empirical Tests.* — the cross-section regression that is still the first linear baseline (units 124, 134).
- ★ Jegadeesh & Titman (1993), *Returns to Buying Winners and Selling Losers.* — 3–12 month cross-sectional momentum; the 12-1 construction (skip the most recent month) is the Year-4 baseline (unit 125).
- ★ Fama & French (1992), *The Cross-Section of Expected Stock Returns*; (1993) *Common Risk Factors…*; (2015) *A Five-Factor Asset Pricing Model.* — value, size, profitability, investment as the characteristics a long-only book must beat or own honestly (units 126–127).
- ★ Asness, Moskowitz & Pedersen (2013), *Value and Momentum Everywhere.* — the two classic premia in one paper, including why they hedge each other (units 125–126).
- ★ Novy-Marx (2013), *The Other Side of Value: The Gross Profitability Premium.* — quality / profitability as a characteristic, not a vibe (unit 127).
- ★ Ang, Hodrick, Xing & Zhang (2006), *The Cross-Section of Volatility and Expected Returns.* — low-volatility in the cross-section; the trap is that it is often a hidden beta bet (unit 127).
- ★ McLean & Pontiff (2016), *Does Academic Research Destroy Stock Return Predictability?* — publication decay: a characteristic's edge shrinks after the paper comes out (units 128, 139, 156).
- ★ Hou, Xue & Zhang (2020), *Replicating Anomalies.* — most of the "factor zoo" does not replicate under a common protocol (unit 128).
- ★ Green, Hand & Zhang (2017), *The Characteristics that Provide Independent Information for the Cross-Section of Stock Returns.* — which of ~90 characteristics are not just the same few bets renamed (unit 132).
- ★ Gu, Kelly & Xiu (2020), *Empirical Asset Pricing via Machine Learning.* — the baseline paper for *monthly* cross-sectional ML (trees, nets) versus a linear model. Year 4 Q2's "must beat or match honestly" result (units 131–135, 139–140).
- ★ Gârleanu & Pedersen (2013), *Dynamic Trading with Predictable Returns and Transaction Costs.* — the continuous-time reason a decaying signal plus costs says "don't fully chase today's alpha" (unit 147).
- ★ Perold (1988), *The Implementation Shortfall: Paper versus Reality.* — the gap between the paper book and the fills you actually get (unit 152).
- ★ Brinson, Hood & Beebower (1986), *Determinants of Portfolio Performance*; Brinson & Fachler (1985), *Measuring Non-U.S. Equity Portfolio Performance.* — allocation vs selection vs interaction (unit 155).
- ◆ Moskowitz, Ooi & Pedersen (2012), *Time Series Momentum.* — trend on an asset versus cash, not winner-vs-loser (unit 125).
- ◆ Sharpe (1991), *The Arithmetic of Active Management.* — why beating the cap-weight index, after fees, is a zero-sum exam (unit 129).
- ◆ Jacobs & Levy, *20 Myths about 130/30* (and related 130/30 notes). — the "a little short sleeve" overlay, not the Year-4 default mandate (units 143, 159).
- ◆ Burges, *From RankNet to LambdaRank to LambdaMART* (Microsoft Research). — pairwise / listwise ranking losses when the job is "who beats whom," not "predict the exact return" (unit 136).
- ◆ Korajczyk & Sadka (2004/2008), liquidity / momentum capacity. — what happens to a slow equity signal when AUM grows (units 156, 189).

### Long-only mid-frequency equity (Year 5)
- ★ Jegadeesh (1990), *Evidence of Predictable Behavior of Security Returns.* — 1-month (and shorter) cross-sectional reversal: yesterday's losers bounce. Year 5's first baseline; the Q1 lab's `rev5` without the shorts (unit 164).
- ★ Lehmann (1990), *Fads, Martingales, and Market Efficiency.* — the companion short-horizon reversal paper (unit 164).
- ★ Bernard & Thomas (1989), *Post-Earnings-Announcement Drift: Delayed Price Response or Risk Premium?*; (1990) *Evidence that Stock Prices Do Not Fully Reflect the Implications of Current Earnings for Future Earnings.* — PEAD: the market is slow to digest earnings. The event baseline a daily long-only book must beat or own honestly (units 166, 177).
- ★ Amihud (2002), *Illiquidity and Stock Returns.* — a simple liquidity measure (average |return| / dollar volume). Year 5 uses it as a *membership rule*, not as a premium to harvest blindly (units 163, 185).
- ★ Heston, Korajczyk & Sadka (2010), *Intraday Patterns in the Cross-Section of Stock Returns.* — the trading day is not one return; open, midday, and close have different cross-sections (unit 162).
- ★ Lou, Polk & Skouras (2019), *A Tug of War: Overnight Versus Intraday Expected Returns.* — who you hold through the close is a different bet from who you hold from open to close (units 162, 167, 191).
- ◆ Tetlock (2007), *Giving Content to Investor Sentiment: The Role of Media in the Stock Market.* — daily text as a feature, with the usual overfitting trap (unit 168).
- ◆ Livnat & Mendenhall (2006), *Comparing the Post–Earnings Announcement Drift for Surprises Calculated from Analyst and Time Series Forecasts.* — PEAD implementation details (unit 166).
- ◆ Blitz, Huij & Martens, residual momentum notes; Da, Qian & Warachka — residual / industry-neutral short-horizon constructions (unit 165).
- ◆ Bogousslavsky, close-auction / overnight papers. — who gets filled at the close (unit 167).
- ◆ Kissell — *The Science of Algorithmic Trading and Portfolio Management.* — practitioner execution at this clock (unit 188). Gârleanu–Pedersen 2013 and Boyd 2017 (already ★ above) are the daily multi-period sources (unit 187).

### Execution & RL
- ★ Almgren & Chriss (2000), *Optimal Execution of Portfolio Transactions.* — unit 092.
- ★ Avellaneda & Stoikov (2008), *High-frequency trading in a limit order book.* — unit 094.
- ★ Mnih et al. (2015), *Human-level control through deep RL (DQN)*; van Hasselt et al. (2016), *Double DQN*; Schulman et al. (2017), *PPO.* — units 096–097.
- ◆ Dean & Barroso (2013), *The Tail at Scale.* — unit 108.

---

## Wisdom (Communities)

- **Quantitative Finance Stack Exchange** (quant.stackexchange.com) — high-signal Q&A on models, pricing, microstructure. Use for: "is my derivation/method right?"
- **r/quant** and **r/algotrading** (read-mostly) — r/quant for career + research taste; treat r/algotrading claims skeptically (survivorship + hype). Use for: firm/role landscape, sanity checks.
- **Wilmott Forums** — long-running derivatives/quant community, strong on stochastic calc & pricing.
- **NuclearPhoenix / QuantStart / Robot Wealth blogs** — practitioner write-ups on backtesting discipline (vet against AFML).
- **Firm engineering & research blogs** — Jane Street Tech Blog, Two Sigma, Hudson River Trading, Optiver, Jump — for the real bar on rigor and systems, and interview style.
- **Local/online:** a study group or Discord for the Green Book / mock interviews once Year 3 Q4 begins — mock market-making games need live partners.

*(No community preference recorded yet — update NOTES.md if you'd rather not join any.)*

---

## Gaps (drives future search)

- **Real LOB data** for Year 2 Q3 labs: LOBSTER (academic), Databento, or the FI-2010 benchmark (Ntakaris et al. 2018, the DeepLOB dataset). Confirm access/licensing before unit 062.
- **RL-for-execution SOTA** moves fast — re-check at the start of Year 3 for post-2023 baselines.
- **Tabular foundation models** are a live frontier (TabPFN v2, TabDPT, TabICL) — apply the quarterly currency rule before unit 078.
- **Cross-sectional ML for monthly equity** moves slower than TFMs but is not frozen — before Year 4 Q2, check whether a post-2020 paper (transformers on characteristics, foundation models for the cross-section) has become the baseline you must beat. Gu-Kelly-Xiu 2020 stays ★ until something *replaces* it, not merely cites it.
- **Daily / intraweek equity ML** is even more leak-prone than the monthly paper. Before Year 5 Q2, confirm you still have a point-in-time earnings calendar and a cost model; do not replace Jegadeesh/Lehmann + Bernard–Thomas as the baselines you must beat.
