from selenium.webdriver.common.by import By
from pages.common.base_page import BasePage

class BusinessInfoPage(BasePage):

    COMPANY_NAME = (By.NAME, "company_name")
    BUSINESS_EMAIL = (By.NAME, "business_email")

    SEND_OTP = (By.XPATH, "//button[contains(text(),'Send OTP')]")
    OTP_INPUT = (By.NAME, "business_email_otp")
    VERIFY_BTN = (By.XPATH, "//button[contains(text(),'Verify')]")

    NEXT_BTN = (By.XPATH, "//button[normalize-space()='Next']")

    def fill_basic_details(self, company):
        self.type(self.COMPANY_NAME, company)

    def send_and_verify_otp(self, otp="123456"):
        self.click(self.SEND_OTP)
        self.type(self.OTP_INPUT, otp)
        self.click(self.VERIFY_BTN)

    def go_next(self):
        self.click(self.NEXT_BTN)
