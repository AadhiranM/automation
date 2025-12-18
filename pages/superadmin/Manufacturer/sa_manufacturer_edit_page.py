from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.common.base_page import BasePage


class SAManufacturerEditPage(BasePage):

    # --------- INPUT FIELDS ----------
    EMAIL = (By.NAME, "email")
    COMPANY_NAME = (By.NAME, "company_name")

    # --------- BUTTON ----------
    UPDATE_BTN = (By.XPATH, "//button[normalize-space()='Update']")

    # --------- PAGE LOAD ----------
    PAGE_MARKER = (By.XPATH, "//h5[normalize-space()='Edit Manufacturer']")

    def wait_for_page(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.PAGE_MARKER)
        )

    # --------- ACTIONS ----------
    def update_email(self, email):
        self.clear(self.EMAIL)
        self.type(self.EMAIL, email)

    def update_company_name(self, name):
        self.clear(self.COMPANY_NAME)
        self.type(self.COMPANY_NAME, name)

    def click_update(self):
        self.click(self.UPDATE_BTN)

    # --------- GETTERS ----------
    def get_email_value(self):
        return self.wait(self.EMAIL).get_attribute("value")

    def get_company_name_value(self):
        return self.wait(self.COMPANY_NAME).get_attribute("value")
