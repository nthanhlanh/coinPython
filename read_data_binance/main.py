import requests
import pandas as pd
import time

# Function to fetch Kline data
def fetch_binance_kline(symbol, interval, start_time, end_time):
    url = "https://api.binance.com/api/v3/klines"
    params = {
        'symbol': symbol,
        'interval': interval,
        'startTime': start_time,
        'endTime': end_time,
        'limit': 1000  # Max limit per request
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    # Transform data into a DataFrame
    df = pd.DataFrame(data, columns=['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume',
                                      'Close Time', 'Quote Asset Volume', 'Number of Trades',
                                      'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore'])
    # Convert Open Time to datetime
    df['Open Time'] = pd.to_datetime(df['Open Time'], unit='ms')
    # Return only relevant columns
    return df[['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume']]

# Function to fetch all data till now
def fetch_all_binance_kline(symbol, interval, start_time):
    all_data = []
    current_start_time = start_time
    current_time = int(time.time() * 1000)  # Current time in milliseconds
    
    while True:
        # Fetch data for a specific time range
        df = fetch_binance_kline(symbol, interval, current_start_time, current_time)
        if df.empty:
            break
        
        all_data.append(df)
        
        # Update start time to the next interval
        current_start_time = int(df['Open Time'].iloc[-1].timestamp() * 1000) + 1
        
        # Break if the last data point is already close to current time
        if current_start_time >= current_time:
            break

    # Concatenate all data frames
    if all_data:
        full_data = pd.concat(all_data, ignore_index=True)
        return full_data
    else:
        return pd.DataFrame()  # Return empty DataFrame if no data

# Example usage
if __name__ == "__main__":
    # Set parameters
    symbol = "BTCUSDT"  # Trading pair
    interval = "1h"     # Hourly data
    start_time = 1483228800000  # Start time in milliseconds (1/1/2017)

    # Fetch data
    btc_data = fetch_all_binance_kline(symbol, interval, start_time)
    
    # Save to CSV
    btc_data.to_csv('btc_data_1h.csv', index=False)  # Save the DataFrame to a CSV file
    print("Data saved to btc_data.csv")
