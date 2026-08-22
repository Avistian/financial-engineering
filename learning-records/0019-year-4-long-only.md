# Year 4 added — long-only mid-horizon equity (ML + optimization)

Learner asked (2026-08-22) whether long-only mid-term stock strategies exist, then asked
to **add curriculum** tailored to that style, using **ML and optimization**, and to
**extend time rather than swap**. They accepted up to an extra year.

## What shipped
- **Units 121–160** appended to `CURRICULUM.md` as **Year 4**. Years 1–3 (001–120) are
  untouched in order and content.
- Student-facing mirrors: `reference/curriculum.html`, `reference/study-roadmap.html`,
  `index.html`, `MISSION.md`.
- Plain-language mandate sheet: `reference/long-only-mid-horizon.html`.
- Sources in `RESOURCES.md`: Qian–Hua–Sorensen (QEPM), Boyd–Vandenberghe, Boyd et al. 2017,
  Bali–Engle–Murray, plus the cross-section canon (Fama–MacBeth, Jegadeesh–Titman,
  Fama–French, AMP 2013, Novy-Marx, AHXZ 2006, McLean–Pontiff, Hou–Xue–Zhang,
  Green–Hand–Zhang, Gu–Kelly–Xiu 2020, Gârleanu–Pedersen, Perold, Brinson).
- Lesson 001 frequency section now points at Year 4 instead of implying the course
  *only* lives at mid-frequency.
- `TEMPLATE_PORTFOLIO.md` keeps the daily dollar-neutral recipe and points at Year 4
  for the long-only mid-horizon job.

## The year, in four quarters
| Q | Units | Skill |
|---|-------|--------|
| Q1 | 121–130 | Mandate (IR vs Sharpe), PIT universe, total return, classic factors as baselines |
| Q2 | 131–140 | Monthly cross-sectional ML ranking; walk-forward; beat or kill vs linear and 12-1 |
| Q3 | 141–150 | Constrained long-only optimization (risk, costs, multi-period, convex toolkit) |
| Q4 | 151–160 | Drift, shortfall, futures overlay, drawdowns, attribution, capacity, capstone |

**Exit (160):** PIT universe → walk-forward ML ranker → constrained optimizer → net IR
versus a named benchmark → capacity + attribution + proceed/kill memo, defended to a PM
who only allows longs.

## Why a full year, not a quarter
The existing Y3 Q1 (081–090) already has MVO, cleaned covariance, the Fundamental Law,
and costs — enough to *talk* about a book, not enough to *run* this mandate. Missing
pieces that each earn units: survivorship-safe universes, corporate actions, the
characteristic-sorted factor baselines, monthly ML targets and ranking losses,
long-only as a binding constraint (transfer coefficient), multi-period cost-aware
rebalancing, Brinson attribution, and a second capstone whose exam is IR-vs-benchmark
rather than market-neutral Sharpe. That is a year of labs, not a sidebar.

## What we did *not* do
- Did not rewrite or reorder Years 1–3.
- Did not author 40 lesson HTML files (same rule as the original plan: a unit row is
  the contract; the lesson is written when the learner arrives).
- Did not move Year 4 earlier. Validation (Y2 Q2) and Grinold–Kahn (Y3 Q1) stay
  prerequisites.

## Hours
Original track ~2,000 h / 3 years. Year 4 adds ~650 h. New totals: **4 years, 160
units, ~2,700 hours.**
