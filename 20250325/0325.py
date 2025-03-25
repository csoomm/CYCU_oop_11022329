import pandas as pd
import matplotlib.pyplot as plt

# 讀取 CSV 檔案，指定編碼為 UTF-8
file_path = 'C:/Users/User/Desktop/CYCU_oop_11022329/20250325/ExchangeRate@202503251847.csv'
df = pd.read_csv(file_path, encoding='utf-8')

# 保留需要的欄位，資料日期、匯率、現金、匯率.1、現金.1
df = df[['資料日期', '匯率', '匯率.1', '幣別', '遠期180天']]

#輸出資料日期
print(df['資料日期'])

# 繪製折線圖，線一的X為資料日期，Y為現金，名稱為匯率，顏色用藍色，線二的X為資料日期，Y為現金.1，名稱為匯率.1，顏色用紅色
df.plot(x='資料日期', y=['匯率', '匯率.1'], label=['幣別','遠期180天'], color=['blue', 'red'])

plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']  # 設定字體
plt.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題

# 設定圖表標題
plt.title('美金匯率走勢圖')

# 設定X軸標題
plt.xlabel('日期')

# 設定Y軸標題
plt.ylabel('匯率')

# 顯示網格
plt.grid()

# 顯示圖例
plt.show()
