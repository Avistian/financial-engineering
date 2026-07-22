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
    }
  ];
})(window);
