import time
from datetime import date, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.common.base_page import BasePage


class SADownloadReportsPage(BasePage):

    URL = "https://beta.digitathya.com/admin/reports"

    DOWNLOAD_TAB = (
        By.XPATH,
        "//button[contains(text(),'Downloads')]"
    )

    SEARCH_BOX = (
        By.XPATH,
        "//input[contains(@placeholder,'Search')]"
    )

    SEARCH_BTN = (
        By.XPATH,
        "//button[contains(@class,'btn')]//*[contains(@class,'ri-search')]"
    )

    DATE_FILTER = (
        By.XPATH,
        "//input[contains(@placeholder,'Select Date')]"
    )

    FORMAT_FILTER = (
        By.XPATH,
        "//input[contains(@placeholder,'Select Format')]"
    )

    STATUS_FILTER = (
        By.XPATH,
        "//input[contains(@placeholder,'Select Status')]"
    )

    FILTER_BTN = (
        By.XPATH,
        "//button[contains(text(),'Filter')]"
    )

    ENTRIES_DROPDOWN = (
        By.XPATH,
        "//select"
    )

    NEXT_BTN = (
        By.XPATH,
        "//a[contains(text(),'Next')]"
    )

    PREVIOUS_BTN = (
        By.XPATH,
        "//a[contains(text(),'Previous')]"
    )

    PAGE_2 = (
        By.XPATH,
        "//a[text()='2']"
    )

    FIRST_ROW_REPORT = (
        By.XPATH,
        "//table/tbody/tr[1]/td[2]"
    )

    FIRST_DOWNLOAD_ICON = (
        By.XPATH,
        "//table/tbody/tr[1]/td[last()]//a"
    )

    TABLE_ROWS = (
        By.XPATH,
        "//table/tbody/tr"
    )

    NO_DATA = (
        By.XPATH,
        "//*[contains(text(),'No data')]"
    )

    def goto_page(self):
        self.driver.get(self.URL)
        time.sleep(3)

        self.driver.execute_script(
            "arguments[0].click();",
            self.wait_for_element(self.DOWNLOAD_TAB)
        )

        time.sleep(2)

    def is_row_present(self):
        rows = self.driver.find_elements(*self.TABLE_ROWS)
        return len(rows) > 0

    def has_no_data(self):
        no_data = self.driver.find_elements(*self.NO_DATA)
        return len(no_data) > 0

    def search_report(self):
        report_name = self.get_text(
            self.FIRST_ROW_REPORT
        )

        self.enter_text(
            self.SEARCH_BOX,
            report_name
        )

        self.click(self.SEARCH_BTN)

        time.sleep(3)

        return report_name

    def filter_by_format(self, file_format):
        wait = WebDriverWait(self.driver, 20)

        self.click(self.FORMAT_FILTER)

        option = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                f"//div[contains(text(),'{file_format}')]"
            ))
        )

        option.click()

        self.click(self.FILTER_BTN)

        time.sleep(3)

    def filter_by_status(self, status):
        wait = WebDriverWait(self.driver, 20)

        self.click(self.STATUS_FILTER)

        option = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                f"//div[contains(text(),'{status}')]"
            ))
        )

        option.click()

        self.click(self.FILTER_BTN)

        time.sleep(3)

    def filter_by_date(self):
        wait = WebDriverWait(self.driver, 20)

        self.click(self.DATE_FILTER)

        time.sleep(2)

        today = date.today()
        week_before = today - timedelta(days=7)

        start_locator = (
            By.XPATH,
            f"//span[@aria-label='{week_before.strftime('%B %-d, %Y')}']"
        )

        end_locator = (
            By.XPATH,
            f"//span[@aria-label='{today.strftime('%B %-d, %Y')}']"
        )

        wait.until(
            EC.element_to_be_clickable(start_locator)
        ).click()

        time.sleep(1)

        wait.until(
            EC.element_to_be_clickable(end_locator)
        ).click()

        self.click(self.FILTER_BTN)

        time.sleep(3)

    def set_entries_per_page(self, value):
        dropdown = self.wait_for_element(
            self.ENTRIES_DROPDOWN
        )

        dropdown.send_keys(value)

        time.sleep(3)

    def click_next(self):
        self.click(self.NEXT_BTN)
        time.sleep(3)

    def click_previous(self):
        self.click(self.PREVIOUS_BTN)
        time.sleep(3)

    def go_to_page_2(self):
        self.click(self.PAGE_2)
        time.sleep(3)

    def download_first_report(self):
        self.click(self.FIRST_DOWNLOAD_ICON)
        time.sleep(5)