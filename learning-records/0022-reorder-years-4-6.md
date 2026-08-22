# Years 4–6 reordered so unit numbers match study order

The study order was already right. The numbering was not. Year 6 Q1 (the data
kit) had to be done before Year 4 backtests, but it was numbered 201–210.

## What changed
Linear numbering, no "do these later units first" exception:

| Units | What |
|-------|------|
| 001–120 | Years 1–3, unchanged |
| 121–130 | Data kit (was 201–210) |
| 131–160 | Monthly book through the optimizer (was 121–150) |
| 161–170 | Run and defend the monthly book (was 151–160) |
| 171–200 | Daily book through the optimizer (was 161–190) |
| 201–210 | Run and defend the daily book (was 191–200) |
| 211–240 | Paper and live (unchanged numbers) |

## Why this order
- You cannot honestly backtest without a point-in-time store.
- The slower book (weeks–months) is the right first mandate: costs are smaller,
  classic factors are monthly, IR vs Sharpe is easier to see.
- The faster book (hours–days) is the same job with costs and ADV first-order.
- Paper and live come after there is a book to trade.

Years 1–3 were not moved. No labs were written.
