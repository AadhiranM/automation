from selenium.webdriver.common.by import By

from pages.common.base_page import BasePage

class SAManufacturerServicePage(BasePage):

    SERVICE_MANAGEMENT = (
        By.XPATH,
        "//a[normalize-space()='Service Management']"
    )

    CHECK_ALL_BTN = (
        By.XPATH,
        "//button[contains(text(),'Check All')]"
    )

    SUBMIT_BTN = (
        By.XPATH,
        "//button[contains(text(),'Submit')]"
    )

    SERVICE_CHECKBOXES = (
        By.XPATH,
        "//input[@type='checkbox']"
    )

    BACK_BTN = (
        By.ID,
        "globalBackButton"
    )


    def check_all_services(self):
        self.click(self.CHECK_ALL_BTN)

    def submit_services(self):
        self.click(self.SUBMIT_BTN)

    def all_services_checked(self):
        checkboxes = self.driver.find_elements(*self.SERVICE_CHECKBOXES)
        return all(cb.is_selected() for cb in checkboxes)

    def click_back(self):
        self.click(self.BACK_BTN)