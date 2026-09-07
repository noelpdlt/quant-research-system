# Week 11 Notes

## Asset Characteristics Findings
- Assets with logistic regression as their best strategy all have beta values of at least 1.10. The assets here also have a relatively high return compared to its volatility, which tends to be moderate in these assets. 
- The assets with momentum as their best strategy all have very different beta values, average returns, and average volatility, which can't be thus turned into a hypothesis about the assets. However, this points to the consideration that this strategy's success might be more related to another characteristic, possibly these assets are more regime-sensitive.
- Both assets with momentum + rolling volatility have beta values above 1 but have relatively lower average returns.
- While there's only one asset with momentum + trend strength as its best strategy, BE, we can observe that such asset has the highest beta value, the second highest average returns, and the highest mean volatility of all assets. Thus, it's possible that this strategy works best for assets with extreme conditions.
- For random forests, the assets that had this as their best strategy tend to have lower beta values, most of them are below 1, with only AAPL being above at 1.21, where most have relatively low volatilities and weaker average returns. 

## Strategy Characteristic Findings
- In most cases, the volatility remained roughly the same between the training and testing sets.
- Mean Reversion is the only strategy that went from an average positive train Sharpe ratio to a negative test Sharpe ratio. We also observe that, without taking into account Random Forest's near perfect training performance, Mean Reversion had the second best training Sharpe ratio, slightly behind Momentum + Rolling Volatility Sharpe ratio. 
- While Momentum had on average a lower Sharpe ratio than Momentum + Rolling Volatility, Momentum alone had a greater generalization ratio and even outperformed Momentum + Rolling Volatility in the testing data.


## Failure Analysis
- For Momentum, on average the strategy with the highest test Sharpe, the training for the the lower half of the assets, i.e. the 8 worst performing assets with this strategy, have more extreme windows than the upper half of the best performing assets, which are mostly in a range of 12-16, with the sole exception of GLD with a 4 day window. The test signal accuracy is overall always close to 0.50, all values range from 0.46 to 0.54. 
- Looking at the worst test performing strategy, Mean Reversion, only NVDA had a meaningfully good performance, with a test sharpe ratio of 1.28, this being the only asset that improved performance between testing and training sets. Followed by NVDA, the other assets with meaningfully positive test Sharpe are MSFT, META, and ECL at values around 0.33. Overall the testing signal is active at a particularly low rate, most of them at a percentage lower than 1%, many at a 0% rate. The model takes in more extreme windows, most of them being very small windows of time; thus, it's possible that the training model is overfitting to very small or particular reversals that don't necessarily occur again in the testing set. 

## ML Reassessment
- While only considering the generalization ratio, we are able to say that our logistic regression yielded the highest generalization ratio while our random forests had the third worse generalization ratio. However, we need to consider that throughout our experiments logistic regression ended up with a model that was highly probable of predicting a signal to be positive and it ended up being functionally a repeat of the buy and hold market strategy. Additionally, the decrease in performance between random forests in the training and testing sets is attributed to the near perfect overfitting it produces over the training set and, thus, its generalization ratio is bound to always be as negative as it is in this case. 

## Final Hypotheses
- Reducing the window range over which we train our strategies to something similar to what's working best for the Momentum strategy, something around a range like 10-15, can improve the testing performance of the assets that ended up with very extreme windows.
- Similarly, for Mean Reversion, adjusting the window and threshold ranges we use to optimize for the training set might help to reduce overfitting with either really high thresholds or very small windows of time. 
