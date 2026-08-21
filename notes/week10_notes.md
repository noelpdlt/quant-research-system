# Week 10 Notes

## Correlation Findings
- As expected, from our assets, SPY and QQQ were the assets with the highest correlation between them at 0.93, both having higher correlation with assets such as AAPL, MSFT, and NVDA.
- Overall, GLD has a very small correlation with other assets, where it remains relatively close to 0 for most assets, except for SCCO, a copper business, with whom it has a correlation of 0.22.
- Aside from DOCS and JNJ correlation of -0.01, the only other negative correlation occurs between JPM and GLD, at -0.09.
- Without considering correlations with SPY or QQQ, our highest correlation is between AAPL and MSFT at 0.68. Other assets with a correlation above 0.50 are AAPL and NVDA, MSFT and NVDA, ECL and MSFT, JPM and IBM, JPM and XOM, JPM and ECL, META and AAPL, and META and MSFT. 

## Diversification Findings
- From our market buy and hold graphs for our 3 portfolios created, A = [AAPL, MSFT, NVDA, IBM], B = [AAPL, NVDA, GLD, JNJ], and C = [SPY, QQQ, GLD] for 2016-2026, we observe that portfolio A had the biggest growth; however, this portfolio's drawdowns tend to be very steep. In contrast, portfolio B, which is more diversified than portfolio A, had a comparable, yet smaller, growth with noticeably less volatility than portfolio A. 
- Finally, portfolio C had a pair of highly correlated assets, SPY and QQQ, with GLD, which tends to be uncorrelated with most assets. Across the years, this portfolio had minimal growth compared to the other two portfolios; however, this also significantly reduced volatility. 
- When comparing Portfolio A against Portfolio B's efficient frontier graph, we observe that A's graph sits slightly towards the bottom-left of B's graph, both ending at around (0.45, 0.6). This implies that in general, we are able to find weights for portfolio B such that for any fixed risk, there's a combination of B that can yield higher returns than portfolio A. 

## Strategy vs Portfolio Results
- The strategies tested on our portfolio A (AAPL, MSFT, NVDA, and IBM) with an initial allocation of 25% each, were Momentum, Momentum + Rolling Volatility, Logistic Regression, and Random Forest.
- From the strategies tested, the average training sharpe ratio for the individual assets was larger than the training sharpe ratio of the portfolio on the strategies for our random forest, which averaged 1.38 on the individual tests and had a value of 1.10 when applied to the portfolio.
- Momentum and Momentum + Rolling Volatility grew slightly between both approaches, 1.26 to 1.46 and 1.18 to 1.26, respectively. Logistic regression saw the largest increase amongst these as it went from 1.38 to 1.90, however, as in previous applications of our logistic regression, we have ended up with a model that had an active signal for 100% of the time period tested. 

## Surprises
- I didn't expect our random forest strategy to be the only of the four strategies tested on our portfolio A to underperform the average of its performance on the four assets included in the portfolio. This could indicate that the algortithms overfitting nature in the training wasn't able to capture correctly how the portfolio worked over time. 
- Since portfolio A had assets with correlations ranging from 0.3 to 0.5 between most of them, the portfolio wasn't as diversified, thus, it's possible that the underperformance of our strategies can be attributed in part to not having a diversified portfolio. 

## New Hypotheses
- In general, most strategies when applied to our portfolio had particularly high volatilities compared to the average volatility of the strategies applied to the 4 assets individually. If we tested our strategies against less correlated portfolios, I expect their volatilities to decrease and possibly improve our Sharpe ratio.
