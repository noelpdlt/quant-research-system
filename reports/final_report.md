# Final Report
## Introduction
This project was built to better understand how statistical models and strategies can be applied to financial data. The main purpose of the project was to learn more about financial concepts while also working on my technical coding skills. Overall, most of this project focuses on observing where do different strategies succeed and where do they fail to develop my intuition on how are strategies built, tested, and refined. 

## Data
The assets used throughout most of our experiments were ['AAPL', 'MSFT','SPY', 'NVDA','TTD','DOCS','IBM','BE','XOM','GLD','JNJ','SCCO','ECL','JPM','META']. Overall, we used data between 01/01/2016 and 01/01/2026, where we set the first 70% of the entries, unless otherwise stated, as the training set and the last 30% of the data as the testing set. Roughly speaking, this means that our strategies were trained on 7 years of data and tested over 3 years of data. 

## Strategies
The rule-based strategies we used in this project were:
- Momentum
- Mean Reversion
- Momentum + Trend
- Momentum + Volatility
- Momentum + Volume Ratio

## Machine Learning
The machine learning algorithm-based strategies used here were:
- Logistic Regression
- Random Forest

## Market Regime Analysis
- Mean reversion often showed a lot of overfitting, having a relatively strong training performance with a poor test performance.
- Moderate time windows for momentum often provided models with better test performance than those with very long or very short time windows.
- Rolling-volatility was often the strongest of the three momentum filters tested throughout our project.

## Factor Analysis
- Assets' beta values didn't show any meaningful relationship with their average test Sharpe. However, we were able to see that for some strategies, the best performing assets had a beta within a particular range. Thus, beta values seemed to be more relevant for an asset's best strategy than for their average test Sharpe.
- Assets having higher test Sharpe values often had lower volatility, lower volume ratios, and higher RSI.
- There was no consistent relationship between test performance and momentum, trend strength, or distance from the 20 day moving average. 

## Portfolio Analysis
- Most asset pairs showed to have moderate to high positive correlations, with very few correlations being close to 0 and/or negative. 
- Less correlated portfolios achieved lower volatilities and drawdowns. This means that portfolios with a higher diversification will often offer reduced risk, but the growth can be negatively affected. 
- Strategies such as momentum and momentum + rolling volatility improved their testing performance when applied to a portfolio compared to the average metrics of such strategies applied on the individual assets within the portfolio tested.

## Key Findings
- Momentum was overall the most robust rule-based strategy, often having some of the highest generalization ratios.
- Mean reversion, although it seemed promising when first introduced to the project, is highly prone to overfitting when generalized. 
- Training sharpe was not a reliable predictor of a model's performance on the testing set. This is best characterized by our random forests, which are naturally overfitting on the training set, getting as high as possible of a sharpe ratio and dropping to a more regular performance on the testing set. While Random Forests can remain competitive with this drop in performance, other models end up underperforming compared to other models when they overfit. 
- Expanding our feature set for our machine learning strategies didn't necessarily improve testing performance, as it mostly introduced more noise to the training of these models instead of reducing the amount of noise. 
- Logistic Regression generalized well overall; however, it yielded positive signals so often that it resembled buy-and-hold.
- The performance of most strategies varied a lot between assets, their individual characteristics, and the time periods tested on. 
- Diversification reduced portfolio risk meaningfully, especially when we chose assets less correlated between them. 

## Limitations
Some current limitations of the project as it stands are:
- Feature selection algorithms aren't covered for our Machine Learning strategies; we only considered two sets of features, one being the expanded version of the other feature set. 
- Although efficient frontiers were examined in this project, we didn't create any tool to optimize the weights of the different assets within a portfolio. Further work on experimenting with portfolios can deepen understanding of how they work and how to decide what assets and weights we're building our portfolios with.
- Something that could potentially have improved testing performance on some of the models that ended up overfitting the training data is to divide the data into training/validation/testing instead of just training/testing.

## Future Work
Some next steps I would take with this project are:
- Expanding assets list to include a wider variety of assets to experiment with.
- Explore more portfolio construction and optimization.
- Adding a validation set in between the current training and testing sets to improve parameter selection and reduce overfitting.
- Experimenting with more machine learning algorithms and applying a more rigorous feature selection process. 