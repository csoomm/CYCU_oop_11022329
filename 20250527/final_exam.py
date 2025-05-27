#讀取url:https://ebus.gov.taipei/Route/StopsOfRoute?routeid=[公車路線ID]
import requests
from bs4 import BeautifulSoup
import openpyxl

def get_bus_stops(route_id):
    url = f"https://ebus.gov.taipei/Route/StopsOfRoute?routeid={route_id}"
    response = requests.get(url)
    
    # 讀取html內容
    if response.status_code == 200:
        html_content = response.text
        print(f"Successfully fetched data for route ID {route_id}")
        
        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 找到目標 <div> 並提取 <span> 資料
        go_direction_route = soup.find('div', id='GoDirectionRoute', class_='auto-list-pool-c stationlist-list-pool-c')
        back_direction_route = soup.find('div', id='BackDirectionRoute', class_='auto-list-pool-c stationlist-list-pool-c')

        # 建立 Excel 檔案
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Bus Stops"
        sheet.append([f"{route_id} (Go)", f"{route_id} (Back)"])  # 標題行

        # 處理去程資料
        if go_direction_route:
            go_station_list = go_direction_route.find_all('span', class_='auto-list-stationlist-place')
            go_stops = [station.get_text(strip=True) for station in go_station_list]
        else:
            go_stops = []
            print("無法找到去程目標 <div>，請檢查 HTML 結構是否正確。")

        # 處理回程資料
        if back_direction_route:
            back_station_list = back_direction_route.find_all('span', class_='auto-list-stationlist-place')
            back_stops = [station.get_text(strip=True) for station in back_station_list]
        else:
            back_stops = []
            print("無法找到回程目標 <div>，請檢查 HTML 結構是否正確。")

        # 將資料寫入 Excel
        max_len = max(len(go_stops), len(back_stops))
        for i in range(max_len):
            go_stop = go_stops[i] if i < len(go_stops) else ""
            back_stop = back_stops[i] if i < len(back_stops) else ""
            sheet.append([go_stop, back_stop])

        # 儲存 Excel 檔案
        file_name = f"bus_stops_{route_id}.xlsx"
        workbook.save(file_name)
        print(f"Data successfully saved to {file_name}")
    

RID = input("請輸入公車路線ID: ")    
get_bus_stops(RID)  # 請輸入公車路線ID
