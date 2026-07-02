from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.common.base_page import BasePage


class SAProductCreateVideoPage(BasePage):

    CREATE_BTN = (
        By.XPATH,
        "//button[.//span[contains(text(),'Create Product')]]"
    )

    # 🔥 COMMON TOAST (handles both success & error)
    TOAST_MSG = (
        By.XPATH,
        "//div[contains(@class,'toastify')]"
    )

    def wait_for_page(self):
        WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(self.CREATE_BTN)
        )

    def create_product(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.CREATE_BTN)
        ).click()

    # ✅ GET ACTUAL MESSAGE
    def get_toast_message(self):
        wait = WebDriverWait(self.driver, 10)

        toast = wait.until(
            EC.visibility_of_element_located(self.TOAST_MSG)
        )

        message = toast.text.strip()
        print(f" Toast Message: {message}")

        return message

    # ✅ FLEXIBLE VALIDATION (MAIN FIX)
    def is_success_or_duplicate(self):
        try:
            msg = self.get_toast_message().lower()

            if "success" in msg:
                print(" Product created successfully")
                return True

            elif "unique" in msg or "already exists" in msg:
                print(" SKU already exists (expected scenario)")
                return True

            else:
                print(f" Unexpected message: {msg}")
                return False

        except Exception as e:
            print(f" No toast found: {e}")
            return False