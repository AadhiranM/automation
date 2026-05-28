from pages.common.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


class SAScheduledReportsCreatePage(BasePage):

    REPORT_DROPDOWN = (
        By.XPATH,
        "//span[@id='select2-schedule_report_name-container']"
    )

    MANUFACTURER_DROPDOWN = (
        By.XPATH,
        "//label[contains(text(),'Manufacturer')]/following::div[contains(@class,'choices')][1]"
    )

    FORMAT_DROPDOWN = (
        By.XPATH,
        "//span[@id='select2-schedule_format-container']"
    )

    MAIL_TIME_DROPDOWN = (
        By.ID,
        "select2-mail_send_at-container"
    )

    DURATION_DROPDOWN = (
        By.ID,
        "select2-duration-container"
    )

    SAVE_BTN = (
        By.XPATH,
        "//button[contains(text(),'Save')]"
    )


    def select_report(self, report_name):
        self.select_select2(
            self.REPORT_DROPDOWN,
            report_name
        )


    def select_format(self, file_format):
        self.select_select2(
            self.FORMAT_DROPDOWN,
            file_format
        )

    def select_mail_time(self, mail_time):
        formatted_time = f"{int(mail_time):02d}:00"

        self.select_select2(
            self.MAIL_TIME_DROPDOWN,
            formatted_time
        )

    def select_duration(self, duration):
        self.select_select2(
            self.DURATION_DROPDOWN,
            duration
        )

    def select_manufacturer(self):
        wait = WebDriverWait(self.driver, 30)

        dropdown = wait.until(
            EC.element_to_be_clickable(self.MANUFACTURER_DROPDOWN)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            dropdown
        )
        time.sleep(1)

        ActionChains(self.driver).move_to_element(dropdown).click().perform()
        print("Manufacturer dropdown opened")
        time.sleep(2)

        active = self.driver.switch_to.active_element

        active.send_keys(Keys.ARROW_DOWN)
        time.sleep(1)

        active.send_keys(Keys.ENTER)
        time.sleep(2)

        print("Manufacturer selected")

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