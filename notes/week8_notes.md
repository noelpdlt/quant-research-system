# Week 8 Notes

## Generalization Findings
### Strategy Findings
- After creating a generalization ratio for each strategy, measuring change in Sharpe ratio, we observe that, as discussed previously, Random Forest, Momentum + Trend Strength, and Mean Reversion strategies have very poor performance over the test sets compared to their training results. All of these have negative generalization ratios of -0.91, -0.91, and -1.10.
- In contrast to the other two, Random Forest's near perfect training and, consequently, its overfitting nature actually lead to a relatively good performance when tested.
- Logistic Regression and Momentum strategies were the strategies that generalized the best, with the former having testing Sharpe ratios over twice as good as the training set. 

### Asset Findings
- META, ECL, and GLD are the assets with a better generalization ratio, with 2.32, 1.22, and 0.91, respectively. 
- TTD, IBM, and XOM all have on average negative generalization ratios, with -1.11, -1.21, and -1.48, these being the assets with the worst generalization.
- Assets such as NVDA and JPM present a change in performance of under 0.1 between the training and testing sets.

## Market Regime Findings
- After training our 8 different strategies for SPY from 2011 to 2015, and testing over the following 10 years for the different market regimes, such as COVID-19, we observe that there's many differences on their performance.
- For the bull market, before 2020, most strategies had a Sharpe ratio from 0.95 to 1.05. Only mean reversion and momentum + volume ratio had values of approximately 0.7. In terms of volatility, most strategies reduced the volatility compared to the market except for logistic regression, which was active 100% of the time. Both ML strategies used had some of the largest drawdowns present, of -0.20 and -0.16.
- During COVID, particularly in 2020, just as the market, most strategies performed poorly compared to their performance in the prior stage. However, Momentum, Momentum + Trend Strength, and Momentum + Rolling Volatility were able to outperform significantly the market's Sharpe of 0.61, with Momentum + Rolling Volatility having the highest Sharpe ratio at 2.47. Although Random Forests had the 2nd highest Sharpe ratio for the bull market, here it presented the 2nd lowest performance. 
- For the recovery period, from 2021 to 2023, only Random Forests and Mean Reversion had better Sharpe ratios than the market at 0.77 and 0.63 respectively. Momentum and Momentum + Rolling Volatility had particularly bad performance in this period, with its growth never being able to surpass 1.
- For the recent period, from 2021 to 2025, only Logistic Regression and Momentum + Volume Ratio were able to have similar Sharpe ratios to the market's 1.19. However, logistic regression, being active all the time, was the only strategy that managed to have the growth that the market had.

## Beta Observations
- When comparing our average test Sharpe ratio values per asset to the asset's beta, there isn't a clear relationship between these two.
- Although there's no clear linear relationship apparent based on the assets tested, we can observe that the closer an asset's beta is to 1, most average test sharpe values lie somewhere between 0.75 and 1.25.
- The further away from either a beta of 1 or an average sharpe of 1 we get a lot of variability. For instance, our 3 highest beta values correspond to NVDA, BE, and TTD, all really close to having 1.8 beta, have average Sharpe ratio values of 1.45, 0.67, and -0.16, respectively. 

## Surprises
- Considering the poor performance that mean reversion has had throughout other tests and observations, I didn't expect for this strategy to be one of the best performing strategies for the recovery period after COVID. 
- It was also surprising that two of the overall top performing strategies, Momentum and Momentum + Rolling Volatility, were the lowest performing strategies during the recovery period.
- I expected the average test sharpe and the beta of each of our assets to have a clear correlation, when in reality we got very dispersed points throughout our graph. 
- I didn't expect to see Random  Forests perform as poorly as it did for COVID given we had observed Random Forests yield some of the best results before. However, this makes sense as the model overfitted a relatively stable training period compared to COVID.

## New Hypotheses
- Finding a set of variables such that the logistic regression doesn't generate models that are active anywhere close to 100% of the time, we might find a strategy that outperforms the market. Currently the strategy with the 'v1' variable set yields a model that is functionally just the market's behavior. 
- By training our random forests with less tree depth, we may be able to reduce the overfitting it's having and make our strategy work better when presented to different scenarios and to improve its performance when tested on unstable periods such as COVID. 
