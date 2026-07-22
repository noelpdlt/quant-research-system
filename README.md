# Quant Research System

Summer 2026 project focused on building trading strategies and analyzing performance.

Experimented with a Pandas tutorial for Data Science in pandastutorial.ipynb. 

The first trading strategy used was a Momentum Strategy in momentumstrategy.ipynb. Our goal was to determine the best performing windows optimizing for the best Sharpe ratio. Repeating this experiment. Repeating this experiment for different tickers, we observe that this strategy mostly tends to have less cumulative returns than the market performance, this strategy shows less volatility, meaning that we are reducing risk with its trade-off being a smaller cumulative return.

The second trading strategy used was a Mean Reversion Strategy in meanreversionstr.ipynb. Here, we tested for the best window using a fixed threshold of 0.5, optimizing for Sharpe ratio, and then we tested for the best Sharpe ratio across all our possible windows and thresholds. For each iteration, we compared the strategy to a Momentum Strategy, whether for the same fixed window or for the best performing Momentum window. We observe that this strategy outperforms a Momentum Strategy whenever we need to control for volatility and when the stock is often perceiving losts in its market value. 
