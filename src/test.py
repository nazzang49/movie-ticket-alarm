from datetime import *

now = datetime.now()

def get_week_no(y, m, d):
    input_date = datetime(y, m, d)
    firstday = input_date.replace(day=1)
    weekday = firstday.isoweekday() % 7

    # 1일 = 일
    if weekday == 0:
        first_sunday = firstday
    # 1일 = 월 ~ 수
    elif weekday < 4:
        first_sunday = firstday - timedelta(days=weekday + 1)
    # 1일 = 목 ~ 토
    else:
        first_sunday = firstday + timedelta(days=6 - weekday)

    # +1 = consider <tr>
    return (input_date - first_sunday).days // 7 + 1

print(get_week_no(2023, 5, 1))
# print(now.isoweekday() % 7)
# print(datetime.strptime(f"2023-04-01", "%Y-%m-%d"))
