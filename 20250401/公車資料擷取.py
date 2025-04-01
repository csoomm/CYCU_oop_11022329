import time  # 確保正確導入 time 模組
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

def fetch_bus_data_with_selenium(url):
    """
    使用 Selenium 抓取公車站與到站時間的資料。
    返回一個字典，鍵為車站名稱，值為到站時間。
    """
    # 初始化 WebDriver
    service = Service(r'C:\Users\User\Desktop\1\cycu_oop_11022345\20250325\chromedriver-win64\chromedriver.exe')  # 確保 'chromedriver' 在 PATH 中
    driver = webdriver.Chrome(service=service)

    try:
        # 開啟目標網址
        print(f"正在嘗試打開網址：{url}")
        driver.get(url)
        print("成功打開網址，準備等待")

        # 抓取車站名稱
        station_elements = driver.find_elements(By.XPATH, '//a[contains(@href, "stop.jsp")]')
        stations = [station.text.strip() for station in station_elements]

        # 抓取到站時間
        time_elements = driver.find_elements(By.XPATH, '//td[starts-with(@id, "tte")]')
        times = [time.text.strip() for time in time_elements]

        # 建立車站與到站時間的對應字典
        bus_data = {}
        for station, time in zip(stations, times):
            bus_data[station] = time

        return bus_data
    finally:
        driver.quit()

def get_bus_arrival_time(bus_data, station_name):
    """
    根據車站名稱查詢到站時間。
    """
    return bus_data.get(station_name, "查無此車站資訊")

if __name__ == "__main__":
    # 指定目標網址
    url = "https://pda5284.gov.taipei/MQS/route.jsp?rid=10417"

    # 抓取公車資料
    bus_data = fetch_bus_data_with_selenium(url)

    # 讓使用者輸入車站名稱
    while True:
        station_name = input("請輸入車站名稱（輸入 'exit' 結束程式）：")
        if station_name.lower() == 'exit':
            print("程式結束。")
            break
        arrival_time = get_bus_arrival_time(bus_data, station_name)
        print(f"{station_name} 的到站時間為：{arrival_time}")