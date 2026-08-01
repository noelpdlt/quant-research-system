import yfinance as yf
import pandas as pd

def get_data(ticker, start, end):
    data = yf.download(
        ticker,
        start=start,
        end=end,
        auto_adjust=False
    )

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    return data