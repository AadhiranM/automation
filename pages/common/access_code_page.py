from selenium.webdriver.common.by import By
from pages.common.base_page import BasePage

class AccessCodePage(BasePage):

    ACCESS_CODE_INPUT = (By.NAME, "access_code")
    SUBMIT_BTN = (By.XPATH, "//button[@type='submit' and contains(text(),'Submit')]")

    def is_loaded(self):
        """Checks if the restricted access page is displayed."""
        return "accessCheck" in self.driver.current_url

    def enter_access_code(self, code):
        self.type(self.ACCESS_CODE_INPUT, code)

    def submit(self):
        self.click(self.SUBMIT_BTN)

    def enter_and_submit(self, code):
        """Main method used by conftest to clear access page."""
        self.enter_access_code(code)
        self.submit()
