# Week 7 Notes

## Models Tested
- Logistic Regression
- Random Forest

## New Features
- RSI
- Distance from MA20
- 5-day Momentum

## Prediction Results
- Considering only our machine learning strategies and the two different feature sets used to train each model, we get that both cases using set v1, i.e. the original feature set, we got better performance than the models trained with set v2.
- In both cases, we got that the logistic regression had a better Sharpe ratio than the random forest. 

## Trading Results
- As expected, the Random Forest algorithm had a near perfect performance for the training sets. Even though this performance drastically drops in the testing set due to overfitting, we still get models that are on average the second best performing based on their Sharpe ratio, just before our momentum strategy.

## Cross-Asset Observations
- When comparing a smaller set of assets consisting of AAPL, JNJ, JPM, NVDA, and XOM, we can observe that XOM, in particular, consistently had poor performance on the applied strategies; only our machine learning algorithms created strategies that had positive Sharpe ratios on the testing set for XOM.
- For NVDA, all 7 strategies work particularly well, even our mean reversion, which tends to have really low, even negative, Sharpe ratio values.


## Surprises
- It was surprising to see how the random forest actually performed better than most models overall; I assumed the model overfitting the training set would lead to a generally bad performance across the different assets.
- I noticed that expanding our feature set made logistic regression go from being active around 88% of the tested period to only 33% of the time. It is possible that our added features made the probability of predicting a positive signal less likely to occur. 

## Failures
- When expanding our feature set from only 4 features to 7 features, both of our machine learning algorithms lowered their testing performance. This can be attributed to having a signal depending on more features that don't provide a statistically significant value to our signal.
- Adding the percentage of the signal being active, we observe that Mean Reversion is on average only active for 1.6% of the time, meaning that this strategy tends to expect signals that are very hard to attain.

## Most Promising Direction
- Our random forest seems like the most promising direction overall. Even though the model naturally overfits the training set, it still performs better than other models when generalizing to the testing sets.
- Our machine learning algorithms are among the best strategies when applied to our testing sets; however, strategies such as momentum alone and momentum + rolling volatility can be useful as additional filters to our strategies.