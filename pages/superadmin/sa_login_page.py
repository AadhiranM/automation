from selenium.webdriver.common.by import By
from pages.common.base_page import BasePage

class SuperAdminLogin(BasePage):

    username_input = (By.XPATH, "//input[@placeholder='Enter your email.']")
    password_input = (By.XPATH, "//input[@placeholder='Enter your login password']")
    login_btn = (By.XPATH, "//button[contains(text(),'Login')]")

    def login(self, username, password):
        self.type(self.username_input, username)
        self.type(self.password_input, password)
        self.click(self.login_btn)
