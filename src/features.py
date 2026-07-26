def generate_features(df, window = 20):
    df["returns"] = df["Close"].pct_change()

    df["volatility"] = (
        df["returns"]
        .rolling(window)
        .std()
    )

    df["volume_ratio"] = (
        df["Volume"] /
        df["Volume"].rolling(window).mean()
    )

    df["ma20"] = df["Close"].rolling(20).mean()
    df["ma50"] = df["Close"].rolling(50).mean()
    if window != 20:
        df["ma" + str(window)] = df["Close"].rolling(window).mean()

    df["trend_strength"] = (
        df["ma20"] - df["ma50"]
    ) / df["ma50"]

    return df
