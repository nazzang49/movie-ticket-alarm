import requests
import time

from selenium import webdriver
from enum import *
from datetime import datetime, timedelta

class CrawlingType(Enum):
    """
    A enum class to be used setting several type-related values
    """
    SCROLL_PAUSE_SEC = 1

def scroll_down(driver: webdriver = None):
    if not driver:
        raise ValueError("[NOT_FOUND_WEBDRIVER]REQUIRED")

    # get scroll height
    latest_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # scroll to the end
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # pause
        time.sleep(CrawlingType.SCROLL_PAUSE_SEC.value)

        # scroll down & get scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == latest_height:
            break
        latest_height = new_height

def is_valid_dates(**kwargs):
    pass

def get_week_no(date: datetime):
    first_day_of_date = date.replace(day=1)

    if first_day_of_date.weekday() == 6:
        origin = first_day_of_date
    elif first_day_of_date.weekday() < 3:
        origin = first_day_of_date - timedelta(days=first_day_of_date.weekday() + 1)
    else:
        origin = first_day_of_date + timedelta(days=6-first_day_of_date.weekday())

    # +1 = consider <tr>
    return (date - origin).days // 7 + 1 + 1

def click_dates(**kwargs):
    if "start" not in kwargs or len(kwargs["start"]) != 3:
        raise KeyError("[NOT_FOUND_START]")

    if "end" not in kwargs or len(kwargs["end"]) != 3:
        raise KeyError("[NOT_FOUND_END]")

    if "driver" not in kwargs:
        raise KeyError("[NOT_FOUND_DRIVER]")

    start_month, start_week_no, start_day = kwargs["start"]
    end_month, end_week_no, end_day = kwargs["end"]

    # start
    kwargs["driver"].find_element_by_xpath(
        f"/html/body/div[1]/div/div[2]/div[2]/div[1]/div[2]/div/div[{start_month}]/table/tbody/tr[{start_week_no}]/td[{start_day}]/button"
    ).click()

    # end
    kwargs["driver"].find_element_by_xpath(
        f"/html/body/div[1]/div/div[2]/div[2]/div[1]/div[2]/div/div[{end_month}]/table/tbody/tr[{end_week_no}]/td[{end_day}]/button"
    ).click()

# (optional) hide chrome ui
# options = webdriver.ChromeOptions()
# options.add_argument("headless")

driver = webdriver.Chrome(
    executable_path='C:\movie-ticket-alarm\chromedriver.exe',
    # options=options
)
driver.get(
    url='https://flight.naver.com/flights/international/SEL-NRT-20230504/NRT-SEL-20230507?'
        'adult=2&isDirect=true&fareType=Y'
)

time.sleep(15)

driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div[3]/div/div[2]/div/button").click()
driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div[3]/div/div[2]/div/div/div[2]/div[2]/button[1]").click()

# frequent exceptions
# selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element:
try:
    start_year, start_month, start_day = input("input start date that you want (e.g. 2023-04-01) : ").split("-")
    end_year, end_month, end_day = input("input end date that you want (e.g. 2023-04-03) : ").split("-")

    start_date = datetime.strptime(f"{start_year}-{start_month}-{start_day}", "%Y-%m-%d")
    end_date = datetime.strptime(f"{end_year}-{end_month}-{end_day}", "%Y-%m-%d")
    today = datetime.now()

    print("==================== TODAY ====================")
    print(today)

    print("==================== START_DATE ====================")
    print(start_date)

    print("==================== END_DATE ====================")
    print(end_date)

    if start_date > end_date:
        raise ValueError(
            f"[INVALID_DATE] (caution) start_date::{start_date} is should not be later than end_date::{end_date}."
        )

    if start_date < today:
        raise ValueError(
            f"[INVALID_DATE] (caution) start_date::{start_date} is should not be earlier than today::{today}."
        )
except Exception as e:
    print("[FAIL_PARSE_DATE]")
    raise e

def map_dates(date: datetime, today: datetime):
    month = (date.month - today.month) + 2     # this_month = 2
    day = date.isoweekday() % 7                         # sunday = 1
    return month, day

try:
    # (!) preprocessing date
    start_week_no = get_week_no(start_date)
    end_week_no = get_week_no(end_date)

    start_month, start_day = map_dates(start_date, today)
    end_month, end_day = map_dates(end_date, today)

    click_dates(
        start=[start_month, start_week_no, start_day],
        end=[end_month, end_week_no, end_day],
        driver=driver
    )
except Exception as e:
    raise e

time.sleep(3)



# departure range
departure_time = ['전체', '00:00 ~ 06:00', '06:00 ~ 09:00', '09:00 ~ 12:00',
                  '12:00 ~ 15:00', '15:00 ~ 18:00', '18:00 ~ 24:00']

for i, d_time in enumerate(departure_time):
    print(f"{i + 1}. {d_time}", end='\t')

print()
timeInput = int(input("출발 시간을 선택하세요 : "))
print()






# departure
driver.find_element_by_xpath("/html/body/div/div/div[1]/div[2]/div[2]/div/div[2]/ul/li[2]/a/span[1]").click()
if timeInput == 1:
    driver.find_element_by_xpath("/html/body/div/div/div[1]/div[2]/div[2]"
                                 "/div/div[2]/ul/li[2]/div/ul/li[1]/span").click()

    # 시간항목이 전체일 경우 : 스크롤 다운 함수 실행
    scroll_down()

elif timeInput == 2:
    driver.find_element_by_xpath("/html/body/div/div/div[1]/div[2]/div[2]"
                                 "/div/div[2]/ul/li[2]/div/ul/li[2]/span").click()
elif timeInput == 3:
    driver.find_element_by_xpath("/html/body/div/div/div[1]/div[2]/div[2]"
                                 "/div/div[2]/ul/li[2]/div/ul/li[3]/span").click()
elif timeInput == 4:
    driver.find_element_by_xpath("/html/body/div/div/div[1]/div[2]/div[2]"
                                 "/div/div[2]/ul/li[2]/div/ul/li[4]/span").click()
elif timeInput == 5:
    driver.find_element_by_xpath("/html/body/div/div/div[1]/div[2]/div[2]"
                                 "/div/div[2]/ul/li[2]/div/ul/li[5]/span").click()
elif timeInput == 6:
    driver.find_element_by_xpath("/html/body/div/div/div[1]/div[2]/div[2]"
                                 "/div/div[2]/ul/li[2]/div/ul/li[6]/span").click()
elif timeInput == 7:
    driver.find_element_by_xpath("/html/body/div/div/div[1]/div[2]/div[2]"
                                 "/div/div[2]/ul/li[2]/div/ul/li[7]/span").click()





# driver.quit()


# /html/body/div[1]/div/div[2]/div[2]/div[1]/div[2]/div/div[5]/table/tbody/tr[5]/td[7]/button












