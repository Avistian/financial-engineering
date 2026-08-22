"""Build student-facing lesson-by-lesson teaching plans for Years 4–6.

This writes HTML only — no notebooks. Run from the repo root:
  python3 scripts/_gen_long_only_syllabus.py
"""
from __future__ import annotations

from pathlib import Path

CSS = """
    table { width: 100%; border-collapse: collapse; font-size: 0.86rem; margin: 1rem 0; }
    th, td { text-align: left; padding: 0.45rem 0.65rem; border-bottom: 1px solid var(--border); vertical-align: top; }
    th { font-family: var(--font-sans); font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.04em; color: var(--muted); }
    .toc { columns: 2; column-gap: 2rem; font-family: var(--font-sans); font-size: 0.88rem; margin: 1rem 0 2rem; }
    @media (max-width: 640px) { .toc { columns: 1; } }
    .unit { margin: 2rem 0 0; padding-top: 1rem; border-top: 1px solid var(--border); }
    .unit h3 { margin: 0 0 0.4rem; font-size: 1.05rem; }
    .unit h3 .n { font-family: var(--font-mono); color: var(--accent); margin-right: 0.4rem; }
    .skill { margin: 0.35rem 0 0.6rem; }
    .beats { margin: 0.4rem 0 0.8rem; padding-left: 1.2rem; }
    .beats li { margin: 0.35rem 0; }
    .chk-unit { background: var(--accent-light); padding: 0.75rem 1rem; border-radius: 4px; }
    .exit-unit { background: #fef9e7; padding: 0.75rem 1rem; border-radius: 4px; }
"""


def page(title, subtitle, intro, units, nav):
    toc = "\n".join(
        f'    <a href="#u{u["n"]}">{u["n"]} {u["title"]}</a><br>' for u in units
    )
    body = []
    for u in units:
        klass = "unit"
        wrap_s = wrap_e = ""
        if u.get("kind") == "chk":
            wrap_s, wrap_e = '<div class="chk-unit">', "</div>"
        elif u.get("kind") == "exit":
            wrap_s, wrap_e = '<div class="exit-unit">', "</div>"
        beats = "\n".join(f"      <li>{b}</li>" for b in u["teach"])
        body.append(
            f"""
  <section class="{klass}" id="u{u['n']}">
    {wrap_s}
    <h3><span class="n">{u['n']}</span> {u['title']}</h3>
    <p class="skill"><strong>Teach this one skill:</strong> {u['skill']}</p>
    <p><strong>What has to be taught, in order:</strong></p>
    <ol class="beats">
{beats}
    </ol>
    <div class="trap"><strong>Trap to teach, not a footnote.</strong> {u['trap']}</div>
    {wrap_e}
  </section>"""
        )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <link rel="stylesheet" href="../assets/lesson.css">
  <style>{CSS}</style>
</head>
<body>
<article>
  <p class="mission-tag">Reference · lesson-by-lesson teaching plan</p>
  <h1>{title}</h1>
  <p class="subtitle">{subtitle}</p>
  {intro}
  <nav class="toc">
{toc}
  </nav>
{''.join(body)}
  <nav class="nav-links">
    <ul>
{nav}
    </ul>
  </nav>
</article>
</body>
</html>
"""


Y4 = [
    dict(
        n=121,
        title="The long-only mid-horizon mandate",
        skill="State the job in one sentence, and keep score with information ratio, not Sharpe.",
        teach=[
            "Everyday picture: you own a shopping cart of stocks for weeks to months; you never borrow shares to bet they fall. That is <strong>long-only</strong>.",
            "Name the <strong>benchmark</strong> — the comparison basket you claim to beat (often the same stocks, cap-weighted). Without a named benchmark the exam is undefined.",
            "<strong>Active return</strong> is your return minus the benchmark's return. Tiny numbers: index +10%, you +12% → active return = +2%.",
            "<strong>Tracking error</strong> is how much that extra piece bounces (the volatility of active return).",
            "<strong>Information ratio (IR)</strong> = active return ÷ tracking error. That is the exam. <strong>Sharpe</strong> = extra return over cash ÷ how hard the whole book bounces — a long-only book can look fine on Sharpe just by riding the market tide (<strong>beta</strong>).",
            "Contrast with the Q1 lab: that book was dollar-neutral (dollars long ≈ dollars short). This book is allowed to go up and down with the market. Teach when each exam is the honest one.",
            "This clock is weeks-to-months. Lesson 001 called it low frequency / factor investing, not mid-frequency (hours–days).",
        ],
        trap="Treating a long-only Sharpe as proof of skill. Most of that number is beta. The lesson must compute both IR and Sharpe on the same toy book.",
    ),
    dict(
        n=122,
        title="Universe construction without quietly dropping losers",
        skill="Build the list of stocks you are allowed to own as of this morning, not as of today looking backward.",
        teach=[
            "A <strong>universe</strong> is the list of names the book may hold. It changes: companies list (IPO), leave, go bankrupt, get bought.",
            "<strong>Point-in-time</strong> means using only what a researcher could have known on that morning. The opposite is peeking at who survived until now.",
            "<strong>Survivorship bias</strong> is the lie you get by studying only the names still alive. Dead names were often the losers; dropping them makes any rule look better.",
            "Teach the two rebuilds side by side: survivors-only vs point-in-time membership. The gap is the fake premium.",
            "IPOs: a name must not appear before its first trade date. Delistings: the last day still has a return (often ugly). Missing days are not 'drop the row.'",
        ],
        trap="Building the universe from today's index members and filling history backward. That is the default vendor download, and it is wrong.",
    ),
    dict(
        n=123,
        title="The return you actually earn: splits, dividends, delistings",
        skill="Turn a vendor price file into the money a holder of the shares would have made.",
        teach=[
            "A <strong>split</strong> is the company cutting each share into pieces (2-for-1: you have twice as many, each worth about half). The raw price jumps; your wealth does not.",
            "A <strong>dividend</strong> is cash the company pays you for holding the share. The price often drops by about that cash; you still received it.",
            "<strong>Price return</strong> ignores dividends. <strong>Total return</strong> includes them. A backtest on raw prices will lie — usually by looking too good on names that never paid you cash, or too jumpy on split days.",
            "Delist / bankruptcy: the last return is part of the record. Dropping the name the day before the crash is another survivorship lie.",
            "Spinoffs and special dividends: same idea — adjust so the series is the holder's wealth, not the ticker print.",
        ],
        trap="A price-only backtest on unadjusted closes. Teach it as a planted lie: same rule, two panels, two Sharpes.",
    ),
    dict(
        n=124,
        title="The cross-section as the unit of observation",
        skill="Ask 'who beats whom next month?' not 'does this one ticker go up?'",
        teach=[
            "A <strong>characteristic</strong> is a number about a stock today (how cheap, how profitable, how much it already went up).",
            "The <strong>cross-section</strong> is the slice across names at one date: 500 numbers today, not 10 years of one name.",
            "<strong>Residual return</strong> is the part of a name's move left after you subtract the market tide (and, later, industry). That is what a ranker is trying to forecast.",
            "Fama–MacBeth in plain words: each month, draw the line 'next month's residual vs today's characteristic'; then average those monthly slopes and ask if the average is noise.",
            "One tiny worked slope: 3 names, characteristic 1 / 2 / 3, next residual −1 / 0 / +1 → the line slants up. That is a positive slope, not a trading rule yet.",
        ],
        trap="Pooling every name-day into one giant regression and quoting a t-stat as if you had 100,000 independent bets. You had ~120 months. Unit 009 already warned; teach it again on this object.",
    ),
    dict(
        n=125,
        title="Classic baseline I — momentum (12-1)",
        skill="Build the 12-1 winner list, long-only, and say what you lose by not shorting losers.",
        teach=[
            "Everyday idea: names that have been winning for a while often keep winning for a few more months.",
            "<strong>12-1 momentum</strong>: look at the last 12 months of return, drop the most recent month (that month is often a bounce, not a trend), rank names, own the top group.",
            "Why skip last month: short-horizon reversal (Year 5) lives there. Mixing it in muddies the baseline.",
            "Show long-only deciles and the long-short (own winners, short losers). The short side is often half the old academic story. A long-only book only gets the winner half.",
            "Time-series trend (own it vs cash if the name itself is up) is a different rule. Name the difference; do not mix the labels.",
        ],
        trap="Calling any 'what went up, buy it' rule momentum. 12-1, 1-month reversal, and time-series trend are three jobs.",
    ),
    dict(
        n=126,
        title="Classic baseline II — value, and value plus momentum",
        skill="Define cheap vs expensive with a point-in-time ratio, then combine it with 12-1 without peeking.",
        teach=[
            "Everyday idea: a cheap name is one whose price is small compared with something real about the company (book equity, earnings). <strong>Value</strong> is that comparison.",
            "Book/price and earnings/price: define each in words, then as a ratio. The ratio must use the book or earnings that was known that morning (unit 122 / later 204).",
            "Fama–French as the baseline you must beat or own honestly — not as a religion. Size (small vs large) sits next to value; teach it as a characteristic, not a vibe.",
            "Value and momentum often hedge each other (when one is ugly the other is less ugly). A 50/50 and an IC-weighted blend are two different combines; teach both.",
        ],
        trap="Using this year's 10-K earnings in a 2014 characteristic. That is restatement leakage; it belongs in the same breath as the ratio.",
    ),
    dict(
        n=127,
        title="Classic baseline III — quality, investment, low-volatility",
        skill="Add profitability and calmness as characteristics, and show that low-vol is often a hidden beta bet.",
        teach=[
            "<strong>Quality / profitability</strong>: highly profitable, conservative firms. Novy-Marx: gross profit as a characteristic, not a slogan.",
            "<strong>Investment</strong> (Fama–French five-factor): firms that are pouring money into expansion have historically paid less. Teach the characteristic, then the story, in that order.",
            "<strong>Low-volatility</strong>: the calmest names have historically paid almost as much as jumpy ones. That is a puzzle, not a free lunch.",
            "Neutralize beta (strip the market tide from the score). After that, a lot of the low-vol 'edge' shrinks. The lesson must show the before/after.",
        ],
        trap="Selling low-vol as alpha when the book is just refusing to own high-beta names. Unhedged, you are underweight the market in a specific way.",
    ),
    dict(
        n=128,
        title="The factor zoo and publication decay",
        skill="Treat a pile of characteristics as a multiple-testing problem, and expect published edges to shrink.",
        teach=[
            "Re-warm Harvey–Liu–Zhu (unit 007): if you search 20 characteristics and keep the winner, the t-stat is a max, not a single test.",
            "McLean–Pontiff: after a paper comes out, the edge often fades. Crowding and data-mining both do this; teach both stories.",
            "Hou–Xue–Zhang: most 'anomalies' do not replicate under one common protocol. The zoo is not a menu of free edges.",
            "Bonferroni and Benjamini–Hochberg on the same 20-characteristic screen. They will disagree; teach what each is promising.",
        ],
        trap="Keeping a characteristic because the story is pretty after you saw the t-stat. Pre-commit the list (unit 157 will make this a habit).",
    ),
    dict(
        n=129,
        title="The benchmark you claim to beat",
        skill="Build the index you will be judged against, and show why beating equal-weight is the easier exam.",
        teach=[
            "Cap-weight vs equal-weight: in cap-weight, bigger companies are a bigger slice. In equal-weight, every name is the same size (you rebalance to keep it that way).",
            "Reconstitution: the index committee (or rule) adds and drops names on known dates. Your universe and your benchmark must use the same as-of membership.",
            "Float: not every share can trade (insiders, governments). A real cap-weight index uses shares that can trade.",
            "Sharpe's arithmetic: after fees, beating the cap-weight market is a zero-sum exam among active managers. Teach why 'I beat the equal-weight basket' is a different, usually easier, claim.",
        ],
        trap="Backtesting against equal-weight and quoting the result as if you beat the S&amp;P 500.",
    ),
    dict(
        n=130,
        title="Q1 checkpoint — honest long-only factor notebook",
        skill="Put 121–129 on one page: PIT universe, total returns, 12-1 + value, IR vs a named benchmark, a multiple-testing note.",
        kind="chk",
        teach=[
            "The learner rebuilds the universe two ways and shows the fake premium.",
            "Total-return vs price-only on the same rule.",
            "12-1 and value, long-only, IR and Sharpe vs a named cap-weight and vs equal-weight.",
            "A written sentence on how many characteristics were searched.",
        ],
        trap="A checkpoint that only reports the pretty Sharpe.",
    ),
    dict(
        n=131,
        title="The monthly prediction target",
        skill="Pick one number the model is trying to forecast, and say why the other two are different jobs.",
        teach=[
            "Three candidates: next-month residual return; next-month rank (who beats whom); next-month excess vs the benchmark.",
            "Triple-barrier (unit 035) is a path-dependent label for a trade. A monthly residual is a simpler label that matches a monthly rebalance. Teach the contrast; do not throw AFML away.",
            "Gu–Kelly–Xiu as the paper that already ran 'ML vs linear' on monthly characteristics. This year must beat or honestly match that kind of baseline, not invent a new exam.",
            "A target that includes next month's market tide will teach the model to forecast beta. Residualize first if the mandate is 'who beats whom.'",
        ],
        trap="Training on next-month raw return and then being surprised the model just bought high-beta names.",
    ),
    dict(
        n=132,
        title="Point-in-time features — no restated numbers",
        skill="Build a feature table whose every cell could have been known that morning.",
        teach=[
            "Features at this clock: lagged returns, size, value ratios, revisions, industry. Each one gets an as-of rule.",
            "Restated fundamentals: the company later changes last year's earnings. A leaked join pastes the new number onto old dates.",
            "Plant the leak on purpose (CCC-style restatement) and catch it with a vintage table: what was on the tape as of date D.",
            "Industry and country are characteristics too; they must be as-of (reclassifications happen).",
        ],
        trap="A 'fundamentals' CSV with one row per name per year and no vintage date. That file cannot support an honest join.",
    ),
    dict(
        n=133,
        title="Information coefficient and matching the rebalance to the decay",
        skill="Measure how well today's scores line up with future residuals, and pick a hold that matches how fast that line dies.",
        teach=[
            "<strong>Information coefficient (IC)</strong>: correlation between today's scores and next period's residual returns. High IC means the ranking is informative, not that you have a book yet.",
            "IC by holding week 1, 2, … 8. The decay tells you whether monthly rebalance is too slow or too fast for this score.",
            "Re-warm the Fundamental Law (unit 084): IR ≈ IC × √breadth × transfer coefficient. Breadth here is ~N names per month, not 10,000 name-days.",
            "A score that dies in five days does not belong in a monthly book (send it to Year 5). A score that is still alive at week 8 can sit still.",
        ],
        trap="Rebalancing monthly because 'that is what factor funds do' while the IC is already dead by week two.",
    ),
    dict(
        n=134,
        title="Linear cross-sectional models",
        skill="Fit a monthly line, after stripping industry, size, and beta from the features.",
        teach=[
            "Weighted least squares in one sentence: names with noisier residuals get less pull on the line.",
            "Industry neutralization: subtract the industry average from the feature (or from the residual) so you are not just buying 'all tech.'",
            "Residualizing size and beta: the leftover characteristic is what is not already 'it is a small name' or 'it rides the market.'",
            "This linear model is the thing the tree model in 135 must beat. Teach it as a respected baseline, not a straw man.",
        ],
        trap="A pooled OLS on the stacked panel with i.i.d. standard errors. The t-stat is a toy.",
    ),
    dict(
        n=135,
        title="Trees on the monthly cross-section",
        skill="Train a gradient-boosted tree as a regressor and as a ranker, with a walk-forward that does not peek.",
        teach=[
            "Re-warm unit 047: a tree asks a sequence of yes/no questions about features. Boosting adds many small trees.",
            "Regressor vs ranker: MSE tries to hit the exact residual; a rank objective tries to get the order of names right. The mandate is closer to order.",
            "Walk-forward year-blocks: train on years 1–7, test 8; then 1–8, test 9. No i.i.d. K-fold.",
            "Gu–Kelly–Xiu: trees helped on monthly characteristics versus a linear model. Teach what they actually did, including the failures.",
        ],
        trap="Tuning hyperparameters on the same years you will quote as out-of-sample (unit 048, again).",
    ),
    dict(
        n=136,
        title="Learning-to-rank for 'who beats whom'",
        skill="State pairwise and listwise losses as 'punish a wrong order,' and compare them to MSE on the same panel.",
        teach=[
            "Pairwise: for two names, was the one we liked more actually better next month? A loss that cares about that pair.",
            "Listwise: the whole day's ranking is one object. LambdaMART / LightGBM rank as the practical tool.",
            "Top-decile IR is the mandate-shaped metric: we only own the names we like most. A model that is great in the middle and wrong at the top is useless here.",
            "This is still a score. Holdings come later (141–150).",
        ],
        trap="Optimizing MSE and then being surprised the top 50 names are a mess.",
    ),
    dict(
        n=137,
        title="Cross-sectional CV that respects time and names",
        skill="Show that ordinary K-fold leaks, and replace it with purged year-blocks.",
        teach=[
            "Re-warm AFML 7: overlapping labels and a shared market day mean random K-fold trains on the future.",
            "A second leak: the same firm in train and test across a split that ignores time.",
            "Walk-forward year-blocks vs i.i.d. K-fold on the same features. The fake lift is the lesson.",
            "Embargo: leave a gap after the train window so the last training residual does not share a path with the first test residual.",
        ],
        trap="Purging days but not embargoing the residual overlap. The leak is quieter, not gone.",
    ),
    dict(
        n=138,
        title="Combining ML scores with classic factors",
        skill="Measure incremental IR: what the blend adds after 12-1 and value are already in the book.",
        teach=[
            "Re-warm unit 049 / Grinold 11–14: stacking, IC-weighting, orthogonalizing a new score to the ones you already have.",
            "A blend of linear + GBDT + 12-1. The question is not 'is the blend's IR high?' It is 'did the tree add anything the 12-1 did not already give?'",
            "Correlation of scores is not correlation of book returns; teach both.",
        ],
        trap="Reporting the blend's raw IR and calling the tree a win when it is 12-1 in costume (Year 5 unit 179 is the daily twin).",
    ),
    dict(
        n=139,
        title="When ML adds nothing",
        skill="Kill your own monthly model on a holdout and write the autopsy.",
        teach=[
            "Small monthly samples: 10 years × 12 = 120 fits. A flexible tree can memorize regimes.",
            "Regime breaks: a rule that worked in 1995–2007 can die after. McLean–Pontiff again.",
            "Feature death: a characteristic that was informative becomes crowded. The model will not announce this; the IC will.",
            "The required artifact is a written autopsy, not a quieter chart.",
        ],
        trap="Retraining until the holdout looks good. That holdout is then gone.",
    ),
    dict(
        n=140,
        title="Q2 checkpoint — leakage-free monthly ranker",
        skill="Defend or kill a walk-forward GBDT against a linear model and 12-1, on IR, with the leak hunt written down.",
        kind="chk",
        teach=[
            "Features → model → walk-forward IC and long-only IR.",
            "Same exam for linear and 12-1.",
            "A paragraph that either defends the incremental IR or kills the net.",
        ],
        trap="A checkpoint that only shows the tree's in-sample IC.",
    ),
    dict(
        n=141,
        title="From score to weight without an optimizer",
        skill="Turn a ranking into holdings three simple ways, and see what an optimizer will later be asked to beat.",
        teach=[
            "Top-N: own the N names you like most, equal weight. Everyday shopping cart.",
            "Quantile tilt: own more of the top fifth, less (or none) of the bottom fifth, still long-only.",
            "Rank-weight / z-score tilt: size the name by how strong the score is, then clip negatives to zero if you cannot short.",
            "Compare turnover and IR of these three to the same-score long-short book. The gap is the long-only tax (143 will name it transfer coefficient).",
        ],
        trap="Jumping to a quadratic program before the learner can do top-N by hand.",
    ),
    dict(
        n=142,
        title="Active weights and the one-period utility",
        skill="Write 'like more of this, minus risk, minus costs' as a function, then solve a 10-name toy by hand and as a QP.",
        teach=[
            "<strong>Active weight</strong> is how much more (or less) of a name you own than the benchmark does. If the index is 2% of AAA and you own 5%, active weight is +3%.",
            "One-period utility in words: expected extra return − λ × risk − costs. λ is how much you hate being different from the index (or how much you hate bounce).",
            "The 10-name toy: write the numbers, take the derivative or complete the square, get the weights. Then show the same answer from a quadratic program.",
            "Re-warm Markowitz (081): unconstrained MVO is brittle. That is why 144–149 exist.",
        ],
        trap="Maximizing expected return with no risk term and calling it optimization. That is 'buy the highest score until the money is gone.'",
    ),
    dict(
        n=143,
        title="Long-only as a constraint",
        skill="Show the optimizer clipping negative weights, and measure what you lose versus long-short (transfer coefficient).",
        teach=[
            "A <strong>constraint</strong> is a rule the holdings must obey. 'No negative weights' is the long-only rule.",
            "When the unconstrained solution wants to short a name, the constrained solution sets that weight to 0 and dumps the leftover into other names. The book is no longer the score.",
            "<strong>Transfer coefficient</strong>: how much of the score's ranking survived the rules. 1 means the book matches the score; 0 means the rules ate the idea.",
            "Same alpha, three mandates: long-only, long-short, 130/30 (a little short sleeve). Teach 130/30 as an overlay, not the default.",
        ],
        trap="Reporting the unconstrained IR as if it were the long-only book.",
    ),
    dict(
        n=144,
        title="Risk models the optimizer trusts",
        skill="Plug three risk models into the same utility and compare promised active risk to realized tracking error.",
        teach=[
            "The optimizer needs a forecast of how names bounce together. That forecast is the <strong>risk model</strong>.",
            "Three families: fundamental (Barra-style: industry + style factors), statistical (PCA / shrinkage from 082), and a naive sample covariance.",
            "Promised active risk vs realized tracking error. A model that is always '2% active risk' and delivers 6% is not conservative — it is wrong.",
            "Re-warm 082–083: cleaned covariance is a risk input, not a trading rule.",
        ],
        trap="Using a 500-name sample covariance with 12 months of daily data and trusting the optimizer's risk number.",
    ),
    dict(
        n=145,
        title="Linear constraints real books have",
        skill="Add sector, name, beta, turnover, and name-count caps one by one, and watch IR and tracking error move.",
        teach=[
            "Name cap: 'no more than 4% in one stock.' Sector cap: 'no more than 20% in banks.' Beta cap: 'stay near the market tide.'",
            "Turnover cap: 'do not trade more than X% of the book this month.' Name count: 'hold between 40 and 80 names.'",
            "Each cap is a sentence a PM can say. Teach the sentence, then the inequality.",
            "A book that hugs the index to satisfy every cap is a closet indexer (158). Tracking error will look tiny and IR will look stable.",
        ],
        trap="Adding constraints until the book is the benchmark, then celebrating the low tracking error.",
    ),
    dict(
        n=146,
        title="Cost-aware optimization and capacity",
        skill="Put spread and impact in the utility, and draw net IR against assets under management.",
        teach=[
            "Re-warm 088: turnover × spread is the first bill. Impact (064, square-root law) is the bill that grows with size.",
            "A turnover penalty is a cheaper cousin of a full impact model. Teach both; use the penalty first.",
            "<strong>Capacity</strong> is the AUM at which net IR hits your hurdle (often zero). Draw the curve.",
            "Boyd et al. 2017 as the clean modern write-up of 'return − risk − costs.'",
        ],
        trap="A paper IR with zero costs, quoted as the live number.",
    ),
    dict(
        n=147,
        title="Multi-period rebalancing: when not to trade",
        skill="Show that a decaying score plus today's cost says 'do not fully chase this month's list.'",
        teach=[
            "Myopic: each month, pretend there is no tomorrow and trade to the new target. That churns.",
            "Gârleanu–Pedersen / Boyd multi-period: because the score fades and trading costs money, the right book is between last month's holdings and this month's dream book.",
            "Count the skipped trades. That count is the lesson, not a footnote.",
            "Half-life of the score (from 133) is an input to this problem, not a separate hobby.",
        ],
        trap="Rebalancing fully to the new target every month 'because the optimizer said so' while IC decay is slow and costs are not.",
    ),
    dict(
        n=148,
        title="Convex optimization toolkit",
        skill="Say what a QP/SOCP is, why convexity lets a solver certify a solution, and what a non-convex tweak throws away.",
        teach=[
            "Everyday picture: you are standing in a bowl. Any local lowest point is the global lowest point. That is <strong>convex</strong>. A solver can promise it found the bottom.",
            "A <strong>quadratic program</strong> has a bowl-shaped objective and straight-line constraints. Long-only + sector caps + a quadratic risk term is a QP.",
            "SOCP: a slightly richer bowl (e.g. some impact terms). Teach when you need it.",
            "A non-convex variant (a ratio, a cardinality trick without a reformulation) cannot be certified. Show one on purpose.",
            "Boyd–Vandenberghe selected chapters; OSQP / Clarabel as the engines, not the idea.",
        ],
        trap="Calling 'we ran scipy.optimize with a random start' an optimal book.",
    ),
    dict(
        n=149,
        title="Robust and resampled optimization",
        skill="Perturb the scores and show naïve MVO thrashing, then compare shrinkage and a simple tilt.",
        teach=[
            "Inputs are noisy. A 1% change in a score can flip a naïve MVO book. Teach this with a perturbation, not a speech.",
            "Resampling (Michaud): average the books from noisy inputs. Shrinkage (Ledoit–Wolf, again): calm the covariance.",
            "A simple tilt (141) is often more stable than a fancy robust program. Honesty about that is in-syllabus.",
        ],
        trap="Treating robustness as a reason to skip the QP. Robustness is a test of the QP, not a replacement for stating the utility.",
    ),
    dict(
        n=150,
        title="Q3 checkpoint — scores become a constrained book",
        skill="Take the Q2 scores through risk + costs + long-only/sector/beta constraints and defend net IR.",
        kind="chk",
        teach=[
            "One written utility. One risk model. One cost model. Constraints listed as sentences.",
            "Transfer coefficient vs the unconstrained book.",
            "Net IR vs the named benchmark. Capacity sentence.",
        ],
        trap="A checkpoint that reports the unconstrained paper IR.",
    ),
    dict(
        n=151,
        title="Between rebalances: drift, dividends, cash",
        skill="Follow the book from this close to next month's close without pretending weights stay put.",
        teach=[
            "Weights <strong>drift</strong>: names that went up become a bigger slice even if you do nothing. That is not a trade; it is arithmetic.",
            "Dividends arrive as cash. Cash earns (almost) nothing in this mandate unless you say otherwise.",
            "A mid-month split or spinoff changes share counts. The wealth series must stay honest (123, again).",
            "P&amp;L split into selection (you picked well) vs interaction (drift helped or hurt). Preview of 155.",
        ],
        trap="Marking the month's return as w'r with frozen start-of-month weights and ignoring cash.",
    ),
    dict(
        n=152,
        title="Implementation shortfall at a monthly horizon",
        skill="Name the gap between the paper book and the fills, and put that gap on the IR.",
        teach=[
            "Perold: <strong>implementation shortfall</strong> is paper return minus live return. Decision price vs arrival vs fills.",
            "Re-warm 091–093: TWAP/VWAP the monthly trade list. At this clock you usually have days, not milliseconds.",
            "Paper IR vs net IR after shortfall. The lesson is the subtraction.",
        ],
        trap="Assuming a monthly book 'doesn't need execution' because it trades rarely. Rare × large is still a bill.",
    ),
    dict(
        n=153,
        title="Index-futures overlay to control beta",
        skill="Keep the stock cart long-only and use a short index future to strip the market tide.",
        teach=[
            "A <strong>future</strong> is a contract to buy or sell the index later. Short the future ≈ bet the index falls (or hedge a long stock cart).",
            "Same names, two books: unhedged (Sharpe is mostly beta) vs hedged (IR and Sharpe should get closer).",
            "Roll cost: futures expire; you replace them. That is a small, real leak.",
            "This is allowed under a long-only *stock* mandate if the PM says so. Teach it as an overlay, not a sneak-short of names.",
        ],
        trap="Calling the hedged book 'market-neutral alpha' when the hedge is sloppy (wrong beta, wrong index, wrong roll).",
    ),
    dict(
        n=154,
        title="Drawdowns a long-only book will eat",
        skill="Walk 2008 and 2020 on the unhedged vs hedged book, and write the client memo.",
        teach=[
            "A <strong>drawdown</strong> is the fall from a peak to a later trough. Long-only unhedged will take the market's drawdown, plus or minus your active return.",
            "Re-warm 085–089: copulas and tails if you stress several names together. A Gaussian '−2σ' is not 2008.",
            "The memo: what happened, what the mandate promised, what would have been different with the futures overlay.",
        ],
        trap="Killing a good ranker because the unhedged book fell with the market. That is the mandate, not a failed signal — unless IR also died.",
    ),
    dict(
        n=155,
        title="Attribution: where the extra return came from",
        skill="Split a year of active return into allocation, selection, interaction, and beta.",
        teach=[
            "Brinson–Fachler in words: did you overweight the right industries (allocation), and inside an industry did you pick the right names (selection)? Interaction is the leftover cross term.",
            "Factor attribution: how much of the extra return is just value or momentum you already knew you owned.",
            "Optimizer-implied bets: the constraints force holdings; those forced bets have P&amp;L too.",
        ],
        trap="A year of 'the book made 2% active' with no sentence about whether it was industry bets or name picks.",
    ),
    dict(
        n=156,
        title="Capacity, crowding, live vs paper for slow equity",
        skill="Scale AUM until net IR hits the hurdle, and say what crowding does to a published characteristic.",
        teach=[
            "Re-warm 088 / 146. Monthly capacity is larger than daily (Year 5 / 189) because you trade less.",
            "Crowding: McLean–Pontiff and Korajczyk–Sadka. Other people's orders are a cost you do not see in a solo backtest.",
            "Live-vs-paper: stale membership, late fundamentals, a reconstitution you missed. Preview of Year 6.",
        ],
        trap="Quoting the paper IR at $10M and the capacity story from a different paper at $10B.",
    ),
    dict(
        n=157,
        title="Pre-register the research",
        skill="Write the kill criteria before looking at results.",
        teach=[
            "Universe, target, constraints, cost model, hurdle IR, what would make you kill the book — on one page, dated, before the run.",
            "TEMPLATE_PORTFOLIO.md as the daily cousin; this page is the monthly cousin.",
            "Changing the target after seeing IC is a new trial (007, again).",
        ],
        trap="A 'pre-registration' written after the first pretty chart.",
    ),
    dict(
        n=158,
        title="Failure modes of this mandate",
        skill="Name and plant four bugs: leaked fundamentals, index-hugging, hidden beta, overfit optimizer.",
        teach=[
            "Leaked fundamentals (132). Index-hugging (145). Hidden beta (127 / 131). Overfit optimizer (149 / 048).",
            "The learner finds the four bugs in a notebook they did not write. That is the skill.",
        ],
        trap="A 'failure modes' lecture with no planted bugs.",
    ),
    dict(
        n=159,
        title="Overlays a real book meets",
        skill="Add a restricted list and a 130/30 sleeve, and measure IR and turnover change.",
        teach=[
            "Restricted list: names you may not own (ESG, compliance, a client ban). The optimizer must treat them as a hard zero.",
            "130/30: 130% long, 30% short. A little short sleeve. Not the default mandate.",
            "Tax-aware / lots: mentioned as a later overlay (Year 6), not a rewrite of the pre-tax book.",
        ],
        trap="Building the research book on an unrestricted universe and then dropping names at the end. The scores were wrong for the constrained world.",
    ),
    dict(
        n=160,
        title="Year-4 exit — monthly long-only capstone",
        skill="Defend a PIT, walk-forward, cost-aware long-only book on net IR vs a named benchmark, including beta, the no-short tax, and capacity.",
        kind="exit",
        teach=[
            "End-to-end: universe → features → ranker → constrained optimizer → net IR → capacity → attribution → proceed/kill memo.",
            "Defended as to a PM who forbids shorts.",
            "This is not the Year-3 capstone and not the Year-5 daily book.",
        ],
        trap="A capstone that is a long-short notebook with the shorts deleted in the last cell.",
    ),
]


Y5 = [
    dict(
        n=161,
        title="Mid-frequency vs mid-horizon: the same rules, a faster clock",
        skill="Keep the long-only exam (IR vs a named benchmark) and put costs in the first sentence, not the last.",
        teach=[
            "Hold is now hours to a few days. Lesson 001 called this <strong>mid-frequency</strong>. Year 4 was weeks-to-months.",
            "Same long-only rule: no borrowed-share shorts. Same exam: net IR vs a named benchmark.",
            "The Q1 lab already lived on this clock, but it was allowed to short. This year drops the shorts and adds a volume cap.",
            "Same scores, daily vs monthly rebalance, after costs: the monthly book often wins on net IR. That comparison is the opening fact.",
            "More independent bets (~2,500 days in 10 years vs ~120 months) means more power and more chances to overfit.",
        ],
        trap="Taking Year 4's monthly optimizer and running it every close. Unit 181 exists to make that pain concrete; preview it here.",
    ),
    dict(
        n=162,
        title="The clock of a trading day",
        skill="Split a day's return into overnight, open-to-close, and the close auction, and say which one your rule is betting on.",
        teach=[
            "Open: the first prints. Continuous session: the day. <strong>Close auction</strong>: the end-of-day match that sets the official close. Overnight / <strong>gap</strong>: close to next open.",
            "Heston–Korajczyk–Sadka: the cross-section is not the same at 10:00 and at 15:50.",
            "Lou–Polk–Skouras: who you hold through the close is a different bet from who you hold from open to close.",
            "A close-to-close target mixes overnight and the session. Teach when that mix is intended.",
        ],
        trap="Scoring at today's close to 'predict' today's close-to-close return. That is the same-day leak (172).",
    ),
    dict(
        n=163,
        title="Liquidity as a membership rule",
        skill="Refuse names you cannot trade, before you compute a score.",
        teach=[
            "<strong>ADV</strong> (average daily dollar volume): roughly how many dollars of this stock trade in a typical day.",
            "<strong>Participation</strong>: the slice of today's volume you take. '3% of ADV' is a hard refusal, not a hope.",
            "<strong>Days-to-trade</strong>: how many days to enter or exit at that participation. If it is 8 days, a 1-day hold is a fantasy.",
            "Amihud as a simple illiquidity number (|return| / dollar volume). Use it as a filter, not as a premium to harvest blindly.",
            "Same signal, liquid-only vs all names: the fake IR from illiquids is the lesson.",
        ],
        trap="A beautiful IR built on names that did not trade enough for your AUM.",
    ),
    dict(
        n=164,
        title="Short-horizon baseline I — 1–5 day reversal",
        skill="Build long-only 1–5 day reversal and net it of costs; contrast it with Year 4's 12-1.",
        teach=[
            "Everyday idea: names that just fell often bounce a bit over the next few days. That is the opposite of 12-1 momentum.",
            "Jegadeesh 1990 and Lehmann 1990 are the papers. The Q1 lab's <code>rev5</code> is this idea with shorts.",
            "Long-only top-decile vs long-short. Costs eat a daily reversal fast. Net IR is the only number that counts.",
        ],
        trap="Calling reversal 'momentum' or running it monthly. Wrong name, wrong clock.",
    ),
    dict(
        n=165,
        title="Residual and industry-neutral reversal",
        skill="Strip industry and the market from the lookback so the bounce is not 'all banks fell yesterday.'",
        teach=[
            "Raw reversal buys everything that fell, including a whole industry that had a bad day.",
            "Residual reversal: bounce relative to industry (and beta). The leftover is closer to 'this name, not this sector.'",
            "Residual momentum (medium horizon) is a different cousin; name it so the labels stay clean.",
        ],
        trap="A 'residual' that still contains yesterday's market because the residualization used the full sample, including today.",
    ),
    dict(
        n=166,
        title="Event baseline — post-earnings announcement drift",
        skill="Own names after an earnings surprise using the timestamp of the print, not the calendar date.",
        teach=[
            "<strong>PEAD</strong>: after a company reports, the price often keeps moving the same way for days. Slow digestion.",
            "Bernard–Thomas. Surprise vs a simple forecast (last year, or analysts). Teach one honest surprise definition.",
            "Announce time: after the close vs before the open. Treating an after-close print as known at that day's close is a leak.",
            "Revisions and upgrades are cousins; PEAD is the required baseline.",
        ],
        trap="An earnings calendar with a date and no time. Half the prints are after 16:00.",
    ),
    dict(
        n=167,
        title="Overnight and the close auction as a holding decision",
        skill="Compare hold-through-close vs flatten-at-close on the same scores.",
        teach=[
            "If you hold through the close, you eat the overnight gap (191). If you flatten, you pay two tickets (exit today, enter tomorrow) and miss the overnight return.",
            "A lot of a daily book's volume happens at the auction (188). Who you are at 15:50 is a design choice.",
            "Net IR of the two holding rules on the same ranker.",
        ],
        trap="Assuming 'daily' means you are flat overnight. Many daily books are not.",
    ),
    dict(
        n=168,
        title="News and text as a daily ranker, not a vibe",
        skill="Turn a filing or headline into a next-day residual feature with an as-of timestamp.",
        teach=[
            "Re-warm 075–076: Loughran–McDonald counts; embeddings later. The job is a rank, not a sentiment essay.",
            "Tetlock as the cautionary daily-media paper: easy to overfit.",
            "Timestamp again: a 16:01 headline is not a 15:59 feature.",
        ],
        trap="A news score that uses the next morning's write-up of today's move.",
    ),
    dict(
        n=169,
        title="Combining short-horizon baselines under more trials",
        skill="Screen ~15 daily signals with a multiple-testing correction that matches how you will commit capital.",
        teach=[
            "More days ⇒ more trials ⇒ more false winners (007, 128). Daily does not relax the bar; it invites more searching.",
            "Bonferroni / BH on the same list. Keep only what survives the bar you would use to fund the book.",
        ],
        trap="'We have 2,500 days so t = 2 is fine.' Breadth is not a license to skip the family of tests.",
    ),
    dict(
        n=170,
        title="Q1 checkpoint — reversal + PEAD, costs first",
        skill="A liquid PIT universe, two baselines net of costs, IR vs a named benchmark, a trial-count sentence.",
        kind="chk",
        teach=[
            "Liquid mask from 163. Reversal and PEAD, long-only, net IR.",
            "Same-day leak hunt on the earnings timestamps.",
        ],
        trap="A checkpoint that reports gross IR.",
    ),
    dict(
        n=171,
        title="The 1–5 day prediction target",
        skill="Choose next-day residual, open-to-close, or a short triple-barrier, and say which clock it matches.",
        teach=[
            "Three targets, same features. IC and long-only IR for each.",
            "A 5-day triple-barrier (035) is legal if the hold is 5 days. Overlap then becomes 174.",
            "Open-to-close drops the overnight. That is a different mandate (162).",
        ],
        trap="A close-to-close target built from a score that already contains today's close.",
    ),
    dict(
        n=172,
        title="Point-in-time daily features",
        skill="Build yesterday's residuals, volume shocks, range, overnight gap — and plant a same-day-close leak.",
        teach=[
            "Allowed: information available at the decision time (e.g. yesterday's close, this morning's open if you trade at 10:00).",
            "Forbidden: today's close in a score that claims to predict today's close-to-close.",
            "Volume shocks and range are magnitude features; they can leak if they include the same interval you forecast.",
        ],
        trap="The leak is one column. The lesson plants it and requires the learner to find it.",
    ),
    dict(
        n=173,
        title="IC decay over hours and days",
        skill="Plot IC at close+1h, +1d, +5d and pick a hold that matches the death of the score.",
        teach=[
            "Same IC idea as 133, faster grid.",
            "A score dead by tomorrow morning does not belong in a 5-day hold.",
            "This number becomes the half-life in 187.",
        ],
        trap="A 5-day hold on a one-hour signal 'to reduce turnover' without checking that the IC is already gone.",
    ),
    dict(
        n=174,
        title="Overlapping daily labels and uniqueness",
        skill="Weight 5-day labels by how unique they are, because Tuesday's 5-day path shares days with Monday's.",
        teach=[
            "Re-warm 038–039. A 5-day residual starting every day is not 2,500 independent bets.",
            "Average uniqueness. Sequential bootstrap as the sampling story.",
            "Unweighted vs uniqueness-weighted IC. The gap is the lesson.",
        ],
        trap="Quoting a t-stat on overlapping 5-day returns as if n = number of rows.",
    ),
    dict(
        n=175,
        title="Trees on the daily cross-section",
        skill="Walk-forward a daily GBDT (regress and rank) against linear and 5-day reversal.",
        teach=[
            "Same tools as 135, daily rows, uniqueness weights from 174.",
            "Purged walk-forward. No i.i.d. K-fold.",
            "Must beat or honestly lose to reversal. A tree that is reversal in costume fails 179.",
        ],
        trap="A giant in-sample daily fit with 200 features and a pretty IC.",
    ),
    dict(
        n=176,
        title="Short return-paths as features, without becoming DeepLOB",
        skill="Compare 20-day path features to simple aggregates under an honest split, and keep tabular unless the path wins.",
        teach=[
            "Re-warm 071–072 only as far as 'a sequence can be a feature.' This is not a LOB net (073).",
            "Aggregates (mean, vol, last residual) vs the raw 20-day vector.",
            "If the path does not win honestly, keep the aggregates. That decision is in-syllabus.",
        ],
        trap="Importing a transformer because Year 2 Q4 exists. Deep sequence models earn their keep on microstructure and text, not by default on 20 daily returns.",
    ),
    dict(
        n=177,
        title="Event-aware ML",
        skill="Flag earnings and news days so the model does not treat them as ordinary Tuesdays.",
        teach=[
            "A PEAD day is a different data-generating process. A flag (or a separate model) is the honest design.",
            "Compare with/without flags. Leftover PEAD after the flag is the test of whether the tree already stole 166.",
        ],
        trap="Dropping earnings days from training and then trading them live.",
    ),
    dict(
        n=178,
        title="Two clocks, one research book",
        skill="Combine a daily ML sleeve with Year 4's monthly scores and measure incremental IR.",
        teach=[
            "Grinold blend again. Correlation of the two sleeves' active returns.",
            "One long-only NAV, two rebalance clocks (234 / 198 will operationalize this).",
            "Incremental IR of adding the daily sleeve to a monthly book that already exists.",
        ],
        trap="Adding the daily sleeve and quoting the combined Sharpe, which is still mostly beta.",
    ),
    dict(
        n=179,
        title="When daily ML is just reversal in costume",
        skill="Residualize the ML score on 5-day reversal and see whether any leftover IR remains.",
        teach=[
            "Orthogonalize the score to the baseline. If leftover IR dies, the tree is a fancy reversal.",
            "Write the autopsy even if the leftover lives — say how much of the IR was the baseline.",
        ],
        trap="A model card that never mentions 164.",
    ),
    dict(
        n=180,
        title="Q2 checkpoint — daily ranker, defend or kill",
        skill="Walk-forward IC/IR vs reversal and PEAD, leak hunt included.",
        kind="chk",
        teach=[
            "Same structure as 140, daily clock, uniqueness weights, costs on the IR.",
        ],
        trap="A checkpoint that reports gross IC.",
    ),
    dict(
        n=181,
        title="Why the Year-4 optimizer, run daily, goes broke",
        skill="Run the monthly-tuned QP every close and watch costs eat the book.",
        teach=[
            "Take the 150 optimizer, change the calendar to daily, do not retune the turnover penalty.",
            "Turnover explodes. Net IR dies. That plot is the lesson.",
            "The fix is not 'trade less for vibes.' The fix is 182–187: ADV caps, impact, multi-period at a 1–5 day half-life.",
        ],
        trap="Silently raising the turnover penalty until the plot looks like Year 4 and calling it the same model.",
    ),
    dict(
        n=182,
        title="Participation caps: do not take more than a slice of ADV",
        skill="Write a hard ADV constraint and list the names the optimizer wanted but could not buy.",
        teach=[
            "Participation as a number (e.g. 3% of ADV) and as an inequality in the QP.",
            "Names you loved and could not own. That list is the capacity story at the name level.",
            "A soft penalty vs a hard cap. Teach both; the PM usually wants a hard cap.",
        ],
        trap="A 'liquidity score' in the ranker instead of a cap in the optimizer. The ranker will still ask for 20% of a name's volume.",
    ),
    dict(
        n=183,
        title="Intraday vs close-only rebalance",
        skill="Compare one close optimization vs an open-and-close pair on net IR.",
        teach=[
            "Close-only: one book a day, auction-heavy (188).",
            "Open + close: two decisions. More chances to be right, more tickets, more ways to leak the open print.",
            "Net IR, not 'more trades look sophisticated.'",
        ],
        trap="Using the 10:00 print in a score that was supposed to be decided at 9:31.",
    ),
    dict(
        n=184,
        title="Temporary impact on a daily trade list",
        skill="Apply the square-root law to today's list and subtract it from paper IR as AUM grows.",
        teach=[
            "Re-warm 064 / Almgren 2005. Temporary impact grows with (your dollars / ADV)^0.5, roughly.",
            "Paper vs impact-adjusted IR. The curve vs AUM is 189's cousin.",
        ],
        trap="A linear cost (spread only) at a size where impact dominates.",
    ),
    dict(
        n=185,
        title="Liquidity-aware risk: exiting is the hard day",
        skill="Stress a 5-day liquidation of the long-only book and watch 'diversifiers' become the same trade.",
        teach=[
            "Names that look diversifying in a covariance can be the same exit when everyone sells.",
            "Kyle / Amihud again: the cost of getting out is part of risk, not a surprise.",
            "A 5-day unwind schedule at the participation cap. Days-to-exit per name.",
        ],
        trap="A risk model that assumes you can trade any name tomorrow at yesterday's spread.",
    ),
    dict(
        n=186,
        title="Daily futures overlay on a high-turnover stock book",
        skill="Hedge beta every day with an index future while the cash names stay long-only; include roll cost.",
        teach=[
            "Same idea as 153, daily. The hedge must move when the stock cart's beta moves.",
            "Unhedged Sharpe vs hedged Sharpe vs IR. Roll cost as a line item.",
        ],
        trap="A hedge sized on yesterday's beta and left for a week on a book that turns over 30% a day.",
    ),
    dict(
        n=187,
        title="Multi-period daily: a 1–5 day half-life",
        skill="Smooth toward the target instead of chasing every close; count the skipped turnover.",
        teach=[
            "Gârleanu–Pedersen / Boyd again, with the half-life from 173.",
            "Myopic daily vs smoothed. Turnover cut vs IR kept.",
        ],
        trap="Copying Year 4's monthly half-life into the daily program.",
    ),
    dict(
        n=188,
        title="Auction-aware execution",
        skill="Decide how much of the list goes to the close auction vs a TWAP, and measure shortfall.",
        teach=[
            "MOC / LOC: market-on-close and limit-on-close. These are the order types a daily book actually uses (222).",
            "Perold shortfall on the daily list. Auction vs TWAP.",
            "Kissell as optional practitioner reading, not a second theory.",
        ],
        trap="Assuming you get the close print as a fill. You get a fill in the auction, which can differ (162's auction jump).",
    ),
    dict(
        n=189,
        title="Capacity is smaller than Year 4",
        skill="Draw net IR vs AUM for the daily book next to the monthly book, same capital.",
        teach=[
            "Daily turnover × impact ⇒ the AUM where IR hits the hurdle is smaller.",
            "Same names, two clocks, two curves. The comparison is the lesson.",
        ],
        trap="Funding the daily book at Year 4's AUM because 'it is the same stocks.'",
    ),
    dict(
        n=190,
        title="Q3 checkpoint — ADV-capped daily book",
        skill="Daily scores + ADV caps + impact + optional futures hedge; defend net IR and the death-AUM.",
        kind="chk",
        teach=[
            "Written constraints. Participation list of refused names. Net IR. AUM where it dies vs Year 4.",
        ],
        trap="A checkpoint that uses Year 4's turnover penalty 'because it was already coded.'",
    ),
    dict(
        n=191,
        title="Overnight gap risk",
        skill="Split P&amp;L into overnight vs session and autopsy a gap day.",
        teach=[
            "You are long into the open if you held the close (167). One ugly gap can be the week's P&amp;L.",
            "Overnight vs intraday contribution over a quarter. A single gap-day write-up.",
        ],
        trap="Averaging overnight returns and calling the risk 'small' because the mean is small. The tail is the risk.",
    ),
    dict(
        n=192,
        title="Corporate actions on a daily book",
        skill="Show that missing a split mid-week lies about P&amp;L when you rebalance every day.",
        teach=[
            "More events per hold than Year 4. The same adjuster (123 / 202) now runs every night.",
            "Miss a split on purpose; the P&amp;L lie is larger when you trade daily.",
        ],
        trap="Reusing a monthly-adjusted panel for a daily book and ignoring intra-month actions.",
    ),
    dict(
        n=193,
        title="Live vs paper at this clock: stale scores and late features",
        skill="Delay features by one bar and measure IR death.",
        teach=[
            "A daily score that arrives at 16:20 is not a 15:50 score. A vendor blip is a missed day.",
            "Delay by one bar. The IR drop is the live-vs-paper lesson (101, again).",
        ],
        trap="A research score that uses a file that lands after the auction you claimed to trade.",
    ),
    dict(
        n=194,
        title="Attribution for a daily long-only",
        skill="Split a quarter of active return into selection, timing, cost, and beta.",
        teach=[
            "Brinson still applies. Add a cost bucket (the bill is first-order) and a timing bucket (when you traded).",
            "Beta: the unhedged daily book still rides the tide.",
        ],
        trap="Attribution that ignores costs on a 40% monthly-turnover-equivalent book.",
    ),
    dict(
        n=195,
        title="Crowding: when everyone fades yesterday",
        skill="Show the post-2009 reversal fade and write the memo.",
        teach=[
            "Short-horizon reversal got crowded. A rule that was easy in 1992 is a different rule now.",
            "McLean–Pontiff / Lou–Polk as the reading. The memo is the skill.",
        ],
        trap="A 1990–2024 backtest whose IR is earned entirely before 2004.",
    ),
    dict(
        n=196,
        title="Pre-register the daily capstone",
        skill="Write kill criteria (universe, hold, ADV cap, hurdle) before the run.",
        teach=[
            "Same discipline as 157, faster clock. Participation cap is a required line.",
        ],
        trap="A pre-registration that omits the ADV cap.",
    ),
    dict(
        n=197,
        title="Failure modes of the daily mandate",
        skill="Plant and find: same-day leak, ADV-blind optimizer, closet indexer, cost-free Sharpe.",
        teach=[
            "Four bugs, one notebook the learner did not write. Twin of 158.",
        ],
        trap="A lecture without planted bugs.",
    ),
    dict(
        n=198,
        title="Two-sleeve NAV: monthly plus daily",
        skill="Put Year 4 and Year 5 on one long-only NAV; report joint IR, correlation of actives, and capacity.",
        teach=[
            "How much capital each sleeve gets. Correlation of active returns (not of scores).",
            "Joint capacity is not the sum of the two capacities if they trade the same names on the same day.",
        ],
        trap="Funding both sleeves at full single-sleeve capacity.",
    ),
    dict(
        n=199,
        title="Overlays: 130/30 and synthetic market-neutral",
        skill="Same names, three mandates: long-only, 130/30, futures-hedged; say what IR and Sharpe each claim.",
        teach=[
            "Cash stays long-only under the futures overlay (153/186). 130/30 is a different permission.",
            "Three columns of numbers. One paragraph on which mandate the PM actually gave you.",
        ],
        trap="Reporting the hedged Sharpe as the long-only result.",
    ),
    dict(
        n=200,
        title="Year-5 exit — daily long-only capstone",
        skill="Defend a liquid, walk-forward, ADV-and-cost-aware long-only book on net IR, with capacity vs Year 4.",
        kind="exit",
        teach=[
            "PIT liquid universe → 1–5 day ranker → ADV-capped optimizer → net IR → capacity vs Year 4 → attribution → proceed/kill.",
            "PM who forbids shorts and rebalances often.",
        ],
        trap="A monthly notebook with the calendar changed to daily.",
    ),
]


Y6 = [
    dict(
        n=201,
        title="What a desk data set is",
        skill="Name the tables a long-only desk must have, and the as-of key that makes each join legal.",
        teach=[
            "Everyday picture: a vendor is a company that sells facts about stocks. You do not get 'the truth.' You get files with timestamps.",
            "The store, in plain words: (1) prices and corporate actions, (2) who was in the universe that morning, (3) company facts as they were known then, (4) earnings/news times, (5) how much each name traded (ADV, spread), (6) the benchmark's membership.",
            "An <strong>as-of key</strong> is the pair (name, morning) that every join must respect. No as-of key ⇒ no honest backtest.",
            "Snapshot vs event: a snapshot is 'as of this morning, this was the row.' An event is 'at 16:05 this print hit the tape.' Both are required. Mixing them is a leak.",
            "This quarter (201–210) is the data kit. <strong>Do it before Year 4 backtests</strong> even though the unit numbers come later. Years 4–5 assume this store exists.",
        ],
        trap="A folder of CSVs with no as-of dates, treated as a database.",
    ),
    dict(
        n=202,
        title="Building a price panel: splits, dividends, delist returns",
        skill="Write the adjuster that turns a vendor close into the holder's wealth, including the last day of a dead name.",
        teach=[
            "This is unit 123 as a standing piece of infrastructure, not a one-off notebook.",
            "Backward split adjustment: multiply past prices so the series does not jump when the split hits.",
            "Dividends in the same units as the adjusted price. Delist terminal return stays in the panel.",
            "Vendor differences: some files are already split-adjusted and not dividend-adjusted. Teach 'read the flag' as a skill.",
        ],
        trap="Trusting a column named 'adjusted close' without reading whether dividends are in it.",
    ),
    dict(
        n=203,
        title="Point-in-time membership",
        skill="Answer 'was this name in my universe on this morning?' from add/drop events, not from today's list.",
        teach=[
            "Unit 122 as a table: date × name → in or out. IPOs, index adds, index drops, delists.",
            "Survivors-only vs PIT, again, because this is the store every later lesson will query.",
            "A reconstitution calendar is part of membership, not a surprise in 208.",
        ],
        trap="Downloading 'current S&amp;P names' and filling ten years backward (122's trap, now as a failing unit test on the store).",
    ),
    dict(
        n=204,
        title="Point-in-time fundamentals (vintages)",
        skill="Join company facts by what was known that morning, using a vintage / as-of table.",
        teach=[
            "A <strong>vintage</strong> is 'this is the earnings number as it stood on date D.' Later restatements create a new vintage, they do not rewrite D.",
            "As-of join: for each (name, morning), take the latest vintage with release time ≤ that morning.",
            "Restated join (the leak): paste the final 10-K onto the whole year. Plant it. Catch it.",
            "Fiscal vs calendar periods. Point-in-time is about the release clock, not the fiscal label.",
        ],
        trap="A fundamentals table keyed only by fiscal year.",
    ),
    dict(
        n=205,
        title="Earnings and event calendar as a first-class table",
        skill="Store announce time (not just date), surprise, and whether the print was before the open or after the close.",
        teach=[
            "Required columns: name, timestamp (timezone named), period, surprise definition, source.",
            "After-close vs before-open. Unit 166's leak is a failing test here.",
            "Revisions and upgrades can live in the same event store with a type flag.",
        ],
        trap="A calendar of 'earnings dates' with no timestamps and no timezone.",
    ),
    dict(
        n=206,
        title="Daily bars: open, close, auction, VWAP, volume, spread",
        skill="Build one row per name per day that a daily book can actually use, and say how each field was made.",
        teach=[
            "Open, close, official auction print, VWAP, dollar volume, a spread estimate.",
            "The auction print is not always the last trade. Teach the difference (162).",
            "From trades/quotes if you have them; from a vendor daily file if you do not. Either way, write the recipe.",
            "Year 5 lives on this table. Year 4 can downsample it, not the other way around.",
        ],
        trap="Using last-trade as 'the close' on a name whose close is an auction.",
    ),
    dict(
        n=207,
        title="Liquidity history: ADV, spread, days-to-trade",
        skill="Store a trailing ADV and a days-to-trade at your intended participation, as-of each morning.",
        teach=[
            "ADV window (e.g. 20 days) must be trailing and causal.",
            "Days-to-trade at 3% participation for a stated AUM. This number feeds 163 and 182.",
            "Spread history: a wide-spread name is expensive even if ADV looks fine.",
        ],
        trap="An ADV computed on the full sample, so tomorrow's volume helps yesterday's filter.",
    ),
    dict(
        n=208,
        title="Benchmark reconstitution as data",
        skill="Store who was in the benchmark each morning, with the same as-of rules as the universe.",
        teach=[
            "Unit 129 as a table, not a vibe. Cap-weight, equal-weight, float flags.",
            "Adds/drops on reconstitution dates. A backtest that beats a frozen starting list is a different exam.",
        ],
        trap="A single 'benchmark.csv' of today's weights used for the whole history.",
    ),
    dict(
        n=209,
        title="The feature store: as-of keys, no future joins",
        skill="Put every feature behind (name, as-of morning) and refuse a join that does not carry that key.",
        teach=[
            "A feature store is just a disciplined table: keys, values, a recipe, a vintage.",
            "Illegal join patterns: restated fundamentals, same-day close into a close-to-close target, a news timestamp after the decision.",
            "Year 4 monthly features and Year 5 daily features are two granularities on one store, not two philosophies.",
        ],
        trap="Each research notebook rebuilding features from raw files with a slightly different as-of rule.",
    ),
    dict(
        n=210,
        title="Q1 checkpoint — one store that serves both clocks",
        skill="Query the store for a Year-4 monthly panel and a Year-5 daily panel; both pass the leak tests from 202–209.",
        kind="chk",
        teach=[
            "Survivorship test (203). Restatement test (204). Timestamp test (205). ADV causality (207). Benchmark membership (208).",
            "Until this checkpoint passes, Years 4–5 backtests are not allowed to use ad-hoc CSVs.",
        ],
        trap="A checkpoint that only checks 'the dataframe has 8 columns.'",
    ),
    dict(
        n=211,
        title="One code path: backtest calls the same functions as live",
        skill="State the rule 'the backtest is not allowed a private score or optimizer,' and show a violation.",
        teach=[
            "Everyday picture: if live calls <code>score(as_of)</code> and the backtest pastes a CSV of scores, they will drift apart.",
            "The backtest loops over mornings and calls the same functions live will call, with that morning's as-of store.",
            "A planted violation: a backtest-only 'adjusted' score. Catch it.",
        ],
        trap="A research notebook and a 'prod script' that are cousins, not the same functions.",
    ),
    dict(
        n=212,
        title="The score job: scheduled, logged, replayable",
        skill="Describe a run that takes an as-of timestamp and writes scores plus a log you can replay.",
        teach=[
            "Inputs: as-of morning, store revision. Outputs: score file, feature snapshot id, git hash, clock.",
            "Replay: same inputs ⇒ same scores. If not, you cannot debug Tuesday.",
            "This is not Airflow worship. It is 'write down what ran.'",
        ],
        trap="Scores that exist only in a laptop session named 'final_v3'.",
    ),
    dict(
        n=213,
        title="The optimizer job: constraints as config",
        skill="Put every constraint in a dated config the PM can read, not in comments in a notebook.",
        teach=[
            "Sentences from 145/182 become fields: name cap, sector cap, ADV participation, turnover penalty, long-only flag.",
            "Changing a cap is a new trial (007) if you peek at IR first.",
        ],
        trap="Hard-coded caps that differ between the backtest and the live job.",
    ),
    dict(
        n=214,
        title="The order list a broker will accept",
        skill="Turn target weights into a list of orders: name, side, quantity, type, limit, auction flag.",
        teach=[
            "A broker does not take a vector of weights. It takes orders.",
            "Long-only: side is buy or sell of what you already own (no short-sell). Quantity is shares, not percent, once you pick NAV.",
            "Rounding, lot sizes, 'do not trade 12 shares of a $4 name.' Teach the boring arithmetic.",
        ],
        trap="Sending weights to a broker API and hoping it guesses shares.",
    ),
    dict(
        n=215,
        title="Fill model vs live fills",
        skill="Keep a table of predicted fill (price, time, shortfall) next to realized fill, and read the gap.",
        teach=[
            "The backtest's fill is a model (close, VWAP, close plus a spread). Live fills are different.",
            "A standing table: date, name, predicted, realized, shortfall. This is how 152/188 stay honest after go-live.",
        ],
        trap="Changing the fill model until paper matches last week's luck.",
    ),
    dict(
        n=216,
        title="Position and cash ledger",
        skill="Keep a book that always adds up: cash + stock market value = NAV, after every fill and dividend.",
        teach=[
            "A <strong>ledger</strong> is the notebook of what you hold and how much cash you have. It is not the broker's screen — it is yours, and you will reconcile (225).",
            "Every fill, dividend, fee, and future variation-margin (if you overlay) is a row.",
            "A broken identity (cash + stock ≠ NAV) is a stop-the-line bug, not a rounding footnote.",
        ],
        trap="NAV taken from the broker and positions taken from the research file, never forced to meet.",
    ),
    dict(
        n=217,
        title="Corporate actions in the live book",
        skill="Apply tonight's split or dividend to positions and to open orders, not only to the research panel.",
        teach=[
            "The adjuster from 202 must run on the ledger. Share counts change. Open limit prices may need to change.",
            "A missed overnight split is a wrong order in the morning.",
        ],
        trap="Adjusting research prices and leaving live share counts on the old split.",
    ),
    dict(
        n=218,
        title="Calendar, holidays, half-days, auction times",
        skill="Know when the market is closed, when it closes early, and when the auction is, in the timezone you trade.",
        teach=[
            "A trading calendar is data. Half-days move the auction. Overseas names have other calendars if the universe ever leaves one country.",
            "A 'daily' job that runs on a holiday produces either nothing or a lie.",
        ],
        trap="A cron job on weekdays that does not know about Good Friday.",
    ),
    dict(
        n=219,
        title="Replay, config, and experiment ids",
        skill="Reproduce Tuesday's book from config + store revision + git hash alone (unit 109, applied).",
        teach=[
            "If you cannot replay, you cannot debug, and you cannot claim the backtest was this code.",
            "Seeds, config, store revision, code version — four fields, always written.",
        ],
        trap="A live book that cannot be rebuilt from logs.",
    ),
    dict(
        n=220,
        title="Q2 checkpoint — backtest and 'live' agree on one morning",
        skill="Pick an as-of date; the backtest path and the live job path produce the same scores, weights, and orders.",
        kind="chk",
        teach=[
            "Same functions. Same store revision. Byte-for-byte or a stated rounding rule.",
            "A planted private backtest path must fail the test.",
        ],
        trap="A checkpoint that compares IR over a year instead of the objects on one morning.",
    ),
    dict(
        n=221,
        title="Broker mechanics for a long-only cash book",
        skill="Explain account, buying power, cash, and why you do not need a stock borrow — and what still can reject an order.",
        teach=[
            "A <strong>broker</strong> is the firm that holds your cash and sends your orders to the exchange.",
            "Buying power: how many dollars you may still spend. Long-only cash: you cannot buy more than cash (plus any agreed margin — teach the default as cash-only).",
            "No short ⇒ no locate. You can still be rejected: halted name, not enough cash, restricted list (228), odd lots.",
            "Paper account vs live account: same objects, fake money. Teach the objects before any API brand.",
        ],
        trap="Assuming 'long-only' means every order is accepted.",
    ),
    dict(
        n=222,
        title="Order types you will actually use",
        skill="Define market, limit, market-on-close, and limit-on-close, and say which one a monthly vs daily book uses.",
        teach=[
            "<strong>Market</strong>: take whatever price is there. Fast, sloppy.",
            "<strong>Limit</strong>: do not pay worse than this price. You may not fill.",
            "<strong>MOC / LOC</strong>: participate in the close auction, with or without a limit.",
            "Year 4 monthly lists often TWAP over days (093) then finish in auctions. Year 5 lives on MOC/LOC. Teach both maps.",
        ],
        trap="A backtest that assumes market orders at the close print.",
    ),
    dict(
        n=223,
        title="How the close auction works, operationally",
        skill="Walk an order from 'I want this many shares at the close' to a fill, including imbalance and why you might not get the print.",
        teach=[
            "Imbalance: more buy interest than sell interest (or the reverse) going into the auction. The print can move.",
            "Cutoff times. A late MOC is a missed trade (193).",
            "This is 188 as operations, not as a shortfall formula.",
        ],
        trap="Treating the official close as a guaranteed fill price decided at 15:00.",
    ),
    dict(
        n=224,
        title="The paper-trading loop",
        skill="Write the daily loop in words and objects: as-of store → score → optimize → orders → fills → ledger → NAV.",
        teach=[
            "Paper trading is doing the whole loop with fake money and (ideally) real or delayed market data.",
            "Each arrow is a function from 211–216. The loop is the product.",
            "A week of paper is 230. This lesson teaches the loop, not the week.",
        ],
        trap="Calling a backtest 'paper trading.' A backtest can peek by construction; paper cannot.",
    ),
    dict(
        n=225,
        title="Reconciliation: your ledger vs the broker",
        skill="Every day, match positions, cash, and fills; a break is a halt, not a footnote.",
        teach=[
            "Three files: your ledger, the broker's positions, the day's fills. They must tell the same story.",
            "Breaks: missed fill, duplicate fill, corporate action only on one side, timezone.",
            "The rule: do not send new orders until yesterday reconciles.",
        ],
        trap="Reconciling once a month on a daily book.",
    ),
    dict(
        n=226,
        title="Kill switch and risk limits",
        skill="Write the limits as sentences and the kill as a single action that flattens or freezes.",
        teach=[
            "Limits: max name, max sector, max gross, min cash, max daily loss, max tracking error, max participation.",
            "A <strong>kill switch</strong> is the button that stops new risk: freeze orders, or flatten to cash / to the benchmark. Teach both flavors and when each is appropriate for long-only.",
            "A limit breach is not 'log and continue.' It is refuse or kill.",
        ],
        trap="Limits that exist in a slide deck and not in the order path.",
    ),
    dict(
        n=227,
        title="Slippage tracking: predicted vs realized",
        skill="Read the 215 table every week and decide whether the fill model is a lie.",
        teach=[
            "Slippage is implementation shortfall per name per day. Predicted vs realized.",
            "A model that is always optimistic will make every paper IR a fiction (152).",
            "Feed the gap back into 146/184. That loop is research, not operations theater.",
        ],
        trap="Resetting the fill model every time last week was unlucky.",
    ),
    dict(
        n=228,
        title="Restricted lists and compliance holds",
        skill="Treat a banned name as a hard zero in the optimizer and as a reject at the broker.",
        teach=[
            "Client bans, insider lists, ESG screens, sanctions. The research universe and the live order path must both see the list.",
            "A name added to the list mid-day: you may not buy more; you may have to exit. Teach the two cases.",
        ],
        trap="Filtering restricted names in the score and not in the optimizer (or the reverse).",
    ),
    dict(
        n=229,
        title="The shape of the trading day",
        skill="Write the runbook times: pre-open checks, decision time, auction cutoff, overnight adjust, reconcile.",
        teach=[
            "Year 4: a quiet month, then a rebalance window of a few days.",
            "Year 5: a clock. Feature ready by T1, scores by T2, orders by T3, auction cutoff T4, ledger T5.",
            "Holidays from 218 sit on this clock.",
        ],
        trap="A 'daily job' with no cutoff times.",
    ),
    dict(
        n=230,
        title="Q3 checkpoint — a reconciled week of paper",
        skill="Five paper days: loop runs, ledger equals broker, a kill-switch test fires on a planted breach, no silent rejects.",
        kind="chk",
        teach=[
            "Reconcile each day (225). One planted limit breach must kill or refuse (226).",
            "A written shortfall table (227) even if the week is tiny.",
        ],
        trap="Five backtest days labeled 'paper.'",
    ),
    dict(
        n=231,
        title="Going live small",
        skill="State the first-week rules: tiny AUM, few names, one sleeve, a written abort.",
        teach=[
            "Small means a size where a mistake is tuition, not a career event. Name a dollar number in the lesson as a worked example, not as advice.",
            "One sleeve first (monthly or daily, not both). Restricted list on. Kill switch tested in paper (230) before live.",
            "Abort: what happens if reconcile fails on day two.",
        ],
        trap="Going live at research AUM because the paper IR was pretty.",
    ),
    dict(
        n=232,
        title="Monitoring expected vs realized",
        skill="Each week: IR, turnover, rejects, shortfall, beta — versus what the backtest promised for this kind of week.",
        teach=[
            "A dashboard is a list of comparisons, not a pile of charts. Teach the list.",
            "Rejects and unfilled MOCs are first-class. They change the book you actually had.",
        ],
        trap="Watching NAV and ignoring rejects.",
    ),
    dict(
        n=233,
        title="Incident log",
        skill="Write one page per incident: missed auction, stale feature, wrong split, vendor hole — cause, P&amp;L, fix, test.",
        teach=[
            "If it is not written, it will recur. This is the operational twin of a research autopsy (139).",
        ],
        trap="Fixing the file by hand and not adding a test to 210/220.",
    ),
    dict(
        n=234,
        title="Two-frequency operations",
        skill="Run a monthly sleeve and a daily sleeve on one NAV without double-counting ADV or cash.",
        teach=[
            "Unit 198 as operations: two clocks, one ledger (216), one restricted list (228), one kill switch (226).",
            "ADV is shared. If both sleeves buy AAA on the same day, participation adds. Teach the combined cap.",
            "Cash is shared. A monthly rebalance week plus a daily book can overdraw buying power (221).",
            "Correlation of active returns is a research number; the operational number is 'did we exceed ADV today?'",
        ],
        trap="Funding both sleeves at full single-sleeve participation.",
    ),
    dict(
        n=235,
        title="Vendor outage and fallback",
        skill="Write what you do when the store does not land: skip, flatten, or use a stale-but-labeled snapshot — never a silent guess.",
        teach=[
            "A missing as-of table is a halt condition for new risk (226). You may hold what you have.",
            "A fallback snapshot must be labeled stale in the log (212 / 219). The backtest is not allowed to invent that morning later.",
            "Which fields are required vs optional (prices required; a news feature can be missing).",
        ],
        trap="Filling a hole with yesterday's scores and not writing it down.",
    ),
    dict(
        n=236,
        title="Tax lots and after-tax as an overlay (awareness)",
        skill="Name what a tax lot is, and why it must not rewrite the pre-tax research book.",
        teach=[
            "A <strong>lot</strong> is a bundle of shares you bought on a given day at a given price. Selling can be 'oldest first' or 'highest cost first.'",
            "After-tax P&amp;L is a different exam. Teach it as an overlay after the pre-tax capstones (160 / 200) are honest.",
            "Do not let tax rules silently change the research target.",
        ],
        trap="Optimizing the research book for a tax story you have not pre-registered.",
    ),
    dict(
        n=237,
        title="Pre-register the live trial",
        skill="Write duration, AUM, abort rules, and what would count as 'paper was a lie' before the first live order.",
        teach=[
            "Twin of 157/196, now with broker and reconcile. Duration (e.g. 20 days), AUM, sleeve, abort (225/226), success definition.",
            "If live shortfall is 3× the model, that is a kill of the fill model, not a nudge of the score.",
        ],
        trap="A live trial whose success definition is 'NAV went up.'",
    ),
    dict(
        n=238,
        title="Failure modes of going live",
        skill="Plant and find: silent stale scores, unreconciled ledger, limits not on the order path, a second sleeve added on day three.",
        teach=[
            "Four operational bugs. The learner finds them in a runbook they did not write.",
            "This is 158/197 for the desk, not for the ranker.",
        ],
        trap="A 'go-live risks' slide with no planted break.",
    ),
    dict(
        n=239,
        title="The runbook",
        skill="Write the one document a tired person can follow: times, commands, who to call, what 'halt' means.",
        teach=[
            "Contents: clock (229), reconcile (225), kill (226), outage (235), incidents (233), two-sleeve notes (234).",
            "If it is not in the runbook, it will be improvised. Improvisation is a failure mode (238).",
        ],
        trap="A runbook that is a copy of the research memo.",
    ),
    dict(
        n=240,
        title="Year-6 exit — a desk you could actually run",
        skill="Defend 20 paper (or tiny live) days: store passes 210, backtest=live on a morning (220), week reconciles (230), runbook, proceed/kill.",
        kind="exit",
        teach=[
            "This capstone is operations, not a prettier IR. The Year-4 and Year-5 books are inputs.",
            "Required: leak tests green, one replayed morning, a reconciled stretch, a kill-switch test, a shortfall table, a written abort/proceed.",
            "PM who forbids shorts and asks 'can we turn this on Monday?'",
        ],
        trap="A capstone that is another backtest with a 'we would paper trade' paragraph.",
    ),
]


def _nav(extra):
    return "\n".join(f"      <li>{x}</li>" for x in extra)


def main():
    root = Path(__file__).resolve().parents[1] / "reference"
    intro4 = """
  <p>
    Everyday picture: once a month you rank stocks, an optimizer turns those ranks into a
    shopping cart you are allowed only to <em>own</em>, and you are judged on beating a named
    index after costs. This page is <strong>what each lesson must teach</strong>, in order.
    Labs are not written yet — the teaching beats are the contract.
  </p>
  <p>
    Years 1–3 stay required. Do the
    <a href="year-6-lessons.html">Year 6 data kit (201–210)</a>
    <strong>before</strong> Year 4 backtests, even though those unit numbers come later.
    Mid-frequency (hours–days) is <a href="year-5-lessons.html">Year 5</a>.
  </p>
"""
    intro5 = """
  <p>
    Everyday picture: each afternoon you re-rank stocks for the next day or few, the optimizer
    may only own shares and may not take more than a slice of each name's daily volume, and
    you are judged on beating a named index <em>after the trading bill</em>. This page is
    <strong>what each lesson must teach</strong>. Labs are not written yet.
  </p>
  <p>
    Same long-only rules as <a href="year-4-lessons.html">Year 4</a>. Different clock
    (this course's mid-frequency). The
    <a href="year-6-lessons.html">data kit (201–210)</a> still comes first.
  </p>
"""
    intro6 = """
  <p>
    Everyday picture: before you backtest, you need a store of facts that could have been
    known that morning. Before you trade, you need a loop that turns those facts into
    orders, a ledger that adds up, and a button that stops you. This year teaches that
    desk — <strong>data preparation and everything needed to start trading</strong> on
    both the monthly and daily clocks.
  </p>
  <p>
    <strong>Recommended order (not the unit numbers):</strong> Years 1–3 →
    <strong>201–210 (data kit)</strong> → Year 4 → Year 5 →
    <strong>211–240 (prod parity, paper, small live)</strong>.
    Years 1–5 stay required; this year is extra calendar.
  </p>
"""
    nav4 = _nav(
        [
            '<a href="year-5-lessons.html">Year 5 teaching plan (hours–days)</a>',
            '<a href="year-6-lessons.html">Year 6 teaching plan (data + go-live)</a>',
            '<a href="curriculum.html#y4">Year 4 in the unit table</a>',
            '<a href="long-only-mid-horizon.html">Year 4 mandate sheet</a>',
            '<a href="../index.html">Home</a>',
        ]
    )
    nav5 = _nav(
        [
            '<a href="year-4-lessons.html">Year 4 teaching plan (weeks–months)</a>',
            '<a href="year-6-lessons.html">Year 6 teaching plan (data + go-live)</a>',
            '<a href="curriculum.html#y5">Year 5 in the unit table</a>',
            '<a href="long-only-mid-frequency.html">Year 5 mandate sheet</a>',
            '<a href="../index.html">Home</a>',
        ]
    )
    nav6 = _nav(
        [
            '<a href="year-4-lessons.html">Year 4 teaching plan</a>',
            '<a href="year-5-lessons.html">Year 5 teaching plan</a>',
            '<a href="curriculum.html#y6">Year 6 in the unit table</a>',
            '<a href="../index.html">Home</a>',
        ]
    )
    (root / "year-4-lessons.html").write_text(
        page(
            "Year 4 — what each lesson must teach",
            "Units 121–160 · long-only · weeks to months · teaching contract, no labs yet",
            intro4,
            Y4,
            nav4,
        ),
        encoding="utf-8",
    )
    (root / "year-5-lessons.html").write_text(
        page(
            "Year 5 — what each lesson must teach",
            "Units 161–200 · long-only · hours to days · teaching contract, no labs yet",
            intro5,
            Y5,
            nav5,
        ),
        encoding="utf-8",
    )
    (root / "year-6-lessons.html").write_text(
        page(
            "Year 6 — what each lesson must teach",
            "Units 201–240 · data kit + going live · teaching contract, no labs yet",
            intro6,
            Y6,
            nav6,
        ),
        encoding="utf-8",
    )
    for label, seq, lo, hi in (
        ("Y4", Y4, 121, 160),
        ("Y5", Y5, 161, 200),
        ("Y6", Y6, 201, 240),
    ):
        nums = [u["n"] for u in seq]
        missing = [i for i in range(lo, hi + 1) if i not in nums]
        if missing:
            raise SystemExit(f"{label} missing {missing}")
        if len(nums) != 40:
            raise SystemExit(f"{label} has {len(nums)} units")
    print("wrote year-4/5/6-lessons.html (40 units each)")


if __name__ == "__main__":
    main()
