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

excel_path = r"mf_products_data.xlsx"
test_data = get_test_data(excel_path, "products")

@pytest.mark.order(5)
@pytest.mark.parametrize("data", test_data)
class Test_product_import_logs(BaseTest):
    logger = LogGen.loggen()

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
