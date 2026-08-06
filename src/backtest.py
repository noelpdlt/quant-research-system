import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from src.features import generate_features
from src.visualization import plot_performance
from src.data import get_data
import os
from pathlib import Path
from sklearn.metrics import accuracy_score, precision_score, recall_score



strategy_names = [
        ('Momentum', None, 'mom', None, None),
        ('Mean Reversion', None, 'mr', None, None),
        ("Momentum + Trend Strength", None, "mo_tr", None, None),
        ("Momentum + Rolling Volatility", None, "mo_vo", None, None),
        ("Momentum + Volume Ratio", None, "mo_vr", None, None),
        ("Logistic Regression", None, "lr", None, None),
        ("Random Forest", None, "rf", None, None)
    ]

def backtest(df):
    df["market_cumulative"] = (1 + df["returns"]).cumprod()
    for _, _, ending, _, _  in strategy_names:
        signal = f"signal_{ending}"
        if signal not in df.columns:
            continue
        returns = f"strategy_returns_{ending}"
        cumulative = f"cumulative_returns_{ending}"
        df[returns] = df["returns"] * df[signal].shift(1)
        df[cumulative] = (1 + df[returns]).cumprod()

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


def results_table(df, strategies = strategy_names):
    table = pd.DataFrame(columns=[
        'Strategy',
        'Sharpe',
        'Volatility',
        'Max DD',
        'Signal Accuracy',
        'Signal Precision',
        'Signal Recall',
        'Signal Active %'
    ])

    table.loc[len(table)] = [
        "Market",
        sharpe_ratio(df["returns"]),
        volatility(df["returns"]),
        max_drawdown(df["market_cumulative"]),
        np.nan,
        np.nan,
        np.nan,
        np.nan
    ]

    for name, _, ending, _, _ in strategies:

        returns = f"strategy_returns_{ending}"
        cumulative = f"cumulative_returns_{ending}"
        signal = f"signal_{ending}"

        if returns not in df.columns:
            continue

        signal_accuracy = np.nan
        signal_precision = np.nan
        signal_recall = np.nan
        signal_active = np.nan

        if signal in df.columns and "target" in df.columns:

            valid = df[[signal, "target"]].dropna()

            if len(valid) > 0:

                signal_accuracy = accuracy_score(
                    valid["target"],
                    valid[signal]
                )

                signal_precision = precision_score(
                    valid["target"],
                    valid[signal],
                    zero_division=0
                )

                signal_recall = recall_score(
                    valid["target"],
                    valid[signal],
                    zero_division=0
                )

                signal_active = 100 * valid[signal].mean()

        table.loc[len(table)] = [
            name,
            sharpe_ratio(df[returns]),
            volatility(df[returns]),
            max_drawdown(df[cumulative]),
            signal_accuracy,
            signal_precision,
            signal_recall,
            signal_active
        ]

    return table

def apply_strategy(df, strategy, window=None, threshold=None, model=None):

    _, strat_func, _, _, trainer = strategy

    df = df.copy()

    if trainer is not None:

        df = strat_func(
            df,
            model
        )

    elif threshold is None:

        df = strat_func(
            df,
            window
        )

    else:

        df = strat_func(
            df,
            window,
            threshold
        )

    return backtest(df)


def window_table(df, strategies, windows=[5, 10, 20, 50]):
    results = pd.DataFrame(
        columns=["Strategy","Window","Sharpe","Volatility","Max DD"]
    )
    for name, strategy, ending, thresholds, trainer in strategies:
        for w in windows:
            if thresholds is None:
                df_copy = apply_strategy(df,(name, strategy, ending, thresholds, trainer),w)
            else:
                df_copy = apply_strategy(df, (name, strategy, ending, thresholds, trainer), w, thresholds[0] / 100)
    return results


def optimize_strategy(df, strategy, windows, windowplot=True):

    name, strat_func, ending, thresholds, trainer = strategy

    # Machine learning strategies
    if trainer is not None:

        model, metrics = trainer(df.copy())

        df = apply_strategy(
            df,
            strategy,
            model=model
        )

        return df, None, None, metrics


    best_window = None
    best_threshold = None
    best_sharpe = float("-inf")

    params = []
    sharpes = []


    if thresholds is None:

        for window in windows:

            df_copy = df.copy()

            df_copy = strat_func(
                df_copy,
                window
            )

            df_copy = backtest(df_copy)

            sharpe = sharpe_ratio(
                df_copy[f"strategy_returns_{ending}"]
            )

            if np.isnan(sharpe):
                continue

            params.append(window)
            sharpes.append(sharpe)

            if sharpe > best_sharpe:

                best_sharpe = sharpe
                best_window = window

        print(f"Market Sharpe Ratio: {sharpe_ratio(df['returns']):.4f}")
        print(f"Best {name} Strategy window: {best_window}")
        print(f"Best Sharpe ratio: {best_sharpe:.4f}")
        print()

        if windowplot:

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

    else:

        for window in windows:

            best_for_window = float("-inf")

            for threshold in thresholds:

                threshold = threshold / 100

                df_copy = strat_func(
                    df.copy(),
                    window,
                    threshold
                )

                df_copy = backtest(df_copy)

                sharpe = sharpe_ratio(
                    df_copy[f"strategy_returns_{ending}"]
                )

                if np.isnan(sharpe):
                    continue

                if sharpe > best_for_window:
                    best_for_window = sharpe

                if sharpe > best_sharpe:

                    best_sharpe = sharpe
                    best_window = window
                    best_threshold = threshold


            if best_for_window != float("-inf"):

                params.append(window)
                sharpes.append(best_for_window)

        if windowplot:

            plt.figure(figsize=(10,5))

            plt.plot(
                params,
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
            plt.ylabel("Sharpe Ratio")
            plt.title(f"{name} Window Optimization")
            plt.grid(alpha=0.3)
            plt.legend()
            plt.show()
        
        print(f"Market Sharpe Ratio: {sharpe_ratio(df['returns']):.4f}")
        print(f"Best {name} Strategy window: {best_window}")
        print(f"Best threshold: {best_threshold*100:.0f}%")
        print(f"Best Sharpe ratio: {best_sharpe:.4f}")
        print()

    if best_threshold is None:

        df = apply_strategy(
            df,
            strategy,
            best_window
        )

    else:

        df = apply_strategy(
            df,
            strategy,
            best_window,
            best_threshold
        )


    return df, best_window, best_threshold, None

def fit_strategy(
    train,
    test,
    strategy,
    windows,
    feature_set,
    windowplot=True
):

    name, strat_func, ending, thresholds, trainer = strategy


    if trainer is not None:

        print("Training ML model...")

        model, metrics = trainer(train.copy(), feature_set=feature_set)

        train = strat_func(train.copy(), model, feature_set)
        test = strat_func(test.copy(), model, feature_set)

        train = backtest(train)
        test = backtest(test)

        print(name + " model trained and tested.")
        print()

        return train, test, None, None, metrics, model


    train, best_window, best_threshold, metrics = optimize_strategy(
        train.copy(),
        strategy,
        windows,
        windowplot
    )


    test = apply_strategy(
        test,
        strategy,
        best_window,
        best_threshold
    )


    return train, test, best_window, best_threshold, metrics, None

def optimize(df, strategies, windows, windowplot=True, performanceplot=True):
    df = backtest(df)
    base = df.copy()
    for strategy in strategies:

        print(strategy[0])

        temp, best_window, best_threshold, metrics = optimize_strategy(
            base.copy(),
            strategy,
            windows,
            windowplot
        )

        ending = strategy[2]
        for col in (
            f"signal_{ending}",
            f"strategy_returns_{ending}",
            f"cumulative_returns_{ending}"
        ):
            if col in temp.columns:
                df[col] = temp[col]
    if performanceplot:
        plot_performance(df)

    return results_table(df, strategies)

def optimize_tt(
    train,
    test,
    strategies,
    windows,
    feature_set,
    asset=None,
    save_csv=False,
    csv_path=None,
    windowplot=True,
    performanceplot=True,
    logscale = False
):

    train = backtest(train)
    test = backtest(test)

    train_base = train.copy()
    test_base = test.copy()

    best_parameters = []

    for strategy in strategies:

        print(strategy[0])

        train_temp, test_temp, best_window, best_threshold, metrics, _ = fit_strategy(
            train_base,
            test_base,
            strategy,
            windows,
            feature_set,
            windowplot
        )

        ending = strategy[2]

        for col in (
            f"strategy_returns_{ending}",
            f"cumulative_returns_{ending}",
            f"signal_{ending}"
        ):

            if col in train_temp.columns:
                train[col] = train_temp[col]

            if col in test_temp.columns:
                test[col] = test_temp[col]

        best_parameters.append({

            "Strategy": strategy[0],
            "Window": best_window,
            "Threshold": (
                best_threshold * 100
                if best_threshold is not None
                else None
            ),
            "Is ML": strategy[4] is not None

        })

    if performanceplot:

        print("Training Performance")
        plot_performance(train, logscale=logscale)

        print("Testing Performance")
        plot_performance(test, logscale=logscale)

    train_results = results_table(train, strategies)
    test_results = results_table(test, strategies)

    if save_csv:

        csv_rows = []

        for params in best_parameters:

            strategy = params["Strategy"]

            train_row = train_results.loc[
                train_results["Strategy"] == strategy
            ].iloc[0]

            test_row = test_results.loc[
                test_results["Strategy"] == strategy
            ].iloc[0]

            csv_rows.append({

                "Asset": asset,
                "Strategy": strategy,
                "Feature Set": (feature_set if params["Is ML"] else None),
                "Window": params["Window"],
                "Threshold": params["Threshold"],

                "Train Sharpe": train_row["Sharpe"],
                "Train Volatility": train_row["Volatility"],
                "Train Max DD": train_row["Max DD"],
                "Train Signal Accuracy": train_row["Signal Accuracy"],
                "Train Signal Precision": train_row["Signal Precision"],
                "Train Signal Recall": train_row["Signal Recall"],
                "Train Signal Active %": train_row["Signal Active %"],

                "Test Sharpe": test_row["Sharpe"],
                "Test Volatility": test_row["Volatility"],
                "Test Max DD": test_row["Max DD"],
                "Test Signal Accuracy": test_row["Signal Accuracy"],
                "Test Signal Precision": test_row["Signal Precision"],
                "Test Signal Recall": test_row["Signal Recall"],
                "Test Signal Active %": test_row["Signal Active %"]

            })

        pd.DataFrame(csv_rows).to_csv(
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
    feature_set = 'v1',
    train_ratio = 0.7,
    save_csv=False,
    windowplot=False,
    performanceplot=True,
    logscale = False
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
            feature_set=feature_set,
            save_csv=save_csv,
            csv_path=csv_path,
            windowplot=windowplot,
            performanceplot=performanceplot,
            logscale = logscale
        )

        print("\nTraining Results")
        print(train_results)

        print("\nTesting Results")
        print(test_results)