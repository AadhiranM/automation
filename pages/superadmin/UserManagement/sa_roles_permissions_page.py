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
    FIRST_MANUFACTURER = (
        By.XPATH,
        "//table/tbody/tr[1]/td[3]"
    )

    FIRST_USERS = (
        By.XPATH,
        "//table/tbody/tr[1]/td[4]"
    )
    ROLE_NAME = (
        By.XPATH,
        "//input[@placeholder='Enter Role Name']"
    )

    USER_TYPE_DROPDOWN = (
        By.XPATH,
        "//span[@role='combobox' and @aria-labelledby='select2-idSelectuser-container']"
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

    MANUFACTURER_CHECKBOX = (
        By.XPATH,
        "//input[@type='checkbox' and @name='role_create_under_manufacturer']"
    )

    MANUFACTURER_DROPDOWN = (
        By.XPATH,
        "//select[@id='role_selected_manufacturer_id']/following-sibling::div[contains(@class,'choices')]"
    )

    MANUFACTURER_SEARCH = (
        By.XPATH,
        "//span[contains(@class,'select2-container')]//input[@type='search']"
    )
    ROLE_NAME_COL = (
        By.XPATH,
        "//table/tbody/tr[1]/td[2]"
    )

    MANUFACTURER_COL = (
        By.XPATH,
        "//table/tbody/tr[1]/td[3]"
    )

    USERS_COL = (
        By.XPATH,
        "//table/tbody/tr[1]/td[4]"
    )

    ROLE_SEARCH = (
        By.XPATH,
        "//input[contains(@placeholder,'Role Name')]"
    )

    SEARCH_BTN = (
        By.XPATH,
        "//button[@id='search-btn'] | //button[contains(@class,'search')]"
    )

    def get_first_manufacturer(self):
        return self.get_text(self.MANUFACTURER_COL).strip()

    def get_first_users_count(self):
        return self.get_text(self.USERS_COL).strip()

    def goto_page(self):
        self.driver.get(
            "https://beta.digitathya.com/admin/role/create"
        )

    def goto_list_page(self):
        # Roles list page
        self.driver.get(
            "https://beta.digitathya.com/admin/role?reset_filters=1"
        )
    def click_create(self):
        self.safe_click(self.CREATE_BTN)

    def enter_role_name(self, role_name):
        self.enter_text(self.ROLE_NAME, role_name)

    def select_user_type(self):
        self.safe_click(self.USER_TYPE_DROPDOWN)

        search = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//input[@class='select2-search__field']"
                )
            )
        )

        time.sleep(1)

        search.send_keys(Keys.ENTER)

        time.sleep(2)

    def select_status(self, status):

        self.safe_click(self.STATUS_DROPDOWN)

        option = (
            By.XPATH,
            f"//li[contains(text(),'{status}')]"
        )

        self.safe_click(option)
        WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(self.CHECK_ALL_BTN)
        )

        time.sleep(2)

    def click_check_all(self):
        WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(self.CHECK_ALL_BTN)
        )

        self.safe_click(self.CHECK_ALL_BTN)

        time.sleep(2)

    def click_submit(self):
        self.safe_click(self.SUBMIT_BTN)

    def get_first_row_role_name(self):
        return self.get_text(
            self.FIRST_ROW_ROLE_NAME
        ).strip()

    def create_role(self, role_name, status):
        self.enter_role_name(role_name)

        self.select_manufacturer()  # selects first manufacturer

        self.select_user_type()  # selects first user type

        self.select_status(status)

        self.click_check_all()

        self.click_submit()

    def select_manufacturer(self):
        self.safe_click(self.MANUFACTURER_CHECKBOX)

        self.safe_click(self.MANUFACTURER_DROPDOWN)

        search = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//input[@type='search']")
            )
        )

        search.send_keys(Keys.ENTER)

        # WAIT HERE
        WebDriverWait(self.driver, 20).until(
            lambda d: d.find_element(*self.USER_TYPE_DROPDOWN).is_enabled()
        )

    def search_role(self, role_name):
        self.enter_text(self.ROLE_SEARCH, role_name)

        time.sleep(1)

        self.driver.find_element(*self.ROLE_SEARCH).send_keys(Keys.ENTER)

        WebDriverWait(self.driver, 20).until(
            lambda d: self.get_first_row_role_name() == role_name
        )