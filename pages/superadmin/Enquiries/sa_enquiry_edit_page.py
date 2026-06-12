# pages/superadmin/Enquiries/sa_enquiry_edit_page.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.common.base_page import BasePage


class SAEnquiryEditPage(BasePage):

    # -------------------------
    # FORM FIELDS
    # -------------------------

    STATUS = (
        By.NAME,
        "status"
    )

    NAME = (
        By.NAME,
        "name"
    )

    PHONE = (
        By.NAME,
        "contact_no_display"
    )

    EMAIL = (
        By.NAME,
        "business_email"
    )

    COMPANY = (
        By.NAME,
        "company"
    )

    MESSAGE = (
        By.NAME,
        "message"
    )

    # -------------------------
    # BUTTONS
    # -------------------------

    SAVE_BUTTON = (
        By.XPATH,
        "//button[contains(text(),'Submit')]"
    )

    CANCEL_BUTTON = (
        By.XPATH,
        "//button[contains(text(),'Cancel')]"
    )

    # -------------------------
    # SUCCESS TOAST
    # -------------------------

    SUCCESS_POPUP = (
        By.CSS_SELECTOR,
        "div.toastify"
    )

    # -------------------------
    # PAGE LOAD
    # -------------------------

    def wait_until_loaded(self):

        WebDriverWait(
            self.driver,
            15
        ).until(
            EC.visibility_of_element_located(
                self.STATUS
            )
        )

    # -------------------------
    # STATUS METHODS
    # -------------------------

    def get_current_status(self):

        dropdown = Select(
            self.driver.find_element(
                *self.STATUS
            )
        )

        return (
            dropdown.first_selected_option.text
            .strip()
        )

    def get_all_statuses(self):

        dropdown = Select(
            self.driver.find_element(
                *self.STATUS
            )
        )

        return [
            option.text.strip()
            for option in dropdown.options
            if option.text.strip()
        ]

    def get_next_status(self):

        current_status = (
            self.get_current_status()
        )

        all_statuses = (
            self.get_all_statuses()
        )

        for status in all_statuses:

            if status != current_status:

                return status

        return current_status

    def change_status(
            self,
            status
    ):

        dropdown = Select(
            self.driver.find_element(
                *self.STATUS
            )
        )

        dropdown.select_by_visible_text(
            status
        )

    # -------------------------
    # VALIDATIONS
    # -------------------------

    def is_submit_enabled(self):

        button = self.driver.find_element(
            *self.SAVE_BUTTON
        )

        return button.is_enabled()

    # -------------------------
    # ACTIONS
    # -------------------------

    def click_save(self):

        self.click(
            self.SAVE_BUTTON
        )

    def click_cancel(self):

        self.click(
            self.CANCEL_BUTTON
        )

    # -------------------------
    # SUCCESS MESSAGE
    # -------------------------

    def wait_success(self):

        WebDriverWait(
            self.driver,
            10
        ).until(
            EC.visibility_of_element_located(
                self.SUCCESS_POPUP
            )
        )

        WebDriverWait(
            self.driver,
            10
        ).until(
            EC.invisibility_of_element_located(
                self.SUCCESS_POPUP
            )
        )

    # -------------------------
    # READ DATA
    # -------------------------

    def get_name(self):

        return self.driver.find_element(
            *self.NAME
        ).get_attribute(
            "value"
        ).strip()

    def get_email(self):

        return self.driver.find_element(
            *self.EMAIL
        ).get_attribute(
            "value"
        ).strip()

    def get_company(self):

        return self.driver.find_element(
            *self.COMPANY
        ).get_attribute(
            "value"
        ).strip()

    def get_message(self):

        return self.driver.find_element(
            *self.MESSAGE
        ).get_attribute(
            "value"
        ).strip()