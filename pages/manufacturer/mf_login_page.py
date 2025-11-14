from selenium.webdriver.common.by import By
from pages.common.base_page import BasePage

class ManufacturerLogin(BasePage):
    username_input = (By.ID, "email")
    password_input = (By.ID, "password")
    login_btn = (By.XPATH, "//button[contains(text(),'Login')]")  # change if different text

    def login(self, username, password):
        self.type(self.username_input, username)
        self.type(self.password_input, password)
        self.click(self.login_btn)
