from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import time


class FlatpickrRangePicker:

    MONTH_DROPDOWN = (
        By.XPATH,
        "(//div[contains(@class,'flatpickr-months')])[1]"
        "//select[contains(@class,'flatpickr-monthDropdown-months')]"
    )

    YEAR_INPUT = (
        By.XPATH,
        "(//div[contains(@class,'flatpickr-months')])[1]"
        "//input[contains(@class,'cur-year')]"
    )

    YEAR_UP = (
        By.XPATH,
        "(//div[contains(@class,'flatpickr-months')])[1]//span[contains(@class,'arrowUp')]"
    )

    YEAR_DOWN = (
        By.XPATH,
        "(//div[contains(@class,'flatpickr-months')])[1]//span[contains(@class,'arrowDown')]"
    )

    NEXT_BTN = (
        By.XPATH,
        "(//div[contains(@class,'flatpickr-months')])[1]//span[contains(@class,'flatpickr-next-month')]"
    )

    PREV_BTN = (
        By.XPATH,
        "(//div[contains(@class,'flatpickr-months')])[1]//span[contains(@class,'flatpickr-prev-month')]"
    )

    DAY = "//span[contains(@class,'flatpickr-day') and normalize-space()='{}']"

    INLINE_CALENDAR = (By.CSS_SELECTOR, "div.flatpickr-calendar.open")
    PANEL_CALENDAR = (By.CSS_SELECTOR, "div.offcanvas.show div.flatpickr-calendar")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.calendar_type = None

    # --------------------------------------------------
    def open_if_needed(self):
        """
        Detect whether calendar is inline or inside an offcanvas panel, set calendar_type,
        and wait for visibility. Raises if neither is visible.
        """
        # Small sleep to let DOM update (sometimes required)
        time.sleep(0.05)

        if self.driver.find_elements(*self.INLINE_CALENDAR):
            self.calendar_type = "inline"
            self.wait.until(EC.visibility_of_element_located(self.INLINE_CALENDAR))
            return

        if self.driver.find_elements(*self.PANEL_CALENDAR):
            self.calendar_type = "panel"
            self.wait.until(EC.visibility_of_element_located(self.PANEL_CALENDAR))
            return

        # If none visible — try a slightly longer wait before failing
        # (some pages take a moment to render the calendar)
        try:
            self.wait.until(
                lambda d: d.find_elements(*self.INLINE_CALENDAR) or d.find_elements(*self.PANEL_CALENDAR)
            )
        except:
            raise Exception("Calendar is not visible.")
        return self.open_if_needed()

    # --------------------------------------------------
    def get_current_month_year(self):
        """Return (month_number 1..12, year) for the LEFT calendar panel (first visible panel)."""
        month_el = self.wait.until(EC.visibility_of_element_located(self.MONTH_DROPDOWN))
        month_index = int(month_el.get_attribute("value")) + 1
        year_el = self.wait.until(EC.visibility_of_element_located(self.YEAR_INPUT))
        year_val = int(year_el.get_attribute("value"))
        return month_index, year_val

    # --------------------------------------------------
    def safe_click(self, locator):
        """Click with fallback to JS click."""
        try:
            el = self.wait.until(EC.element_to_be_clickable(locator))
            el.click()
            return True
        except Exception:
            try:
                el = self.wait.until(EC.presence_of_element_located(locator))
                self.driver.execute_script("arguments[0].click();", el)
                return True
            except Exception:
                return False

    # --------------------------------------------------
    def adjust_year(self, cur_year, target_year):
        if cur_year == target_year:
            return
        diff = abs(target_year - cur_year)
        arrow = self.YEAR_UP if target_year > cur_year else self.YEAR_DOWN
        for _ in range(diff):
            clicked = self.safe_click(arrow)
            if not clicked:
                # small pause and retry once
                time.sleep(0.05)
                self.safe_click(arrow)

    # --------------------------------------------------
    def goto_month(self, target_date):
        """Navigate calendar to the requested month & year (left panel)."""
        self.open_if_needed()
        # loop until we see desired month/year
        attempts = 0
        while True:
            cur_month, cur_year = self.get_current_month_year()

            if cur_year != target_date.year:
                self.adjust_year(cur_year, target_date.year)
                attempts += 1
                if attempts > 50:
                    raise Exception("Unable to set target year in calendar.")
                continue

            if cur_month == target_date.month:
                break

            if cur_month < target_date.month:
                if not self.safe_click(self.NEXT_BTN):
                    time.sleep(0.05)
                    self.safe_click(self.NEXT_BTN)
            else:
                if not self.safe_click(self.PREV_BTN):
                    time.sleep(0.05)
                    self.safe_click(self.PREV_BTN)

            # ensure DOM updated for next iteration
            self.open_if_needed()

    # --------------------------------------------------
    def click_day(self, day):
        """
        Try to click the given day. Returns True on success, False if day is disabled or click fails.
        """
        locator = (By.XPATH, self.DAY.format(day))
        try:
            el = self.wait.until(EC.presence_of_element_located(locator))
        except Exception:
            return False

        classes = el.get_attribute("class") or ""
        if "flatpickr-disabled" in classes:
            return False

        try:
            el.click()
            return True
        except Exception:
            try:
                self.driver.execute_script("arguments[0].click();", el)
                return True
            except Exception:
                return False

    # --------------------------------------------------
    def is_day_disabled(self, day):
        locator = (By.XPATH, self.DAY.format(day))
        try:
            el = self.wait.until(EC.presence_of_element_located(locator))
            return "flatpickr-disabled" in (el.get_attribute("class") or "")
        except Exception:
            # If we can't find the element, treat it as disabled/unselectable.
            return True

    # --------------------------------------------------
    def is_range_disabled(self, start_date, end_date):
        """
        Return True if ALL days in requested range are disabled.
        Ensures calendar is visible and iterates months if range spans months.
        """
        # ensure calendar visible & determine mode
        self.open_if_needed()

        # inline calendars on this app may also show disabled days, but treat inline as not globally disabled
        if self.calendar_type == "inline":
            # still perform a specific check across the range to be safe
            pass

        cur = start_date.replace(day=1)
        last = end_date.replace(day=1)

        while (cur.year, cur.month) <= (last.year, last.month):
            self.goto_month(cur)

            if cur.year == start_date.year and cur.month == start_date.month:
                d_from = start_date.day
            else:
                d_from = 1

            if cur.year == end_date.year and cur.month == end_date.month:
                d_to = end_date.day
            else:
                next_m = (cur.replace(day=28) + datetime.timedelta(days=4)).replace(day=1)
                d_to = (next_m - datetime.timedelta(days=1)).day

            # if we find any enabled day in the requested interval => range not fully-disabled
            for d in range(d_from, d_to + 1):
                if not self.is_day_disabled(d):
                    return False

            # next month
            cur = (cur.replace(day=28) + datetime.timedelta(days=4)).replace(day=1)

        # all checked days were disabled
        return True

    # --------------------------------------------------
    def select_range(self, start_date, end_date):
        """
        Try to perform the range selection.
        Returns True if selection succeeded, False if selection couldn't be performed (disabled days or click failure).
        """
        self.open_if_needed()

        # INLINE mode selection
        if self.calendar_type == "inline":
            # Navigate and attempt to click start
            self.goto_month(start_date)
            if self.is_day_disabled(start_date.day):
                return False
            if not self.click_day(start_date.day):
                return False

            # if same date, click twice (flatpickr range behavior)
            if start_date == end_date:
                # attempt second click (if required)
                self.goto_month(start_date)
                self.click_day(start_date.day)
                return True

            # navigate to end and click
            self.goto_month(end_date)
            if self.is_day_disabled(end_date.day):
                return False
            if not self.click_day(end_date.day):
                return False

            return True

        # PANEL mode selection
        # if full range disabled -> caller may choose to bail out early; return False here
        if self.is_range_disabled(start_date, end_date):
            return False

        # start date
        self.goto_month(start_date)
        if self.is_day_disabled(start_date.day):
            return False
        if not self.click_day(start_date.day):
            return False

        # same date double-click if necessary
        if start_date == end_date:
            self.goto_month(start_date)
            self.click_day(start_date.day)
            return True

        # end date
        self.goto_month(end_date)
        if self.is_day_disabled(end_date.day):
            return False
        if not self.click_day(end_date.day):
            return False

        return True
