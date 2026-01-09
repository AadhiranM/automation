from selenium.webdriver.common.by import By
from pages.common.base_page import BasePage

class VerificationStatusPage(BasePage):

    STATUS_TEXT = (By.XPATH, "//h2[contains(text(),'Verification')]")

    def is_displayed(self):
        return self.is_visible(self.STATUS_TEXT)
