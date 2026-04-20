from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.common.base_page import BasePage


class SAProductCreateVideoPage(BasePage):

    CREATE_BTN = (By.XPATH, "//button[contains(text(),'Create Product')]")

    SUCCESS_TOAST = (
        By.XPATH,
        "//div[contains(@class,'toast') or contains(@class,'toastify')]"
    )

    # =========================
    # PAGE LOAD
    # =========================
    def wait_for_page(self):
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(self.CREATE_BTN)
        )

    # =========================
    # ACTION
    # =========================
    def create_product(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.CREATE_BTN)
        ).click()

    # =========================
    # VALIDATION
    # =========================
    def is_product_created_successfully(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.SUCCESS_TOAST)
            )
            return True
        except:
            return False