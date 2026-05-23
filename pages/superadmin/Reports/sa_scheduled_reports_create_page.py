from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.common.base_page import BasePage

class SAScheduledReportsCreatePage(BasePage):

    REPORT_DROPDOWN = (
        By.XPATH,
        "//label[contains(text(),'Report')]/following::span[contains(@class,'select2-selection')][1]"
    )

    FORMAT_DROPDOWN = (
        By.XPATH,
        "//label[contains(text(),'Format')]/following::span[contains(@class,'select2-selection')][1]"
    )

    MAIL_TIME_DROPDOWN = (
        By.XPATH,
        "//label[contains(text(),'Mail Receiving Duration')]/following::span[contains(@class,'select2-selection')][1]"
    )

    DURATION_DROPDOWN = (
        By.XPATH,
        "//label[contains(text(),'Duration')]/following::span[contains(@class,'select2-selection')][1]"
    )

    SAVE_BTN = (
        By.XPATH,
        "//button[contains(text(),'Save')]"
    )

    def select_select2_dropdown(self, dropdown_locator, option_text):
        wait = WebDriverWait(self.driver, 20)

        dropdown = wait.until(
            EC.visibility_of_element_located(dropdown_locator)
        )

        self.click_with_events(dropdown)

        option = wait.until(
            EC.visibility_of_element_located((
                By.XPATH,
                f"//li[contains(@class,'select2-results__option') and normalize-space()='{option_text}']"
            ))
        )

        self.click_with_events(option)

        self.wait_until_dropdown_updated(dropdown)

    def select_report(self, report_name):
        self.select_select2_dropdown(
            self.REPORT_DROPDOWN,
            report_name
        )

    def select_format(self, file_format):
        self.select_select2_dropdown(
            self.FORMAT_DROPDOWN,
            file_format
        )

    def select_mail_time(self, mail_time):
        self.select_select2_dropdown(
            self.MAIL_TIME_DROPDOWN,
            mail_time
        )

    def select_duration(self, duration):
        self.select_select2_dropdown(
            self.DURATION_DROPDOWN,
            duration
        )

    def select_manufacturer(self):
        self.select_searchable_dropdown_js(
            (
                By.XPATH,
                "//label[contains(text(),'Manufacturer')]/following::div[contains(@class,'choices')][1]"
            ),
            "TATA"
        )

    def click_save(self):
        self.safe_click(self.SAVE_BTN)

    def create_schedule_report(
            self,
            report_name,
            file_format,
            mail_time,
            duration,
            manufacturer_required=False
    ):
        self.select_report(report_name)

        if manufacturer_required:
            self.select_manufacturer()

        self.select_format(file_format)
        self.select_mail_time(mail_time)
        self.select_duration(duration)
        self.click_save()