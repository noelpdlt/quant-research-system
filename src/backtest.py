import numpy as np

def backtest_mom(df):
    df["strategy_returns_mom"] = df["returns"] * df["signal_mom"].shift(1)
    df["cumulative_returns_mom"] = (1 + df["strategy_returns_mom"]).cumprod()
    return df

def backtest_mr(df):
    df["strategy_returns_mr"] = df["returns"] * df["signal_mr"].shift(1)
    df["cumulative_returns_mr"] = (1 + df["strategy_returns_mr"]).cumprod()
    return df

def sharpe_ratio(returns):
    return np.mean(returns) / np.std(returns) * np.sqrt(252)


def volatility(returns):
    return np.std(returns) * np.sqrt(252)

def max_drawdown(cumulative_returns):
    running_max = cumulative_returns.cummax()
    drawdown = (
        cumulative_returns - running_max
    ) / running_max

    return drawdown.min()
