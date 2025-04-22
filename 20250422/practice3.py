import os
import subprocess
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

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

def generate_png(matched_stops, output_dir, geojson_file):
    """
    將所有站點繪製成一個 PNG 圖檔，GeoJSON 中的站點用灰色標記，CSV 中的站點用紅色標記。
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 繪製所有站點的圖表
    print("Generating PNG file...")
    geojson_data = gpd.read_file(geojson_file)
    plt.figure(figsize=(10, 10))
    geojson_data.plot(color='gray', markersize=5, label='GeoJSON Stops')
    plt.axis('equal')
    plt.xlim(121.5, 121.6)
    plt.ylim(24.95, 25.2)
    plt.legend()
    


    # 繪製匹配的站點（紅色）
    for stop in matched_stops:
        name = stop['name']
        lng, lat = stop['coordinates']
        plt.scatter(lng, lat, color='red', label=f'CSV Stop: {name}')

    plt.title("Matched Bus Stops")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True)

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
    generate_png(matched_stops, OUTPUT_DIR, GEOJSON_FILE)

if __name__ == "__main__":
    main()