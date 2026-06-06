def momentum_strategy(df, window=10):
    df["momentum"] = df["Close"].pct_change(window)
    df["signal"] = (df["momentum"] > 0).astype(int)
    return df