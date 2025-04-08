import requests
from bs4 import BeautifulSoup
import os
from playwright.sync_api import sync_playwright

# input 輸入車站代號
station_id = input("請輸入車站代號：")

# 檢查輸出目錄是否存在，若不存在則建立
output_dir = 'C:\\Users\\User\\Desktop\\CYCU_oop_11022329\\20250408\\P1'
os.makedirs(output_dir, exist_ok=True)

# 下載輸入的 HTML 網址
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    station_url = f"https://ebus.gov.taipei/Route/StopsOfRoute?routeid={station_id}"
    page.goto(station_url)
    content = page.content()
    file_path = os.path.join(output_dir, f"{station_id}.html")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    browser.close()

from bs4 import BeautifulSoup
import csv

def extract_bus_info(file_path):
    # 讀取 HTML 檔案
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # 找到所有的公車站點資訊
    stops = soup.find_all('li')

    # 儲存結果的列表
    bus_info_list = []

    for stop in stops:
        # 提取所需資訊
        arrival_info = stop.find('span', class_='auto-list-stationlist-position')
        stop_number = stop.find('span', class_='auto-list-stationlist-number')
        stop_name = stop.find('span', class_='auto-list-stationlist-place')
        stop_id = stop.find('input', {'name': 'item.UniStopId'})
        latitude = stop.find('input', {'name': 'item.Latitude'})
        longitude = stop.find('input', {'name': 'item.Longitude'})

        # 確保所有欄位存在
        if arrival_info and stop_number and stop_name and stop_id and latitude and longitude:
            bus_info = {
                "arrival_info": arrival_info.text.strip(),
                "stop_number": stop_number.text.strip(),
                "stop_name": stop_name.text.strip(),
                "stop_id": stop_id['value'],
                "latitude": latitude['value'],
                "longitude": longitude['value']
            }
            bus_info_list.append(bus_info)

    return bus_info_list

def save_to_csv(bus_info_list, output_csv_path):
    # 定義 CSV 欄位名稱
    fieldnames = ["arrival_info", "stop_number", "stop_name", "stop_id", "latitude", "longitude"]

    # 寫入 CSV 檔案
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(bus_info_list)

# 測試函數
if __name__ == "__main__":
    file_path = os.path.join(output_dir, f"{station_id}.html")
    output_csv_path = r'C:\\Users\\User\\Desktop\\CYCU_oop_11022329\\20250408\\bus_info.csv'

    bus_info_list = extract_bus_info(file_path)
    save_to_csv(bus_info_list, output_csv_path)

    print(f"公車資訊已儲存至 {output_csv_path}")