import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.support.ui import (
    WebDriverWait
)

from selenium.webdriver.support import expected_conditions as EC

from pages.common.base_page import BasePage


class SAManufacturerFilterPage(BasePage):

    # =====================================================
    # FILTER PANEL
    # =====================================================

    FILTER_BTN = (
        By.ID,
        "filterToggleBtn"
    )

    FILTER_DRAWER = (
        By.CLASS_NAME,
        "offcanvas-end"
    )

    # =====================================================
    # FILTER FIELDS
    # =====================================================

    COMPANY_NAME = (
        By.ID,
        "name"
    )

    BUSINESS_EMAIL = (
        By.ID,
        "email"
    )

    PAN_NUMBER = (
        By.ID,
        "pan_no"
    )

    APPROVAL_STATUS_DROPDOWN = (
        By.XPATH,
        "//div[contains(@class,'choices__placeholder') and contains(text(),'Select Approval Status')]"
    )

    # =====================================================
    # BUTTONS
    # =====================================================

    APPLY_BTN = (
        By.XPATH,
        "//button[normalize-space()='Apply']"
    )

    CLEAR_BTN = (
        By.XPATH,
        "//button[contains(text(),'Clear Filter')]"
    )

    # =====================================================
    # TABLE
    # =====================================================

    FIRST_ROW = (
        By.XPATH,
        "//table/tbody/tr[1]"
    )

    NO_DATA_ROW = (
        By.XPATH,
        "//td[contains(@class,'dataTables_empty')]"
    )

    # =====================================================
    # OPEN FILTER
    # =====================================================

    def open_filter_panel(self):

        self.click(
            self.FILTER_BTN
        )

        WebDriverWait(
            self.driver,
            10
        ).until(
            EC.visibility_of_element_located(
                self.COMPANY_NAME
            )
        )

    # =====================================================
    # FILTER METHODS
    # =====================================================

    def filter_by_company_name(
            self,
            company_name
    ):

        self.open_filter_panel()

        self.type(
            self.COMPANY_NAME,
            company_name
        )

        self.click_apply()

    def filter_by_business_email(
            self,
            email
    ):

        self.open_filter_panel()

        self.type(
            self.BUSINESS_EMAIL,
            email
        )

        self.click_apply()

    def filter_by_pan_number(
            self,
            pan_number
    ):

        self.open_filter_panel()

        self.type(
            self.PAN_NUMBER,
            pan_number
        )

        self.click_apply()

    def filter_by_approval_status(self):
        self.open_filter_panel()

        dropdown = WebDriverWait(
            self.driver,
            20
        ).until(
            EC.element_to_be_clickable(
                self.APPROVAL_STATUS_DROPDOWN
            )
        )

        dropdown.click()

        approved_option = WebDriverWait(
            self.driver,
            20
        ).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//li[contains(@class,'select2-results__option') "
                    "and normalize-space()='Approved']"
                )
            )
        )

        approved_option.click()

        self.click_apply()

    # =====================================================
    # BUTTON ACTIONS
    # =====================================================

    def click_apply(self):

        self.click(
            self.APPLY_BTN
        )

        self.wait_for_results()

    def click_clear(self):

        self.click(
            self.CLEAR_BTN
        )

        self.wait_for_clear()

    # =====================================================
    # STATES
    # =====================================================

    def is_apply_enabled(self):

        return self.driver.find_element(
            *self.APPLY_BTN
        ).is_enabled()

    def is_clear_enabled(self):

        return self.driver.find_element(
            *self.CLEAR_BTN
        ).is_enabled()

    # =====================================================
    # RESULTS
    # =====================================================

    def wait_for_results(self):

        WebDriverWait(
            self.driver,
            15
        ).until(
            lambda d:
            d.find_elements(*self.FIRST_ROW)
            or
            d.find_elements(*self.NO_DATA_ROW)
        )

    def is_row_present(self):

        return len(
            self.driver.find_elements(
                *self.FIRST_ROW
            )
        ) > 0

    def is_no_data_displayed(self):

        return len(
            self.driver.find_elements(
                *self.NO_DATA_ROW
            )
        ) > 0

    # =====================================================
    # CLEAR VALIDATION
    # =====================================================

    def wait_for_clear(self):

        WebDriverWait(
            self.driver,
            10
        ).until(
            lambda d:
            not d.find_element(
                *self.APPLY_BTN
            ).is_enabled()
        )

    def is_company_name_empty(self):

        return self.get_value(
            self.COMPANY_NAME
        ) == ""

    def is_business_email_empty(self):

        return self.get_value(
            self.BUSINESS_EMAIL
        ) == ""

    def is_pan_number_empty(self):

        return self.get_value(
            self.PAN_NUMBER
        ) == ""