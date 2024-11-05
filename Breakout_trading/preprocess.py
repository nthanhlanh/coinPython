# preprocess.py
import numpy as np

def create_sequences(data, lookback=60):
    sequences, labels = [], []
    for i in range(lookback, len(data)):
        sequences.append(data[i-lookback:i].values)
        labels.append(data['Close_15m'].values[i])
    return np.array(sequences), np.array(labels)
