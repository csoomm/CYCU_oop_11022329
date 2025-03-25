from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# 設定 Chrome 瀏覽器
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 啟動無頭模式
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

# 啟動 Chrome 瀏覽器
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 讀取網頁內容
url = 'https://pda5284.gov.taipei/MQS/route.jsp?rid=10417'
driver.get(url)

#開啟網頁後，取得html內容
html = driver.page_source
sp = BeautifulSoup(html, 'html.parser')

# 等待網頁加載完成
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ttego1')))

# 獲取網頁源代碼
html = driver.page_source
sp = BeautifulSoup(html, 'html.parser')

# 找到所有的 <tr> 標籤中的 class 為 "ttego1" 的元素
all_tr = sp.find_all('tr', class_='ttego1')

# 只保留 <td> 中包含 "tte" 的元素
for tr in all_tr:
    stop_name_td = tr.find('td')
    arrival_time_td = tr.find('td', id=lambda x: x and x.startswith('tte'))
    if stop_name_td and arrival_time_td:
        stop_name = stop_name_td.text.strip()
        arrival_time = arrival_time_td.text.strip()
        print(f'公車站: {stop_name}, 到站時間: {arrival_time}')

# 關閉瀏覽器
driver.quit()