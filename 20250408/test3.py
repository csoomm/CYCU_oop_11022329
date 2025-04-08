import requests
from bs4 import BeautifulSoup
import os
from playwright.sync_api import sync_playwright

# input 輸入車站代號
station_id = input("請輸入車站代號：")
#0100000A00

# 檢查輸出目錄是否存在，若不存在則建立
output_dir = 'C:\\Users\\Cosmos\\Desktop\\CYCU_oop_11022329\\20250408\P1'
os.makedirs(output_dir, exist_ok=True)

# 在網頁中開啟HTML檔案，並利用playwright進行渲染，直接在終端機顯示
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    station_url = f"https://ebus.gov.taipei/Route/StopsOfRoute?routeid={station_id}"
    page.goto(station_url)
    content = page.content()
    #讀取HTML檔案中的”arrival_info", "stop_number", "stop_name", "stop_id", "latitude", "longitude”，並在終端機中顯示
    soup = BeautifulSoup(content, 'html.parser')
    # 找到去程與回程的站點資訊
    go_stops = soup.find('div', id='GoDirectionRoute').find_all('li')
    back_stops = soup.find('div', id='BackDirectionRoute').find_all('li')
    # 提取站點資訊的輔助函數
    def extract_stops_info(stops):
        bus_info_list = []
        for stop in stops:
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
    
    

    # 儲存成 CSV 檔案
    import csv
    go_stops_info = extract_stops_info(go_stops)
    back_stops_info = extract_stops_info(back_stops)
    go_file_path = os.path.join(output_dir, f"{station_id}_go.csv")
    back_file_path = os.path.join(output_dir, f"{station_id}_back.csv")
    with open(go_file_path, 'w', encoding='utf-8') as go_file:
        writer = csv.DictWriter(go_file, fieldnames=go_stops_info[0].keys())
        writer.writeheader()
        writer.writerows(go_stops_info) 
    with open(back_file_path, 'w', encoding='utf-8') as back_file:
        writer = csv.DictWriter(back_file, fieldnames=back_stops_info[0].keys())
        writer.writeheader()
        writer.writerows(back_stops_info)
    
    browser.close()
