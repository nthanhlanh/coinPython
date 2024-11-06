# model.py
from keras.api.models import Sequential
from keras.api.layers import LSTM, Dense, Dropout

def build_lstm_model(input_shape, output_steps=4):
    model = Sequential([
        LSTM(100, return_sequences=True, input_shape=input_shape),
        Dropout(0.2),
        LSTM(100, return_sequences=False),
        Dropout(0.2),
        Dense(25),
        Dense(output_steps)  # Đầu ra sẽ gồm 4 giá trị cho 4 nến 15m
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model
