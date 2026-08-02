# Week 6 Notes

## ML Model Tested
- Logistic Regression

## Features Used
- Momentum
- Rolling Volatility
- Trend Strength
- Volume Ratio

## Results
- On average, the Sharpe ratio for logistic regression went up 0.4 while reducing volatility and max drawdown. Signal accuracy, precision, and recall all stayed at similar levels between training and testing sets. 
- Signal accuracy and precision were both at around 0.5 in general for logistic regression, and 0.8 for signal recall.

## Feature Importance
- When testing on 'AAPL'
    - Momentum had the only positive coefficient.
    - Trend strength had a large negative coefficient.
    - Volume ratio contributed little.
    - Volatility had a moderate negative relationship with positive returns.

## Comparison to Rule-Based Strategies
- Logistic Regression generalized the best, having the largest growth from training Sharpe ratio to testing Sharpe ratio.

## Surprises
- Even though the test Sharpe ratio mean for logistic regression was behind momentum strategy, logistic regression had the best growth, indicating the potential for generalizability across different assets.
- Logistic regression had the highest signal recall for both the training and testing sets, meaning the model captures more of the actual positive cases than any other strategy tested so far.

## Failures
- Although signal recall is the highest, i.e., it has the largest ratio of true positives found, its signal precisio is not as high, its average is close to 0.50. This can indicate that many false positives are being captured by the strategy.

## New Hypotheses
- Making our logistic regression models less likely to generate a positive signal would improve our signal precision and possibly improve performance on the testing set, even if we lose some of its signal recall.
- Testing for how useful or not each of our predictors is to the model might make our model's performance on the testing set better. 