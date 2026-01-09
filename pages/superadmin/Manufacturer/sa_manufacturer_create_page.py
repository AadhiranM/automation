from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.common.base_page import BasePage


class SAManufacturerCreatePage(BasePage):

    # ---------------- MODAL ----------------
    CREATE_MODAL = (By.ID, "showModal")

    # ---------------- INPUT FIELDS ----------------
    EMAIL = (
        By.XPATH,
        "//div[@id='showModal' and contains(@class,'show')]//input[@name='email']"
    )

    COMPANY_NAME = (
        By.XPATH,
        "//div[@id='showModal' and contains(@class,'show')]//input[@name='company_name']"
    )

    # ---------------- BUTTON ----------------
    SAVE_BTN = (
        By.XPATH,
        "//div[@id='showModal']//button[normalize-space()='Save']"
    )

    # ---------------- BACKEND VALIDATION ERRORS (CORRECT) ----------------
    ERROR_EMAIL = (
        By.XPATH,
        "//input[@name='email' and contains(@class,'is-invalid')]"
        "/following-sibling::div[contains(@class,'invalid-feedback')]"
    )

    ERROR_COMPANY = (
        By.XPATH,
        "//input[@name='company_name' and contains(@class,'is-invalid')]"
        "/following-sibling::div[contains(@class,'invalid-feedback')]"
    )

    # ---------------- SUCCESS TOAST ----------------
    SUCCESS_TOAST = (
        By.XPATH,
        "//div[contains(@class,'toastify') and contains(@class,'bg-success')]"
    )

    # ---------------- PAGE LOAD ----------------
    def wait_for_page(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.CREATE_MODAL)
        )

    # ---------------- ACTIONS ----------------
    def fill_email(self, email):
        self.clear(self.EMAIL)
        self.type(self.EMAIL, email)

    def fill_company_name(self, name):
        self.clear(self.COMPANY_NAME)
        self.type(self.COMPANY_NAME, name)

    def click_save(self):
        self.click(self.SAVE_BTN)

    # ---------------- VALIDATION CHECKS ----------------
    def is_email_error_visible(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.ERROR_EMAIL)
            )
            return True
        except:
            return False

    def is_company_error_visible(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.ERROR_COMPANY)
            )
            return True
        except:
            return False

    # ---------------- SUCCESS ----------------
    def wait_for_success(self):
        toast = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(self.SUCCESS_TOAST)
        )
        return toast.text

    # ---------------- IMPORTANT (MNC PRACTICE) ----------------
    def disable_browser_validation(self):
        script = """
            const modal = document.querySelector('#showModal');
            if (!modal) return;

            const form = modal.querySelector('form');
            if (!form) return;

            form.setAttribute('novalidate', 'true');
        """
        self.driver.execute_script(script)

