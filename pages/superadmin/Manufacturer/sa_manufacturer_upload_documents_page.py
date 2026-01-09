from selenium.webdriver.common.by import By
from pages.common.base_page import BasePage

class UploadDocumentsPage(BasePage):

    PAN_UPLOAD = (By.NAME, "pan_document")
    SUBMIT_BTN = (By.XPATH, "//button[normalize-space()='Submit']")

    def upload_pan(self, path):
        self.upload_file(self.PAN_UPLOAD, path)

    def submit(self):
        self.click(self.SUBMIT_BTN)
