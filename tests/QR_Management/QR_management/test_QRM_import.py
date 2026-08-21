# import pytest
# import time
# import os
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from pages.QR_Management.QR_management_QR_m import QR_Management_QR_m_Page
# from pages.QR_Management.QR_management_category import QR_Management_Category_Page
# from utilities.customlogger import LogGen
# from pages.common.base_page import BaseTest
# from utilities.screenshot_util import take_screenshot
# from selenium.common.exceptions import TimeoutException
#
# @pytest.mark.order(5)
# class Test_QRM_import(BaseTest):
#     logger = LogGen.loggen()
#     upload_file = r"C:\Users\Suresh V\Downloads\qr-import-sample (8).xlsx"
#
#     def test_QR_management_generate_import(self, driver):
#         self.logger.info("===== QR Management QR Test Started =====")
#
#         wait = WebDriverWait(driver, 15)
#
#         self.driver = driver
#         self.login_and_access()
#
#         qr_page = QR_Management_Category_Page(driver)
#         qr_page.Click_Dashboard()
#         qr_page.Click_QR_management()
#         qr_QR_page = QR_Management_QR_m_Page(driver)
#         qr_QR_page.Click_Qr_management()
#         qr_QR_page.Click_import_btn()
#         qr_QR_page.Click_import_continue_btn()
#         qr_QR_page.Enter_upload_QR_file(self.upload_file)
#         qr_QR_page.Click_upload_btn()
#
#
#         try:
#             toast = WebDriverWait(driver,10).until(
#                 EC.visibility_of_element_located((By.CSS_SELECTOR, ".toastify"))
#             ).text
#             print("Toast:",toast)
#
#         except TimeoutException:
#             toast = "Toast not displayed"
#             print("Toast:",toast)
#
#         # VALIDATION
#         if toast and "QR import initiated successfully" in toast:
#
#             self.logger.info(f"QR file import initiated successfully | {toast}")
#
#         else:
#
#             take_screenshot(
#                 driver,
#                 test_name="test_QR_file_import_failed",
#                 folder_name="Screenshots\\QRM_import"
#             )
#             self.logger.error(f"File import failed | Toast: {toast}")
#             assert False, f"Import failed | Toast: {toast}"

import pytest
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.QR_Management.QR_management_QR_m import QR_Management_QR_m_Page
from pages.QR_Management.QR_management_category import QR_Management_Category_Page
from utilities.customlogger import LogGen
from pages.common.base_page import BaseTest
from utilities.screenshot_util import take_screenshot
from selenium.common.exceptions import TimeoutException


@pytest.mark.order(1)
class Test_QRM_import(BaseTest):

    logger = LogGen.loggen()
    upload_file = r"C:\Users\Suresh V\Downloads\qr-import-sample (8).xlsx"

    def test_QR_management_generate_import(self, driver):

        self.logger.info(
            "===== QR Management Import Flow Started ====="
        )

        wait = WebDriverWait(driver, 15)

        # LOGIN
        # self.driver = driver
        # self.login_and_access()
        # self.logger.info("Login successful")

        # NAVIGATION
        self.logger.info(
            "Starting navigation to QR Import module"
        )

        qr_page = QR_Management_Category_Page(driver)

        qr_page.Click_Dashboard()
        self.logger.info(
            "Clicked Dashboard"
        )

        qr_page.Click_QR_management()
        self.logger.info(
            "Opened QR Management module"
        )

        qr_QR_page = QR_Management_QR_m_Page(driver)

        qr_QR_page.Click_Qr_management()
        self.logger.info(
            "Opened QR Management page"
        )

        qr_QR_page.Click_import_btn()
        self.logger.info(
            "Clicked Import QR button"
        )

        time.sleep(0.5)

        qr_QR_page.Click_import_continue_btn()
        self.logger.info(
            "Clicked Continue button in QR Import flow"
        )

        time.sleep(0.5)

        # UPLOAD QR FILE
        self.logger.info(
            f"Starting QR file upload | File: {self.upload_file}"
        )

        qr_QR_page.Enter_upload_QR_file(self.upload_file)
        self.logger.info(
            f"Selected QR import file | File: {self.upload_file}"
        )

        time.sleep(1)

        qr_QR_page.Click_upload_btn()
        self.logger.info(
            "Clicked Upload button"
        )

        time.sleep(0.5)

        # TOAST
        try:
            self.logger.info(
                "Waiting for QR import success toast message"
            )

            toast = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, ".toastify")
                )
            ).text

            toast = toast.encode(
                "ascii",
                errors="ignore"
            ).decode()

            self.logger.info(
                f"Toast received: {toast}"
            )

            print("Toast:", toast)

        except TimeoutException:

            toast = "Toast not displayed"

            print("Toast:", toast)

            self.logger.error(
                "Toast message not displayed after QR file upload"
            )

        # VALIDATION
        if toast and "QR import initiated successfully" in toast:

            self.logger.info(
                f"QR file import initiated successfully | "
                f"File: {self.upload_file} | "
                f"Toast: {toast}"
            )

        else:

            take_screenshot(
                driver,
                test_name="test_QR_file_import_failed",
                folder_name="Screenshots\\QR_Management\\QR_Management\\QRM_import"
            )

            self.logger.error(
                f"QR file import failed | "
                f"File: {self.upload_file} | "
                f"Toast: {toast}"
            )

            assert False, f"Import failed | Toast: {toast}"