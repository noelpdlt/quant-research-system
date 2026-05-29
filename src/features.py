def compute_returns(df):
    df["returns"] = df["Close"].pct_change()
    return df

def moving_average(df, window=10):
    df["ma"] = df["Close"].rolling(window).mean()
    return df