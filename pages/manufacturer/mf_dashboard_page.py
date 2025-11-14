from selenium.webdriver.common.by import By
from pages.common.base_page import BasePage

class ManufacturerDashboard(BasePage):
    dashboard_title = (By.XPATH, "//h1[contains(text(),'Dashboard')]")

    def is_loaded(self):
        return "Dashboard" in self.get_text(self.dashboard_title)
