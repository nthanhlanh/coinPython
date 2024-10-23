import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from plot_utils import plot_predictions
import matplotlib.pyplot as plt

def load_data(file_path):
    """Tải dữ liệu từ file CSV với encoding thích hợp."""
    try:
        return pd.read_csv(file_path, parse_dates=['Open Time'], encoding='utf-8')
    except UnicodeDecodeError:
        return pd.read_csv(file_path, parse_dates=['Open Time'], encoding='latin1')

def calculate_rsi(data, window=14):
    """Tính toán RSI."""
    delta = data['Close'].diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(data):
    """Tính toán MACD và tín hiệu."""
    short_ema = data['Close'].ewm(span=12, adjust=False).mean()
    long_ema = data['Close'].ewm(span=26, adjust=False).mean()
    macd = short_ema - long_ema
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd, signal

def calculate_ema(data, window):
    """Tính toán Exponential Moving Average (EMA)."""
    return data['Close'].ewm(span=window, adjust=False).mean()

def calculate_bollinger_bands(data, window=20, num_std=2):
    """Tính toán Bollinger Bands."""
    sma = data['Close'].rolling(window=window).mean()
    rstd = data['Close'].rolling(window=window).std()
    upper_band = sma + (rstd * num_std)
    lower_band = sma - (rstd * num_std)
    return upper_band, lower_band

def calculate_stochastic(data, window=14):
    """Tính toán Stochastic Oscillator."""
    low_min = data['Low'].rolling(window=window).min()
    high_max = data['High'].rolling(window=window).max()
    k = 100 * (data['Close'] - low_min) / (high_max - low_min)
    d = k.rolling(window=3).mean()  # D là SMA của %K
    return k, d

def calculate_atr(data, window=14):
    """Tính toán Average True Range (ATR)."""
    high_low = data['High'] - data['Low']
    high_close = (data['High'] - data['Close'].shift(1)).abs()
    low_close = (data['Low'] - data['Close'].shift(1)).abs()
    true_range = high_low.combine(high_close, max).combine(low_close, max)
    atr = true_range.rolling(window=window).mean()
    return atr

def calculate_obv(data):
    """Tính toán On-Balance Volume (OBV)."""
    obv = (data['Volume'] * (data['Close'].diff().apply(lambda x: 1 if x > 0 else -1 if x < 0 else 0))).cumsum()
    return obv

def calculate_momentum(data, window=10):
    """Tính toán Momentum Indicator."""
    momentum = data['Close'].diff(window)
    return momentum

def generate_signals(data):
    """Tạo tín hiệu mua/bán dựa trên RSI và MACD."""
    rsi = calculate_rsi(data)
    macd, signal = calculate_macd(data)
    
    data['RSI'] = rsi
    data['MACD'] = macd
    data['Signal'] = signal
    data['EMA_20'] = calculate_ema(data, window=20)
    data['Upper_Band'], data['Lower_Band'] = calculate_bollinger_bands(data)
    data['ATR'] = calculate_atr(data)

    # Tín hiệu mua
    data['Buy Signal'] = (
        (data['RSI'] < 30) &                            # RSI thấp
        (data['MACD'] > data['Signal']) &               # MACD vượt lên tín hiệu
        (data['Close'] < data['Lower_Band']) &          # Giá đóng cửa dưới dải dưới Bollinger Bands
        (data['Close'] > data['EMA_20'])                # Giá đóng cửa trên EMA 20
    ).astype(int)

    # Tín hiệu bán
    data['Sell Signal'] = (
        (data['RSI'] > 70) &                            # RSI cao
        (data['MACD'] < data['Signal']) &               # MACD vượt xuống tín hiệu
        (data['Close'] > data['Upper_Band']) &          # Giá đóng cửa trên dải trên Bollinger Bands
        (data['Close'] < data['EMA_20'])                # Giá đóng cửa dưới EMA 20
    ).astype(int)

    return data

def predict_next_candles(data, num_candles=10):
    """Dự đoán giá cho n cây nến tiếp theo."""
    last_data = data[['Open', 'High', 'Low', 'Close', 'Volume']].iloc[-1].values.reshape(1, -1)
    predictions = []

    for _ in range(num_candles):
        next_price = last_data[0][3]  # Sử dụng giá đóng cửa cuối cùng làm giá dự đoán
        predictions.append(next_price)
        
        # Cập nhật dữ liệu giả định cho cây nến tiếp theo
        next_data = np.array([next_price] * 4 + [last_data[0][4]]).reshape(1, -1)
        last_data = next_data

    return predictions

import pandas as pd

def save_results(results, file_path):
    """Lưu kết quả vào file CSV, xóa dữ liệu trùng lặp trước khi thêm mới."""
    try:
        # Đọc file CSV và tự động suy diễn định dạng ngày tháng
        existing_data = pd.read_csv(file_path, encoding='latin1', parse_dates=['Date'], infer_datetime_format=True)
        
        # Nếu cột 'Date' không tồn tại hoặc có giá trị không hợp lệ, tạo một DataFrame rỗng
        if 'Date' not in existing_data.columns or existing_data['Date'].isnull().any():
            print("Cảnh báo: Có giá trị không hợp lệ trong cột 'Date'. Tạo DataFrame rỗng.")
            existing_data = pd.DataFrame()
    except FileNotFoundError:
        # Nếu file không tồn tại, tạo một DataFrame rỗng
        existing_data = pd.DataFrame()

    # Chuyển đổi kết quả thành DataFrame
    result_df = pd.DataFrame(results)

    # Xóa các dòng trùng lặp dựa trên cột 'Date'
    if not existing_data.empty:
        existing_data = existing_data[~existing_data['Date'].isin(result_df['Date'])]

    # Kết hợp dữ liệu hiện có và dữ liệu mới
    final_data = pd.concat([existing_data, result_df], ignore_index=True)

    # Lưu DataFrame cuối cùng vào file CSV
    final_data.to_csv(file_path, index=False)

    print(f"Dữ liệu đã được lưu vào {file_path}.")


def main():
    # Đọc dữ liệu
    data = load_data('btc_data_1h.csv')
    
    # Tính toán các chỉ báo
    data = generate_signals(data)

    # Dự đoán cho 10 cây nến tiếp theo
    predictions = predict_next_candles(data, num_candles=10)
    
    # Lấy thời gian hiện tại
    current_time = datetime.now()
    results = []

    for i, predicted_price in enumerate(predictions):
        forecast_time = current_time + timedelta(hours=i + 1)  # Dự đoán cho mỗi giờ tiếp theo
        results.append({'Date': forecast_time, 'Predicted Price': predicted_price})

    # Lưu kết quả vào file
    save_results(results, 'prediction_results.csv')

    print("Kết quả dự đoán cho 10 cây nến tiếp theo đã được lưu vào file prediction_results.csv.")

    # Vẽ biểu đồ từ file dự đoán
    # plot_predictions('prediction_results.csv')

if __name__ == "__main__":
    main()
