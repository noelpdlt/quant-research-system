# Week 5 Notes

## Strategies Tested
- Momentum
- Mean Reversion
- Momentum + Trend Strength
- Momentum + Rolling Volatility
- Momentum + Volume Ratio

## Assets
- Large-cap Tech: AAPL, MSFT, META, IBM
- Growth Tech: NVDA, TTD, DOCS
- Financials: JPM
- Healthcare: JNJ
- Energy: XOM, BE
- Materials: SCCO, ECL
- Alternative Asset: GLD
- Market Benchmark: SPY

## Best Performing Strategies
- On average, Momentum + Rolling Volatility and Mean Reversion strategies tend to have the higher training Sharpe ratio.
- On average, Momentum and Momentum + Rolling Volatility strategies had the best performance on their test set Sharpe ratio. 

## Generalization Results
- On average, Momentum, Momentum + Rolling Volatility, and Momentum + Trend Strength strategies improved their Sharpe ratios when applying their strategies on the test set, maintaining similar volatilities and slightly improved max drawdowns. 
- Momentum + Volume Ratio strategy maintained a similar sharpe ratio, volatility, and max drawdown when generalized.
- While Mean Reversion had one of the highest Sharpe ratios on average for the training set, its test Sharpe ratios dropped to approximately 0 on average.

## Asset-Specific Observations
- Across the 5 different strategies tested, XOM, TTD, and, SCCO were the assets with the highest average Sharpe decay.
- IBM is the asset with the most growth in its average Sharpe ratio between the assets tested. 
- Assets like BE and SPY had very little change on average.

## Surprises
- Based on the performance of the mean reversion strategy on the training sets, I wouldn't have expected to see this performance drastically drop even to negative Sharpe ratio values.
- I expected most of the tested strategies to drop at least some of its performance when applied to the testing sets. However, strategies such as Momentum and Momentum + Rolling Volatility improved their performance. 
- The only strategy with a box and whiskers plot whose min is not well below 0 is the - Momentum + Trend Strength strategy. All boxes but the one for mean reversion lie completely above 0, where mean reversion's mean is close to 0.

## Failures
- Based on our experiments so far, it is easy to observe that the mean reversion strategy is overfitting its training set. Thus, even though it gets one of the two best performances on average when using the training set, it performs poorly when applied to the testing set.
- Momentum + Volume Ratio was the lowest performing strategy on the training sets; however, this strategy was able to maintain steady results, even if these were lower than other better performing strategies.

## New Hypotheses
- Strategies considering momentum generalize the best.
- Testing on a broader range of assets, considering many different categories, will give us a better idea of what strategies are the most robust. 
- Selecting only the best parameter for each strategy on the training set might be inducing overfitting in our strategies, particularly in the mean reversion strategy. An idea to reduce overfitting might be to have a selection of the top values for each parameter in an initial training set and choose the best performing value on a following training set before reaching the testing set. 