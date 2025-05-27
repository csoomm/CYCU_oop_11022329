import geopandas as gpd

# 檔案路徑
file_path = r"C:/Users/User/Desktop/CYCU_oop_11022329/taipei_city_bus_route.gpkg"
output_excel_path = r"C:/Users/User/Desktop/CYCU_oop_11022329/taipei_city_bus_route.xlsx"

# 讀取 GeoPackage 檔案
try:
    gdf = gpd.read_file(file_path)
    print("成功讀取 GeoPackage 檔案！")
    print(gdf.head())  # 顯示前幾筆資料

    # 將資料輸出成 Excel
    gdf.to_excel(output_excel_path, index=False)
    print(f"成功輸出成 Excel 檔案：{output_excel_path}")
except Exception as e:
    print(f"讀取檔案或輸出時發生錯誤: {e}")