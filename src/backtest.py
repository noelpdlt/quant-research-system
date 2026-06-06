import numpy as np

def backtest(df):
    df["strategy_returns"] = df["returns"] * df["signal"].shift(1)
    df["cumulative_returns"] = (1 + df["strategy_returns"]).cumprod()
    return df

def sharpe_ratio(returns):
    return np.mean(returns) / np.std(returns) * np.sqrt(252)