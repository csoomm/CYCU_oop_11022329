from playwright.sync_api import sync_playwright

# 定義檔案路徑
input_file_path = "file:///C:/Users/User/Desktop/CYCU_oop_11022329/20250401/P1/三安里.html"
output_file_path = "C:/Users/User/Desktop/CYCU_oop_11022329/20250401/P1/三安里_rendered.html"

# 使用 Playwright 渲染 HTML
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    # 載入 HTML 檔案
    page.goto(input_file_path)

    # 等待特定的 API 請求完成
    def handle_response(response):
        if "StopLocationDyna" in response.url and response.status == 200:
            print(f"API 請求完成: {response.url}")

    page.on("response", handle_response)

    # 等待一段時間以確保 JavaScript 完全執行
    page.wait_for_load_state("networkidle")

    # 取得完整的 HTML
    rendered_html = page.content()

    # 儲存渲染後的 HTML
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(rendered_html)

    print(f"渲染完成，輸出檔案位於: {output_file_path}")
    browser.close()
