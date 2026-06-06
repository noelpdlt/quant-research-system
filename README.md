# Quant Research System

Summer 2026 project focused on building trading strategies and analyzing performance.

Experimented with a Pandas tutorial for Data Science in pandastutorial.ipynb. 

Added functions get_data() to data.py and compute_returns() and moving_average() to features.py.
Used these functions to graph the price and moving_average of 'AAPL' in financialdataset1.ipynb under 'Trial 1.'

The first trading strategy used was a Momentum Strategy in momentumstrategy.ipynb, using the function momentum_strategy() we built in strategy.py. Here, we considered different windows for percentage change and compared the Sharpe ratio of both the Momentum strategy and the Market (Buy / Hold) performance. We also optimized the window value to find the window value within a range that yielded the highest Sharpe ratio value. Repeating this experiment for different tickers, we observe that this strategy mostly tends to have less cumulative returns than the market performance, this strategy shows less volatility, meaning that we are reducing risk with its trade-off being a smaller cumulative return.

 
