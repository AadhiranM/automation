from selenium.webdriver.common.by import By
from pages.common.base_page import BasePage


class SAManufacturerCreatePage(BasePage):

    EMAIL = (By.NAME, "email")
    TEMP_PASSWORD = (By.NAME, "temp_password_masked")  # readonly
    COMPANY_NAME = (By.NAME, "company_name")

    SAVE_BTN = (By.XPATH, "//button[normalize-space()='Save']")
    CLOSE_BTN = (By.CSS_SELECTOR, "button.btn-close")

    SUCCESS_TOAST = (By.XPATH, "//div[contains(text(),'successfully')]")
    ERROR_EMAIL = (By.ID, "error-email")
    ERROR_COMPANY = (By.ID, "error-company_name")

    def fill_email(self, email):
        self.type(self.EMAIL, email)

    def fill_company_name(self, name):
        self.type(self.COMPANY_NAME, name)

    def submit(self):
        self.click(self.SAVE_BTN)

    def wait_for_success(self):
        self.wait(self.SUCCESS_TOAST)

    def is_email_error_visible(self):
        return self.is_visible(self.ERROR_EMAIL)

    def is_company_error_visible(self):
        return self.is_visible(self.ERROR_COMPANY)
