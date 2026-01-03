from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from pages.common.base_page import BasePage


class SAManufacturerFilterPage(BasePage):

    # ---------------- FILTER DRAWER ----------------
    FILTER_BTN = (By.XPATH, "//button[contains(.,'Filters')]")
    FILTER_DRAWER = (By.CLASS_NAME, "offcanvas-end")

    # ---------------- INPUT FIELDS ----------------
    COMPANY_NAME = (By.ID, "name")
    BUSINESS_EMAIL = (By.ID, "email")
    PAN_NUMBER = (By.ID, "pan_no")
    APPROVAL_STATUS = (By.ID, "approval_status")

    # ---------------- BUTTONS ----------------
    APPLY_BTN = (By.XPATH, "//button[normalize-space()='Apply']")
    CLEAR_BTN = (By.XPATH, "//button[normalize-space()='Clear Filter']")

    # ---------------- TABLE ----------------
    FIRST_ROW = (By.XPATH, "//table[@id='crudTable']//tbody/tr")
    NO_DATA_ROW = (By.XPATH, "//td[contains(@class,'dataTables_empty')]")

    # ---------------- NAVIGATION ----------------
    def open_filter_drawer(self):
        self.click(self.FILTER_BTN)
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.FILTER_DRAWER)
        )

    # ---------------- SETTERS ----------------
    def set_company_name(self, value):
        self.type(self.COMPANY_NAME, value)

    def set_business_email(self, value):
        self.type(self.BUSINESS_EMAIL, value)

    def set_pan_number(self, value):
        self.type(self.PAN_NUMBER, value)

    def select_approval_status(self, text):
        dropdown = self.wait(self.APPROVAL_STATUS)
        Select(dropdown).select_by_visible_text(text)

    # ---------------- ACTIONS ----------------
    def click_apply(self):
        self.click(self.APPLY_BTN)
        self.wait_for_results()

    def click_clear(self):
        self.click(self.CLEAR_BTN)
        self.wait_for_clear()

    # ---------------- STATES ----------------
    def is_apply_enabled(self):
        return self.driver.find_element(*self.APPLY_BTN).is_enabled()

    def is_clear_enabled(self):
        return self.driver.find_element(*self.CLEAR_BTN).is_enabled()

    # ---------------- TABLE HELPERS ----------------
    def wait_for_results(self):
        WebDriverWait(self.driver, 10).until(
            lambda d: d.find_elements(*self.FIRST_ROW)
            or d.find_elements(*self.NO_DATA_ROW)
        )

    def is_row_present(self):
        return len(self.driver.find_elements(*self.FIRST_ROW)) > 0

    def is_no_data_displayed(self):
        return len(self.driver.find_elements(*self.NO_DATA_ROW)) > 0

    # ---------------- CLEAR FILTER VALIDATIONS ----------------
    def wait_for_clear(self):
        WebDriverWait(self.driver, 10).until(
            lambda d: not d.find_element(*self.APPLY_BTN).is_enabled()
        )

    def is_company_name_empty(self):
        return self.get_value(self.COMPANY_NAME) == ""

    def is_business_email_empty(self):
        return self.get_value(self.BUSINESS_EMAIL) == ""

    def is_pan_number_empty(self):
        return self.get_value(self.PAN_NUMBER) == ""

    def is_approval_status_default(self):
        dropdown = Select(self.wait(self.APPROVAL_STATUS))
        return dropdown.first_selected_option.text == "Select Approval Status"
