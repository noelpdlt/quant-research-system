import matplotlib.pyplot as plt

strategies = [
        ('Momentum Strategy', 'mom'),
        ('Mean Reversion Strategy', 'mr'),
        ('Momentum + Trend Filter Strategy', 'mo_tr'),
        ('Momentum + Low Volatility Filter Strategy', 'mo_vo'),
        ('Momentum + Volume Ratio Filter Strategy', 'mo_vr')
    ]

features = [
    ('Volatility', 'volatility'),
    ('Volume Ratio', 'volume_ratio'),
    ('Trend Strength', 'trend_strength')
]

def plot_performance(df):
    plt.figure(figsize=(10, 6))
    
    plt.plot(
        df.index,
        df["market_cumulative"],
        label="Market"
    )

    for name, ending in strategies:
        cumulative_returns = 'cumulative_returns_' + ending
        if  cumulative_returns in df.columns:
            plt.plot(
                df.index,
                df[cumulative_returns],
                label = name
            )

    plt.title("Strategy vs Market Performance")
    plt.xlabel("Date")
    plt.ylabel("Growth of $1")
    plt.legend()

    plt.show()

def plot_features(df):
    for name, feature in features:
        plt.figure(figsize=(10,6))
        plt.plot(df.index, df[feature])

        plt.title(name)
        plt.xlabel("Date")
        plt.ylabel(name)
        plt.legend()
        plt.show()