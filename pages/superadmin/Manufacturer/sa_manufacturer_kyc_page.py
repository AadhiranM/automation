from selenium.webdriver.common.by import By
from pages.common.base_page import BasePage

class KYCPage(BasePage):

    FULL_NAME = (By.NAME, "full_name")
    MOBILE = (By.NAME, "mobile")

    SEND_OTP = (By.XPATH, "//button[contains(text(),'Send OTP')]")
    OTP_INPUT = (By.NAME, "mobile_otp")
    VERIFY_BTN = (By.XPATH, "//button[contains(text(),'Verify')]")

    NEXT_BTN = (By.XPATH, "//button[normalize-space()='Next']")

    def fill_kyc(self, name, mobile):
        self.type(self.FULL_NAME, name)
        self.type(self.MOBILE, mobile)

    def verify_mobile_otp(self, otp="123456"):
        self.click(self.SEND_OTP)
        self.type(self.OTP_INPUT, otp)
        self.click(self.VERIFY_BTN)

    def go_next(self):
        self.click(self.NEXT_BTN)
