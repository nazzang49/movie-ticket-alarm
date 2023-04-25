from datetime import *

now = datetime.now()

def get_week_no(y, m, d):
    input_date = datetime(y, m, d)
    firstday = input_date.replace(day=1)
    weekday = firstday.isoweekday() % 7

    if weekday == 0:
        first_sunday = firstday
    elif weekday < 7:
        first_sunday = firstday + timedelta(days=7 - weekday)
    else:
        raise ValueError("[OUT_OF_RANGE]")

    # +1 = consider <tr>
    return (input_date - first_sunday).days // 7 + 1

print(get_week_no(2023, 4, 29))
