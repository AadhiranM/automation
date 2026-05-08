import random
import time
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from pages.common.base_page import BasePage
from utilities.flatpickr import FlatpickrRangePicker
from selenium.webdriver.common.action_chains import ActionChains

class SAQRMonitoringPage(BasePage):

    # ======================================================
    # SEARCH
    # ======================================================
    SEARCH_BOX = (By.ID, "search-vale")
    SEARCH_BTN = (By.ID, "search-btn")

    # ======================================================
    # DATE FILTER
    # ======================================================
    DATE_FILTER = (
        By.ID,
        "datepicker-range"
    )

    # ======================================================
    # STATUS FILTER
    # ======================================================
    STATUS_DROPDOWN = (
        By.ID,
        "select2-idStatus-container"
    )

    # ======================================================
    # FILTER / RESET
    # ======================================================
    FILTER_BTN = (
        By.XPATH,
        "//button[contains(.,'Filter')]"
    )

    RESET_BTN = (
        By.XPATH,
        "//a[contains(@href,'reset_filters')]"
    )

    # ======================================================
    # TABLE
    # ======================================================
    FIRST_ROW = (
        By.XPATH,
        "//table/tbody/tr[1]"
    )

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

    ID_BASED_TAB = (
        By.ID, "id-tab")


    START_ID = (
        By.XPATH,
        "//input[contains(@placeholder,'Enter Report Start ID')]"
    )

    END_ID = (
        By.XPATH,
        "//input[contains(@placeholder,'Enter Report End ID')]"
    )

    SELECT_USERS_DROPDOWN = (
        By.NAME, "search_terms")

    EXPORT_SUBMIT = (
        By.XPATH,
        "//button[contains(.,'Submit')]"
    )

    EXPORT_SUCCESS = (
        By.XPATH,
        "//h4[contains(.,'Report Export Queued')]"
    )

    GO_TO_REPORTS = (
        By.XPATH,
        "//a[contains(.,'Go to Reports Page')]"
    )

    REPORT_TABLE = (
        By.XPATH,
        "//table"
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

        # open dropdown
        self.click(self.STATUS_DROPDOWN)

        time.sleep(2)

        # select option
        option = (
            By.XPATH,
            f"//li[contains(@class,'select2-results__option')]//span[normalize-space()='{status}']"
        )

        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(option)
        )

        self.click(option)

        time.sleep(2)

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

        time.sleep(2)

        self.wait_for_results()

    # ======================================================
    # ENTRIES
    # ======================================================
    def set_entries_per_page(self, value):

        dropdown = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                self.ENTRIES_DROPDOWN
            )
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

        # REAL browser scroll
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            next_btn
        )

        time.sleep(2)

        next_btn.click()

        self.wait_for_results()

    def click_previous(self):

        prev_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.PREVIOUS_BTN)
        )

        self.driver.execute_script(
            "arguments[0].click();",
            prev_btn
        )

        self.wait_for_results()

    def go_to_page(self, number):

        page = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    self.PAGE_NUMBER.format(number)
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            page
        )

        self.wait_for_results()

    # ======================================================
    # EXPORT
    # ======================================================
    def click_export(self):

        self.click(self.EXPORT_BTN)

        time.sleep(2)

    from selenium.webdriver.common.action_chains import ActionChains

    def go_to_reports_page(self):

        self.click(self.GO_TO_REPORTS)

        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(
                self.REPORT_TABLE
            )
        )

    def export_id_based(self):

        self.click(self.ID_BASED_TAB)
        time.sleep(2)

        # open dropdown first
        def export_id_based(self):
            self.click(self.ID_BASED_TAB)
            time.sleep(2)

            # open dropdown first
            self.click(self.SELECT_USERS_DROPDOWN)
            time.sleep(2)

            # correct xpath
            users = WebDriverWait(self.driver, 15).until(
                EC.presence_of_all_elements_located((
                    By.XPATH,
                    "//div[contains(@class,'choices__item--choice')]"
                ))
            )

            valid_users = [u for u in users if u.text.strip()]

            print("Users found:", len(valid_users))

            if not valid_users:
                raise Exception("No users found")

            selected = random.choice(valid_users)

            print("Selecting:", selected.text)

            # JS click exact element
            self.driver.execute_script("arguments[0].click();", selected)

            time.sleep(2)

            # click end id (your manual flow)
            self.click(self.END_ID)
            self.type(self.END_ID, "2")

            self.click(self.START_ID)
            self.type(self.START_ID, "1")

            self.click(self.EXPORT_SUBMIT)

    # ======================================================
    # VALIDATIONS
    # ======================================================
    def is_row_present(self):

        return len(
            self.driver.find_elements(*self.FIRST_ROW)
        ) > 0

    def has_no_data(self):

        return len(
            self.driver.find_elements(*self.NO_DATA)
        ) > 0