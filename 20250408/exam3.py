import requests
from bs4 import BeautifulSoup
import os
from playwright.sync_api import sync_playwright

# input 輸入車站代號
station_id = input("請輸入車站代號：")

# 檢查輸出目錄是否存在，若不存在則建立
output_dir = 'C:\\Users\\Cosmos\\Desktop\\CYCU_oop_11022329\\20250408\P1'
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

def extract_bus_info_by_direction(file_path):
    # 讀取 HTML 檔案
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

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
    


    # 提取去程與回程的站點資訊
    go_bus_info_list = extract_stops_info(go_stops)
    back_bus_info_list = extract_stops_info(back_stops)

    return go_bus_info_list, back_bus_info_list


if __name__ == "__main__":
    file_path = os.path.join(output_dir, f"{station_id}.html")
    go_output_csv_path = r'C:\\Users\\Cosmos\\Desktop\\CYCU_oop_11022329\\20250408\\go_bus_info.csv'
    back_output_csv_path = r'C:\\Users\\Cosmos\\Desktop\\CYCU_oop_11022329\\20250408\\back_bus_info.csv'


    # 提取去程與回程的公車資訊
    go_bus_info_list, back_bus_info_list = extract_bus_info_by_direction(file_path)

    def save_to_csv(data_list, file_path):
    # 確保資料不為空
        if not data_list:
            print(f"資料為空，無法儲存至 {file_path}")
            return

        # 取得資料的欄位名稱
        fieldnames = data_list[0].keys()

        # 將資料寫入 CSV 檔案
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data_list)

    # 儲存去程與回程的公車資訊到不同的 CSV 檔案
    save_to_csv(go_bus_info_list, go_output_csv_path)
    save_to_csv(back_bus_info_list, back_output_csv_path)

    print(f"去程公車資訊已儲存至 {go_output_csv_path}")
    print(f"回程公車資訊已儲存至 {back_output_csv_path}")