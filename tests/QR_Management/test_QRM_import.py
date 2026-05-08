
import pytest
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from pages.QR_Management.QR_management_QR_m import QR_Management_QR_m_Page
from pages.QR_Management.QR_management_category import QR_Management_Category_Page
from utilities.customlogger import LogGen
from pages.common.base_page import BaseTest
from utilities.screenshot_util import take_screenshot

@pytest.mark.order(9)
class Test_QRM_import(BaseTest):
    logger = LogGen.loggen()
    upload_file = r"C:\Users\Suresh V\Downloads\qr-import-sample (8).xlsx"

    def test_QR_management_generate_import(self, driver):
        self.logger.info("===== QR Management QR Test Started =====")

        wait = WebDriverWait(driver, 15)

        # self.driver = driver
        # self.login_and_access()

        qr_page = QR_Management_Category_Page(driver)
        qr_page.Click_Dashboard()
        qr_page.Click_QR_management()

        qr_QR_page = QR_Management_QR_m_Page(driver)

        qr_QR_page.Click_Qr_management()
        qr_QR_page.Click_import_btn()

        qr_QR_page.Click_import_continue_btn()
        qr_QR_page.Enter_upload_QR_file(self.upload_file)
        qr_QR_page.Click_upload_btn()
        time.sleep(4)


        success_text = driver.execute_script("""
            return document.querySelector('.toastify')?.innerText;
        """)

        print("Page Text:", success_text)

        if "QR import initiated successfully" in success_text:
            self.logger.info(f"QR file import initiated successfully!,{success_text}")

        else:
            take_screenshot(
                driver,
                test_name="test_QR_file_import_failed",
                folder_name="Screenshots\\QRM_import"
            )
            self.logger.error(f"File import failed. Text: {success_text}")
            assert False, f"Import failed. Text: {success_text}"


