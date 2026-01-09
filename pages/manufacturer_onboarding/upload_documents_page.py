from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.common.base_page import BasePage


class UploadDocumentsPage(BasePage):

    # ----------- FILE INPUTS -----------
    BUSINESS_PAN = (By.NAME, "business_pan")
    CERTIFICATE_OF_INCORP = (By.NAME, "certificate_of_incorporation")
    MOA = (By.NAME, "memorandum_of_association")
    BOARD_RESOLUTION = (By.NAME, "board_resolution")

    # ----------- BUTTONS -----------
    SUBMIT_BTN = (By.XPATH, "//button[normalize-space()='Submit Documents']")

    # ----------- PAGE MARKER -----------
    PAGE_MARKER = (By.XPATH, "//h5[normalize-space()='Upload Document']")

    # ----------- STATUS -----------
    SUCCESS_POPUP = (By.XPATH, "//div[contains(@class,'swal2-success')]")
    ERROR_TEXT = (By.CLASS_NAME, "invalid-feedback")

    # ================= PAGE LOAD =================

    def wait_for_page(self, timeout=15):
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.PAGE_MARKER)
        )

    # ================= UPLOAD METHODS =================

    def upload_business_pan(self, path):
        self.driver.find_element(*self.BUSINESS_PAN).send_keys(path)

    def upload_certificate(self, path):
        self.driver.find_element(*self.CERTIFICATE_OF_INCORP).send_keys(path)

    def upload_moa(self, path):
        self.driver.find_element(*self.MOA).send_keys(path)

    def upload_board_resolution(self, path):
        self.driver.find_element(*self.BOARD_RESOLUTION).send_keys(path)

    # ================= ACTION =================

    def submit(self):
        self.click(self.SUBMIT_BTN)

    # ================= VALIDATION =================

    def is_error_visible(self):
        return len(self.driver.find_elements(*self.ERROR_TEXT)) > 0

    def is_success_message_visible(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.SUCCESS_POPUP)
            )
            return True
        except:
            return False
