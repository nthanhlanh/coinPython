# preprocess.py
import numpy as np

def create_sequences(data, lookback=60, forecast_horizon=4):
    sequences, labels = [], []
    for i in range(lookback, len(data) - forecast_horizon + 1):
        sequences.append(data[i-lookback:i].values)
        # Lấy 4 giá trị "Close_15m" tiếp theo làm nhãn
        labels.append(data['Close_15m'].values[i:i + forecast_horizon])
    return np.array(sequences), np.array(labels)
