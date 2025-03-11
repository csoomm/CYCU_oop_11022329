import datetime
import lunardate

def get_zodiac(year):
    zodiacs = ["鼠", "牛", "虎", "兔", "龍", "蛇", "馬", "羊", "猴", "雞", "狗", "豬"]
    return zodiacs[(year - 4) % 12]

def main():
    # 輸入西元年、月、日
    year = int(input("請輸入西元年: "))
    month = int(input("請輸入月: "))
    day = int(input("請輸入日: "))

    # 計算農曆日期
    solar_date = datetime.date(year, month, day)
    lunar_date = lunardate.LunarDate.fromSolarDate(year, month, day)

    # 獲取生肖
    zodiac = get_zodiac(lunar_date.year)

    # 獲取星期幾
    week_day = solar_date.strftime("%A")

    # 輸出結果
    print(f"西元日期: {solar_date}")
    print(f"農曆日期: {lunar_date.year}年{lunar_date.month}月{lunar_date.day}日")
    print(f"生肖: {zodiac}")
    print(f"星期: {week_day}")

if __name__ == "__main__":
    main()