#讀取C:\Users\User\Desktop\CYCU_oop_11022329\20250325\[忠孝幹線(公車雙向轉乘優惠)]公車動態資訊.html的資料

import requests
import os
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

url = 'https://pda5284.gov.taipei/MQS/route.jsp?rid=10417'

#讀取html檔案
response = requests.get(url)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'html.parser')

#製作資料夾名為P1
os.makedirs('C:\\Users\\User\\Desktop\\CYCU_oop_11022329\\20250401\\P1', exist_ok=True)


#讀取所有的a標籤
a_tags = soup.find_all('a')
print('去程-----------------------------')
for tag in a_tags:
    print(tag.text)
    print(tag.get('href'))
    if tag.text== "松山車站(松山)":
        print('回程-----------------------------')

    # 使用 Playwright 渲染後再儲存車站的 HTML 檔案，並儲存在 C:\Users\User\Desktop\CYCU_oop_11022329\20250401

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        station_url = 'https://pda5284.gov.taipei/MQS/' + tag.get('href')
        page.goto(station_url)
        content = page.content()
        with open(os.path.join('C:\\Users\\User\\Desktop\\CYCU_oop_11022329\\20250401\\P1', tag.text + '.html'), 'w', encoding='utf-8') as f:
            f.write(content)
        browser.close()





