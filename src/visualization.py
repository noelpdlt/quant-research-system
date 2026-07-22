import matplotlib.pyplot as plt

def plot_performance(df):
    plt.figure(figsize=(10, 6))

    plt.plot(
        df.index,
        df["market_cumulative"],
        label="Market"
    )

    if "cumulative_returns_mom" in df.columns:
        plt.plot(
            df.index,
            df["cumulative_returns_mom"],
            label="Momentum Strategy"
        )
    
    if "cumulative_returns_mr" in df.columns:
        plt.plot(
            df.index,
            df["cumulative_returns_mr"],
            label="Mean Reversion Strategy"
        )
    
    if "cumulative_returns_mo_tr" in df.columns:
        plt.plot(
            df.index,
            df["cumulative_returns_mo_tr"],
            label="Momentum + Trend Filter Strategy"
        )

    if "cumulative_returns_mo_vo" in df.columns:
        plt.plot(
            df.index,
            df["cumulative_returns_mo_vo"],
            label="Momentum + Low Volatility Filter Strategy"
        )

    if "cumulative_returns_mo_vr" in df.columns:
        plt.plot(
            df.index,
            df["cumulative_returns_mo_vr"],
            label="Momentum + Volume Ratio Filter Strategy"
        )

    plt.title("Strategy vs Market Performance")
    plt.xlabel("Date")
    plt.ylabel("Growth of $1")
    plt.legend()

    plt.show()
