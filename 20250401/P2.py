from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import os

# 讀取目錄中的所有 HTML 檔案
directory_path = "C:\\Users\\User\\Desktop\\CYCU_oop_11022329\\20250401\\P1"
html_files = [f for f in os.listdir(directory_path) if f.endswith('.html')]

with sync_playwright() as p:
    # 啟動瀏覽器
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()

    for html_file in html_files:
        file_path = f"file:///{directory_path}/{html_file}"
        page = context.new_page()
        page.goto(file_path)

        # 等待 JavaScript 執行完成
        page.wait_for_timeout(3000)

        # 取得完整的 HTML
        html = page.content()

        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(html, 'html.parser')

        # 提取資料
        rows = soup.find_all('tr', class_='ttego1') + soup.find_all('tr', class_='ttego2')
        for row in rows:
            route = row.find('a').text  # 路線名稱
            if route == "忠孝幹線":  # 篩選路線為"忠孝幹線"
                stop = row.find_all('a')[1].text  # 站牌名稱
                direction = row.find_all('td')[2].text  # 去返程
                estimate = row.find_all('td')[3].text  # 預估到站
                print(f"路線: {route}, 站牌: {stop}, 去返程: {direction}, 預估到站: {estimate}")

    # 關閉瀏覽器
    browser.close()
