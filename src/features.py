def compute_returns(df):
    df["returns"] = df["Close"].pct_change()
    return df

def moving_average(df, window=10):
    df["ma"] = df["Close"].rolling(window).mean()
    return df

def rolling_volatility(df, window=20):
    df["volatility"] = (
        df["returns"]
        .rolling(window)
        .std()
    )
    return df

def volume_ratio(df, window=20):
    df["volume_ratio"] = (
        df["Volume"] /
        df["Volume"].rolling(window).mean()
    )
    return df

def trend_strength(df):
    df["ma20"] = df["Close"].rolling(20).mean()
    df["ma50"] = df["Close"].rolling(50).mean()

    df["trend_strength"] = (
        df["ma20"] - df["ma50"]
    ) / df["ma50"]

    return df