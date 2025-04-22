from datetime import datetime
#https://ebus.gov.taipei/thb/StopsOfRoute?nameZh=1818%E8%87%BA%E5%8C%97%E2%86%92%E4%B8%AD%E5%A3%A2

def calculate_julian_date(input_time_str):
    # 將輸入的時間字串轉換為 datetime 物件
    input_time = datetime.strptime(input_time_str, "%Y-%m-%d %H:%M")

    # 計算該天是星期幾
    weekday = input_time.strftime("%A")  # 星期幾（英文）

    # 計算輸入時間的 Julian 日期
    year = input_time.year
    month = input_time.month
    day = input_time.day + (input_time.hour / 24) + (input_time.minute / 1440)

    # Julian Day 計算公式
    if month <= 2:
        year -= 1
        month += 12

    A = year // 100
    B = 2 - A + (A // 4)
    julian_date = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + B - 1524.5

    # 計算輸入時間至現在的經過天數（以 Julian 日期表示）
    now = datetime.now()
    now_year = now.year
    now_month = now.month
    now_day = now.day + (now.hour / 24) + (now.minute / 1440)

    if now_month <= 2:
        now_year -= 1
        now_month += 12

    A_now = now_year // 100
    B_now = 2 - A_now + (A_now // 4)
    now_julian_date = int(365.25 * (now_year + 4716)) + int(30.6001 * (now_month + 1)) + now_day + B_now - 1524.5

    days_elapsed = now_julian_date - julian_date

    return weekday, julian_date, days_elapsed

def day_of_year(input_time_str):
    # 將輸入的時間字串轉換為 datetime 物件
    input_time = datetime.strptime(input_time_str, "%Y-%m-%d %H:%M")
    
    # 計算該天是當年的第幾天
    day_of_year_result = input_time.timetuple().tm_yday
    
    return day_of_year_result


# 測試函數
if __name__ == "__main__":
    input_time_str = input("請輸入時間 (格式為 YYYY-MM-DD HH:MM，例如 2020-04-15 20:30)：")
    try:
        weekday, julian_date, days_elapsed = calculate_julian_date(input_time_str)
        print(f"該天是星期：{weekday}")
        print(f"該時刻至今經過的太陽日數：{days_elapsed:.6f}")
        day_of_year_result = day_of_year(input_time_str)
        print(f"該天是當年的第 {day_of_year_result} 天")
    except ValueError:
        print("輸入的時間格式不正確，請使用 YYYY-MM-DD HH:MM 格式！")