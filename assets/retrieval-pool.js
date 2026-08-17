/**
 * Spaced-retrieval question pool (single source of truth for RetrievalBank).
 *
 * Loaded as a plain <script> so it works on file:// and GitHub Pages (no fetch/CORS).
 * Assigns window.RETRIEVAL_POOL = [ item, ... ].
 *
 * Each item:
 *   id          unique string, stable forever (Leitner state is keyed on it) — never renumber
 *   lesson      integer origin lesson (used for spacing: only resurfaces in lessons AFTER this)
 *   quarter     "Q1" | "Q2" | ...  (used to interleave across quarters)
 *   concept     short tag (used to avoid two same-concept items in one warm-up)
 *   question    prompt (retrieval — recall from memory, not recognition of just-read text)
 *   options     [{ label, value }]  — keep labels similar length (quiz-fairness standard)
 *   correct     value of the correct option
 *   explain     one-sentence why (shown after answering)
 *   misconception  true if this item mirrors a row in misconceptions.md (kept in sync)
 *
 * ADD an item whenever a lesson ships a durable, testable idea, and whenever a misconception
 * is logged. Do NOT change an existing id.
 */
(function (global) {
  "use strict";

  global.RETRIEVAL_POOL = [
    // ---- L001: the quant landscape ----
    {
      id: "l001-qr-skill", lesson: 1, quarter: "Q1", concept: "role-map",
      question: "A quant researcher's single most valuable skill is best described as:",
      options: [
        { label: "Proving an edge is real, not overfit", value: "a" },
        { label: "Writing the fastest low-latency C++", value: "b" },
        { label: "Calling the market's next big move", value: "c" },
        { label: "Training the largest possible network", value: "d" }
      ],
      correct: "a",
      explain: "Markets are low-signal and adversarial, so validation discipline beats model complexity — the thesis of the whole track."
    },
    {
      id: "l001-alpha", lesson: 1, quarter: "Q1", concept: "alpha",
      question: "In r = α + β·r_market + ε, the alpha term represents:",
      options: [
        { label: "Return beyond market-risk exposure", value: "a" },
        { label: "The overall volatility of returns", value: "b" },
        { label: "Correlation between fund and index", value: "c" },
        { label: "The total gross return of a fund", value: "d" }
      ],
      correct: "a",
      explain: "Alpha is the intercept — performance from skill/edge, independent of simply being paid to bear market risk (beta)."
    },

    // ---- L002: instruments & mechanics ----
    {
      id: "l002-nonlinear", lesson: 2, quarter: "Q1", concept: "instruments",
      question: "Which instrument has a payoff that is non-linear in the underlying price?",
      options: [
        { label: "An equity call option contract", value: "a" },
        { label: "A single share of common stock", value: "b" },
        { label: "A standard index futures trade", value: "c" },
        { label: "A broad-market equity index ETF", value: "d" }
      ],
      correct: "a",
      explain: "Options pay max(S−K,0)-style payoffs — non-linear, which is exactly why they need stochastic-calculus pricing."
    },
    {
      id: "l002-spread", lesson: 2, quarter: "Q1", concept: "trading-cost", misconception: true,
      question: "Why does treating 'the price' as one number bias a backtest upward?",
      options: [
        { label: "There is a bid and an ask, not one price", value: "a" },
        { label: "Prices are always quoted after the close", value: "b" },
        { label: "Dividends are omitted from the price feed", value: "c" },
        { label: "The mid price already includes all costs", value: "d" }
      ],
      correct: "a",
      explain: "Taking liquidity crosses the spread every trade; filling at the mid/close ignores that recurring, real cost."
    },

    // ---- L003: the limit order book ----
    {
      id: "l003-priority", lesson: 3, quarter: "Q1", concept: "matching",
      question: "Under price-time priority, resting orders are ranked by:",
      options: [
        { label: "Best price first, then earliest time", value: "a" },
        { label: "Largest size first, then any price", value: "b" },
        { label: "Earliest time first, then any price", value: "c" },
        { label: "Random draw among all live orders", value: "d" }
      ],
      correct: "a",
      explain: "Price is the primary key (better prices match first); time breaks ties at the same price — FIFO."
    },
    {
      id: "l003-walk", lesson: 3, quarter: "Q1", concept: "slippage", misconception: true,
      question: "A large market order that 'walks the book' fills, on average, at a price that is:",
      options: [
        { label: "Worse than the best displayed quote", value: "a" },
        { label: "Exactly equal to the mid at arrival", value: "b" },
        { label: "Better than the best quote by design", value: "c" },
        { label: "Fixed at yesterday's official close", value: "d" }
      ],
      correct: "a",
      explain: "It consumes level 1, then level 2, and so on, so the average fill is worse than the top quote — that gap is slippage."
    },

    // ---- L004: returns & stylized facts ----
    {
      id: "l004-logadd", lesson: 4, quarter: "Q1", concept: "returns",
      question: "Quants default to log returns for time-series work mainly because they:",
      options: [
        { label: "Add cleanly across time periods", value: "a" },
        { label: "Are always bigger than simple ones", value: "b" },
        { label: "Remove all volatility from a series", value: "c" },
        { label: "Force a normal return distribution", value: "d" }
      ],
      correct: "a",
      explain: "A k-period log return is the sum of one-period log returns, which fits the Brownian-motion models of Q2."
    },
    {
      id: "l004-clustering", lesson: 4, quarter: "Q1", concept: "volatility",
      question: "Volatility clustering shows up empirically as positive autocorrelation of:",
      options: [
        { label: "Absolute (or squared) returns", value: "a" },
        { label: "The raw signed return series", value: "b" },
        { label: "The series' rolling mean level", value: "c" },
        { label: "The daily traded dollar volume", value: "d" }
      ],
      correct: "a",
      explain: "Raw returns show ~0 autocorrelation, but |returns| are positively autocorrelated — big moves cluster and vol is forecastable."
    },
    {
      id: "l004-fattails", lesson: 4, quarter: "Q1", concept: "tails", misconception: true,
      question: "Because real returns have fat tails, a Gaussian risk model will tend to:",
      options: [
        { label: "Underestimate extreme-loss probability", value: "a" },
        { label: "Overestimate extreme-loss probability", value: "b" },
        { label: "Match crash frequencies almost exactly", value: "c" },
        { label: "Eliminate any volatility clustering", value: "d" }
      ],
      correct: "a",
      explain: "Returns have far more extreme moves than a normal predicts, so Gaussian VaR undercounts tail risk."
    },

    // ---- L005: probability refresher ----
    {
      id: "l005-lognormal", lesson: 5, quarter: "Q1", concept: "distributions",
      question: "If log returns are normally distributed, the price level itself is:",
      options: [
        { label: "Lognormal and strictly positive", value: "a" },
        { label: "Normal around its own mean", value: "b" },
        { label: "Uniform over a fixed interval", value: "c" },
        { label: "Poisson, being a count value", value: "d" }
      ],
      correct: "a",
      explain: "Price = P₀·exp(Σ log returns); the exponential of a normal is lognormal — positive and right-skewed."
    },
    {
      id: "l005-conditional", lesson: 5, quarter: "Q1", concept: "conditioning",
      question: "A model's forecast is, at heart, best thought of as a:",
      options: [
        { label: "Conditional expectation given info", value: "a" },
        { label: "Unconditional average of history", value: "b" },
        { label: "Single realized draw from the past", value: "c" },
        { label: "Variance of the observed targets", value: "d" }
      ],
      correct: "a",
      explain: "E[X | information] is the optimal (MSE) forecast given what you know — the backbone of regression, signals, and pricing."
    },

    // ---- deeper Q1 ideas (added when lessons were expanded) ----
    {
      id: "l001-capacity", lesson: 1, quarter: "Q1", concept: "capacity",
      question: "A strategy's 'capacity' is the maximum size it can run before:",
      options: [
        { label: "Its own market impact eats the edge", value: "a" },
        { label: "The backtest runs out of memory", value: "b" },
        { label: "It needs more features to keep going", value: "c" },
        { label: "The Sharpe ratio becomes undefined", value: "d" }
      ],
      correct: "a",
      explain: "Beyond some size, the strategy's impact moves prices against it and erodes the edge — that ceiling is its capacity."
    },
    {
      id: "l002-timevalue", lesson: 2, quarter: "Q1", concept: "option-value",
      question: "An option's premium equals its intrinsic value plus its:",
      options: [
        { label: "Time value, decaying toward expiry", value: "a" },
        { label: "Bid-ask spread on the underlying", value: "b" },
        { label: "Dividend paid out before expiry", value: "c" },
        { label: "Broker commission on the contract", value: "d" }
      ],
      correct: "a",
      explain: "Premium = intrinsic + time value; time value reflects possible future moves and shrinks to zero at expiry."
    },
    {
      id: "l003-microprice", lesson: 3, quarter: "Q1", concept: "microprice",
      question: "When the best bid holds more size than the best ask, the micro-price sits:",
      options: [
        { label: "Above the mid, leaning to an up-tick", value: "a" },
        { label: "Exactly at the mid, size aside", value: "b" },
        { label: "Below the mid, leaning to a drop", value: "c" },
        { label: "At the best ask by construction", value: "d" }
      ],
      correct: "a",
      explain: "The size-weighted micro-price is pulled toward the heavier side; more bid size lifts it above the mid, hinting at buy pressure."
    },
    {
      id: "l004-sqrt-t", lesson: 4, quarter: "Q1", concept: "vol-scaling",
      question: "Under the IID assumption, T-period volatility scales with the one-period value as:",
      options: [
        { label: "σ · √T (square-root of horizon)", value: "a" },
        { label: "σ · T (linear in the horizon)", value: "b" },
        { label: "σ / √T (shrinks with horizon)", value: "c" },
        { label: "σ itself (independent of horizon)", value: "d" }
      ],
      correct: "a",
      explain: "Variance adds across IID periods, so volatility scales as σ·√T (e.g. annual ≈ daily·√252) — only approximate under clustering and fat tails."
    },
    {
      id: "l005-uncorrelated", lesson: 5, quarter: "Q1", concept: "dependence", misconception: true,
      question: "Two variables having zero correlation tells you that they:",
      options: [
        { label: "Have no linear relation, but may depend", value: "a" },
        { label: "Are guaranteed statistically independent", value: "b" },
        { label: "Must both be normally distributed too", value: "c" },
        { label: "Cannot ever move together in a crisis", value: "d" }
      ],
      correct: "a",
      explain: "Correlation captures only linear association; uncorrelated variables can still be strongly (nonlinearly or tail-) dependent."
    },

    // ---- L006: estimation & inference ----
    {
      id: "l006-mse", lesson: 6, quarter: "Q1", concept: "estimator-error",
      question: "An estimator's mean squared error decomposes exactly into:",
      options: [
        { label: "Bias squared plus its variance", value: "a" },
        { label: "Bias plus the variance squared", value: "b" },
        { label: "Variance minus the squared bias", value: "c" },
        { label: "Standard error times its bias", value: "d" }
      ],
      correct: "a",
      explain: "MSE = bias² + variance, so a biased low-variance estimator can beat an unbiased one — the logic behind shrinkage."
    },
    {
      id: "l006-sqrtn", lesson: 6, quarter: "Q1", concept: "sample-size",
      question: "To halve the standard error of an estimate, you need roughly:",
      options: [
        { label: "Four times as much data", value: "a" },
        { label: "Twice as much data used", value: "b" },
        { label: "Half as much data used", value: "c" },
        { label: "Ten times as much data", value: "d" }
      ],
      correct: "a",
      explain: "SE ∝ 1/√n, so halving it requires √n to double — i.e. 4× the data. The √n wall is why small edges need long histories."
    },
    {
      id: "l006-ci", lesson: 6, quarter: "Q1", concept: "confidence", misconception: true,
      question: "The correct reading of a 95% confidence interval is that:",
      options: [
        { label: "95% of such intervals cover the truth", value: "a" },
        { label: "The value lies inside with 95% odds", value: "b" },
        { label: "95% of the data fall in the interval", value: "c" },
        { label: "The estimate is right 95% of the time", value: "d" }
      ],
      correct: "a",
      explain: "The parameter is fixed and the interval is random; 95% is the procedure's long-run coverage, not a probability about this one interval."
    },
    {
      id: "l006-bootstrap", lesson: 6, quarter: "Q1", concept: "bootstrap",
      question: "The bootstrap estimates a statistic's uncertainty by:",
      options: [
        { label: "Resampling the data with replacement", value: "a" },
        { label: "Assuming returns are exactly normal", value: "b" },
        { label: "Dropping the most extreme outliers", value: "c" },
        { label: "Fitting one model to the full sample", value: "d" }
      ],
      correct: "a",
      explain: "It treats the sample as a stand-in for the population (plug-in), resamples n points with replacement many times, and reads percentiles for a CI."
    },
    {
      id: "l006-mle", lesson: 6, quarter: "Q1", concept: "likelihood",
      question: "The maximum-likelihood estimate is the parameter value that:",
      options: [
        { label: "Makes the observed data most probable", value: "a" },
        { label: "Minimizes the sample's total variance", value: "b" },
        { label: "Sets the sample bias exactly to zero", value: "c" },
        { label: "Maximizes the width of the interval", value: "d" }
      ],
      correct: "a",
      explain: "MLE maximizes L(θ)=P(data|θ) (usually its log); its SE comes from the curvature at the peak — the Fisher information."
    },

    // ---- L007: hypothesis testing & multiple-testing traps ----
    {
      id: "l007-pvalue", lesson: 7, quarter: "Q1", concept: "p-value", misconception: true,
      question: "A p-value is best defined as the probability of:",
      options: [
        { label: "Data this extreme, if H\u2080 is true", value: "a" },
        { label: "The null hypothesis being truly true", value: "b" },
        { label: "The strategy having a genuine edge", value: "c" },
        { label: "Making a Type II error at level \u03b1", value: "d" }
      ],
      correct: "a",
      explain: "p = P(statistic at least this extreme | H\u2080). It is P(data | H\u2080), not P(H\u2080 | data), and not the chance the edge is real."
    },
    {
      id: "l007-t-sharpe", lesson: 7, quarter: "Q1", concept: "t-stat",
      question: "For a return series, a strategy's t-statistic equals roughly:",
      options: [
        { label: "Annualized Sharpe times \u221ayears", value: "a" },
        { label: "Annualized Sharpe divided by n", value: "b" },
        { label: "Mean return times the sample size", value: "c" },
        { label: "Volatility over the mean return", value: "d" }
      ],
      correct: "a",
      explain: "t = SR_period\u00b7\u221an = SR_annual\u00b7\u221ayears, so a Sharpe-1 strategy needs ~4 years just to clear the single-test 1.96 bar."
    },
    {
      id: "l007-fwer", lesson: 7, quarter: "Q1", concept: "multiple-testing",
      question: "Test 100 zero-edge strategies at 5%; the chance of at least one false 'winner' is about:",
      options: [
        { label: "99% (nearly guaranteed by chance)", value: "a" },
        { label: "5% (equal to the chosen level)", value: "b" },
        { label: "1% (rare, so safe to ignore)", value: "c" },
        { label: "50% (a straight coin-flip risk)", value: "d" }
      ],
      correct: "a",
      explain: "FWER = 1\u2212(1\u2212\u03b1)^M = 1\u22120.95^100 \u2248 0.994 \u2014 the classic bar becomes a false-discovery generator under a search."
    },
    {
      id: "l007-bonf-bh", lesson: 7, quarter: "Q1", concept: "corrections",
      question: "Unlike Bonferroni's family-wise control, Benjamini-Hochberg controls the:",
      options: [
        { label: "Expected false-discovery proportion", value: "a" },
        { label: "Chance of any single false positive", value: "b" },
        { label: "Total number of tests you may run", value: "c" },
        { label: "Variance of every strategy's return", value: "d" }
      ],
      correct: "a",
      explain: "BH controls the FDR (expected fraction of discoveries that are false), keeping more power than Bonferroni's 'not even one' rule."
    },

    // ---- L008: linear algebra, covariance & PCA ----
    {
      id: "l008-eigen", lesson: 8, quarter: "Q1", concept: "eigen",
      question: "A nonzero vector v is an eigenvector of a matrix M exactly when:",
      options: [
        { label: "M v = \u03bb v for some scalar \u03bb", value: "a" },
        { label: "M v equals the zero vector always", value: "b" },
        { label: "v is perpendicular to the vector M v", value: "c" },
        { label: "M v has the same length as vector v", value: "d" }
      ],
      correct: "a",
      explain: "An eigenvector keeps its direction under M; it is only scaled by its eigenvalue \u03bb (Mv = \u03bbv)."
    },
    {
      id: "l008-var-explained", lesson: 8, quarter: "Q1", concept: "pca-variance",
      question: "In PCA, the fraction of total variance explained by component k is:",
      options: [
        { label: "\u03bb\u2096 over the sum of all eigenvalues", value: "a" },
        { label: "\u03bb\u2096 over the largest eigenvalue \u03bb\u2081", value: "b" },
        { label: "\u03bb\u2096 multiplied by the matrix trace", value: "c" },
        { label: "one over the number of components d", value: "d" }
      ],
      correct: "a",
      explain: "Variance explained = \u03bb\u2096 / tr(\u03a3) = \u03bb\u2096 / \u03a3\u03bb, since the trace (total variance) equals the sum of eigenvalues."
    },
    {
      id: "l008-scale", lesson: 8, quarter: "Q1", concept: "pca-scale", misconception: true,
      question: "Running PCA on the raw covariance of assets with very different vols mainly risks:",
      options: [
        { label: "PC1 just being the loudest single asset", value: "a" },
        { label: "Eigenvalues coming out complex-valued", value: "b" },
        { label: "The components no longer being orthogonal", value: "c" },
        { label: "Losing the sign of every eigenvector", value: "d" }
      ],
      correct: "a",
      explain: "Covariance is scale-sensitive, so a high-vol asset dominates by being loud; standardize columns (decompose the correlation matrix) first."
    },
    {
      id: "l008-market-factor", lesson: 8, quarter: "Q1", concept: "market-factor",
      question: "On an equity returns panel, the first principal component usually represents:",
      options: [
        { label: "The market factor (all names, same sign)", value: "a" },
        { label: "A long-short spread between two sectors", value: "b" },
        { label: "The single lowest-variance idiosyncratic name", value: "c" },
        { label: "Pure estimation noise with no interpretation", value: "d" }
      ],
      correct: "a",
      explain: "PC1 loads with the same sign on nearly every stock \u2014 the 'everything moves together' direction \u2014 because common market risk dominates variance; its share spikes in crises as \u03c1\u21921."
    },

    // ---- L009: regression, robust standard errors ----
    {
      id: "l009-slope", lesson: 9, quarter: "Q1", concept: "ols-slope",
      question: "In a one-predictor regression, the OLS slope \u03b2\u0302\u2081 equals:",
      options: [
        { label: "Cov(x, y) over the variance of x", value: "a" },
        { label: "Cov(x, y) over the variance of y", value: "b" },
        { label: "The plain correlation of x and y", value: "c" },
        { label: "Mean of y minus the mean of x", value: "d" }
      ],
      correct: "a",
      explain: "\u03b2\u0302\u2081 = Cov(x,y)/Var(x): co-movement normalized by the predictor's own spread (= \u03c1\u00b7\u03c3_y/\u03c3_x)."
    },
    {
      id: "l009-hetero", lesson: 9, quarter: "Q1", concept: "robust-se", misconception: true,
      question: "Under heteroskedasticity, ordinary least squares gives you:",
      options: [
        { label: "An unbiased \u03b2\u0302 but a wrong standard error", value: "a" },
        { label: "A biased \u03b2\u0302 but a correct standard error", value: "b" },
        { label: "Both a biased \u03b2\u0302 and a wrong error", value: "c" },
        { label: "Everything correct \u2014 no fix is needed", value: "d" }
      ],
      correct: "a",
      explain: "OLS needs neither constant variance nor independence to be unbiased; only the SE breaks. Fix it with White/HC, keep the estimate."
    },
    {
      id: "l009-overlap", lesson: 9, quarter: "Q1", concept: "overlap", misconception: true,
      question: "Regressing overlapping multi-period returns sampled daily inflates the t-stat because it:",
      options: [
        { label: "Positively autocorrelates the errors", value: "a" },
        { label: "Strongly biases the estimate \u03b2\u0302", value: "b" },
        { label: "Inflates the residual variance \u03c3\u0302\u00b2", value: "c" },
        { label: "Makes the design matrix singular", value: "d" }
      ],
      correct: "a",
      explain: "Overlapping windows share most of their days, so consecutive errors correlate; the effective sample shrinks, the naïve SE is too small, and t is inflated. Fix with Newey\u2013West."
    },
    {
      id: "l009-hac", lesson: 9, quarter: "Q1", concept: "newey-west",
      question: "The Newey\u2013West (HAC) standard error is consistent under:",
      options: [
        { label: "Heteroskedasticity and autocorrelation both", value: "a" },
        { label: "Only heteroskedasticity, not autocorrelation", value: "b" },
        { label: "Omitted-variable bias in the coefficients", value: "c" },
        { label: "A non-stationary price-on-price regression", value: "d" }
      ],
      correct: "a",
      explain: "HAC = Heteroskedasticity- And Autocorrelation-Consistent. It extends White with Bartlett-weighted residual autocovariances; it cannot cure bias or spurious level regressions."
    },

    // ---- L010: Q1 checkpoint (statistical hygiene) ----
    {
      id: "l010-se-lie", lesson: 10, quarter: "Q1", concept: "hygiene-core",
      question: "Across heteroskedasticity, overlap, and selection bias, the thing that is usually wrong is the:",
      options: [
        { label: "Standard error, hence the t-statistic", value: "a" },
        { label: "Point estimate of the slope \u03b2\u0302", value: "b" },
        { label: "Sign of the fitted relationship", value: "c" },
        { label: "Units the return was measured in", value: "d" }
      ],
      correct: "a",
      explain: "In all three the estimate stays about right; the inference \u2014 the SE and the t-stat you claim \u2014 breaks. Fix the SE, keep the estimate."
    },
    {
      id: "l010-selection-bar", lesson: 10, quarter: "Q1", concept: "selection-bar", misconception: true,
      question: "A t-statistic that is the best of M = 100 tried signals should be judged against a bar of about:",
      options: [
        { label: "The expected max of M nulls (\u2248 2.5)", value: "a" },
        { label: "The single-test 1.96, as usual", value: "b" },
        { label: "Zero, since search cannot bias t", value: "c" },
        { label: "The mean of the M t-statistics", value: "d" }
      ],
      correct: "a",
      explain: "Under a search the fair benchmark is E[max of M] draws under H\u2080 (\u22482.5 for M=100), not 1.96 \u2014 that gap is the selection haircut."
    },
    {
      id: "l010-neff", lesson: 10, quarter: "Q1", concept: "effective-n",
      question: "If overlapping returns inflate the honest SE by a factor of 3, your effective sample size is about:",
      options: [
        { label: "n divided by nine (inflation squared)", value: "a" },
        { label: "n divided by three (the inflation)", value: "b" },
        { label: "n times three (more overlap, more data)", value: "c" },
        { label: "n itself (overlap adds observations)", value: "d" }
      ],
      correct: "a",
      explain: "n_eff = n / inflation\u00b2, so a 3\u00d7 SE inflation means only ~n/9 independent observations \u2014 the concrete cost of overlap."
    },
    {
      id: "l010-verdict", lesson: 10, quarter: "Q1", concept: "kill-is-a-win",
      question: "For a quant researcher, the professionally valuable result of an honest audit is often to:",
      options: [
        { label: "Correctly kill a great-looking backtest", value: "a" },
        { label: "Report the highest in-sample R\u00b2", value: "b" },
        { label: "Confirm every signal past t = 1.96", value: "c" },
        { label: "Maximize the count of shipped signals", value: "d" }
      ],
      correct: "a",
      explain: "The value is negative knowledge \u2014 not staking capital on noise. A killed bad backtest saves real out-of-sample money; that is the checkpoint's ethos."
    },

    // ---- L011: information, filtrations, conditional expectation ----
    {
      id: "l011-condexp-type", lesson: 11, quarter: "Q2", concept: "cond-exp", misconception: true,
      question: "E[X | \u2131\u209c] \u2014 the best guess of X given time-t information \u2014 is:",
      options: [
        { label: "A random variable, constant on cells", value: "a" },
        { label: "A single number, fixed at time zero", value: "b" },
        { label: "A probability that the event X holds", value: "c" },
        { label: "A function of X's own future value", value: "d" }
      ],
      correct: "a",
      explain: "It gives one value per atom of \u2131\u209c, so it is an \u2131\u209c-measurable random variable \u2014 a plan for guessing, revealed when time t arrives."
    },
    {
      id: "l011-measurable-leak", lesson: 11, quarter: "Q2", concept: "measurability", misconception: true,
      question: "Standardising a signal with the full sample's mean and volatility is, formally:",
      options: [
        { label: "Conditioning on a too-large \u03c3-algebra", value: "a" },
        { label: "Conditioning on a coarser \u03c3-algebra", value: "b" },
        { label: "A rescaling that changes no inference", value: "c" },
        { label: "An instance of the tower property", value: "d" }
      ],
      correct: "a",
      explain: "The signal becomes \u2131_T-measurable while being used as if \u2131\u209c-measurable. Leakage IS a measurability violation, and a bigger \u03c3-algebra always flatters the fit."
    },
    {
      id: "l011-tower", lesson: 11, quarter: "Q2", concept: "tower",
      question: "By the tower property, E[ E[X | \u2131\u2082] | \u2131\u2081 ] equals:",
      options: [
        { label: "E[X | \u2131\u2081] \u2014 the coarser conditioning", value: "a" },
        { label: "E[X | \u2131\u2082] \u2014 the finer conditioning", value: "b" },
        { label: "X itself, as the averages cancel out", value: "c" },
        { label: "Var(X), by the variance decomposition", value: "d" }
      ],
      correct: "a",
      explain: "A guess about a guess collapses to the coarser guess. On the standard tree: (21.00 + 4.45)/2 = 12.725 = E[V|\u2131\u2081] on the up branch."
    },
    {
      id: "l011-projection", lesson: 11, quarter: "Q2", concept: "projection",
      question: "Among all guesses your information allows, E[X|\u2131] is the unique one that:",
      options: [
        { label: "Minimises the squared error E[(X\u2212Y)\u00b2]", value: "a" },
        { label: "Maximises the correlation of X and Y", value: "b" },
        { label: "Matches the variance of the target X", value: "c" },
        { label: "Leaves the largest possible residual", value: "d" }
      ],
      correct: "a",
      explain: "It is the L\u00b2 projection onto the \u2131-measurable subspace, so the residual X \u2212 E[X|\u2131] is orthogonal to everything you know \u2014 the general form of \"residuals \u22a5 regressors\"."
    },
    {
      id: "l011-martingale", lesson: 11, quarter: "Q2", concept: "martingale", misconception: true,
      question: "Saying \"this price process is a martingale\" is incomplete unless you also state:",
      options: [
        { label: "The measure and filtration it is under", value: "a" },
        { label: "The volatility of the price increments", value: "b" },
        { label: "That the tree recombines at each node", value: "c" },
        { label: "The strike of the option being priced", value: "d" }
      ],
      correct: "a",
      explain: "E[M\u209c|\u2131\u209b] = M\u209b is a joint claim about process, filtration and measure: the same tree is a martingale at p = \u00bd and drifts up 2%/step at p = 0.6."
    },

    // ---- L012: random walks & Brownian motion ----
    {
      id: "l012-scaling", lesson: 12, quarter: "Q2", concept: "bm-scaling",
      question: "The random walk M_{nt} is divided by \u221an (not n) so that:",
      options: [
        { label: "Var(W_t) stays equal to t at all n", value: "a" },
        { label: "each step keeps a fixed size of one", value: "b" },
        { label: "the path becomes smooth in the limit", value: "c" },
        { label: "the mean of W_t grows in step with t", value: "d" }
      ],
      correct: "a",
      explain: "Dividing by a constant c divides variance by c\u00b2, so \u221an turns raw variance nt into t \u2014 finite and non-zero. Dividing by n sends it to 0 (a flat line)."
    },
    {
      id: "l012-bm-def", lesson: 12, quarter: "Q2", concept: "bm-def",
      question: "For Brownian motion, the increment W_t \u2212 W_s is distributed as:",
      options: [
        { label: "Normal, mean 0, variance t \u2212 s", value: "a" },
        { label: "Normal, mean t \u2212 s, variance one", value: "b" },
        { label: "Uniform on the interval s to t", value: "c" },
        { label: "Poisson with the rate set to t", value: "d" }
      ],
      correct: "a",
      explain: "Gaussian increments with mean 0 and variance equal to the elapsed time t \u2212 s, and independent of everything up to time s."
    },
    {
      id: "l012-qvar", lesson: 12, quarter: "Q2", concept: "quadratic-variation",
      question: "The quadratic variation of Brownian motion, \u03a3(\u0394W)\u00b2 over [0,t], converges to:",
      options: [
        { label: "t \u2014 it does not vanish here", value: "a" },
        { label: "zero, like any smooth line", value: "b" },
        { label: "infinity, with no real limit", value: "c" },
        { label: "just the last step variance", value: "d" }
      ],
      correct: "a",
      explain: "Mean m\u00b7\u0394t = t at every mesh; wobble 2t\u00b2/m \u2192 0, so the sum is the non-random value t. (The FIRST-power sum \u03a3|\u0394W| is the one that blows up.)"
    },
    {
      id: "l012-nowhere-diff", lesson: 12, quarter: "Q2", concept: "bm-roughness", misconception: true,
      question: "A Brownian path is continuous everywhere, and at the same time:",
      options: [
        { label: "nowhere smooth \u2014 slopes blow up", value: "a" },
        { label: "differentiable at all but a point", value: "b" },
        { label: "smooth once its steps get small", value: "c" },
        { label: "flat, as its mean stays at zero", value: "d" }
      ],
      correct: "a",
      explain: "The move over \u0394t is \u221a\u0394t, so the slope |\u0394W|/\u0394t \u2248 1/\u221a\u0394t \u2192 \u221e. Continuous because \u221a\u0394t \u2192 0; not smooth because the slope explodes."
    },
    {
      id: "l012-dw2dt", lesson: 12, quarter: "Q2", concept: "dw-squared", misconception: true,
      question: "In stochastic calculus the term (dW)\u00b2 is replaced by:",
      options: [
        { label: "dt \u2014 it is first-order, not junk", value: "a" },
        { label: "0, being second-order and tiny", value: "b" },
        { label: "dW, since squaring changes little", value: "c" },
        { label: "(dt)\u00b2, a negligible correction", value: "d" }
      ],
      correct: "a",
      explain: "Since [W]_t = t, the squared increment (dW)\u00b2 accumulates at rate 1: (dW)\u00b2 = dt. Only dW\u00b7dt and (dt)\u00b2 are dropped. This surviving term is the extra piece in It\u00f4's lemma."
    },

    // ---- L013: the Itô integral & Itô's lemma ----
    {
      id: "l013-lemma", lesson: 13, quarter: "Q2", concept: "ito-lemma",
      question: "It\u00f4's lemma for f(W) says df equals:",
      options: [
        { label: "f'(W)\u00b7dW + \u00bd f''(W)\u00b7dt", value: "a" },
        { label: "f'(W)\u00b7dW, as in calculus", value: "b" },
        { label: "\u00bd f''(W)\u00b7dW + f'(W)\u00b7dt", value: "c" },
        { label: "f'(W)\u00b7dt + \u00bd f''(W)\u00b7dW", value: "d" }
      ],
      correct: "a",
      explain: "Taylor-expand and substitute (dW)\u00b2 = dt: the surviving second-order term \u00bd f''(W)\u00b7dt is the drift the ordinary chain rule misses."
    },
    {
      id: "l013-dw2", lesson: 13, quarter: "Q2", concept: "ito-dw2", misconception: true,
      question: "Applying It\u00f4's lemma to f(W) = W\u00b2 gives d(W\u00b2) =",
      options: [
        { label: "2W\u00b7dW + dt \u2014 has a drift", value: "a" },
        { label: "2W\u00b7dW \u2014 the naive one", value: "b" },
        { label: "W\u00b7dW + \u00bd dt \u2014 all halved", value: "c" },
        { label: "2\u00b7dW + 2W\u00b7dt \u2014 swapped", value: "d" }
      ],
      correct: "a",
      explain: "f'=2W, f''=2, so d(W\u00b2)=2W dW + \u00bd\u00b72\u00b7dt = 2W dW + dt. That +dt is why W\u00b2 \u2212 t (not W\u00b2) is the martingale."
    },
    {
      id: "l013-ito-integral", lesson: 13, quarter: "Q2", concept: "ito-integral",
      question: "An It\u00f4 integral \u222bH dW is a martingale (zero drift) because H is taken at each step's:",
      options: [
        { label: "start, before the shock is seen", value: "a" },
        { label: "end, after the shock is seen", value: "b" },
        { label: "midpoint, averaging both ends", value: "c" },
        { label: "peak, the largest value hit", value: "d" }
      ],
      correct: "a",
      explain: "Left-endpoint (adapted) sizing: H is known and the next increment is fresh with mean 0, so every term H\u00b7E[\u0394W]=0. You bet before the coin is flipped."
    },
    {
      id: "l013-logdrift", lesson: 13, quarter: "Q2", concept: "gbm-logdrift", misconception: true,
      question: "For GBM dS = \u03bcS dt + \u03c3S dW, the drift of log S is:",
      options: [
        { label: "\u03bc \u2212 \u00bd\u03c3\u00b2 \u2014 a vol drag", value: "a" },
        { label: "\u03bc exactly \u2014 no change", value: "b" },
        { label: "\u03bc + \u00bd\u03c3\u00b2 \u2014 a vol boost", value: "c" },
        { label: "\u00bd\u03c3\u00b2 \u2212 \u03bc \u2014 mostly vol", value: "d" }
      ],
      correct: "a",
      explain: "log curves down (f''=\u22121/S\u00b2), so the It\u00f4 correction is a penalty: \u03bcS(1/S) + \u00bd(\u03c3S)\u00b2(\u22121/S\u00b2) = \u03bc \u2212 \u00bd\u03c3\u00b2. The mean price still grows at \u03bc, the median at \u03bc \u2212 \u00bd\u03c3\u00b2."
    },
    {
      id: "l013-correction-sign", lesson: 13, quarter: "Q2", concept: "ito-correction",
      question: "The It\u00f4 correction \u00bd f''\u00b7dt vanishes exactly when the function is:",
      options: [
        { label: "linear \u2014 its curvature is zero", value: "a" },
        { label: "convex \u2014 its curvature is up", value: "b" },
        { label: "concave \u2014 its curvature is down", value: "c" },
        { label: "positive \u2014 its value stays up", value: "d" }
      ],
      correct: "a",
      explain: "The correction is \u00bd f''\u00b7dt, zero only when f''=0 (a straight line). Then It\u00f4's lemma collapses to the ordinary chain rule."
    },

    // ---- L014: stochastic differential equations (GBM & OU) ----
    {
      id: "l014-sde-def", lesson: 14, quarter: "Q2", concept: "sde-def",
      question: "What single feature makes dX = a dt + b dW a stochastic (not ordinary) differential equation?",
      options: [
        { label: "the fresh random shove b\u00b7dW", value: "a" },
        { label: "the steady drift term a\u00b7dt", value: "b" },
        { label: "that a and b may depend on t", value: "c" },
        { label: "the fact that X starts at X\u2080", value: "d" }
      ],
      correct: "a",
      explain: "The b\u00b7dW term is a fresh random draw (mean 0, variance dt). Drop it and you have an ODE with one determined solution; keep it and each run gives a different path."
    },
    {
      id: "l014-solve-trick", lesson: 14, quarter: "Q2", concept: "sde-solve",
      question: "The trick to solve an SDE in closed form is to apply It\u00f4 to a function f whose expansion:",
      options: [
        { label: "has no X left on the right side", value: "a" },
        { label: "removes the random dW entirely", value: "b" },
        { label: "makes the drift a exactly zero", value: "c" },
        { label: "is always positive for any X", value: "d" }
      ],
      correct: "a",
      explain: "If df has only t and dW on the right (no X), the steps stop referring to where you are, so you can integrate directly. log S does it for GBM; e^{\u03b8t}X for OU."
    },
    {
      id: "l014-ou-revert", lesson: 14, quarter: "Q2", concept: "ou-mean", misconception: true,
      question: "For OU dX = \u03b8(m\u2212X)dt + \u03c3 dW started below m, the long-run mean of X is:",
      options: [
        { label: "m \u2014 pulled to the target", value: "a" },
        { label: "X\u2080 \u2014 it returns to the start", value: "b" },
        { label: "0 \u2014 the pull drains it away", value: "c" },
        { label: "\u221e \u2014 it grows without bound", value: "d" }
      ],
      correct: "a",
      explain: "The drift \u03b8(m\u2212X) points toward m from either side, so E[X_t] = X\u2080e^{\u2212\u03b8t} + m(1\u2212e^{\u2212\u03b8t}) \u2192 m. It wobbles around m with variance \u03c3\u00b2/2\u03b8, never pinning to one value."
    },
    {
      id: "l014-ou-nocorr", lesson: 14, quarter: "Q2", concept: "ou-solve", misconception: true,
      question: "Solving OU with f = e^{\u03b8t}X carries no \u00bd b\u00b2 f_xx correction because f is:",
      options: [
        { label: "it is linear in X, so f_xx = 0", value: "a" },
        { label: "growing, so the term cancels", value: "b" },
        { label: "positive, so curvature is nil", value: "c" },
        { label: "random, so It\u00f4 does not apply", value: "d" }
      ],
      correct: "a",
      explain: "e^{\u03b8t}X is a straight line in X, so f_xx = 0 and the It\u00f4 correction vanishes \u2014 unlike the GBM/log solve, where log S curves (f_xx = \u22121/S\u00b2) and the \u2212\u00bd\u03c3\u00b2 appears."
    },
    {
      id: "l014-existence", lesson: 14, quarter: "Q2", concept: "existence",
      question: "An SDE is guaranteed a single solution for all time when its drift and diffusion have:",
      options: [
        { label: "bounded slope and at-most-linear growth", value: "a" },
        { label: "values that are always strictly positive", value: "b" },
        { label: "faster-than-linear growth to self-correct", value: "c" },
        { label: "no dependence on the state X at all", value: "d" }
      ],
      correct: "a",
      explain: "Bounded steepness (Lipschitz) makes the path unique; no faster-than-linear growth prevents finite-time blow-up (dx/dt=x\u00b2 explodes at t*=1/x\u2080). GBM and OU satisfy both."
    },

    // ---- L015: risk-neutral pricing & Girsanov ----
    {
      id: "l015-replication", lesson: 15, quarter: "Q2", concept: "replication", misconception: true,
      question: "On a one-period binomial tree, the arbitrage-free option price depends on the real-world probability p:",
      options: [
        { label: "not at all \u2014 replication ignores p", value: "a" },
        { label: "yes \u2014 a likelier payoff costs more", value: "b" },
        { label: "only through the discount factor R", value: "c" },
        { label: "only when the option ends in money", value: "d" }
      ],
      correct: "a",
      explain: "The price is the cost of the portfolio (\u0394 shares + B cash) that matches the payoff in BOTH states. Solving those two equations never uses p, so the price cannot depend on it."
    },
    {
      id: "l015-pstar", lesson: 15, quarter: "Q2", concept: "risk-neutral-prob",
      question: "The risk-neutral weight p* = (R \u2212 d)/(u \u2212 d) is the probability under which:",
      options: [
        { label: "the discounted stock is a martingale", value: "a" },
        { label: "up and down moves are equally likely", value: "b" },
        { label: "the option's payoff becomes riskless", value: "c" },
        { label: "nobody demands any premium for risk", value: "d" }
      ],
      correct: "a",
      explain: "Discounting by R and averaging the stock with p* returns exactly today's price \u2014 a fair game. Every asset then appears to grow at the risk-free rate, which is what 'risk-neutral' names."
    },
    {
      id: "l015-girsanov", lesson: 15, quarter: "Q2", concept: "girsanov", misconception: true,
      question: "Applying Girsanov's change of measure to dS = \u03bcS dt + \u03c3S dW changes:",
      options: [
        { label: "the drift only, never the volatility", value: "a" },
        { label: "the volatility only, never the drift", value: "b" },
        { label: "both the drift and the volatility \u03c3", value: "c" },
        { label: "neither one \u2014 only the discount rate", value: "d" }
      ],
      correct: "a",
      explain: "dW = dW\u0303 \u2212 \u03b8dt gives dS = (\u03bc\u2212\u03c3\u03b8)S dt + \u03c3S dW\u0303. \u03c3 cannot move: quadratic variation [W]_t = t is a path-by-path fact, and equivalent measures must agree on those."
    },
    {
      id: "l015-mpr", lesson: 15, quarter: "Q2", concept: "market-price-risk",
      question: "The market price of risk \u03b8, the shift that turns the real drift \u03bc into the rate r, equals:",
      options: [
        { label: "(\u03bc \u2212 r)/\u03c3 \u2014 the Sharpe ratio", value: "a" },
        { label: "(\u03bc \u2212 r)\u00b7\u03c3 \u2014 a scaled premium", value: "b" },
        { label: "\u03bc/\u03c3 \u2014 the plain reward ratio", value: "c" },
        { label: "(r \u2212 \u03bc)/\u03c3 \u2014 the reverse ratio", value: "d" }
      ],
      correct: "a",
      explain: "Setting \u03bc \u2212 \u03c3\u03b8 = r gives \u03b8 = (\u03bc\u2212r)/\u03c3: extra return over cash per unit of volatility \u2014 the asset's Sharpe ratio, and exactly the size of the Brownian shift."
    },
    {
      id: "l015-qnotp", lesson: 15, quarter: "Q2", concept: "q-vs-p", misconception: true,
      question: "In C = S\u2080N(d\u2081) \u2212 Ke^{\u2212rT}N(d\u2082), the number N(d\u2082) is the probability of exercise:",
      options: [
        { label: "under Q, the risk-neutral weights", value: "a" },
        { label: "under P, the true real-world odds", value: "b" },
        { label: "under either measure \u2014 they agree", value: "c" },
        { label: "under neither \u2014 it is the delta \u0394", value: "d" }
      ],
      correct: "a",
      explain: "N(d\u2082) = Q(S_T > K). The real-world chance uses \u03bc in place of r and is generally different \u2014 74% vs 56% in the lesson's example. Quoting one for the other is a professional-grade error."
    }
  ];
})(window);
