#讀取C:\Users\User\Desktop\CYCU_oop_11022329\20250325\[忠孝幹線(公車雙向轉乘優惠)]公車動態資訊.html的資料

import requests
import os
from bs4 import BeautifulSoup

url = 'https://pda5284.gov.taipei/MQS/route.jsp?rid=10417'

#讀取html檔案
response = requests.get(url)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'html.parser')

#讀取所有的a標籤
a_tags = soup.find_all('a')
for tag in a_tags:
    print(tag.text)
    print(tag.get('href'))
    print('-----------------------------')
    


