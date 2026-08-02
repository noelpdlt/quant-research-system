import numpy as np

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

    df["ma5"] = df["Close"].rolling(5).mean()
    df["ma20"] = df["Close"].rolling(20).mean()
    df["ma50"] = df["Close"].rolling(50).mean()
    if window != 20:
        df["ma" + str(window)] = df["Close"].rolling(window).mean()

    df["trend_strength"] = (
        df["ma20"] - df["ma50"]
    ) / df["ma50"]

    df["distance_ma20"] = (
        (df["Close"] - df["ma20"]) /
        df["ma20"]
    )

    delta = df["Close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window).mean()
    avg_loss = loss.rolling(window).mean()
    rs = avg_gain / avg_loss
    df["rsi"] = 100 - (100 / (1 + rs))

    df["momentum"] = df["Close"].pct_change(window)
    
    df["target"] = (
        df["returns"].shift(-1) > 0
    ).astype(int)

    return df