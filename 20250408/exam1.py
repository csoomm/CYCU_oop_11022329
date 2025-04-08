import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erf  # 匯入 erf 函數

def plot_lognormal_cdf(num1, num2):
    # 生成對數常態分布的 x 軸數據
    x = np.linspace(0.01, 5, 1000)  # 避免 log(0)，x 從 0.01 開始

    # 計算對數常態累積分布函數 (CDF)
    cdf = 0.5 + 0.5 * erf((np.log(x) - num1) / (num2 * np.sqrt(2)))

    # 繪製圖表
    plt.figure(figsize=(8, 6))
    plt.plot(x, cdf, label=f'μ={num1}, σ={num2}', color='blue')
    plt.title("Lognormal cumulative distribution function")
    plt.xlabel("x")
    plt.ylabel("Cumulative distribution function (CDF)")
    plt.legend()
    plt.grid()

    # 儲存圖表為 JPG 檔案
    output_filename = "lognormal_cdf.jpg"
    plt.savefig(output_filename, format='jpg')
    print(f"圖表已儲存為 {output_filename}")

    # 顯示圖表
    plt.show()

# 讀取兩個數字
num1 = float(input("請輸入第一個數字 (均值 μ)："))
num2 = float(input("請輸入第二個數字 (標準差 σ)："))
#執行函數
plot_lognormal_cdf(num1, num2)