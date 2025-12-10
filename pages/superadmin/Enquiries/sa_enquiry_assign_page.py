from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.common.base_page import BasePage


class SAEnquiryAssignPage(BasePage):

    # ---------------- LOCATORS ----------------
    USER_DROPDOWN = (By.ID, "assigned_to")

    SUBMIT_BUTTON = (By.XPATH, "//button[normalize-space()='Submit']")
    CLOSE_ICON = (By.XPATH, "//button[@aria-label='Close this dialog']")

    SUCCESS_MESSAGE = (
        By.XPATH,
        "//div[@id='swal2-html-container' and contains(text(),'assigned successfully')]"
    )
    SUCCESS_OK_BUTTON = (By.XPATH, "//button[contains(@class,'swal2-confirm')]")

    ERROR_POPUP = (
        By.XPATH,
        "//div[contains(@id,'swal2-html') and contains(text(),'error')]"
    )

    # ---------------- ACTION METHODS ----------------

    def select_internal_user(self, name: str):
        dropdown = self.is_visible(self.USER_DROPDOWN)
        Select(dropdown).select_by_visible_text(name)

    def submit(self):
        self.click(self.SUBMIT_BUTTON)

    def confirm_success(self):
        self.is_visible(self.SUCCESS_MESSAGE)
        self.click(self.SUCCESS_OK_BUTTON)

    def wait_for_error_popup(self):
        return self.is_visible(self.ERROR_POPUP)

    def close_modal(self):
        self.click(self.CLOSE_ICON)

    def assign_user(self, name: str):
        """Full flow: select user → submit → confirm success popup"""
        self.select_internal_user(name)
        self.submit()
        self.confirm_success()
