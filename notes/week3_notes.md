# Week 3 Notes

## Strategies Tested
- Momentum (10-, 20-, 50-day)
- Momentum (1-day through 50-day)
- Mean Reversion (5-, 10-, 20-, 50-day at 0.5 threshold)
- Mean Reversion (1-day through 50-day, optimizing threshold as well)

## Results
- Mean Reversion tends to outperform Momentum when strategy is applied to generally losing stocks.
- Momentum tends to have a higher volatility than Mean Reversion.
- Longer windows reduced volatility in both strategies.
- When optimizing for thresholds in Mean Reversion, the test gave back low thresholds compared to our fixed 0.5 threshold.

## Surprises
- Mean Reversion entered trades less frequently than expected.
- Sharpe ratio changed significantly with small parameter changes.

## Failures
- 5-day windows performed poorly: momentum generated too many trades, mean reversion generated too little trades.
- 50-day windows also performed poorly: 
- Some signals occurred during highly volatile periods.

## Hypotheses
- Combining momentum with a moving average filter may improve performance.
- Signal quality may improve if volatility is incorporated.