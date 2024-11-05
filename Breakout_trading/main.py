# main.py
import numpy as np
from load_data import load_data, resample_and_merge
from indicators import calculate_technical_indicators
from preprocess import create_sequences
from model import build_lstm_model
# from telegram_bot import send_signal
from predict import predict_price

# Cài đặt thông số
file_paths = {
    '1m': 'data/btc_data_1m.csv',
    '3m': 'data/btc_data_3m.csv',
    '5m': 'data/btc_data_5m.csv',
    '15m': 'data/btc_data_15m.csv',
    '30m': 'data/btc_data_30m.csv',
    '1h': 'data/btc_data_1h.csv',
    '4h': 'data/btc_data_4h.csv'
}
lookback = 60
bot_token = "YOUR_BOT_TOKEN"
chat_id = "YOUR_CHAT_ID"

# 1. Tải và gộp dữ liệu
data = load_data(file_paths)
merged_data = resample_and_merge(data)

# 2. Tạo các chỉ báo kỹ thuật
merged_data = calculate_technical_indicators(merged_data)
# print(merged_data.isnull().sum())
print("Số lượng NaN trong dữ liệu:", merged_data.isnull().sum())
print("Thống kê mô tả:", merged_data.describe())



# 3. Chuẩn bị dữ liệu cho mô hình
x_train, y_train = create_sequences(merged_data, lookback=lookback)
# nan_indices = np.where(np.isnan(x_train))
# print("Indices of NaN in x_train:", nan_indices)
# print("Has NaN in x_train:", np.isnan(x_train).any())
# print("Has Inf in x_train:", np.isinf(x_train).any())
# print("Has NaN in y_train:", np.isnan(y_train).any())
# print("Has Inf in y_train:", np.isinf(y_train).any())



# 4. Xây dựng và huấn luyện mô hình
model = build_lstm_model((x_train.shape[1], x_train.shape[2]))
model.fit(x_train, y_train, epochs=200, batch_size=32)

# 5. Dự đoán giá và gửi tín hiệu
recent_data = x_train[-1]

predicted_price = predict_price(model, recent_data)
actual_price = data['15m'].tail(1)['Close'].values[0]
print(f"Actual Price: {actual_price}, Predicted Price: {predicted_price}")
print("Predicted Price:", predicted_price)
# model.summary()
# send_signal(predicted_price, bot_token, chat_id)
