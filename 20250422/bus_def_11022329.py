import requests
from bs4 import BeautifulSoup
import os
from playwright.sync_api import sync_playwright

output_dir = 'C:\\Users\\User\\Desktop\\CYCU_oop_11022329\\20250422'#輸入自己的路徑
os.makedirs(output_dir, exist_ok=True)


def bus_call(bus_id:str):
    #URL=https://bus.pcrest.tw/Bus/Route/TPE/11152?X=121.49282723665239&Y=25.144383810172837&Z=18
    
    #讀取網頁
    # 下載輸入的 HTML 網址
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        station_url=f"https://bus.pcrest.tw/Bus/Route/TPE/{bus_id}?X=121.49282723665239&Y=25.144383810172837&Z=18"
        page.goto(station_url)
        content = page.content()
        #讀取所有<strong>標籤的資料
        soup = BeautifulSoup(content, 'html.parser')
        strong_tags = soup.find_all('strong')
        file_path = os.path.join(output_dir, f"{bus_id}.html")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        browser.close()

bus_call("11152")
