# predict.py
import numpy as np
import pandas as pd

def predict_price(model, recent_data, start_time):
    recent_data = np.expand_dims(recent_data, axis=0)
    predicted_prices = model.predict(recent_data)[0]  # Dự đoán 4 bước

    # Tạo DataFrame để hiển thị kết quả giống như dữ liệu đầu vào
    future_times = pd.date_range(start=start_time, periods=4, freq='15T')  # Tạo thời gian cho 4 cây nến 15 phút tiếp theo
    predictions_df = pd.DataFrame({
        'Open Time': future_times,
        'Open': [predicted_prices[0]] + list(predicted_prices[:-1]),  # Dùng giá trị trước làm "Open"
        'High': predicted_prices,  # Giả sử giá dự đoán là giá cao nhất
        'Low': predicted_prices,   # Giả sử giá dự đoán là giá thấp nhất
        'Close': predicted_prices, # Giá đóng cửa dự đoán
        'Volume': [0]*4  # Giả sử không dự đoán Volume
    })
    return predictions_df
