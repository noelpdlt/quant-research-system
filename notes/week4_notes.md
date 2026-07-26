# Week 4 Notes

## Strategies Tested
- Momentum + Trend Strength Filter
- Momentum + Low Volatility Filter
- Momentum + Volume Ratio Filter

## Results
- When optimizing for the best window for each strategy according to their Sharpe ratio, testing against a couple of different stocks, our Momentum + Low Volatility filter tends to outperform the other two strategies tested.
- Our Momentum + Volume Ratio filter tends to deeply underperform against both other strategies and also against the market value of the stocks tested. 

## Surprises
- The low volatility and the volume ratio filters seem to work best when windows are shorter and the trend strength filter works better with longer windows. 
- The trend filter acts as a good in between for the Low Volatility Filter and the Volume Ratio Filter strategies, since it's not as volatile as the strategy with a Low Volatility Filter nor is it as underperforming as the Volume Ratio strategy. 

## Failures
- Very rarely does the best Momentum + Volume Ratio Filter strategy outperform the market value of a stock; however, it results in strategies with a very low volatility.
- Even though the Low Volatility Filter is consistently the best performing strategy among these threee strategies, it is still not that good of a strategy for reducing volatility.

## Hypotheses
- Forcing the Low Volatility filter to have longer windows instead of using its best performing shorter windows might reduce volatility, even though that costs us some of its performance.
- Additional optimization for the thresholds of each of these 3 strategies might help us either improve performance or decrease volatility. 