from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import re
from selenium.webdriver.support.ui import Select

class FlatpickrRangePicker:

    # ✅ ALWAYS TARGET OPEN CALENDAR ONLY
    CALENDAR = (By.XPATH, "//div[contains(@class,'flatpickr-calendar') and contains(@class,'open')]")

    MONTH_HEADER = (
        By.XPATH,
        "//div[contains(@class,'flatpickr-calendar') and contains(@class,'open')]//div[contains(@class,'flatpickr-current-month')]"
    )

    NEXT_BTN = (
        By.XPATH,
        "//div[contains(@class,'flatpickr-calendar') and contains(@class,'open')]//span[contains(@class,'flatpickr-next-month')]"
    )

    PREV_BTN = (
        By.XPATH,
        "//div[contains(@class,'flatpickr-calendar') and contains(@class,'open')]//span[contains(@class,'flatpickr-prev-month')]"
    )

    DAY = "//div[contains(@class,'flatpickr-calendar') and contains(@class,'open')]//span[contains(@class,'flatpickr-day') and not(contains(@class,'disabled')) and normalize-space()='{}']"

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # =============================
    # OPEN CALENDAR
    # =============================
    def open_calendar(self):
        self.wait.until(
            EC.visibility_of_element_located(self.CALENDAR)
        )
        time.sleep(0.5)  # allow animation

    # =============================
    # GET CURRENT MONTH/YEAR
    # =============================

    def get_current_month_year(self):
        # ✅ Month from dropdown VALUE
        month_select = self.wait.until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//div[contains(@class,'flatpickr-calendar') and contains(@class,'open')]//select[contains(@class,'flatpickr-monthDropdown-months')]"
            ))
        )

        select = Select(month_select)
        selected_month_text = select.first_selected_option.text

        month = datetime.strptime(selected_month_text, "%B").month

        # ✅ Year from input
        year_input = self.wait.until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//div[contains(@class,'flatpickr-calendar') and contains(@class,'open')]//input[contains(@class,'numInput')]"
            ))
        )

        year = int(year_input.get_attribute("value"))

        return month, year

    # =============================
    # NAVIGATE TO MONTH
    # =============================
    def goto_month(self, target_date):
        target_month = target_date.month
        target_year = target_date.year

        for _ in range(15):  # increased safety loop
            cur_month, cur_year = self.get_current_month_year()

            if cur_month == target_month and cur_year == target_year:
                return

            if (cur_year, cur_month) < (target_year, target_month):
                btn = self.wait.until(EC.element_to_be_clickable(self.NEXT_BTN))
            else:
                btn = self.wait.until(EC.element_to_be_clickable(self.PREV_BTN))

            # 🔥 JS click (more reliable)
            self.driver.execute_script("arguments[0].click();", btn)
            time.sleep(0.5)

        raise Exception("Unable to navigate to target month")

    # =============================
    # SELECT DAY (ROBUST)
    # =============================
    def select_day(self, day):
        xpath = self.DAY.format(day)

        elements = self.wait.until(
            EC.presence_of_all_elements_located((By.XPATH, xpath))
        )

        for el in elements:
            if el.is_displayed():
                try:
                    # scroll + JS click (VERY IMPORTANT)
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", el)
                    time.sleep(0.2)
                    self.driver.execute_script("arguments[0].click();", el)
                    return True
                except:
                    continue

        return False

    # =============================
    # SELECT RANGE
    # =============================
    def select_range(self, start_date, end_date):
        self.open_calendar()

        # Start date
        self.goto_month(start_date)
        if not self.select_day(start_date.day):
            return False

        # Same date (double click case)
        if start_date == end_date:
            self.select_day(start_date.day)
            return True

        # End date
        self.goto_month(end_date)
        if not self.select_day(end_date.day):
            return False

        return True