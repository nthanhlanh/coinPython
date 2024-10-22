import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np

def main():
    # Đọc dữ liệu từ file CSV
    data = pd.read_csv('data.csv', parse_dates=['Open Time'])
    data['Next Close'] = data['Close'].shift(-1)  # Giá đóng cửa ngày tiếp theo
    
    # Chọn biến đầu vào và biến mục tiêu
    X = data[['Open', 'High', 'Low', 'Close', 'Volume']].iloc[:-1]  # Biến đầu vào
    y = data['Next Close'].iloc[:-1]  # Biến mục tiêu

    # Chia dữ liệu
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Tạo mô hình hồi quy
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Dự đoán giá ngày tiếp theo
    last_data = data[['Open', 'High', 'Low', 'Close', 'Volume']].iloc[-1].values.reshape(1, -1)
    predicted_price = model.predict(last_data)[0]

    # Lấy giá hiện tại
    current_price = data['Close'].iloc[-1]

    # In ra kết quả dự đoán
    print(f"Giá hiện tại: {current_price:.2f} USD")
    print(f"Dự đoán giá Bitcoin cho ngày tiếp theo: {predicted_price:.2f} USD")

    # Quyết định mua hay bán
    if predicted_price > current_price:
        print(f"Nên mua vào tại giá: {current_price:.2f} USD")
        print(f"Mục tiêu bán ra: {predicted_price:.2f} USD")
    else:
        print(f"Nên bán ra tại giá: {current_price:.2f} USD")
        print(f"Mục tiêu mua lại: {predicted_price:.2f} USD")

if __name__ == "__main__":
    main()
