def momentum_strategy(df, window=10):
    df["momentum"] = df["Close"].pct_change(window)
    df["signal_mom"] = (df["momentum"] > 0).astype(int)
    return df


def mean_reversion_strategy(df, window=10, threshold=0.05):
    rolling_mean = df["Close"].rolling(window).mean()

    df["signal_mr"] = (
        (df["Close"] < rolling_mean * (1 - threshold))
    ).astype(int)

    return df


def momentum_trend_strategy(df, window=10):
    df["momentum"] = df["Close"].pct_change(window)
    df["signal_mo_tr"] = ((df["momentum"] > 0) & 
                          (df["trend_strength"] > 0)).astype(int)
    return df


def momentum_volatility_strategy(df, window=10, threshold=0.5):
    df["momentum"] = df["Close"].pct_change(window)
    df["signal_mo_vo"] = ((df["momentum"] > 0) & 
                          (df["volatility"] < threshold)).astype(int)
    return df


def momentum_voluratio_strategy(df, window=10):
    df["momentum"] = df["Close"].pct_change(window)
    df["signal_mo_vr"] = ((df["momentum"] > 0) & 
                          (df["volume_ratio"] > 1)).astype(int)
    return df