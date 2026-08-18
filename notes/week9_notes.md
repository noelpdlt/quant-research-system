# Week 9 Notes

## Beta Findings
- As discussed in last weeks notes, using our set of 15 assets, we can't observe any relevant correlation between an asset's beta and its average test sharpe.
- We can observe, however, that many assets are concentrated around a beta of 0.75 to 1.25 and an average test sharpe of 0.80 to 1.20.
- If we don't consider GLD and JPM and only consider the places 3 to 7 there's less variability in the assets' beta  than in the lowest performing half of the assets, i.e. places 8 through 14. 

## Cross-Sectional Findings
- Our 3 assets with the best test sharpe were GLD, NVDA, and JPM. These were obtained with random forest, logistic regression, and momentum + rolling volatility, respectively. For these 3 assets, we reaffirm that the beta of these assets doesn't provide much meaningful data for our test sharpe ratios since they have beta values of 0.04, 1.80, and 1.09, respectively.
- We observe that the top half assets with the best test sharpe ratios have on average lower volatilities than the lower half.
- We can also see that for no single asset its best performing strategy is neither mean reversion nor momentum + volume ratio. Both of our machine learning strategies, logistic regression and random forests, were the best strategies for 4 assets each. Followed by these two, we have that momentum was the best strategy for 3 assets, momentum + rolling volatility for 2, and momentum + trend strength for 1.

## Feature Insights
- The top half assets with the best test sharpe ratios have on average very low average volume ratio values, with the higher average volume ratios being close to 1.1. From the lower half, BE, DOCS, and TTD all have volume ratio values close to or above 1.25
- In contrast, the top assets tend to have higher RSI values, only one of them had an RSI value below 53. From the lower half, only one asset, MSFT, had an RSI value well above 53, close to 56.
- For the other features, momentum, trend strength, and distance MA, no significant difference shows up in terms of whether an asset appeared in the top half or the bottom half of the best test sharpe ratios.

## Research Question: Why do some higher beta assets don't survive out-of-sample testing?
- Some of our strategies may be overfitting to the noise of these high beta assets instead of capturing the true risk. Thus, even though the training on some of these higher beta assets might have a good performance, this overfitting is acting negatively on the test sets.
- The market regimes used for the training of our strategies compared to that of the testing set might have had different effects on some of these higher beta assets and, thus, the market trends captured by the model weren't able to hold in the testing period.
- Since high beta assets amplify both gains and loses, it's possible that when our strategies wrongly expect a positive movement of the asset's price, its more difficult to recover from these wrong predictions than from a wrong prediction in a lower beta asset.