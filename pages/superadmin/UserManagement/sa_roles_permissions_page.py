import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.common.base_page import BasePage


class SARolesPermissionsPage(BasePage):

    CREATE_BTN = (
        By.XPATH,
        "//button[contains(.,'+ Create')]"
    )

    ROLE_NAME = (
        By.XPATH,
        "//input[@placeholder='Enter Role Name']"
    )

    USER_TYPE_DROPDOWN = (
        By.XPATH,
        "//label[contains(text(),'User Type')]/following::span[1]"
    )

    STATUS_DROPDOWN = (
        By.XPATH,
        "//label[contains(text(),'Status')]/following::span[1]"
    )

    CHECK_ALL_BTN = (
        By.XPATH,
        "//button[contains(.,'Check All')]"
    )

    SUBMIT_BTN = (
        By.XPATH,
        "//button[contains(text(),'Submit')]"
    )

    FIRST_ROW_ROLE_NAME = (
        By.XPATH,
        "//table/tbody/tr[1]/td[2]"
    )

    def goto_page(self):
        self.driver.get(
            "https://beta.digitathya.com/admin/role/create"
        )

    def click_create(self):
        self.safe_click(self.CREATE_BTN)

    def enter_role_name(self, role_name):
        self.enter_text(self.ROLE_NAME, role_name)

    def select_user_type(self, user_type):

        self.safe_click(self.USER_TYPE_DROPDOWN)

        time.sleep(2)

        search_box = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//input[@type='search']")
            )
        )

        search_box.send_keys(user_type)

        time.sleep(1)

        search_box.send_keys(Keys.ENTER)

        time.sleep(3)

    def select_status(self, status):

        self.safe_click(self.STATUS_DROPDOWN)

        option = (
            By.XPATH,
            f"//li[contains(text(),'{status}')]"
        )

        self.safe_click(option)

        time.sleep(2)

    def click_check_all(self):
        self.safe_click(self.CHECK_ALL_BTN)

        time.sleep(2)

    def click_submit(self):
        self.safe_click(self.SUBMIT_BTN)

    def get_first_row_role_name(self):
        return self.get_text(
            self.FIRST_ROW_ROLE_NAME
        ).strip()

    def create_role(self, role_name, user_type, status):
        self.enter_role_name(role_name)

        self.select_user_type(user_type)

        self.select_status(status)

        self.click_check_all()

        self.click_submit()