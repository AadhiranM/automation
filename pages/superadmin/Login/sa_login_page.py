from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from pages.common.base_page import BasePage


class SuperAdminLoginPage(BasePage):

    # ---------- LOCATORS ----------
    LOGIN_BTN = (By.XPATH, "//button[contains(text(),'Login')]")
    USER_NAME = (By.XPATH, "//span[contains(@class,'user-name-text')]")
    EMAIL = (By.NAME, "email")
    PASSWORD = (By.NAME, "password")

    ERROR_MESSAGE = (By.XPATH, "//div[contains(@class,'error') or contains(@class,'pwd-incrt')]/p")

    DASHBOARD_TITLE = (By.XPATH, "//p[normalize-space()='Dashboard']")

    # ---------- FIELD ACTIONS ----------

    def get_logged_in_username(self):
        return self.get_text(self.USER_NAME).strip()

    def enter_email(self, email):
        self.type(self.EMAIL, email)

    def enter_password(self, password):
        self.type(self.PASSWORD, password)

    # ---------- LOGIN BUTTON BEHAVIOR ----------
    def is_login_button_enabled(self):
        return self.driver.find_element(*self.LOGIN_BTN).is_enabled()

    def click_login(self):
        self.click(self.LOGIN_BTN)

    # ---------- FULL LOGIN WORKFLOW ----------
    def login(self, email, password):
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

        # Wait for dashboard
        WebDriverWait(self.driver, 10).until(
            lambda d: self.is_dashboard_loaded()
        )

        # Return username
        return self.get_logged_in_username()

    # ---------- VALIDATION HELPERS ----------
    def get_error_message(self):
        return self.get_text(self.ERROR_MESSAGE)

    def is_dashboard_loaded(self):
        return self.is_visible(self.DASHBOARD_TITLE)
