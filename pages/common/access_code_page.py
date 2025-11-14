from selenium.webdriver.common.by import By
from pages.common.base_page import BasePage

class AccessCodePage(BasePage):

    access_input = (By.XPATH, "//input[@placeholder='Enter Access Code']")
    submit_btn = (By.XPATH, "//button[contains(text(),'Submit')]")

    def enter_access_code(self, code):
        self.type(self.access_input, code)
        self.click(self.submit_btn)
