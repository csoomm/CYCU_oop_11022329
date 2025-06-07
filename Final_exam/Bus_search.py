import pandas as pd
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import os
from playwright.sync_api import sync_playwright
#---------------------------------------------------------------------------------------------------------------------------------                                             
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
#--------------------------------------------------------------------------------------------------------------------------------
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
        change_route(stop1, stop2)
        
#--------------------------------------------------------------------------------------------------------------------------------
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
#--------------------------------------------------------------------------------------------------------------------------------
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
                    return

                # 處理末班已過
                last_bus_over_element = parent_div.find('span', class_='auto-list-stationlist-position auto-list-stationlist-position-none')
                if last_bus_over_element and last_bus_over_element.text.strip() == "末班已過":
                    print(f"{A} ({direction}) 該車末班已過。")
                    return

                # 處理進站中
                in_station_element = parent_div.find('span', class_='auto-list-stationlist-position auto-list-stationlist-position-now')
                if in_station_element:
                    text = in_station_element.text.strip()
                    if text == "進站中":
                        print(f"{A} ({direction}) 進站中。")
                        calculate_time(route_id, A, direction, B)
                        return
                    elif text.startswith("預計") and "發車" in text:
                        print(f"{A} ({direction}) {text}")
                        return

                if arrival_time_element:
                    arrival_time = arrival_time_element.text.strip()
                    print(f"{A} ({direction}) 的抵達時間為: {arrival_time}")
                    calculate_time(route_id, A, direction, B)
                    return
            print(f"未找到 {A} 的抵達時間。")
            return

    print(f"未找到站名 {A} ({direction})。")
#--------------------------------------------------------------------------------------------------------------------------------
def calculate_time(route_id, A, direction, B):
    """
    根據 route_id 和 direction 讀取 HTML 檔案，將車站名稱 A 後、車站名稱 B 之前的所有車站抵達時間合併成列表輸出，
    並取得這些車站的經緯度，傳給 create_map()
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

            # 將time_between中每個資料最後兩個字元去除
            cleaned_times = [time[:-2] for time in times_between]
            #將資料改成數字格式，如果是"進"則為0
            combined_times = []
            for time in cleaned_times:
                if time == "進":
                    combined_times.append(0)
                else:
                    try:
                        combined_times.append(int(time))
                    except ValueError:
                        print(f"無法將時間 '{time}' 轉換為數字格式。")
            #依序檢查列表combined_times中的數字，若前一筆數字大於後一筆數字，則將前一筆資料放入新列表total_times
            total_times = []
            for i in range(len(combined_times) - 1):
                if combined_times[i] > combined_times[i + 1]:
                    total_times.append(combined_times[i])
            # 將最後一筆資料也放入 total_times
            if combined_times:
                total_times.append(combined_times[-1])
            #輸出total_times的總和
            print(f"預計抵達時間: {sum(total_times)}分鐘")

            # 取得A到B之間所有車站的經緯度
            # 取得對應的車站span元素
            # stops_between 需包含 stopA 與 stopB
            stops_between = stop_elements[idx_A:idx_B + 1]
            latlng_list = []
            for stop in stops_between:
                parent = stop.find_parent('span', class_='auto-list-stationlist')
                if parent:
                    lat_input = parent.find('input', {'name': 'item.Latitude'})
                    lng_input = parent.find('input', {'name': 'item.Longitude'})
                    if lat_input and lng_input:
                        try:
                            lat = float(lat_input.get('value', ''))
                            lng = float(lng_input.get('value', ''))
                            latlng_list.append((lat, lng))
                        except ValueError:
                            continue
            print(f"車站 {A} 到 {B}（含）之間的經緯度列表: {latlng_list}")
            create_map(latlng_list)
            return combined_times
        else:
            print(f"{A} 在 {B} 之後，無法計算進站時間。")
    else:
        print(f"未找到 {A} 或 {B} 車站。")
#--------------------------------------------------------------------------------------------------------------------------------
def change_route(stop1, stop2):
    """
    搜尋無法直達時，找出擁有 stop1 的路線與擁有 stop2 的路線，並找出兩者的共同車站（轉乘站）。
    共同車站需滿足：routeA上stop1在stop3前，routeB上stop3在stop2前。
    輸出格式：route:277(Back)<->280(Back):中轉站「士林,捷運芝山站一,...」
    """
    if bus_stops_data is None:
        print("資料未正確載入，無法搜尋。")
        return

    exclude_cols = ['Route ID', 'Route Name', 'Direction']
    stop_cols = [col for col in bus_stops_data.columns if col not in exclude_cols]

    # 找出擁有 stop1 的所有路線
    routes_with_stop1 = {}
    for idx, row in bus_stops_data.iterrows():
        stops = [str(row[col]) for col in stop_cols if pd.notna(row[col])]
        if stop1 in stops:
            route_id = row['RouteID']
            routes_with_stop1[(route_id, row['RouteName'], row['Direction'])] = stops

    # 找出擁有 stop2 的所有路線
    routes_with_stop2 = {}
    for idx, row in bus_stops_data.iterrows():
        stops = [str(row[col]) for col in stop_cols if pd.notna(row[col])]
        if stop2 in stops:
            route_id = row['RouteID']
            routes_with_stop2[(route_id, row['RouteName'], row['Direction'])] = stops

    found = False
    # key: (routeA_name, routeA_dir, routeB_name, routeB_dir) -> set(中轉站)
    transfer_dict = {}

    for (routeA_id, routeA_name, routeA_dir), stopsA in routes_with_stop1.items():
        for (routeB_id, routeB_name, routeB_dir), stopsB in routes_with_stop2.items():
            common_stops = set(stopsA) & set(stopsB)
            common_stops.discard(stop1)
            common_stops.discard(stop2)
            valid_stops = []
            for stop3 in common_stops:
                try:
                    idx1 = stopsA.index(stop1)
                    idx3_A = stopsA.index(stop3)
                    idx3_B = stopsB.index(stop3)
                    idx2 = stopsB.index(stop2)
                    if idx1 < idx3_A and idx3_B < idx2:
                        valid_stops.append(stop3)
                        found = True
                except ValueError:
                    continue
            if valid_stops:
                key = (routeA_name, routeA_dir, routeB_name, routeB_dir)
                if key not in transfer_dict:
                    transfer_dict[key] = set()
                transfer_dict[key].update(valid_stops)

    # 合併輸出
    for (routeA_name, routeA_dir, routeB_name, routeB_dir), stops in transfer_dict.items():
        if stops:
            stops_str = "、".join(sorted(stops, key=lambda x: list(routes_with_stop1.values())[0].index(x) if x in list(routes_with_stop1.values())[0] else 0))
            print(f"route:{routeA_name}({routeA_dir})<->{routeB_name}({routeB_dir}):中轉站「{stops_str}」")
    if not found:
        print(f"{stop1} 和 {stop2} 之間沒有符合條件的轉乘站。")
#--------------------------------------------------------------------------------------------------------------------------------
import geopandas as gpd
import folium

def create_map(latlng_list):
    # 讀取 Shapefile 檔案
    data_path = r'C:\Users\31002\OneDrive\桌面\CYCU_oop_11022329\Final_exam\OFiles_9e222fea-bafb-4436-9b17-10921abc6ef2\TOWN_MOI_1140318.shp'
    geo_data = gpd.read_file(data_path)

    # 只留下指定縣市
    geo_data = geo_data[geo_data['COUNTYNAME'].isin(['臺北市', '新北市', '桃園市', '基隆市'])]

    # 計算地圖中心
    center = geo_data.geometry.centroid.unary_union.centroid
    m = folium.Map(location=[center.y, center.x], zoom_start=10)

    # 加入 GeoJson 圖層
    folium.GeoJson(
        geo_data,
        name="北北基桃行政區",
        tooltip=folium.GeoJsonTooltip(fields=["COUNTYNAME", "TOWNNAME"], aliases=["縣市", "鄉鎮"])
    ).add_to(m)

    # 讓使用者輸入起點與終點的圖片路徑
    start_img =  r"C:\Users\31002\OneDrive\桌面\CYCU_oop_11022329\Final_exam\image.png"
    end_img = r"C:\Users\31002\OneDrive\桌面\CYCU_oop_11022329\Final_exam\圖片1.png"

    # 加入紅色圓點
    for i, (lat, lng) in enumerate(latlng_list):
        folium.CircleMarker(
            location=[lat, lng],
            radius=5,
            color='red',
            fill=True,
            fill_color='red',
            fill_opacity=0.8
        ).add_to(m)

    # 起點加圖片
    if latlng_list:
        folium.Marker(
            location=latlng_list[0],
            icon=folium.CustomIcon(start_img, icon_size=(40, 40)),
            tooltip="起點"
        ).add_to(m)
    # 終點加圖片
    if len(latlng_list) > 1:
        folium.Marker(
            location=latlng_list[-1],
            icon=folium.CustomIcon(end_img, icon_size=(40, 40)),
            tooltip="終點"
        ).add_to(m)

    # 用紅線連起所有點
    if len(latlng_list) >= 2:
        folium.PolyLine(
            locations=latlng_list,
            color='red',
            weight=3,
            opacity=0.8
        ).add_to(m)

    # 儲存並開啟網頁
    m.save('north_tw_map.html')

    import webbrowser
    webbrowser.open('north_tw_map.html')


# 主程式
A = input("請輸入起點車站名稱：")
B = input("請輸入終點車站名稱：")
search_bus_route(A, B)