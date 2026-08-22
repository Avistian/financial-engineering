# Year 5 added — long-only mid-frequency equity (ML + optimization)

Learner follow-up (2026-08-22): the long-only book can also be **mid-frequency**
(hours to days), and they want that extended too. Still extra time, not a swap.

## What shipped
- **Units 161–200** appended as **Year 5**. Years 1–4 stay in order.
- Plain-language sheet: `reference/long-only-mid-frequency.html`.
- Year 4 sheet / Lesson 001 / `TEMPLATE_PORTFOLIO.md` now point at the sibling year.
- Sources: Jegadeesh 1990, Lehmann 1990, Bernard–Thomas 1989/90, Amihud 2002,
  Heston–Korajczyk–Sadka 2010, Lou–Polk–Skouras 2019, plus Boyd / Gârleanu–Pedersen
  reused from Year 4 at a daily half-life.

## Why a second year, not extra Year-4 quarters
Year 4's monthly optimizer, run every close, goes broke (that is unit 181's lab).
The faster clock needs its own baselines (1–5 day reversal, PEAD, overnight vs
open-to-close), its own leak (same-day close), overlapping daily labels, ADV
participation caps, and a smaller capacity curve. That is a year of labs.

## The year, in four quarters
| Q | Units | Skill |
|---|-------|--------|
| Q1 | 161–170 | Faster mandate, liquidity filter, reversal + PEAD after costs |
| Q2 | 171–180 | 1–5 day ML ranker; uniqueness; beat or kill vs reversal and PEAD |
| Q3 | 181–190 | Daily optimizer: ADV caps, impact, optional futures hedge |
| Q4 | 191–200 | Gaps, two-sleeve NAV with Year 4, capstone |

**Exit (200):** liquid PIT universe → daily/multi-day ML ranker → ADV-and-cost-aware
long-only optimizer → net IR vs a named benchmark → capacity vs Year 4 →
attribution + proceed/kill memo.

## Hours
New totals: **5 years, 200 units, ~3,350 hours.** Years 1–3 still ~2,000 h.
Years 4–5 are two ~650 h specializations.
