import pandas as pd
import matplotlib.pyplot as plt

def read_excel(file_path, x_col, y_col):
    # 讀取Excel文件
    df = pd.read_excel(file_path)

    # 獲取x和y欄位的數據
    x_data = df[x_col]
    y_data = df[y_col]

    return x_data, y_data

def main():
    file_path = 'C:/Users/User/Desktop/CYCU_oop_11022329/20250311/311.xlsx'  # 替換為您的Excel文件路徑
    x_col = 'x'  # 替換為您的x欄位名稱
    y_col = 'y'  # 替換為您的y欄位名稱

    x_data, y_data = read_excel(file_path, x_col, y_col)

    # 將x和y欄位相加
    sum_data = x_data + y_data

    # 輸出結果
    for i, value in enumerate(sum_data):
        print(f"Row {i+1}: {value}")

    # 繪製散佈圖
    plt.scatter(x_data, y_data)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title('Scatter Plot of x and y')
    plt.show()

if __name__ == "__main__":
    main()