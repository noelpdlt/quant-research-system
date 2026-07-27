import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from src.features import generate_features
from src.visualization import plot_performance
from src.data import get_data
import os
from pathlib import Path


strategy_names = [
        ('Momentum', 'mom'),
        ('Mean Reversion', 'mr'),
        ('Momentum + Trend Filter', 'mo_tr'),
        ('Momentum + Low Volatility Filter', 'mo_vo'),
        ('Momentum + Volume Ratio Filter', 'mo_vr')
    ]

def backtest(df):
    df["market_cumulative"] = (1 + df["returns"]).cumprod()
    for _, ending in strategy_names:
        signal = 'signal_' + ending
        if signal in df.columns:
            strategy_returns = 'strategy_returns_' + ending
            cumulative_returns = 'cumulative_returns_' + ending
            df[strategy_returns] = df["returns"] * df[signal].shift(1)
            df[cumulative_returns] = (1 + df[strategy_returns]).cumprod()
    return df


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
    for name, ending in strategy_names:
        returns , cumulative = "strategy_returns_" + ending, "cumulative_returns_" + ending
        if returns in df.columns:
            strategy_sharpe = sharpe_ratio(df[returns])
            strategy_vol = volatility(df[returns])
            strategy_max_dd = max_drawdown(df[cumulative])

            table.loc[len(table)] = [name, strategy_sharpe, strategy_vol, strategy_max_dd]

    return table

def csv_row(
    asset,
    strategy,
    window,
    threshold,
    train_df,
    test_df
):
    """
    Create one CSV row containing both train and test performance.
    """

    name, _, ending, _ = strategy

    return {
        "Asset": asset,
        "Strategy": name,
        "Window": window,
        "Threshold": (
            threshold * 100
            if threshold is not None
            else None
        ),

        "Train Sharpe": sharpe_ratio(
            train_df[f"strategy_returns_{ending}"]
        ),
        "Train Volatility": volatility(
            train_df[f"strategy_returns_{ending}"]
        ),
        "Train Max DD": max_drawdown(
            train_df[f"cumulative_returns_{ending}"]
        ),

        "Test Sharpe": sharpe_ratio(
            test_df[f"strategy_returns_{ending}"]
        ),
        "Test Volatility": volatility(
            test_df[f"strategy_returns_{ending}"]
        ),
        "Test Max DD": max_drawdown(
            test_df[f"cumulative_returns_{ending}"]
        )
    }

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

def find_best_window(df, strategy, windows):

    _, strat_func, ending, _ = strategy

    best_sharpe = float("-inf")
    best_window = None

    for window in windows:

        df_copy = df.copy()

        df_copy = strat_func(df_copy, window)
        df_copy = backtest(df_copy)

        sharpe = sharpe_ratio(
            df_copy[f"strategy_returns_{ending}"].dropna()
        )

        if np.isnan(sharpe):
            continue

        if sharpe > best_sharpe:
            best_sharpe = sharpe
            best_window = window

    return best_window, best_sharpe

def find_best_window_threshold(df, strategy, windows):

    _, strat_func, ending, thresholds = strategy

    best_window = None
    best_threshold = None
    best_sharpe = float("-inf")

    for window in windows:

        for threshold in thresholds:

            threshold = threshold / 100

            df_copy = df.copy()

            df_copy = strat_func(
                df_copy,
                window,
                threshold
            )

            df_copy = backtest(df_copy)

            sharpe = sharpe_ratio(
                df_copy[f"strategy_returns_{ending}"].dropna()
            )

            if np.isnan(sharpe):
                continue

            if sharpe > best_sharpe:

                best_sharpe = sharpe
                best_window = window
                best_threshold = threshold

    return (
        best_window,
        best_threshold,
        best_sharpe
    )

def apply_strategy(df, strategy, window, threshold=None):
    """
    Apply a strategy with fixed parameters and run the backtest.
    """

    _, strat_func, _, thresholds = strategy

    df = df.copy()

    if thresholds is None:
        df = strat_func(df, window)
    else:
        df = strat_func(df, window, threshold)

    df = backtest(df)

    return df


def optimize_w(df, strategy, windows, windowplot):

    name, _, ending, _ = strategy

    best_window, best_sharpe = find_best_window(
        df,
        strategy,
        windows
    )

    print(f"Market Sharpe Ratio: {sharpe_ratio(df['returns']):.4f}")
    print(f"Best {name} Strategy window: {best_window}")
    print(f"Best Sharpe ratio: {best_sharpe:.4f}")

    if windowplot:

        params = []
        sharpes = []

        for window in windows:

            df_copy = apply_strategy(
                df,
                strategy,
                window
            )

            sharpe = sharpe_ratio(
                df_copy[f"strategy_returns_{ending}"].dropna()
            )

            params.append(window)
            sharpes.append(sharpe)

        plt.figure(figsize=(10,5))

        plt.plot(
            params,
            sharpes,
            marker="o"
        )

        plt.axvline(
            best_window,
            color="red",
            linestyle="--",
            label=f"Best = {best_window}"
        )

        plt.xlabel(f"{name} Window")
        plt.ylabel("Sharpe Ratio")
        plt.title(f"{name} Window Optimization")
        plt.grid(alpha=0.3)
        plt.legend()
        plt.show()

    df = apply_strategy(
        df,
        strategy,
        best_window
    )

    return df, best_window, None

def optimize_w_th(df, strategy, windows, windowplot):

    name, _, ending, thresholds = strategy

    (
        best_window,
        best_threshold,
        best_sharpe
    ) = find_best_window_threshold(
        df,
        strategy,
        windows
    )

    print(f"Market Sharpe Ratio: {sharpe_ratio(df['returns']):.4f}")

    if best_window is None:

        print("No valid parameter combination found.")
        return df, None, None

    print(f"Best window: {best_window}")
    print(f"Best threshold: {best_threshold * 100:.0f}%")
    print(f"Best Sharpe: {best_sharpe:.4f}")

    if windowplot:

        window_params = []
        sharpes = []

        for window in windows:

            best_for_window = float("-inf")

            for threshold in thresholds:

                threshold = threshold / 100

                df_copy = apply_strategy(
                    df,
                    strategy,
                    window,
                    threshold
                )

                sharpe = sharpe_ratio(
                    df_copy[f"strategy_returns_{ending}"].dropna()
                )

                if np.isnan(sharpe):
                    continue

                if sharpe > best_for_window:
                    best_for_window = sharpe

            if best_for_window != float("-inf"):

                window_params.append(window)
                sharpes.append(best_for_window)

        plt.figure(figsize=(10,5))

        plt.plot(
            window_params,
            sharpes,
            marker="o"
        )

        plt.scatter(
            best_window,
            best_sharpe,
            color="red",
            s=100,
            label=f"Best = ({best_window}, {best_threshold:.2f})"
        )

        plt.xlabel("Window")
        plt.ylabel("Sharpe")
        plt.title(f"{name} Optimization")
        plt.grid(alpha=0.3)
        plt.legend()
        plt.show()

    df = apply_strategy(
        df,
        strategy,
        best_window,
        best_threshold
    )

    return df, best_window, best_threshold

def optimize_strategy(df, strategy, windows, windowplot=True):
    """
    Optimize a single strategy and return the optimized dataframe
    together with the best parameters.
    """

    if strategy[3] is not None:
        return optimize_w_th(
            df,
            strategy,
            windows,
            windowplot
        )

    return optimize_w(
        df,
        strategy,
        windows,
        windowplot
    )

def copy_strategy_columns(source, destination, ending):

    strategy_returns = f"strategy_returns_{ending}"
    cumulative_returns = f"cumulative_returns_{ending}"

    for col in [strategy_returns, cumulative_returns]:

        if col in source.columns:
            destination[col] = source[col]
    

def optimize(df, strategies, windows, windowplot=True, performanceplot=True):
    df = backtest(df)
    base = df.copy()

    for strategy in strategies:

        print(strategy[0])

        temp, best_window, best_threshold = optimize_strategy(
            base.copy(),
            strategy,
            windows,
            windowplot
        )

        ending = strategy[2]

        copy_strategy_columns(
            temp,
            df,
            ending
        )

    if performanceplot:
        plot_performance(df)

    return results_table(df)

def optimize_tt(
    train,
    test,
    strategies,
    windows,
    asset=None,
    save_csv=False,
    csv_path=None,
    windowplot=True,
    performanceplot=True
):

    train = backtest(train)
    test = backtest(test)

    train_base = train.copy()
    test_base = test.copy()
    csv_rows = []

    for strategy in strategies:

        print(strategy[0])

        train_temp, best_window, best_threshold = optimize_strategy(
            train_base.copy(),
            strategy,
            windows,
            windowplot
        )

        if best_threshold is None:

            test_temp = apply_strategy(
                test_base.copy(),
                strategy,
                best_window
            )

        else:

            test_temp = apply_strategy(
                test_base.copy(),
                strategy,
                best_window,
                best_threshold
            )

        ending = strategy[2]

        copy_strategy_columns(
            train_temp,
            train,
            ending
        )

        copy_strategy_columns(
            test_temp,
            test,
            ending
        )

        if save_csv:

            csv_rows.append(
                csv_row(
                    asset,
                    strategy,
                    best_window,
                    best_threshold,
                    train_temp,
                    test_temp
                )
            )

    if performanceplot:

        print("Training Performance")
        plot_performance(train)

        print("Testing Performance")
        plot_performance(test)


    train_results = results_table(train)

    test_results = results_table(test)

    if save_csv:

        csv_df = pd.DataFrame(csv_rows)

        csv_df.to_csv(
            csv_path,
            mode="a",
            index=False,
            header=not os.path.exists(csv_path)
        )

    return train_results, test_results


def optimize_assets(
    assets,
    start_date,
    end_date,
    strategies,
    windows,
    train_ratio = 0.7,
    save_csv=False,
    windowplot=False,
    performanceplot=True
):

    csv_path = None
    if save_csv:

        project_root = Path(__file__).resolve().parent.parent

        output_folder = project_root / "outputs"
        output_folder.mkdir(exist_ok=True)

        csv_path = output_folder / "experiment_results.csv"

    for asset in assets:

        print("=" * 60)
        print(asset)
        print("=" * 60)

        base_df = get_data(
            asset,
            start_date,
            end_date
        )

        base_df = generate_features(base_df)

        split_idx = int(len(base_df) * train_ratio)

        train = base_df.iloc[:split_idx].copy()
        test = base_df.iloc[split_idx:].copy()

        train_results, test_results = optimize_tt(
            train=train,
            test=test,
            strategies=strategies,
            windows=windows,
            asset=asset,
            save_csv=save_csv,
            csv_path=csv_path,
            windowplot=windowplot,
            performanceplot=performanceplot
        )

        print("\nTraining Results")
        print(train_results)

        print("\nTesting Results")
        print(test_results)