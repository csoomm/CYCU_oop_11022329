import os
import subprocess
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rc('font', family='Microsoft JhengHei')

# 檔案路徑
EXAM3_SCRIPT = "C:/Users/User/Desktop/CYCU_oop_11022329/20250422/exam3.py"
CSV_FILE = "C:/Users/User/Desktop/CYCU_oop_11022329/20250422/output/go_bus_info.csv"
GEOJSON_FILE = "C:/Users/User/Desktop/CYCU_oop_11022329/20250422/bus_stops.geojson"
OUTPUT_DIR = "C:/Users/User/Desktop/CYCU_oop_11022329/20250422/output"

def run_exam3():
    """
    執行 exam3.py，生成 CSV 檔案。
    """
    print("Running exam3.py...")
    subprocess.run(["python", EXAM3_SCRIPT], check=True)
    print(f"CSV file generated: {CSV_FILE}")

def read_csv_and_geojson(csv_file, geojson_file):
    """
    讀取 CSV 和 GeoJSON 檔案。
    """
    print("Reading CSV and GeoJSON files...")
    csv_data = pd.read_csv(csv_file)
    geojson_data = gpd.read_file(geojson_file)
    return csv_data, geojson_data

def List_station(csv_data):
    station_list = []
    for index, row in csv_data.iterrows():
        station_name = row['車站站名']
        longitude = row['longitude']
        latitude = row['latitude']
        time = row['公車到達時間']
        station_list.append(f'{station_name},{longitude},{latitude},{time}')
    print("List of all bus stops:\n" + "\n".join(station_list))
    return station_list
    

def select_station(csv_data, station_list):
    """
    選取車站，並回傳選取的車站名稱。
    """
    print("Available bus stops:")
    for index, station in enumerate(station_list):
        print(f"{index + 1}: {station}")
    
    # 讓使用者選擇車站
    while True:
        try:
            choice = int(input("請輸入車站編號："))
            if 1 <= choice <= len(station_list):
                selected_station = station_list[choice - 1]
                print(f"Selected bus stop: {selected_station}")
                return selected_station
            else:
                print("無效的選擇，請重新輸入。")
        except ValueError:
            print("請輸入有效的數字。")

def match_stops(csv_data, geojson_data):
    """
    比對 CSV 和 GeoJSON 的經緯度（到小數點後三位）。
    """
    print("Matching stops based on coordinates...")
    matched_stops = []

    for _, csv_row in csv_data.iterrows():
        csv_name = csv_row['車站站名']
        csv_lng = round(csv_row['longitude'], 3)
        csv_lat = round(csv_row['latitude'], 3)

        for _, geojson_row in geojson_data.iterrows():
            geojson_name = geojson_row.get('BSM_CHINES', '未知站名')
            if geojson_row.geometry:
                geojson_lng, geojson_lat = map(lambda x: round(x, 3), geojson_row.geometry.coords[0])
                if csv_lng == geojson_lng and csv_lat == geojson_lat:
                    matched_stops.append({'name': csv_name, 'coordinates': (csv_lng, csv_lat)})
                    break

    print(f"Matched {len(matched_stops)} stops.")
    return matched_stops

def generate_png(matched_stops, output_dir, geojson_file, selected_station, csv_data):
    """
    將所有站點繪製成一個 PNG 圖檔，GeoJSON 中的站點用灰色標記，CSV 中的站點用紅色標記。
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 繪製所有站點的圖表
    print("Generating PNG file...")
    geojson_data = gpd.read_file(geojson_file)
    plt.figure(figsize=(10, 10))
    geojson_data.plot(color='gray', markersize=1, label='GeoJSON Stops')
    plt.axis('equal')
    plt.xlim(121.45, 121.7)
    plt.ylim(24.95, 25.2)
    plt.legend()
    
    # 繪製匹配的站點（紅色）並依照順序連接
    lngs, lats = [], []
    for stop in matched_stops:
        name = stop['name']
        lng, lat = stop['coordinates']
        lngs.append(lng)
        lats.append(lat)
        plt.scatter(lng, lat, color='red', s=5, label=f'CSV Stop: {name}')  # s=10 調整紅點大小

    # 連接紅點
    if len(lngs) > 1:
        plt.plot(lngs, lats, color='red', linewidth=1, linestyle='-', label='Route')

    plt.title("Matched Bus Stops")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True)

    # 繪製選取的車站，並將圖片往右上方偏移
    selected_name, selected_lng, selected_lat, time = selected_station.split(',')
    selected_lng, selected_lat = float(selected_lng), float(selected_lat)
    img1 = plt.imread("C:/Users/User/Desktop/CYCU_oop_11022329/20250422/onepiece11_arlong.png")
    offset_lng = 0.001  # 向右偏移量
    offset_lat = 0.011  # 向上偏移量
    plt.imshow(img1, extent=(selected_lng - 0.003 + offset_lng, selected_lng + 0.003 + offset_lng, 
                             selected_lat - 0.01 + offset_lat, selected_lat + 0.01 + offset_lat), 
               aspect='auto', zorder=20)
    
    plt.legend


    # 過濾"進站中"的資料
    df_filtered = csv_data[csv_data['公車到達時間'] == '進站中']
    # 獲取"進站中"的車站名稱
    in_station_stops = df_filtered['車站站名'].tolist()
    # 繪製"進站中"的車站
    img2 = plt.imread("C:/Users/User/Desktop/CYCU_oop_11022329/20250422/bus.jpg")
    for stop in matched_stops:
        name = stop['name']
        lng, lat = stop['coordinates']
        if name in in_station_stops:
            offset_lng = 0.001  # 向右偏移量
            plt.imshow(img2, extent=(lng - 0.001+offset_lng, lng + 0.001+offset_lng, lat - 0.003, lat + 0.003), aspect='auto', zorder=10)

    # 過濾"分鐘"的資料並顯示數字
    df_minutes = csv_data[csv_data['公車到達時間'].str.contains('分鐘', na=False)]
    for _, row in df_minutes.iterrows():
        station_name = row['車站站名']
        lng = row['longitude']
        lat = row['latitude']
        time = row['公車到達時間']
        plt.text(lng - 0.001, lat, time, color='black', fontsize=4, ha='center', va='center', zorder=15)
    
            
    
    # 儲存圖檔
    output_path = os.path.join(output_dir, "matched_bus_stops.png")
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Saved: {output_path}")

def main():
    """
    主程式：執行 exam3.py，讀取資料，比對站點，並生成 PNG 圖檔。
    """
    # 執行 exam3.py
    run_exam3()

    # 讀取 CSV 和 GeoJSON
    csv_data, geojson_data = read_csv_and_geojson(CSV_FILE, GEOJSON_FILE)

    # 比對站點
    matched_stops = match_stops(csv_data, geojson_data)

    # 生成 PNG 圖檔
    station_list = List_station(csv_data)
    selected_station=select_station(csv_data, station_list)
    generate_png(matched_stops, OUTPUT_DIR, GEOJSON_FILE, selected_station,  csv_data)

    

if __name__ == "__main__":
    main()