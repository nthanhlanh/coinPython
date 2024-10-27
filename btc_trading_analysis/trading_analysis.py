import pandas as pd
import backtrader as bt
import os

# Định nghĩa chiến lược sử dụng SMA
class SmaStrategy(bt.Strategy):
    params = (('sma_period', 15),)

    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.sma_period)

    def next(self):
        pass  # Không cần thực hiện bất kỳ hành động nào trong quá trình chạy

    def predict_next_candles(self):
        last_price = self.data.close[0]
        predicted_prices = []
        
        for i in range(5):  # Dự đoán cho 5 cây nến tiếp theo
            next_price = last_price + (self.sma[0] - last_price) * (i + 1) / 5  # Điều chỉnh dự đoán dựa trên SMA
            predicted_prices.append(next_price)
            last_price = next_price  # Cập nhật giá cho dự đoán tiếp theo
            
        return predicted_prices

def run_backtrader_for_file(file_name):
    # Tạo đối tượng Cerebro
    cerebro = bt.Cerebro()

    # Đọc dữ liệu từ CSV
    data = pd.read_csv(file_name, parse_dates=['Open Time'])
    data.set_index('Open Time', inplace=True)

    # Định nghĩa cấu trúc dữ liệu cho Backtrader
    data_feed = bt.feeds.PandasData(
        dataname=data,
        datetime=None,
        open='Open',
        high='High',
        low='Low',
        close='Close',
        volume='Volume',
    )

    # Thêm dữ liệu vào Cerebro
    cerebro.adddata(data_feed)

    # Thêm chiến lược vào Cerebro
    cerebro.addstrategy(SmaStrategy)

    # Chạy backtest
    results = cerebro.run()

    # Lấy chiến lược đã chạy
    strategy = results[0]

    # Dự đoán 5 cây nến tiếp theo
    predicted_prices = strategy.predict_next_candles()
    return predicted_prices

if __name__ == "__main__":
    # Đường dẫn tới thư mục chứa dữ liệu
    data_folder = 'data'

    # Duyệt qua tất cả các file trong thư mục
    for file in os.listdir(data_folder):
        if file.endswith('.csv'):
            file_path = os.path.join(data_folder, file)
            print(f"\nDự đoán cho file: {file}")
            predicted_prices = run_backtrader_for_file(file_path)
            print("Dự đoán 5 cây nến tiếp theo:")
            for i, price in enumerate(predicted_prices, start=1):
                print(f"Cây nến {i}: Giá dự đoán = {price:.2f}")
