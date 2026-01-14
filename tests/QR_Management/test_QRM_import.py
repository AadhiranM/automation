import pytest
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.QR_Management.QR_management_QR_m import QR_Management_QR_m_Page  # Your POM
from pages.QR_Management.QR_management_category import QR_Management_Category_Page
from utilities.customlogger import LogGen
from pages.common.base_page import BaseTest
from utilities.read_excel import get_test_data
from utilities.screenshot_util import take_screenshot

@pytest.mark.order(9)
class Test_QRM_import(BaseTest):
    logger = LogGen.loggen()
    upload_file = r"C:\Users\Suresh V\Downloads\qr-import-sample (8).xlsx"

    def test_QR_management_generate_import(self, driver):
        self.logger.info("===== QR Management QR Test Started =====")
        # self.driver = driver
        # self.login_and_access()

        qr_page = QR_Management_Category_Page(driver)
        qr_page.Click_Dashboard()
        qr_page.Click_QR_management()

        qr_QR_page=QR_Management_QR_m_Page(driver)

        # Navigate to QR management
        qr_QR_page.Click_Qr_management()
        qr_QR_page.Click_import_btn()
        time.sleep(1)
        qr_QR_page.Click_import_continue_btn()
        time.sleep(1)
        qr_QR_page.Enter_upload_QR_file(self.upload_file)
        time.sleep(1)
        qr_QR_page.Click_upload_btn()
        time.sleep(1)

        try:
            WebDriverWait(driver, 25).until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"),"QR import initiated successfully."))
            self.logger.info("file import successfully!")

        except:
            take_screenshot(
                driver,
                test_name="test_QR file import_failed_scr.png",
                folder_name="Screenshots\\QRM_import"
            )
            self.logger.error("File import failed")
            assert False


