import geopandas as gpd

# 讀取 Shapefile 檔案
data_path = r'C:\Users\User\Desktop\CYCU_oop_11022329\20250520\OFiles_9e222fea-bafb-4436-9b17-10921abc6ef2\TOWN_MOI_1140318.shp'
geo_data = gpd.read_file(data_path)

# 檢查資料欄位
print("資料欄位名稱：", geo_data.columns)

# 只留下COUNTYNAME為「台北市」「新北市」「桃園市」「基隆市」的資料
geo_data = geo_data[geo_data['COUNTYNAME'].isin(['臺北市', '新北市', '桃園市', '基隆市'])]

# 製作地圖
import matplotlib.pyplot as plt
import geopandas as gpd
# 設定地圖大小
fig, ax = plt.subplots(figsize=(10, 10))
# 畫出地圖
geo_data.boundary.plot(ax=ax, linewidth=1, color='blue')  # 將顏色改為藍色
# 設定地圖標題
ax.set_title('map', fontsize=20)
# 設定地圖坐標軸
ax.set_xlabel('經度', fontsize=15)
ax.set_ylabel('緯度', fontsize=15)


url = 'https://ebus.gov.taipei/Route/StopsOfRoute?routeid=0161000900'
import requests
from bs4 import BeautifulSoup
import matplotlib
matplotlib.rc('font', family='Microsoft JhengHei')
# 取得網頁內容
response = requests.get(url)
# 解析網頁內容
soup = BeautifulSoup(response.content, 'html.parser')
#找到帶有<div id="GoDirectionRoute" class="auto-list-pool-c stationlist-list-pool-c" >的資料，讀出每個<span class="auto-list-stationlist-place"後的名字
station_list = []
for div in soup.find_all('div', id='GoDirectionRoute'):
    for span in div.find_all('span', class_='auto-list-stationlist-place'):
        station_list.append(span.text.strip())
# 顯示車站名稱
print("車站名稱：")
for station in station_list:
    print(station)
#找到url中每個車站的經緯度，範例<input data-val="true" data-val-number="欄位 Latitude 必須是數字。" data-val-required="Latitude 欄位是必要項。" id="item_Latitude" name="item.Latitude" type="hidden" value="25.14506" /> <input data-val="true" data-val-number="欄位 Longitude 必須是數字。" data-val-required="Longitude 欄位是必要項。" id="item_Longitude" name="item.Longitude" type="hidden" value="121.49262" />
latitude_list = []
longitude_list = []
for div in soup.find_all('div', id='GoDirectionRoute'):
    for input_tag in div.find_all('input'):
        if input_tag.get('id') == 'item_Latitude':
            latitude_list.append(input_tag.get('value'))
        elif input_tag.get('id') == 'item_Longitude':
            longitude_list.append(input_tag.get('value'))

# 顯示經緯度
print("經緯度：")
for i in range(len(latitude_list)):
    print(f"車站：{station_list[i]}，經度：{longitude_list[i]}，緯度：{latitude_list[i]}")


# 設定地圖大小
fig, ax = plt.subplots(figsize=(10, 10))
# 畫出地圖
geo_data.boundary.plot(ax=ax, linewidth=1, color='blue')  # 將顏色改為藍色
# 設定地圖標題
ax.set_title('map_承德幹線', fontsize=20)
# 設定地圖坐標軸
ax.set_xlabel('經度', fontsize=15)
ax.set_ylabel('緯度', fontsize=15)
# 將經緯度以紅點顯示並標註車站名稱，並用紅線依照順序將點連起來
# 將經緯度轉換為浮點數並存入列表
coordinates = [(float(longitude_list[i]), float(latitude_list[i])) for i in range(len(latitude_list))]

# 繪製紅點並用紅線連接
for lon, lat in coordinates:
    ax.plot(lon, lat, 'ro', markersize=5)  # 用紅點標記經緯度

# 解壓縮經緯度列表，分別繪製紅線
lons, lats = zip(*coordinates)
ax.plot(lons, lats, 'g-', linewidth=1)  # 用紅線連接點
    


# 顯示地圖
plt.show()

