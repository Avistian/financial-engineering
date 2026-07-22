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
  The standard bridge for a strong-math student new to SDEs. Use for: Brownian motion, Itô, Girsanov, BS PDE, Feynman-Kac (Year 1 Q2).
- ◆ **Shreve — *Volume I: The Binomial Asset Pricing Model***. Discrete warm-up; read first if Vol II feels abrupt.
- ◆ **Baxter & Rennie — *Financial Calculus***. Gentler, intuition-first companion to Shreve.
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
- ★ **Grinold & Kahn — *Active Portfolio Management*** (2nd ed.). The Fundamental Law, IC/breadth, factor risk, alpha combination. Year 3 Q1.
- ◆ **Bouchaud & Potters — *Theory of Financial Risk and Derivative Pricing***. RMT for covariance cleaning.
- ◆ **McNeil, Frey & Embrechts — *Quantitative Risk Management***. VaR/ES done rigorously.

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
- ★ Ledoit & Wolf (2004), *A well-conditioned estimator for large-dimensional covariance matrices.* — unit 083.
- ★ Laloux, Cizeau, Bouchaud & Potters (1999), *Noise Dressing of the Financial Correlation Matrix* (RMT). — unit 082.
- ★ López de Prado (2016), *Building Diversified Portfolios that Outperform Out of Sample* (HRP). — unit 087.

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
