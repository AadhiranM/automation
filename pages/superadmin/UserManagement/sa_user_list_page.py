from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from pages.common.base_page import BasePage
import time


class SAUserListPage(BasePage):

    # =====================================================
    # SEARCH
    # =====================================================

    SEARCH_BOX = (By.ID, "search-vale")
    SEARCH_BTN = (By.ID, "search-btn")

    # =====================================================
    # STATUS FILTER
    # =====================================================

    STATUS_DROPDOWN = (
        By.XPATH,
        "//span[contains(@class,'selection')]//span[contains(text(),'Select Status')]"
    )

    # =====================================================
    # TABLE
    # =====================================================

    FIRST_ROW = (
        By.XPATH,
        "//table/tbody/tr[1]"
    )

    NO_DATA = (
        By.XPATH,
        "//td[contains(@class,'dataTables_empty')]"
    )

    FIRST_ROW_NAME = (
        By.XPATH,
        "//table/tbody/tr[1]/td[2]"
    )

    FIRST_MANUFACTURER = (
        By.XPATH,
        "//table/tbody/tr[1]/td[3]"
    )

    FIRST_USERS = (
        By.XPATH,
        "//table/tbody/tr[1]/td[4]"
    )


    # =====================================================
    # ENTRIES
    # =====================================================

    ENTRIES_DROPDOWN = (
        By.NAME,
        "crudTable_length"
    )

    # =====================================================
    # PAGINATION
    # =====================================================

    NEXT_BTN = (
        By.XPATH,
        "//a[normalize-space()='Next']"
    )

    PREVIOUS_BTN = (
        By.XPATH,
        "//a[normalize-space()='Previous']"
    )

    PAGE_NUMBER = "//a[normalize-space()='{}']"

    # =====================================================
    # PAGE LOAD
    # =====================================================

    VIEW_OPTION = (
        By.XPATH,
        "//ul[contains(@class,'show')]//a[contains(@href,'/show')]"
    )


    FIRST_ROW_THREE_DOTS = (
        By.XPATH,
        "//table[@id='crudTable']/tbody/tr[1]/td[last()]//button[contains(@class,'dropdown')]"
    )

    EDIT_OPTION = (
        By.XPATH,
        "//ul[contains(@class,'dropdown-menu') and contains(@class,'show')]//button[contains(@class,'edit-report-btn')]"
    )

    EDIT_NAME_INPUT = (
        By.NAME,
        "name"
    )
    UPDATE_BTN = (
        By.XPATH,
        "//button[contains(text(),'Submit')]"
    )

    ROLE_PERMISSION_OPTION = (
        By.XPATH,
        "//a[contains(.,'Role & Permissions')]"
    )

    SUSPEND_OPTION = (
        By.XPATH,
        "//a[contains(.,'Suspend')] | //button[contains(.,'Suspend')] | //li[contains(.,'Suspend')]"
    )

    ACTIVATE_OPTION = (
        By.XPATH,
        "//a[contains(.,'Activate')]"
    )

    CONFIRM_SUSPEND_BTN = (
        By.XPATH,
        "//button[contains(text(),'Suspend')]"
    )

    CONFIRM_ACTIVATE_BTN = (
        By.XPATH,
        "//button[contains(text(),'Activate')]"
    )

    FIRST_ROW_STATUS = (
        By.XPATH,
        "(//td[contains(@class,'sorting_1')]/following-sibling::td//span)[1]"
    )

    FIRST_ROW_ACTIVE_STATUS = (
        By.XPATH,
        "//table/tbody/tr[1]//span[contains(text(),'Active')]"
    )

    FIRST_ROW_SUSPENDED_STATUS = (
        By.XPATH,
        "//table/tbody/tr[1]//span[contains(text(),'Suspended')]"
    )
    def goto_page(self):

        self.driver.get(
            "https://beta.digitathya.com/admin/user?reset_filters=1"
        )

        self.wait_for_results()

    def get_first_manufacturer(self):
        return self.get_text(
            self.FIRST_MANUFACTURER
        ).strip()

    def get_first_users_count(self):
        return self.get_text(
            self.FIRST_USERS
        ).strip()

    # =====================================================
    # WAIT
    # =====================================================
    def open_first_row_actions(self):

        self.safe_click(self.FIRST_ROW_THREE_DOTS)

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//ul[contains(@class,'dd_action') and contains(@class,'show')]"
            ))
        )

    def click_three_dots(self):

        self.safe_click(self.FIRST_ROW_THREE_DOTS)

        time.sleep(2)

    def click_suspend(self):

        time.sleep(2)

        suspend_btn = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                self.SUSPEND_OPTION
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            suspend_btn
        )

        time.sleep(2)

    def click_status_action(self):

        self.click_three_dots()

        time.sleep(2)

        try:
            suspend = self.driver.find_element(
                By.XPATH,
                "//*[contains(text(),'Suspend')]"
            )

            suspend.click()

            return "Suspended"

        except:

            activate = self.driver.find_element(
                By.XPATH,
                "//*[contains(text(),'Activate')]"
            )

            activate.click()

            return "Active"
    def confirm_suspend(self):

        self.safe_click(self.CONFIRM_SUSPEND_BTN)

        time.sleep(5)

    def click_activate(self):

        # Re-open dropdown
        self.click_three_dots()

        activate_btn = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//a[contains(.,'Activate')]"
            ))
        )

        self.driver.execute_script(
            "arguments[0].click();",
            activate_btn
        )

        time.sleep(2)

    def click_view(self):

        self.open_first_row_actions()

        wait = WebDriverWait(self.driver, 10)

        view = wait.until(
            EC.visibility_of_element_located(self.VIEW_OPTION)
        )

        self.driver.execute_script(
            "arguments[0].click();",
            view
        )

        wait.until(
            lambda d: "/show" in d.current_url
        )

        print(self.driver.current_url)

    def click_edit(self):
        # Open 3 dots menu
        self.safe_click(self.FIRST_ROW_THREE_DOTS)

        time.sleep(2)

        # Click Edit using direct xpath
        edit_btn = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//a[contains(.,'Edit')]"
            ))
        )

        self.driver.execute_script(
            "arguments[0].click();",
            edit_btn
        )

        time.sleep(3)

    def suspend_user(self):
        self.open_first_row_actions()

        self.safe_click(self.SUSPEND_OPTION)

        time.sleep(2)

        self.safe_click(self.CONFIRM_SUSPEND_BTN)

        time.sleep(4)

    def activate_user(self):
        self.open_first_row_actions()

        self.safe_click(self.ACTIVATE_OPTION)

        time.sleep(2)

        self.safe_click(self.CONFIRM_ACTIVATE_BTN)

        time.sleep(4)

    def is_element_present(self, locator):

        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(locator)
            )
            return True

        except:
            return False

    def get_first_row_status(self):

        time.sleep(4)

        if self.is_element_present(self.FIRST_ROW_ACTIVE_STATUS):
            return "Active"

        elif self.is_element_present(self.FIRST_ROW_SUSPENDED_STATUS):
            return "Suspended"

        return "Unknown"

    def click_role_permissions(self):

        # Re-open 3 dots menu
        self.click_three_dots()

        role_btn = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//a[contains(.,'Role & Permissions')]"
            ))
        )

        self.driver.execute_script(
            "arguments[0].click();",
            role_btn
        )

        time.sleep(3)
    def wait_for_results(self):

        WebDriverWait(self.driver, 15).until(
            lambda d:
            d.find_elements(*self.FIRST_ROW)
            or
            d.find_elements(*self.NO_DATA)
        )

    # =====================================================
    # SEARCH
    # =====================================================

    def search_first_user(self):

        user_name = self.get_text(
            self.FIRST_ROW_NAME
        ).strip()

        self.type(
            self.SEARCH_BOX,
            user_name
        )

        self.click(self.SEARCH_BTN)

        self.wait_for_results()

        return user_name

    # =====================================================
    # STATUS FILTER
    # =====================================================

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

        time.sleep(1)

        ActionChains(self.driver)\
            .move_to_element(dropdown)\
            .click()\
            .perform()

        print("Status dropdown clicked")

        time.sleep(2)

        option = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                f"//li[contains(text(),'{status}')]"
            ))
        )

        ActionChains(self.driver)\
            .move_to_element(option)\
            .click()\
            .perform()

        print(f"Selected status = {status}")

        time.sleep(3)

        self.wait_for_results()

    # =====================================================
    # ENTRIES
    # =====================================================

    def set_entries_per_page(self, value):

        dropdown = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                self.ENTRIES_DROPDOWN
            )
        )

        Select(dropdown).select_by_value(str(value))

        self.wait_for_results()

    # =====================================================
    # PAGINATION
    # =====================================================

    def click_next(self):

        next_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                self.NEXT_BTN
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            next_btn
        )

        self.wait_for_results()

    def click_previous(self):

        prev_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                self.PREVIOUS_BTN
            )
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

    # =====================================================
    # VALIDATIONS
    # =====================================================

    def is_row_present(self):

        return len(
            self.driver.find_elements(*self.FIRST_ROW)
        ) > 0

    def has_no_data(self):

        return len(
            self.driver.find_elements(*self.NO_DATA)
        ) > 0

    def search_user(self, user_name):
        self.type(self.SEARCH_BOX, user_name)

        time.sleep(3)

    def get_first_row_name(self):
        return self.get_text(
            self.FIRST_ROW_NAME
        ).strip()

    def update_user_name(self, new_name):
        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(self.EDIT_NAME_INPUT)
        )

        name_field = self.driver.find_element(*self.EDIT_NAME_INPUT)

        name_field.clear()

        time.sleep(1)

        name_field.send_keys(new_name)

        time.sleep(1)

        self.safe_click(self.UPDATE_BTN)

        time.sleep(4)