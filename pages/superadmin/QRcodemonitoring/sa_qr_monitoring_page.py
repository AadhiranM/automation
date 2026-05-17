import random
import time
from datetime import timedelta, date

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from pages.common.base_page import BasePage
from utilities.flatpickr import FlatpickrRangePicker
from selenium.webdriver.common.keys import Keys


class SAQRMonitoringPage(BasePage):

    # ======================================================
    # SEARCH
    # ======================================================
    SEARCH_BOX = (By.ID, "search-vale")
    SEARCH_BTN = (By.ID, "search-btn")

    # ======================================================
    # DATE FILTER
    # ======================================================
    DATE_FILTER = (By.ID, "datepicker-range")

    # ======================================================
    # STATUS FILTER
    # ======================================================
    STATUS_DROPDOWN = (By.ID, "select2-idStatus-container")

    # ======================================================
    # TABLE
    # ======================================================
    FIRST_ROW = (By.XPATH, "//table/tbody/tr[1]")

    NO_DATA = (
        By.XPATH,
        "//td[contains(@class,'dataTables_empty')]"
    )

    SCAN_IDS = (
        By.XPATH,
        "//table/tbody/tr/td[1]"
    )

    # ======================================================
    # ENTRIES
    # ======================================================
    ENTRIES_DROPDOWN = (
        By.NAME,
        "crudTable_length"
    )

    # ======================================================
    # PAGINATION
    # ======================================================
    NEXT_BTN = (
        By.XPATH,
        "//a[normalize-space()='Next']"
    )

    PREVIOUS_BTN = (
        By.XPATH,
        "//a[normalize-space()='Previous']"
    )

    PAGE_NUMBER = "//a[normalize-space()='{}']"

    # ======================================================
    # EXPORT
    # ======================================================
    EXPORT_BTN = (
        By.XPATH,
        "//button[contains(.,'Export')]"
    )

    EXPORT_POPUP = (
        By.XPATH,
        "//h5[contains(.,'Choose Export Criteria')]"
    )

    ID_BASED_TAB = (By.ID, "id-tab")

    START_ID = (
        By.XPATH,
        "//input[@placeholder='Enter Report Start ID']"
    )

    END_ID = (
        By.XPATH,
        "//input[@placeholder='Enter Report End ID']"
    )

    GO_TO_REPORTS = (
        By.XPATH,
        "//a[contains(.,'Go to Reports Page')]"
    )

    REPORT_TABLE = (
        By.XPATH,
        "//table"
    )

    USER_BASED_TAB = (By.ID, "user-tab")

    USER_SELECT = (
        By.XPATH,
        "//div[@id='userTabPane']//div[contains(@class,'choices__inner')]"
    )

    USER_SEARCH_BOX = (
        By.XPATH,
        "//div[@id='userTabPane']//input[contains(@class,'choices__input')]"
    )

    DATE_RANGE = (
        By.XPATH,
        "//input[contains(@placeholder,'Select Date Range')]"
    )

    DATE_BASED_TAB = (By.ID, "date-tab")
    DATE_BASED_RANGE = (
        By.XPATH,
        "//div[@id='dateTabPane']//input[contains(@placeholder,'Select Date Range')]"
    )
    START_TIME = (By.ID, "start_time")
    END_TIME = (By.ID, "end_time")

    EXPORT_SUBMIT = (
        By.XPATH,
        "//button[contains(.,'Submit')]"
    )

    EXPORT_SUCCESS = (
        By.XPATH,
        "//h4[contains(.,'Report Export Queued')]"
    )

    SCAN_ID_FIRST = (
        By.XPATH,
        "//table/tbody/tr[1]/td[1]"
    )

    SCAN_ID_SECOND = (
        By.XPATH,
        "//table/tbody/tr[2]/td[1]"
    )

    FIRST_ROW_USER = (
        By.XPATH,
        "//table/tbody/tr[1]/td[2]"
    )

    LATEST_DOWNLOAD_BTN = (
        By.XPATH,
        "(//table/tbody/tr[1]//a | //table/tbody/tr[1]//button)[last()]"
    )

    # ======================================================
    # NAVIGATION
    # ======================================================
    def goto_page(self):
        self.driver.get(
            "https://beta.digitathya.com/admin/qr-code-monitoring?reset_filters=1"
        )
        self.wait_for_results()

    # ======================================================
    # COMMON WAIT
    # ======================================================
    def wait_for_results(self):
        WebDriverWait(self.driver, 15).until(
            lambda d:
            d.find_elements(*self.FIRST_ROW)
            or
            d.find_elements(*self.NO_DATA)
        )

    # ======================================================
    # SEARCH
    # ======================================================
    def search(self, value):
        rows = self.driver.find_elements(*self.SCAN_IDS)

        if rows:
            value = rows[0].text.strip()

        self.type(self.SEARCH_BOX, value)
        self.click(self.SEARCH_BTN)
        self.wait_for_results()

    # ======================================================
    # STATUS FILTER
    # ======================================================
    def filter_by_status(self, status):
        self.click(self.STATUS_DROPDOWN)

        option = (
            By.XPATH,
            f"//li[contains(@class,'select2-results__option')]//span[normalize-space()='{status}']"
        )

        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(option)
        )

        self.click(option)
        self.wait_for_results()

    # ======================================================
    # DATE FILTER
    # ======================================================
    def filter_date(self, start, end):
        self.click(self.DATE_FILTER)

        picker = FlatpickrRangePicker(self.driver)
        success = picker.select_range(start, end)

        if not success:
            raise Exception("Date range selection failed")

        self.wait_for_results()

    # ======================================================
    # ENTRIES
    # ======================================================
    def set_entries_per_page(self, value):
        dropdown = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.ENTRIES_DROPDOWN)
        )

        Select(dropdown).select_by_value(str(value))
        self.wait_for_results()

    # ======================================================
    # PAGINATION
    # ======================================================
    def click_next(self):
        next_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.NEXT_BTN)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            next_btn
        )

        next_btn.click()
        self.wait_for_results()

    def click_previous(self):
        prev_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.PREVIOUS_BTN)
        )

        self.driver.execute_script("arguments[0].click();", prev_btn)
        self.wait_for_results()

    def go_to_page(self, number):
        page = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, self.PAGE_NUMBER.format(number))
            )
        )

        self.driver.execute_script("arguments[0].click();", page)
        self.wait_for_results()

    # ======================================================
    # EXPORT
    # ======================================================
    def click_export(self):
        self.click(self.EXPORT_BTN)

        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(self.EXPORT_POPUP)
        )

    def go_to_reports_page(self):
        self.click(self.GO_TO_REPORTS)

        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(self.REPORT_TABLE)
        )

    def export_id_based(self):
        wait = WebDriverWait(self.driver, 25)

        start_id = wait.until(
            EC.visibility_of_element_located(self.SCAN_ID_SECOND)
        ).text.strip()

        end_id = wait.until(
            EC.visibility_of_element_located(self.SCAN_ID_FIRST)
        ).text.strip()

        user_name = wait.until(
            EC.visibility_of_element_located(self.FIRST_ROW_USER)
        ).text.strip().split("\n")[0]

        self.click(self.ID_BASED_TAB)
        time.sleep(2)

        # START ID
        start_box = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//input[@placeholder='Enter Report Start ID']"
            ))
        )
        start_box.click()
        start_box.send_keys(Keys.CONTROL, "a")
        start_box.send_keys(Keys.DELETE)
        start_box.send_keys(start_id)

        # END ID
        end_box = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//input[@placeholder='Enter Report End ID']"
            ))
        )
        end_box.click()
        end_box.send_keys(Keys.CONTROL, "a")
        end_box.send_keys(Keys.DELETE)
        end_box.send_keys(end_id)

        # USER DROPDOWN
        dropdown = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//div[contains(@class,'choices__inner')]"
            ))
        )
        dropdown.click()

        search_box = wait.until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//input[contains(@class,'choices__input')]"
            ))
        )

        search_box.click()
        search_box.clear()
        search_box.send_keys(user_name)

        # wait exact Raj option
        exact_option = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                f"//div[contains(@class,'choices__item--choice') and starts-with(normalize-space(), '{user_name}')]"
            ))
        )

        self.driver.execute_script("arguments[0].scrollIntoView(true);", exact_option)
        time.sleep(1)
        exact_option.click()

        # verify selected chip
        wait.until(
            EC.visibility_of_element_located((
                By.XPATH,
                f"//div[contains(@class,'choices__item')][contains(.,'{user_name}')]"
            ))
        )

        self.click(self.EXPORT_SUBMIT)


    # ======================================================
    # USER BASED EXPORT FIXED
    # ======================================================
    def export_user_based(self):
        wait = WebDriverWait(self.driver, 20)

        self.click(self.USER_BASED_TAB)

        wait.until(
            EC.visibility_of_element_located(
                (By.ID, "userTabPane")
            )
        )

        # open dropdown
        dropdown = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//div[@id='userTabPane']//div[contains(@class,'choices__inner')]"
            ))
        )
        dropdown.click()

        # search box
        search_box = wait.until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//div[@id='userTabPane']//input[contains(@class,'choices__input')]"
            ))
        )

        search_box.clear()
        search_box.send_keys("T")

        # wait options
        wait.until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//div[@id='userTabPane']//div[contains(@class,'choices__item--choice')]"
            ))
        )

        # select first option
        search_box.send_keys(Keys.ARROW_DOWN)
        search_box.send_keys(Keys.ENTER)

        # CLOSE dropdown properly
        search_box.send_keys(Keys.TAB)

        # wait dropdown disappears
        wait.until(
            EC.invisibility_of_element_located((
                By.XPATH,
                "//div[@id='userTabPane']//div[contains(@class,'choices__list--dropdown')]"
            ))
        )

        # click date
        date_input = wait.until(
            EC.element_to_be_clickable(self.DATE_RANGE)
        )
        date_input.click()

        picker = FlatpickrRangePicker(self.driver)
        picker.select_range(
            date.today() - timedelta(days=7),
            date.today()
        )

        # start time
        Select(
            wait.until(
                EC.element_to_be_clickable(self.START_TIME)
            )
        ).select_by_visible_text("01:00:00")

        # end time
        Select(
            wait.until(
                EC.element_to_be_clickable(self.END_TIME)
            )
        ).select_by_visible_text("02:00:00")

        self.click(self.EXPORT_SUBMIT)

        wait.until(
            EC.visibility_of_element_located(
                self.EXPORT_SUCCESS
            )
        )

    # ======================================================
    # VALIDATIONS
    # ======================================================
    def is_row_present(self):
        return len(self.driver.find_elements(*self.FIRST_ROW)) > 0

    def has_no_data(self):
        return len(self.driver.find_elements(*self.NO_DATA)) > 0

    def export_bulk_id_based(self):
        wait = WebDriverWait(self.driver, 20)

        scan_ids = self.driver.find_elements(
            By.XPATH,
            "//table//tbody/tr/td[1]"
        )

        ids = [scan_ids[i].text.strip() for i in range(min(3, len(scan_ids)))]
        bulk_ids = ",".join(ids)

        self.click(self.EXPORT_BTN)
        self.click((By.ID, "bulk-tab"))

        bulk_box = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//textarea[contains(@placeholder,'Enter scan ID')]"
            ))
        )

        bulk_box.clear()
        bulk_box.send_keys(bulk_ids)

        self.click(self.EXPORT_SUBMIT)

    def export_date_based(self):
        wait = WebDriverWait(self.driver, 20)

        self.click(self.EXPORT_BTN)

        wait.until(
            EC.visibility_of_element_located(self.EXPORT_POPUP)
        )

        self.click(self.DATE_BASED_TAB)

        wait.until(
            EC.visibility_of_element_located(
                (By.ID, "dateTabPane")
            )
        )

        date_input = wait.until(
            EC.element_to_be_clickable(self.DATE_BASED_RANGE)
        )
        date_input.click()

        time.sleep(1)

        picker = FlatpickrRangePicker(self.driver)
        picker.select_range(
            date.today() - timedelta(days=7),
            date.today()
        )

        self.click(self.EXPORT_SUBMIT)

        wait.until(
            EC.visibility_of_element_located(self.EXPORT_SUCCESS)
        )