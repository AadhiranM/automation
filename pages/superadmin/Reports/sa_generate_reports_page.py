import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from pages.common.base_page import BasePage
from datetime import datetime
from selenium.webdriver.common.keys import Keys
class SAGenerateReportsPage(BasePage):

    URL = "https://beta.digitathya.com/admin/reports?reset_filters=1"

    REPORT_NAME_INPUT = (By.ID, "report_name")

    FORMAT_DROPDOWN = (
        By.ID,
        "select2-selectFormat-container"
    )

    DURATION_DROPDOWN = (
        By.ID,
        "select2-selectDuration-container"
    )

    GENERATE_BTN = (
        By.XPATH,
        "//button[contains(text(),'Generate')]"
    )

    DOWNLOADS_TAB = (
        By.XPATH,
        "//a[contains(text(),'Downloads')]"
    )

    def __init__(self, driver):
        super().__init__(driver)

    def goto_page(self):
        wait = WebDriverWait(self.driver, 60)

        self.driver.get(self.URL)

        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[@data-table='manufacturer_details']")
            )
        )

        time.sleep(3)

    def click_report_button(self, data_table):
        wait = WebDriverWait(self.driver, 30)

        btn = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                f"//a[@data-table='{data_table}']"
            ))
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            btn
        )

        time.sleep(2)

        ActionChains(self.driver).move_to_element(btn).click().perform()

        time.sleep(3)


    def select_manufacturer(self):
        wait = WebDriverWait(self.driver, 30)

        print("Selecting manufacturer via keyboard")

        dropdown = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//label[contains(text(),'Manufacturer')]/following::div[contains(@class,'choices')][1]"
            ))
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            dropdown
        )

        time.sleep(2)

        self.driver.execute_script(
            "arguments[0].click();",
            dropdown
        )

        print("Dropdown opened")

        time.sleep(2)

        active = self.driver.switch_to.active_element

        # type filter
        active.send_keys("i")

        print("Typed i")

        time.sleep(2)

        # choose first visible option
        active.send_keys(Keys.ARROW_DOWN)

        time.sleep(1)

        active.send_keys(Keys.ENTER)

        print("Manufacturer selected")

        time.sleep(2)

    def fill_popup(
            self,
            report_name,
            file_format,
            duration,
            manufacturer_required=False
    ):
        wait = WebDriverWait(self.driver, 30)

        # report name
        report = wait.until(
            EC.visibility_of_element_located(
                self.REPORT_NAME_INPUT
            )
        )

        report.clear()
        report.send_keys(report_name)

        # manufacturer dropdown only for activity report
        if manufacturer_required:
            self.select_manufacturer()

        # format
        wait.until(
            EC.element_to_be_clickable(
                self.FORMAT_DROPDOWN
            )
        ).click()

        wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                f"//li[normalize-space()='{file_format}']"
            ))
        ).click()

        # duration
        wait.until(
            EC.element_to_be_clickable(
                self.DURATION_DROPDOWN
            )
        ).click()

        wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                f"//li[normalize-space()='{duration}']"
            ))
        ).click()

        # submit
        wait.until(
            EC.element_to_be_clickable(
                self.GENERATE_BTN
            )
        ).click()

        print("Generate clicked")

        expected_url = (
            "https://beta.digitathya.com/admin/reports"
            "?reset_filters=1"
        )

        wait.until(
            EC.url_to_be(expected_url)
        )

        actual_url = self.driver.current_url

        print("ACTUAL URL =", actual_url)

        assert actual_url == expected_url, \
            f"Expected URL: {expected_url}, but got: {actual_url}"

        print("Report generation successful")

        return actual_url

    def generate_manufacturer_report(
        self,
        report_name,
        file_format,
        duration
    ):
        self.goto_page()
        self.click_report_button("manufacturer_details")
        return self.fill_popup(
            report_name,
            file_format,
            duration
        )

    def generate_manufacturer_activity_report(
        self,
        report_name,
        file_format,
        duration
    ):
        self.goto_page()
        self.click_report_button("manufacturer_activity_report")
        return self.fill_popup(
            report_name,
            file_format,
            duration,
            manufacturer_required=True
        )
