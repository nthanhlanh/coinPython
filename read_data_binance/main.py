import pandas as pd
import requests
import time

def fetch_all_binance_kline(symbol, interval, start_time):
    base_url = "https://api.binance.com/api/v3/klines"
    all_data = []

    while True:
        params = {
            'symbol': symbol,
            'interval': interval,
            'startTime': start_time,
            'limit': 1000  # Binance API supports a maximum of 1000 records per request
        }

        response = requests.get(base_url, params=params)
        data = response.json()

        if not data:
            break  # No more data available

        all_data.extend(data)

        # Update start_time to the last timestamp in the current data
        start_time = int(data[-1][0]) + 1  # Next request starts after the last time

        # Sleep for a short time to avoid hitting the rate limit
        time.sleep(0.5)

    # Convert to DataFrame and format the data
    df = pd.DataFrame(all_data, columns=[
        'Open Time', 'Open', 'High', 'Low', 'Close', 'Volume',
        'Close Time', 'Quote Asset Volume', 'Number of Trades',
        'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore'
    ])

    # Chọn các cột cần thiết
    df = df[['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume']]
    df['Open Time'] = pd.to_datetime(df['Open Time'], unit='ms')  # Chuyển đổi thời gian
    df.set_index('Open Time', inplace=True)  # Đặt thời gian làm chỉ mục

    return df

if __name__ == "__main__":
    # Set parameters
    symbol = "BTCUSDT"  # Trading pair
    intervals = ["1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "1d"]  # List of intervals
    start_time = int(pd.Timestamp("2024-10-01").timestamp() * 1000)

    for interval in intervals:
        # Fetch data
        btc_data = fetch_all_binance_kline(symbol, interval, start_time)
        
        # Save to CSV with the interval in the filename
        file_name = f'btc_data_{interval}.csv'
        btc_data.to_csv(file_name, index=True)  # Save the DataFrame to a CSV file
        print(f"Data saved to {file_name}")
