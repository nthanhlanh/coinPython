# indicators.py
import pandas as pd

def calculate_technical_indicators(df):
    df['SMA_15m'] = df['Close_15m'].rolling(window=15).mean()
    # Kiểm tra số lượng hàng dữ liệu cho EMA_1h
    df['EMA_1h'] = df['Close_1h'].ewm(span=10, adjust=False).mean()
    # Kiểm tra số lượng hàng dữ liệu cho RSI
    df['RSI_4h'] = compute_rsi(df['Close_4h'], window=14)
    # Xóa 15 hàng đầu tiên
    df = df.drop(df.index[:15])

    # Kiểm tra giá trị NaN
    # if df['SMA_15m'].isnull().values.any():
    #     print("NaN values found in SMA_15m")
    # if df['EMA_1h'].isnull().values.any():
    #     print("NaN values found in EMA_1h")
    # if df['RSI_4h'].isnull().values.any():
    #     print("NaN values found in RSI_4h")

    return df

def compute_rsi(series, window=14):
    delta = series.diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))
