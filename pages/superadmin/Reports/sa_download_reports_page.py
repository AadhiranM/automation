import time
from datetime import date, timedelta

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from pages.common.base_page import BasePage
from utilities.flatpickr import FlatpickrRangePicker


class SADownloadReportsPage(BasePage):

    URL = "https://beta.digitathya.com/admin/reports?reset_filters=1&export_download"

    SEARCH_BOX = (By.ID, "search-vale")
    SEARCH_BTN = (By.ID, "search-btn")

    DATE_FILTER = (
        By.XPATH,
        "//input[@type='text' and @placeholder='Created At']"
    )

    FORMAT_DROPDOWN = (
        By.XPATH,
        "//span[@id='select2-format-container']"
    )

    STATUS_DROPDOWN = (
        By.XPATH,
        "//span[@id='select2-idStatus-container']"
    )

    FILTER_BTN = (
        By.XPATH,
        "//button[contains(text(),'Filter')]"
    )

    ENTRIES_DROPDOWN = (
        By.NAME,
        "crudTable_length"
    )

    NEXT_BTN = (
        By.XPATH,
        "//a[normalize-space()='Next']"
    )

    PREVIOUS_BTN = (
        By.XPATH,
        "//a[normalize-space()='Previous']"
    )

    PAGE_NUMBER = "//a[normalize-space()='{}']"

    FIRST_ROW_REPORT = (
        By.XPATH,
        "//table/tbody/tr[1]/td[2]"
    )

    FIRST_ROW = (
        By.XPATH,
        "//table/tbody/tr[1]"
    )

    TABLE_ROWS = (
        By.XPATH,
        "//table/tbody/tr"
    )

    NO_DATA = (
        By.XPATH,
        "//*[contains(text(),'No data')]"
    )

    DOWNLOAD_ICONS = (
        By.XPATH,
        "//table/tbody/tr/td[last()]//a"
    )

    def goto_page(self):
        self.driver.get(self.URL)
        self.wait_for_results()

    def wait_for_results(self):
        wait = WebDriverWait(self.driver, 30)

        wait.until(
            lambda d:
            len(d.find_elements(*self.TABLE_ROWS)) > 0
            or
            len(d.find_elements(*self.NO_DATA)) > 0
        )

    def is_row_present(self):
        return len(self.driver.find_elements(*self.TABLE_ROWS)) > 0

    def has_no_data(self):
        return len(self.driver.find_elements(*self.NO_DATA)) > 0

    def search_report(self):
        wait = WebDriverWait(self.driver, 20)

        report_name = self.get_text(
            self.FIRST_ROW_REPORT
        ).strip()

        self.type(self.SEARCH_BOX, report_name)

        btn = wait.until(
            EC.element_to_be_clickable(self.SEARCH_BTN)
        )

        self.driver.execute_script(
            "arguments[0].click();",
            btn
        )

        self.wait_for_results()

        return report_name

    def filter_by_format(self, file_format):
        wait = WebDriverWait(self.driver, 30)

        print(f"Selecting format = {file_format}")

        dropdown = wait.until(
            EC.presence_of_element_located(
                self.FORMAT_DROPDOWN
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            dropdown
        )
        time.sleep(2)

        ActionChains(self.driver).move_to_element(dropdown).click().perform()

        print("Format dropdown clicked")
        time.sleep(2)

        option = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                f"//li[@role='option' and normalize-space()='{file_format}']"
            ))
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'nearest'});",
            option
        )
        time.sleep(1)

        ActionChains(self.driver).move_to_element(option).click().perform()

        print(f"Selected format = {file_format}")

        time.sleep(3)
        self.wait_for_results()

    def filter_by_status(self, status):
        wait = WebDriverWait(self.driver, 30)

        print(f"Selecting status = {status}")

        dropdown = wait.until(
            EC.presence_of_element_located(
                self.STATUS_DROPDOWN
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            dropdown
        )
        time.sleep(2)

        ActionChains(self.driver).move_to_element(dropdown).click().perform()

        print("Status dropdown clicked")
        time.sleep(2)

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
        self.wait_for_results()

    def filter_date(self, start, end):
        self.click(self.DATE_FILTER)

        picker = FlatpickrRangePicker(self.driver)

        picker.select_range(start, end)

        self.wait_for_results()



    def set_entries_per_page(self, value):
        dropdown = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                self.ENTRIES_DROPDOWN
            )
        )

        Select(dropdown).select_by_value(str(value))

        self.wait_for_results()

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

    def download_first_report(self):
        icons = self.driver.find_elements(*self.DOWNLOAD_ICONS)

        if not icons:
            return "NO_DATA"

        self.driver.execute_script(
            "arguments[0].click();",
            icons[0]
        )

        time.sleep(5)

        return "DOWNLOADED"