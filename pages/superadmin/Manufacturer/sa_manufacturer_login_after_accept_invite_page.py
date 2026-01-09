from selenium.webdriver.common.by import By
from pages.common.base_page import BasePage

class ManufacturerLoginPage(BasePage):

    EMAIL = (By.NAME, "email")
    PASSWORD = (By.NAME, "password")
    LOGIN_BTN = (By.XPATH, "//button[normalize-space()='Login']")

    def login(self, email, password):
        self.type(self.EMAIL, email)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BTN)
