# load_data.py
import pandas as pd

def load_data(file_paths):
    data = {}
    for timeframe, path in file_paths.items():
        data[timeframe] = pd.read_csv(path, parse_dates=['Open Time'], index_col='Open Time')
    return data

def resample_and_merge(data, target_timeframe='15T'):
    resampled_data = {}
    for timeframe, df in data.items():
        resampled_data[timeframe] = df.resample(target_timeframe).agg({
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'sum'
        }).dropna()

    merged_data = resampled_data['1m'].copy()
    for timeframe, df in resampled_data.items():
        if timeframe != '1m':
            df = df.add_suffix(f'_{timeframe}')
            merged_data = merged_data.join(df, how='inner')
    return merged_data
