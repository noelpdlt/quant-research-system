import numpy as np

def calculate_beta(asset_returns, market_returns):
    covariance = np.cov(asset_returns, market_returns)[0, 1]
    market_variance = np.var(market_returns)

    return covariance / market_variance