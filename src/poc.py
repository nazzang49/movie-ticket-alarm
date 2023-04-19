import requests
import time

from selenium import webdriver
from enum import *
from datetime import datetime

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

month = input("type month {start|end} (2=this_month)")
week = input("type week {start|end} (1=week_1, 2=week_2, 3=week_3, 4=week_4, 5=week_5)")
day = input("type day {start|end} (1=sunday, 2=monday, 3=tuesday, 4=wednesday, 5=thursday, 6=friday, 7=saturday)")

# frequent exceptions
# selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element:
try:
    start_month, end_month = map(int, month.split("|"))
    start_week, end_week = map(int, week.split("|"))
    start_day, end_day = map(int, day.split("|"))

    if start_month > end_month:
        raise ValueError("[INVALID_DATE] (caution) start_month is should not be later than end_month.")

    if start_week > end_week:
        raise ValueError("[INVALID_DATE] (caution) start_week is should not be later than end_week.")

    if start_week == end_week and start_day > end_day:
        raise ValueError("[INVALID_DATE] (caution) start_week is should not be later than end_week.")

except Exception as e:
    print("[FAIL_PARSE_DATE]")
    raise e


# start
driver.find_element_by_xpath(f"/html/body/div[1]/div/div[2]/div[2]/div[1]/div[2]/div/div[{start_month}]/table/tbody/tr[{start_week}]/td[{start_day}]/button")

# end
driver.find_element_by_xpath(f"/html/body/div[1]/div/div[2]/div[2]/div[1]/div[2]/div/div[{end_month}]/table/tbody/tr[{end_week}]/td[{end_day}]/button")

# driver.quit()












