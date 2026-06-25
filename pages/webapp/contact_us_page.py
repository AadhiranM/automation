from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from pages.common.base_page import BasePage


class ContactUsPage(BasePage):

    NAME = (By.ID, "name")
    PHONE = (By.ID, "phone")
    EMAIL = (By.ID, "email")
    COMPANY = (By.ID, "company")
    MESSAGE = (By.ID, "message")
    SUBMIT = (By.ID, "contactSubmit")

    SUCCESS_MSG = (
        By.XPATH,
        "//*[contains(text(),'success') or contains(text(),'Thank')]"
    )

    def open(self):
        super().open("https://digitathya.com/contact-us")

    def fill_form(self, name, phone, email, company, message):
        self.type(self.NAME, name)
        self.type(self.PHONE, phone)
        self.type(self.EMAIL, email)
        self.type(self.COMPANY, company)
        self.type(self.MESSAGE, message)

    def submit(self):
        self.click(self.SUBMIT)

    def get_success_message(self):
        return self.get_text(self.SUCCESS_MSG)

    # ---------------------------------------------------
    # Safe helper for negative scenarios
    # ---------------------------------------------------

    def is_success_message_displayed(self, timeout=3):
        try:
            self.wait(
                self.SUCCESS_MSG,
                timeout=timeout
            )
            return True
        except TimeoutException:
            return False

    def has_success_message(self):
        if self.is_success_message_displayed():
            return self.get_success_message()
        return ""