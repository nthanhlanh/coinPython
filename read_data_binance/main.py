import requests
import pandas as pd

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

# Example usage
if __name__ == "__main__":
    # Set parameters
    symbol = "BTCUSDT"  # Trading pair
    interval = "1d"     # Daily data
    start_time = 1483228800000  # Start time in milliseconds (1/1/2017)
    end_time = 1697452800000    # End time in milliseconds (e.g., 10/18/2024)

    # Fetch data
    btc_data = fetch_binance_kline(symbol, interval, start_time, end_time)
    
    # Save to CSV
    btc_data.to_csv('data.csv', index=False)  # Save the DataFrame to a CSV file
    print("Data saved to btc_data.csv")
