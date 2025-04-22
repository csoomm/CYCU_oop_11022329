import json
import os
import matplotlib.pyplot as plt
import re
import geopandas as gpd

# filepath: /C:/Users/User/Desktop/CYCU_oop_11022329/20250422/bus_stops.geojson
GEOJSON_FILE = "C:/Users/User/Desktop/CYCU_oop_11022329/20250422/bus_stops.geojson"
OUTPUT_DIR = "C:/Users/User/Desktop/CYCU_oop_11022329/20250422/output"


def parse_geojson(file_path):
    """
    使用 GeoDataFrame 解析 GeoJSON 檔案，提取站名和座標。
    """
    gdf = gpd.read_file(file_path)
    
    bus_stops = []
    for _, row in gdf.iterrows():
        name = row.get('BSM_CHINES', '未知站名')
        coordinates = row.geometry.coords[0] if row.geometry else []
        if coordinates:
            bus_stops.append({'name': name, 'coordinates': coordinates})
    return bus_stops


def sanitize_filename(name):
    """
    移除或替換檔案名稱中的無效字元。
    """
    return re.sub(r'[\/:*?"<>|]', '_', name)

def generate_png(bus_stops, output_dir):
    """
    將所有站點統整成一張圖片並儲存。
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 繪製所有站點的圖表
    plt.figure(figsize=(10, 10))
    for stop in bus_stops:
        name = stop['name']
        coordinates = stop['coordinates']
        lng, lat = coordinates
        plt.scatter(lng, lat, label=name)

    plt.title("All Bus Stops")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.legend(fontsize='small', loc='best')
    plt.grid(True)

    # 儲存圖檔
    output_path = os.path.join(output_dir, "all_bus_stops.png")
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Saved: {output_path}")

    #儲存HTML檔案
    html_output_path = os.path.join(output_dir, "all_bus_stops.html")
    with open(html_output_path, 'w', encoding='utf-8') as f:
        f.write("<html><body>")
        for stop in bus_stops:
            name = stop['name']
            coordinates = stop['coordinates']
            f.write(f"<p>{name}: {coordinates}</p>")
        f.write("</body></html>")
        

def main():
    """
    主程式：解析 GeoJSON 並生成 PNG 圖檔。
    """
    print("Parsing GeoJSON file...")
    bus_stops = parse_geojson(GEOJSON_FILE)
    print(f"Found {len(bus_stops)} bus stops.")

    print("Generating PNG files...")
    generate_png(bus_stops, OUTPUT_DIR)
    print("All PNG files have been generated.")

if __name__ == "__main__":
    main()