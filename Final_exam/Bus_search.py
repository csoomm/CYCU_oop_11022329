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
    processed = set()  # 新增集合避免重複
    for idx, row in bus_stops_data.iterrows():
        stops = [str(row[col]) for col in stop_cols if pd.notna(row[col])]
        if stop1 in stops and stop2 in stops:
            idx1 = stops.index(stop1)
            idx2 = stops.index(stop2)
            key = (row['RouteID'], row['Direction'])
            if idx1 < idx2 and key not in processed:  # 起點在終點左邊且未處理過
                print("---------------------------------")
                print(f"Route ID: {row['RouteID']}, Route Name: {row['RouteName']}, Direction: {row['Direction']}")
                search_url(row['RouteID'], row['RouteName'], row['Direction'], stop1, stop2)
                found = True
                processed.add(key)
    if not found:
        print("查無同時包含兩站且順序正確的路線。")

def search_url(route_id, route_name, direction, A, B):
    """
    根據 Route ID、Route Name、Direction 使用 Playwright 渲染後下載 HTML，並解析對應路線的站名及抵達時間
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        url = f"https://ebus.gov.taipei/Route/StopsOfRoute?routeid={route_id}"
        page.goto(url)

        try:
            # 根據 direction 點擊按鈕
            if direction == "Go":
                go_button_selector = ".stationlist-go.stationlist-come-go"
                page.wait_for_selector(go_button_selector, timeout=10000)  # 等待最多 10 秒
                page.click(go_button_selector)
                page.wait_for_timeout(3000)  # 等待按鈕點擊後的渲染完成
            elif direction == "Back":
                back_button_selector = ".stationlist-come.stationlist-come-go-gray"
                page.wait_for_selector(back_button_selector, timeout=10000)  # 等待最多 10 秒
                page.click(back_button_selector)
                page.wait_for_timeout(3000)  # 等待按鈕點擊後的渲染完成

            # 下載 HTML 儲存在當前目錄
            html_content = page.content()
            html_file_path = f"{route_id}_route.html"
            with open(html_file_path, 'w', encoding='utf-8') as file:
                file.write(html_content)
            print(f"已下載 {route_name} ({direction}) 的 HTML 到 {html_file_path}")
            arrival_time(route_id, A, direction, B)
        except Exception as e:
            print(f"發生例外狀況: {type(e).__name__}, {e}")
        #讀取下載的 HTML 檔案，找尋對應站名及抵達時間
        finally:
            context.close()
            browser.close()

def arrival_time(route_id, A, direction, B):
    """
    根據 route_id 和 direction 讀取 HTML 檔案，尋找站名 A 的抵達時間
    """
    html_file_path = f"{route_id}_route.html"
    
    # 檢查檔案是否存在
    if not os.path.exists(html_file_path):
        print(f"HTML 檔案 {html_file_path} 不存在，請確認檔案是否已下載。")
        return

    # 讀取 HTML 檔案
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # 根據 direction 選擇對應的路徑
    if direction == "Go":
        route_div = soup.find('div', id="GoDirectionRoute")
    elif direction == "Back":
        route_div = soup.find('div', id="BackDirectionRoute")
    else:
        print(f"無效的方向: {direction}")
        return

    # 確認路徑是否存在
    if not route_div:
        print(f"未找到方向 {direction} 的路徑，請確認 HTML 結構。")
        return

    # 在路徑下尋找站名 A
    stop_elements = route_div.find_all('span', class_='auto-list-stationlist-place')
    for stop in stop_elements:
        if stop.text.strip() == A:
            # 找到站名後，尋找其父元素中的抵達時間
            parent_div = stop.find_parent('span', class_='auto-list-stationlist')
            if parent_div:
                arrival_time_element = parent_div.find('span', class_='auto-list-stationlist-position-time')
                no_service_element = parent_div.find('span', class_='auto-list-stationlist-position auto-list-stationlist-position-none')
                last_bus_element = parent_div.find('span', class_='auto-list-stationlist-position auto-list-stationlist-position-last')

                if no_service_element and no_service_element.text.strip() == "今日未營運":
                    print(f"{A} ({direction}) 今天未營運。")
                    break
                
                if no_service_element and no_service_element.text.strip() == "末班已過":
                    print(f"{A} ({direction}) 該車末班已過。")
                    break
                
                # 處理進站中
                in_station_element = parent_div.find('span', class_='auto-list-stationlist-position auto-list-stationlist-position-now')
                if in_station_element and in_station_element.text.strip() == "進站中":
                    print(f"{A} ({direction}) 進站中。")
                    calculate_time(route_id, A, direction, B)
                    return
                
                if arrival_time_element:
                    arrival_time = arrival_time_element.text.strip()
                    print(f"{A} ({direction}) 的抵達時間為: {arrival_time}")
                    calculate_time(route_id, A, direction, B)
                    return
            print(f"未找到 {A} 的抵達時間。")
            return

    print(f"未找到站名 {A} ({direction})。")

def calculate_time(route_id, A, direction, B):
    """
    根據 route_id 和 direction 讀取 HTML 檔案，將車站名稱 A 後、車站名稱 B 之前的所有車站抵達時間合併成列表輸出
    """
    html_file_path = f"{route_id}_route.html"
    
    # 檢查檔案是否存在
    if not os.path.exists(html_file_path):
        print(f"HTML 檔案 {html_file_path} 不存在，請確認檔案是否已下載。")
        return

    # 讀取 HTML 檔案
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # 根據 direction 選擇對應的路徑
    if direction == "Go":
        route_div = soup.find('div', id="GoDirectionRoute")
    elif direction == "Back":
        route_div = soup.find('div', id="BackDirectionRoute")
    else:
        print(f"無效的方向: {direction}")
        return

    # 確認路徑是否存在
    if not route_div:
        print(f"未找到方向 {direction} 的路徑，請確認 HTML 結構。")
        return

    # 在路徑下尋找所有車站
    stop_elements = route_div.find_all('span', class_='auto-list-stationlist-place')
    stop_times = route_div.find_all('span', class_='auto-list-stationlist-position')

    # 建立車站與抵達時間的對應
    stop_times_list = [time.text.strip() for time in stop_times]

    # 找出 A 和 B 車站的索引
    stop_names = [stop.text.strip() for stop in stop_elements]
    if A in stop_names and B in stop_names:
        idx_A = stop_names.index(A)
        idx_B = stop_names.index(B)
        if idx_A < idx_B:
            # 取 A 和 B 車站之間及包含 B 車站的進站時間
            times_between = stop_times_list[idx_A + 1:idx_B + 1]
            print(f"{A} 到 {B} 之間及包含 {B} 的進站時間: {times_between}")

            # 依序讀取 time_between，遇到 "進站中" 則將前一個資料加入新列表
            combined_times = []
            prev_time = None  # 新增變數記錄上一個資料
            for i, time in enumerate(times_between):
                if time == "進站中":
                    if i > 0 and times_between[i - 1] != "進站中":
                        combined_times.append(times_between[i - 1])
                prev_time = time
            # 最後一個資料若不是 "進站中"，也加入新列表
            if times_between and times_between[-1] != "進站中":
                # 將每個資料的最後兩個文字刪除，並轉為數字
                cleaned_times = []
                for t in combined_times + [times_between[-1]]:
                    # 移除最後兩個字元，並嘗試轉為整數
                    num_str = t[:-2]
                    try:
                        num = int(num_str)
                        cleaned_times.append(num)
                    except ValueError:
                        continue
                total_time = sum(cleaned_times)
                print(f"預計抵達時間總和: {total_time} 分鐘")
            else:
                cleaned_times = []
                for t in combined_times:
                    # 移除最後兩個字元，並嘗試轉為整數
                    num_str = t[:-2]
                    try:
                        num = int(num_str)
                        cleaned_times.append(num)
                    except ValueError:
                        continue
                total_time = sum(cleaned_times)
                print(f"預計抵達時間總和: {total_time} 分鐘")
                combined_times = cleaned_times
            return combined_times
        else:
            print(f"{A} 在 {B} 之後，無法計算進站時間。")
    else:
        print(f"未找到 {A} 或 {B} 車站。")
    



# 主程式
A = input("請輸入起點車站名稱：")
B = input("請輸入終點車站名稱：")
search_bus_route(A, B)