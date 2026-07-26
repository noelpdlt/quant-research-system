import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from src.features import generate_features
from src.visualization import plot_performance


strategies = [
        ('Momentum', 'mom'),
        ('Mean Reversion', 'mr'),
        ('Momentum + Trend Filter', 'mo_tr'),
        ('Momentum + Low Volatility Filter', 'mo_vo'),
        ('Momentum + Volume Ratio Filter', 'mo_vr')
    ]

def backtest(df):
    df["market_cumulative"] = (1 + df["returns"]).cumprod()
    for _, ending in strategies:
        signal = 'signal_' + ending
        if signal in df.columns:
            strategy_returns = 'strategy_returns_' + ending
            cumulative_returns = 'cumulative_returns_' + ending
            df[strategy_returns] = df["returns"] * df[signal].shift(1)
            df[cumulative_returns] = (1 + df[strategy_returns]).cumprod()
    return df


#def sharpe_ratio(returns):
 #   return np.mean(returns) / np.std(returns) * np.sqrt(252)
def sharpe_ratio(returns):
    returns = returns.dropna()

    if returns.empty:
        return np.nan

    std = returns.std()

    if std == 0 or np.isnan(std):
        return np.nan

    return returns.mean() / std * np.sqrt(252)

def volatility(returns):
    return np.std(returns) * np.sqrt(252)


def max_drawdown(cumulative_returns):
    running_max = cumulative_returns.cummax()
    drawdown = (
        cumulative_returns - running_max
    ) / running_max

    return drawdown.min()


def results_table(df):
    table = pd.DataFrame(columns=['Strategy', 'Sharpe', 'Volatility', 'Max DD'])
    
    table.loc[len(table)] = ['Market', sharpe_ratio(df['returns']), 
                             volatility(df['returns']), max_drawdown(df["market_cumulative"])]
    for name, ending in strategies:
        returns , cumulative = "strategy_returns_" + ending, "cumulative_returns_" + ending
        if returns in df.columns:
            strategy_sharpe = sharpe_ratio(df[returns])
            strategy_vol = volatility(df[returns])
            strategy_max_dd = max_drawdown(df[cumulative])

            table.loc[len(table)] = [name, strategy_sharpe, strategy_vol, strategy_max_dd]

    return table


def window_table(df, strategies, windows = [5, 10, 20, 50]):
    results = pd.DataFrame(columns=['Strategy', 'Window', 'Sharpe', 'Volatility', 'Max DD'])
    for name, strategy, ending, _ in strategies:
        returns , cumulative = "strategy_returns_" + ending, "cumulative_returns_" + ending
        for w in windows:
            df_copy = df.copy()
            df_copy = strategy(df_copy, window = w)

            df_copy = backtest(df_copy)
            strategy_sharpe = sharpe_ratio(df_copy[returns].dropna())
            strategy_vol = volatility(df_copy[returns])
            strategy_max_dd = max_drawdown(df_copy[cumulative])

            results.loc[len(results)] = [name, w, strategy_sharpe, strategy_vol, strategy_max_dd]
    return results


def optimize_w(df, strategy, windows, windowplot):
    name, strat_func, ending, _ = strategy
    bestsharpe = float('-inf')
    bestsharpe_strat = None

    params = []
    sharpes = []

    for i in windows:
        df_copy = df.copy()

        df_copy = strat_func(df_copy, i)
        df_copy = backtest(df_copy)

        sharpe = sharpe_ratio(df_copy['strategy_returns_' + ending].dropna())

        params.append(i)
        sharpes.append(sharpe)

        if sharpe > bestsharpe:
            bestsharpe = sharpe
            bestsharpe_strat = i

    print(f"Market Returns Sharpe Ratio: {sharpe_ratio(df['returns'])}")
    print(f"Best {name} Strategy window: {bestsharpe_strat}")
    print(f"Best Sharpe ratio: {bestsharpe:.4f}")

    if windowplot == True: 
        plt.figure(figsize=(10, 5))
        plt.plot(params, sharpes, marker='o')
        plt.axvline(bestsharpe_strat,
                    color='red',
                    linestyle='--',
                    label=f'Best = {bestsharpe_strat}')
        plt.xlabel(name + ' Window')
        plt.ylabel('Sharpe Ratio')
        plt.title(name + ' Window Optimization')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.show()

    df = generate_features(df)
    df = strat_func(df, bestsharpe_strat)
    df = backtest(df)

    return df

def optimize_w_th(df, strategy, window, windowplot):
    import numpy as np

    name, strat_func, ending, threshold = strategy

    bestsharpe = float('-inf')
    best_i = None
    best_j = None

    windowparams = []
    sharpes = []
    best_js = []

    for i in window:

        best_sharpe_for_i = float('-inf')
        best_j_for_i = None

        for j in threshold:

            test_threshold = j / 100

            df_copy = df.copy()

            df_copy = strat_func(df_copy, i, test_threshold)
            df_copy = backtest(df_copy)

            sharpe = sharpe_ratio(
                df_copy['strategy_returns_' + ending].dropna()
            )

            # Skip invalid Sharpe values
            if np.isnan(sharpe):
                continue

            # Best threshold for this window
            if sharpe > best_sharpe_for_i:
                best_sharpe_for_i = sharpe
                best_j_for_i = test_threshold

            # Best overall
            if sharpe > bestsharpe:
                bestsharpe = sharpe
                best_i = i
                best_j = test_threshold

        if best_j_for_i is not None:
            windowparams.append(i)
            sharpes.append(best_sharpe_for_i)
            best_js.append(best_j_for_i)

    print(f"Market Sharpe Ratio: {sharpe_ratio(df['returns']):.4f}")

    if best_i is None:
        print("No valid parameter combination found.")
        return df

    print(f"Best window: {best_i}")
    print(f"Best threshold: {best_j:.2f}")
    print(f"Best Sharpe: {bestsharpe:.4f}")

    if windowplot:

        plt.figure(figsize=(10,5))
        plt.plot(windowparams, sharpes, marker='o')

        plt.scatter(
            best_i,
            bestsharpe,
            color='red',
            s=100,
            label=f'Best: i={best_i}, j={best_j:.2f}'
        )

        plt.xlabel("Window")
        plt.ylabel("Sharpe")
        plt.title(f"{name} Optimization")
        plt.grid(alpha=0.3)
        plt.legend()
        plt.show()

    df = generate_features(df)
    df = strat_func(df, best_i, best_j)
    df = backtest(df)

    return df

def optimize(df, strategies, window, windowplot=True, performanceplot=True):
    df = backtest(df)
    base = df.copy()

    for strategy in strategies:
        print(strategy[0])

        if strategy[3]:
            temp = optimize_w_th(base.copy(), strategy, window, windowplot)
        else:
            temp = optimize_w(base.copy(), strategy, window, windowplot)

        ending = strategy[2]

        cols = [
            f"strategy_returns_{ending}", 
            f"cumulative_returns_{ending}" 
            ]

        for col in cols: 
            if col in temp.columns: 
                df[col] = temp[col]

    if performanceplot:
        plot_performance(df)

    return results_table(df)