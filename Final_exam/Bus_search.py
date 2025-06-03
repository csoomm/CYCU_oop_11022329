import pandas as pd
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import os
from playwright.sync_api import sync_playwright


# 定義檔案路徑
file_path = r"C:\Users\31002\OneDrive\桌面\CYCU_oop_11022329\Final_exam\taipei_bus_stops.xlsx"

# 讀取 Excel 檔案
try:
    # 使用 pandas 讀取 Excel
    bus_stops_data = pd.read_excel(file_path)
    
    # 顯示前幾筆資料
    print("資料載入成功")
except FileNotFoundError:
    print("檔案未找到，請確認檔案路徑是否正確。")
except Exception as e:
    print(f"讀取檔案時發生錯誤: {e}")

def search_bus_route(stop1, stop2):
    if bus_stops_data is None:
        print("資料未正確載入，無法搜尋。")
        return

    exclude_cols = ['Route ID', 'Route Name', 'Direction']
    stop_cols = [col for col in bus_stops_data.columns if col not in exclude_cols]

    found = False
    for idx, row in bus_stops_data.iterrows():
        stops = [str(row[col]) for col in stop_cols if pd.notna(row[col])]
        if stop1 in stops and stop2 in stops:
            idx1 = stops.index(stop1)
            idx2 = stops.index(stop2)
            if idx1 < idx2:  # 起點在終點左邊
                print(f"Route ID: {row['RouteID']}, Route Name: {row['RouteName']}, Direction: {row['Direction']}")
                search_url(row['RouteID'], row['RouteName'], row['Direction'])
                found = True
    if not found:
        print("查無同時包含兩站且順序正確的路線。")

def search_url(route_id, route_name, direction):
    """
    根據 Route ID、Route Name、Direction 爬取對應路線的站名
    """
    url = f"https://ebus.gov.taipei/Route/StopsOfRoute?routeid={route_id}"
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        if direction == "Go":
            route_div = soup.find('div', id='GoDirectionRoute', class_='auto-list-pool-c stationlist-list-pool-c')
        else:
            route_div = soup.find('div', id='BackDirectionRoute', class_='auto-list-pool-c stationlist-list-pool-c')
        if route_div:
            stops = [station.get_text(strip=True) for station in route_div.find_all('span', class_='auto-list-stationlist-place')]
            print(f"{route_name} ({direction}) 站名：")
            
            get_station_time(route_id, A, direction)
        else:
            print(f"找不到 {route_name} ({direction}) 的站名資料。")
    else:
        print(f"無法連線到 {url}")

def get_station_time(route_id, station_name, direction="Go"):
    url = f"https://ebus.gov.taipei/Route/StopsOfRoute?routeid={route_id}"

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)

        # 對應方向的 HTML ID
        direction_id = "GoDirectionRoute" if direction == "Go" else "BackDirectionRoute"

        try:
            # 等待方向區塊載入
            page.wait_for_selector(f"#{direction_id}", timeout=5000, state="attached")
            
            # 有些方向預設是隱藏的，需手動顯示
            page.eval_on_selector(f"#{direction_id}", "e => e.style.display = 'block'")
            section = page.query_selector(f"#{direction_id}")

            if not section:
                print(f"❌ 無法找到方向 '{direction}' 的資料區塊。")
                return

            items = section.query_selector_all(".stationlist-list-pool-c > div")

            for item in items:
                place = item.query_selector(".auto-list-stationlist-place")
                time = item.query_selector(".auto-list-stationlist-position.auto-list-stationlist-position-time")
                
                if place and place.inner_text().strip() == station_name:
                    time_text = time.inner_text().strip() if time else "無時間資訊"
                    print(f"✅ {station_name} 進站時間：{time_text}")
                    return

            print(f"❌ 找不到站名「{station_name}」。")

        finally:
            browser.close()

A = input("請輸入起點車站名稱：")
B = input("請輸入終點車站名稱：")
search_bus_route(A, B)