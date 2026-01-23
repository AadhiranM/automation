from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from pages.common.base_page import BasePage


class UploadDocumentsPage(BasePage):

    # -------- FILE INPUTS --------
    BUSINESS_PAN = (By.ID, "doc_1")
    CERTIFICATE_OF_INCORP = (By.ID, "doc_2")
    MOA = (By.ID, "doc_3")
    BOARD_RESOLUTION = (By.ID, "doc_4")

    # -------- BUTTON --------
    SUBMIT_BTN = (By.XPATH, "//button[normalize-space()='Submit Documents']")

    # -------- TOAST --------
    TOAST_BODY = (By.XPATH, "//div[contains(@class,'toast-body')]")

    # -------- PAGE LOAD --------
    def wait_for_page(self, timeout=15):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.BUSINESS_PAN)
        )

    # -------- UPLOAD --------
    def upload_business_pan(self, path):
        self.driver.find_element(*self.BUSINESS_PAN).send_keys(path)

    def upload_certificate(self, path):
        self.driver.find_element(*self.CERTIFICATE_OF_INCORP).send_keys(path)

    def upload_moa(self, path):
        self.driver.find_element(*self.MOA).send_keys(path)

    def upload_board_resolution(self, path):
        self.driver.find_element(*self.BOARD_RESOLUTION).send_keys(path)

    # -------- SUBMIT --------
    def submit(self):
        self.driver.find_element(*self.SUBMIT_BTN).click()

    def submit_safe(self):
        btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.SUBMIT_BTN)
        )
        self.driver.execute_script("arguments[0].click();", btn)

    # -------- VALIDATION --------
    def has_any_validation_error(self, timeout=8):
        end_time = time.time() + timeout
        while time.time() < end_time:
            toast = self.driver.execute_script("""
                let t = document.querySelector('.toast.show .toast-body');
                return t ? t.innerText : null;
            """)
            if toast:
                print("🔴 UPLOAD TOAST:", toast)
                return True
            time.sleep(0.3)
        return False

    def get_business_pan_error(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[@class='invalid-feedback' and contains(text(),'Invalid file type')]")
            )
        ).text.strip()

    # 🔥 UI processing wait (negative + positive safe)
    def wait_for_upload_processing(self, seconds=4):
        time.sleep(seconds)

    def is_on_upload_page(self):
        return "upload" in self.driver.current_url.lower()

    def is_file_accepted(self):
        el = self.driver.find_element(*self.BUSINESS_PAN)
        return el.get_attribute("value") != ""

    # =====================================================
    # ✅ POSITIVE TEST SUPPORT (TOAST-BASED RESULT)
    # =====================================================
    def wait_and_get_result(self, timeout=15):
        """
        Used ONLY by positive test.
        Waits for toast and returns (STATUS, MESSAGE)
        """
        end_time = time.time() + timeout

        while time.time() < end_time:
            toast_text = self.driver.execute_script("""
                let t = document.querySelector('.toast.show .toast-body');
                return t ? t.innerText : null;
            """)

            if toast_text:
                toast_text = toast_text.strip()
                print("🟢 UPLOAD TOAST:", toast_text)

                if "success" in toast_text.lower():
                    return "SUCCESS", toast_text

                return "ERROR", toast_text

            time.sleep(0.3)

        return "UNKNOWN", "No toast appeared"


    # =====================================================
    # ❌ NEGATIVE TEST SUPPORT (INLINE VALIDATION)
    # =====================================================
    def has_inline_file_error(self, timeout=5):
        """
        Detects immediate validation error shown
        right after invalid file upload (NO submit)
        """
        end_time = time.time() + timeout

        while time.time() < end_time:
            errors = self.driver.find_elements(
                By.XPATH, "//div[contains(@class,'invalid-feedback')]"
            )

            for e in errors:
                if e.is_displayed() and e.text.strip():
                    print("🔴 INLINE FILE ERROR:", e.text.strip())
                    return True

            time.sleep(0.3)

        return False


    def get_inline_file_error_text(self, timeout=5):
        """
        Returns inline error text for assertions
        """
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@class,'invalid-feedback')]")
            )
        ).text.strip()
