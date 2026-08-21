import pandas as pd
import numpy as np
import matplotlib as plt
from src.backtest import get_data, optimize_tt, results_table
from src.features import generate_features
from src.visualization import plot_performance

def create_portfolio_df(weights, start_date, end_date):

    asset_data = {}

    for asset in weights.keys():

        df = get_data(
            asset,
            start_date,
            end_date
        )

        asset_data[asset] = df

    common_index = asset_data[
        list(weights.keys())[0]
    ].index

    for asset in weights.keys():

        common_index = common_index.intersection(
            asset_data[asset].index
        )

    normalized_prices = pd.DataFrame(index=common_index)

    for asset in weights.keys():

        prices = asset_data[asset].loc[
            common_index,
            "Close"
        ]

        normalized_prices[asset] = (
            prices / prices.iloc[0]
        )

    portfolio_close = (
        normalized_prices[list(weights.keys())]
        * list(weights.values())
    ).sum(axis=1)

    portfolio_volume = pd.Series(
        0.0,
        index=common_index
    )

    for asset, weight in weights.items():

        portfolio_volume += (
            asset_data[asset]
            .loc[common_index, "Volume"]
            * weight
        )

    portfolio_df = pd.DataFrame(index=common_index)

    portfolio_df["Close"] = portfolio_close
    portfolio_df["Adj Close"] = portfolio_close
    portfolio_df["Open"] = portfolio_close
    portfolio_df["High"] = portfolio_close
    portfolio_df["Low"] = portfolio_close
    portfolio_df["Volume"] = portfolio_volume

    return portfolio_df

def optimize_portfolio(
    weights,
    start_date,
    end_date,
    strategies,
    windows,
    feature_set='v1',
    train_ratio=0.7,
    performanceplot=True,
    logscale=False
):

    print("=" * 60)
    print("PORTFOLIO")
    print("=" * 60)

    train_asset_results = {}
    test_asset_results = {}

    for asset, weight in weights.items():

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
            save_csv=False,
            csv_path=None,
            windowplot=False,
            performanceplot=False,
            logscale=logscale
        )

        train_asset_results[asset] = train
        test_asset_results[asset] = test


    train_index = None
    test_index = None

    for asset in weights:

        if train_index is None:
            train_index = train_asset_results[asset].index
        else:
            train_index = train_index.intersection(
                train_asset_results[asset].index
            )

        if test_index is None:
            test_index = test_asset_results[asset].index
        else:
            test_index = test_index.intersection(
                test_asset_results[asset].index
            )

    train_portfolio = pd.DataFrame(index=train_index)
    test_portfolio = pd.DataFrame(index=test_index)


    train_market_values = pd.DataFrame(index=train_index)
    test_market_values = pd.DataFrame(index=test_index)

    for asset, initial_weight in weights.items():

        train_returns = train_asset_results[asset].loc[
            train_index,
            "returns"
        ].fillna(0)

        test_returns = test_asset_results[asset].loc[
            test_index,
            "returns"
        ].fillna(0)

        train_market_values[asset] = (
            initial_weight *
            (1 + train_returns).cumprod()
        )

        ending_train_value = train_market_values[
            asset
        ].iloc[-1]

        test_market_values[asset] = (
            ending_train_value *
            (1 + test_returns).cumprod()
        )

    train_market_value = train_market_values.sum(axis=1)

    test_market_value = test_market_values.sum(axis=1)

    train_portfolio["returns"] = (
        train_market_value.pct_change()
    ).fillna(0)

    test_portfolio["returns"] = (
        test_market_value.pct_change()
    ).fillna(0)

    train_portfolio["market_cumulative"] = (
        train_market_value /
        train_market_value.iloc[0]
    )

    test_portfolio["market_cumulative"] = (
        test_market_value /
        test_market_value.iloc[0]
    )


    for strategy in strategies:

        ending = strategy[2]

        train_strategy_values = pd.DataFrame(
            index=train_index
        )

        test_strategy_values = pd.DataFrame(
            index=test_index
        )

        for asset, initial_weight in weights.items():

            train_returns = train_asset_results[asset].loc[
                train_index,
                f"strategy_returns_{ending}"
            ].fillna(0)

            test_returns = test_asset_results[asset].loc[
                test_index,
                f"strategy_returns_{ending}"
            ].fillna(0)

            train_strategy_values[asset] = (
                initial_weight *
                (1 + train_returns).cumprod()
            )

            ending_train_value = train_strategy_values[
                asset
            ].iloc[-1]

            test_strategy_values[asset] = (
                ending_train_value *
                (1 + test_returns).cumprod()
            )

        train_strategy_value = (
            train_strategy_values.sum(axis=1)
        )

        test_strategy_value = (
            test_strategy_values.sum(axis=1)
        )

        train_portfolio[
            f"strategy_returns_{ending}"
        ] = (
            train_strategy_value.pct_change()
        ).fillna(0)

        test_portfolio[
            f"strategy_returns_{ending}"
        ] = (
            test_strategy_value.pct_change()
        ).fillna(0)

        train_portfolio[
            f"cumulative_returns_{ending}"
        ] = (
            train_strategy_value /
            train_strategy_value.iloc[0]
        )

        test_portfolio[
            f"cumulative_returns_{ending}"
        ] = (
            test_strategy_value /
            test_strategy_value.iloc[0]
        )

    train_results = results_table(
        train_portfolio,
        strategies
    )

    test_results = results_table(
        test_portfolio,
        strategies
    )

    print("\nTraining Results")
    print(train_results)

    print("\nTesting Results")
    print(test_results)

    if performanceplot:

        print("\nTraining Performance")

        plot_performance(
            train_portfolio,
            logscale=logscale
        )

        print("Testing Performance")

        plot_performance(
            test_portfolio,
            logscale=logscale
        )

    return train_results, test_results


import numpy as np
import matplotlib.pyplot as plt


def efficient_frontier(returns_df, assets, num_portfolios=5000):
    selected_returns = returns_df[assets]

    annual_returns = selected_returns.mean() * 252
    cov_matrix = selected_returns.cov() * 252

    portfolio_returns = []
    portfolio_risks = []

    for _ in range(num_portfolios):

        weights = np.random.random(len(assets))
        weights /= weights.sum()

        port_return = np.sum(weights * annual_returns)

        port_risk = np.sqrt(
            weights.T @ cov_matrix @ weights
        )

        portfolio_returns.append(port_return)
        portfolio_risks.append(port_risk)

    portfolio_returns = np.array(portfolio_returns)
    portfolio_risks = np.array(portfolio_risks)

    plt.figure(figsize=(10, 6))

    plt.scatter(
        portfolio_risks,
        portfolio_returns,
        alpha=0.4
    )

    plt.xlabel("Volatility")
    plt.ylabel("Expected Return")
    plt.title("Portfolio Simulation")
    plt.grid(alpha=0.2)

    plt.show()

    return portfolio_returns, portfolio_risks