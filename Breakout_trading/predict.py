# predict.py
import numpy as np

def predict_price(model, recent_data):
    recent_data = np.expand_dims(recent_data, axis=0)
    # print("Shape of recent_data:", recent_data.shape)  # Kiểm tra kích thước
    # print("Recent Data Values:", recent_data)
    # print("Has NaN:", np.isnan(recent_data).any())  # Kiểm tra xem có giá trị NaN không
    # print("Has Inf:", np.isinf(recent_data).any())  # Kiểm tra xem có giá trị Inf không
    predicted_price = model.predict(recent_data)
    return predicted_price[0][0]
