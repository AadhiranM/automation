from datetime import date, timedelta
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from pages.common.base_page import BasePage
from utilities.flatpickr import FlatpickrRangePicker
from selenium.webdriver.common.action_chains import ActionChains



class SAScheduledReportsPage(BasePage):

    # ======================================================
    # SEARCH
    # ======================================================
    SEARCH_BOX = (By.ID, "search-vale")
    SEARCH_BTN = (By.ID, "search-btn")

    # ======================================================
    # FILTERS
    # ======================================================
    DATE_FILTER = (
        By.ID,
        "datepicker-range"
    )

    STATUS_DROPDOWN = (
        By.ID,
        "select2-idStatus-container"
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

    FIRST_PRODUCT = (
        By.XPATH,
        "//table/tbody/tr[1]/td[6]"
    )

    FIRST_COMMENT = (
        By.XPATH,
        "//table/tbody/tr[1]/td[last()]"
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

    FIRST_SCAN_ID = (
        By.XPATH,
        "//table/tbody/tr[1]/td[2]"
    )

    EDIT_BTN = (
        By.XPATH,
        "//a[contains(.,'Edit')]"
    )

    ACTIONS_BTN = (
        By.XPATH,
        "(//table/tbody/tr[1]//button[contains(@class,'btn')])[last()]"
    )

    PREVIOUS_BTN = (
        By.XPATH,
        "//a[normalize-space()='Previous']"
    )
    PAGE_NUMBER = "//a[normalize-space()='{}']"

    # ======================================================
    # EDIT PAGE
    # ======================================================


    SUBMIT_BTN = (
         By.XPATH,
         "//button[contains(text(),'Submit')]"
    )

    SUCCESS_MSG = (
        By.XPATH,
        "//*[contains(text(),'successfully')]"
    )
    # ======================================================
    # EXPORT
    # ======================================================

    CREATE_BTN = (
        By.XPATH,
        "//button[contains(.,'Create')]"
    )

    def click_create(self):
        wait = WebDriverWait(self.driver, 30)

        wait.until(
            EC.element_to_be_clickable(self.CREATE_BTN)
        ).click()

        time.sleep(3)
    def goto_page(self):
        self.driver.get(
            "https://beta.digitathya.com/admin/auto-generate-report?reset_filters=1"
        )
        self.wait_for_results()
    # ======================================================
    # WAIT
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

    def search_first_record(self):
        scan_id = self.get_text(
            self.FIRST_SCAN_ID
        ).strip()

        self.type(self.SEARCH_BOX, scan_id)
        self.click(self.SEARCH_BTN)

        self.wait_for_results()

        return scan_id
    # ======================================================
    # STATUS FILTER
    # ======================================================

    def filter_by_status(self, status):
        wait = WebDriverWait(self.driver, 30)

        print(f"Selecting status = {status}")

        # exact visible status dropdown
        dropdown = wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                "//span[@id='select2-idStatus-container']"
            ))
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            dropdown
        )
        time.sleep(2)

        # ActionChains click (stronger than normal click)
        ActionChains(self.driver).move_to_element(dropdown).click().perform()

        print("Status dropdown clicked")
        time.sleep(2)

        # select option from opened dropdown
        option = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                f"//li[@role='option' and normalize-space()='{status}']"
            ))
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'nearest'});",
            option
        )
        time.sleep(1)

        ActionChains(self.driver).move_to_element(option).click().perform()

        print(f"Selected status = {status}")

        time.sleep(3)

        rows = self.driver.find_elements(
            By.XPATH,
            "//table/tbody/tr"
        )

        no_data = self.driver.find_elements(
            By.XPATH,
            "//*[contains(text(),'No data available')]"
        )

        assert len(rows) > 0 or len(no_data) > 0
    # ======================================================
    # DATE FILTER
    # ======================================================

    def filter_date(self, start, end):

        self.click(self.DATE_FILTER)

        picker = FlatpickrRangePicker(self.driver)

        picker.select_range(start, end)

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

        self.driver.execute_script(
            "arguments[0].click();",
            next_btn
        )

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
            EC.element_to_be_clickable((
                By.XPATH,
                self.PAGE_NUMBER.format(number)
            ))
        )

        self.driver.execute_script(
            "arguments[0].click();",
            page
        )

        self.wait_for_results()
    # ======================================================
    # VIEW
    # ======================================================


    def is_row_present(self):

        return len(
            self.driver.find_elements(*self.FIRST_ROW)
        ) > 0

    def has_no_data(self):

        return len(
            self.driver.find_elements(*self.NO_DATA)
        ) > 0


