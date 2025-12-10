# File: pages/webapp/contact_us_page.py

from selenium.webdriver.common.by import By
from pages.common.base_page import BasePage

class ContactUsPage(BasePage):

    NAME = (By.ID, "name")
    PHONE = (By.ID, "phone")
    EMAIL = (By.ID, "email")
    COMPANY = (By.ID, "company")
    MESSAGE = (By.ID, "message")
    SUBMIT = (By.ID, "contactSubmit")
    FORM = (By.ID, "contactForm")

    SUCCESS_MSG = (By.XPATH, "//*[contains(text(),'success') or contains(text(),'Thank')]")

    # FINAL CORRECT OPEN METHOD
    def open(self, url="https://digitathya.com/contact-us"):
        super().open(url)

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
