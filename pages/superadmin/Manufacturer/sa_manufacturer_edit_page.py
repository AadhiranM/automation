from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.common.base_page import BasePage


class SAManufacturerEditPage(BasePage):

    # ---------------- MODAL ----------------
    EDIT_MODAL = (By.ID, "showModal")

    # ---------------- INPUT FIELDS (MODAL SCOPED) ----------------
    EMAIL = (
        By.XPATH,
        "//div[@id='showModal' and contains(@class,'show')]//input[@name='email']"
    )

    COMPANY_NAME = (
        By.XPATH,
        "//div[@id='showModal' and contains(@class,'show')]//input[@name='company_name']"
    )

    # ---------------- BUTTON ----------------
    UPDATE_BTN = (
        By.XPATH,
        "//div[@id='showModal']//button[normalize-space()='Update']"
    )

    # ---------------- SUCCESS TOAST ----------------
    SUCCESS_TOAST = (
        By.XPATH,
        "//div[contains(text(),'updated successfully')]"
    )

    # ---------------- PAGE LOAD ----------------
    def wait_for_page(self):
        """Wait until Edit modal is visible"""
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(self.EDIT_MODAL)
        )

    # ---------------- ACTIONS ----------------
    def update_email(self, email):
        self.wait(self.EMAIL)
        self.clear(self.EMAIL)
        self.type(self.EMAIL, email)

    def update_company_name(self, name):
        self.wait(self.COMPANY_NAME)
        self.clear(self.COMPANY_NAME)
        self.type(self.COMPANY_NAME, name)

    def click_update(self):
        self.click(self.UPDATE_BTN)

    # ---------------- WAIT AFTER UPDATE ----------------
    def wait_for_update_success(self):
        """
        Some environments show toast,
        some directly close modal.
        Handle both safely.
        """
        WebDriverWait(self.driver, 15).until(
            lambda d:
            d.find_elements(*self.SUCCESS_TOAST) or
            not d.find_elements(*self.EDIT_MODAL)
        )

    def wait_for_modal_close(self):
        """Explicit wait if needed"""
        WebDriverWait(self.driver, 15).until(
            EC.invisibility_of_element_located(self.EDIT_MODAL)
        )

    # ---------------- GETTERS ----------------
    def get_email_value(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.EMAIL)
        ).get_attribute("value")

    def get_company_name_value(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.COMPANY_NAME)
        ).get_attribute("value")
