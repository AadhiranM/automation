import pytest
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.QR_Management.QR_management_category import QR_Management_Category_Page
from pages.QR_Management.QR_management_products import QR_Management_products_Page
from utilities.customlogger import LogGen
from pages.common.base_page import BaseTest
from utilities.read_excel import get_test_data
from utilities.screenshot_util import take_screenshot
from utilities.sku_utils import generate_next_sku

@pytest.mark.order(4)
class Test_product_import(BaseTest):
    logger = LogGen.loggen()
    # import_file =r"C:\Users\Suresh V\Downloads\qr-import-sample (8).xlsx"
    import_file= r"C:\Users\Suresh V\Downloads\Product_Import (3).xlsx"

    def test_QR_management_products_flow(self, driver):

        self.logger.info(
            f"===== QR Management Product import Flow Started ====="
        )

        wait = WebDriverWait(driver, 5)

        self.driver = driver
        self.login_and_access()
        self.logger.info("Login successful (first iteration)")

        # NAVIGATION
        self.logger.info("Starting navigation to Products module")

        qr_page = QR_Management_Category_Page(driver)

        qr_page.Click_Dashboard()
        self.logger.info("Clicked Dashboard")

        driver.refresh()
        self.logger.info("Page refreshed successfully")

        qr_page.Click_QR_management()
        self.logger.info("Opened QR Management module")

        qr_products_page = QR_Management_products_Page(driver)

        qr_products_page.Click_products()
        self.logger.info("Opened Products page")

        qr_products_page.click_import_btn()
        self.logger.info("Clicked Import button")

        # qr_products_page.click_download_sample_file()
        # self.logger.info("Clicked Download Sample File button")

        qr_products_page.click_import_continue_btn()
        self.logger.info("Clicked Continue button")
        time.sleep(1)

        qr_products_page.import_file_upload(self.import_file)
        self.logger.info("Uploaded import file")

        qr_products_page.click_import_upload_btn()
        self.logger.info("Clicked Upload button")

        # TOAST
        try:
            toast = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".toastify"))
            ).text
            toast = toast.encode("ascii", errors="ignore").decode()

            print("Toast:", toast)

        except TimeoutException:
            toast = "Toast not displayed"
            print("Toast:", toast)
            self.logger.error("Toast message not displayed after upload")

        # VALIDATION
        if toast and "Product import initiated successfully" in toast:

            self.logger.info(
                f"QR file import initiated successfully | Toast: {toast}"
            )

        else:

            take_screenshot(
                driver,
                test_name="test_QR_file_import_failed",
                folder_name="Screenshots\\QRM_import"
            )

            self.logger.error(
                f"QR file import failed | Toast: {toast}"
            )

            assert False, f"Import failed | Toast: {toast}"




