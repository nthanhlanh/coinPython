import pandas as pd
import matplotlib.pyplot as plt

def plot_predictions(file_path='prediction_results.csv', time_frame='1h'):
    """
    Hàm để vẽ biểu đồ từ dữ liệu dự đoán trong file CSV.

    Parameters:
    - file_path (str): Đường dẫn tới file CSV chứa dữ liệu dự đoán.
    - time_frame (str): Khung thời gian của dữ liệu dự đoán (ví dụ: '1h', '2h', '4h').
    """
    # Đọc dữ liệu từ file CSV
    try:
        print(f"Đang đọc file: {file_path}")
        data = pd.read_csv(file_path, encoding='ISO-8859-1')

        # Chuyển đổi cột 'Date' sang kiểu datetime
        data['Date'] = pd.to_datetime(data['Date'], errors='coerce')

        # Kiểm tra xem có giá trị NaT nào không
        if data['Date'].isnull().any():
            print("Cảnh báo: Có giá trị không hợp lệ trong cột 'Date'.")

        print(f"Đã đọc dữ liệu từ {file_path}")
    except FileNotFoundError:
        print(f"Lỗi: File {file_path} không tồn tại.")
        return
    
    # Kiểm tra các cột cần thiết
    required_columns = ['Date', 'Predicted Price', 'Decision']
    for col in required_columns:
        if col not in data.columns:
            print(f"Lỗi: Cột '{col}' không tồn tại trong dữ liệu.")
            return

    # Tạo figure và axes
    plt.figure(figsize=(12, 6))

    # Plot giá dự đoán
    plt.plot(data['Date'], data['Predicted Price'], marker='o', label='Giá dự đoán', color='blue', linestyle='--')

    # Vẽ quyết định Mua/Bán
    buy_signals = data[data['Decision'] == 'Mua vào']
    sell_signals = data[data['Decision'] == 'Bán ra']

    # Plot điểm mua vào
    plt.scatter(buy_signals['Date'], buy_signals['Predicted Price'], label='Mua vào', color='green', marker='^', s=100)
    
    # Plot điểm bán ra
    plt.scatter(sell_signals['Date'], sell_signals['Predicted Price'], label='Bán ra', color='red', marker='v', s=100)

    # Thêm tiêu đề và nhãn
    plt.title(f'Dự đoán giá Bitcoin ({time_frame}) và Quyết định Mua/Bán')
    plt.xlabel('Ngày')
    plt.ylabel('Giá Bitcoin (USD)')
    plt.legend(loc='best')
    plt.grid(True)

    # Hiển thị biểu đồ
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
