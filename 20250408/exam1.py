import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import lognorm #匯入CDF函數

def plot_normal_pdf(mu, sigma):
    # 生成常態分布的 x 軸數據
    x = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 1000)

    # 計算常態機率密度函數 (PDF)
    pdf = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2))

    # 繪製圖表
    plt.figure(figsize=(8, 6))
    plt.plot(x, pdf, label=f'μ={mu}, σ={sigma}', color='blue')
    plt.title("Normal Probability Density Function (PDF)")
    plt.xlabel("x")
    plt.ylabel("Probability Density Function (PDF)")
    plt.legend()
    plt.grid()

    # 儲存圖表為 JPG 檔案
    output_filename = r"C:\\Users\\Cosmos\\Desktop\\CYCU_oop_11022329\\20250408\\normal_PDF.jpg"#改成自己的路徑
    plt.savefig(output_filename, format='jpg')
    print(f"圖表已儲存為 {output_filename}")

    # 顯示圖表
    plt.show()

# 讀取兩個數字
num1 = float(input("請輸入第一個數字 (均值 mu)："))
num2 = float(input("請輸入第二個數字 (標準差 simga)："))
#執行函數
plot_normal_pdf(num1, num2)