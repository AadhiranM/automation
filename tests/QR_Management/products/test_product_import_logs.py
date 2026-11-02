import time
import pytest
from datetime import datetime, timedelta
from pages.QR_Management.QR_management_category import QR_Management_Category_Page
from pages.QR_Management.QR_management_products import QR_Management_products_Page
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# from pages.QR_Management.QR_management_products import (QR_Management_Import_Logs_Page)
from pages.common.base_page import BaseTest
from utilities.customlogger import LogGen
from utilities.screenshot_util import take_screenshot

@pytest.mark.order(5)
class Test_product_import_logs(BaseTest):

    logger = LogGen.loggen()

    def test_product_import_logs_filters(self, driver):

        self.logger.info(
            "===== Product Import Logs Filter Test Started ====="
        )
        wait = WebDriverWait(driver, 10)

        driver.refresh()
        self.logger.info("Page refreshed successfully")

        qr_products_page = QR_Management_products_Page(driver)

        qr_products_page.Click_Dashboard()
        self.logger.info("Clicked Dashboard")

        qr_products_page.Click_QR_Management()
        self.logger.info("Opened QR Management module")

        qr_products_page.Click_products()
        self.logger.info("Opened Products page")

        # Open Import Logs
        qr_products_page.click_import_logs()

        # Fetch Imported By from first row
        imported_by = (
            qr_products_page.get_imported_by_first_row()
        )

        self.logger.info(
            f"Imported By value fetched: {imported_by}"
        )

        date_value = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//tbody/tr[1]/td[7]")
            )
        ).text.strip()

        actual_date = datetime.strptime(
            date_value, "%d %b %Y %I:%M %p"
        ).date()

        start_date = (
            actual_date - timedelta(days=1)
        ).strftime("%Y-%m-%d")

        end_date = actual_date.strftime("%Y-%m-%d")

        self.logger.info(
            f"Created At date range: {start_date} to {end_date}"
        )

        # Enter Imported By
        qr_products_page.enter_imported_by(imported_by)

        qr_products_page.click_filter_calender()
        qr_products_page.select_date_range(start_date, end_date)

        # Select All status
        qr_products_page.select_status("All")
        time.sleep(2)
        qr_products_page.Click_action_btn()

        # Check Uploaded File
        uploaded_file = wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//ul[@class='dropdown-menu dropdown-menu-end dd_action show']//a[@class='dropdown-item'][normalize-space()='Uploaded File']"
                )
            )
        )
        assert uploaded_file.is_displayed(), \
            "Uploaded File option is not present or visible"

        self.logger.info("Uploaded File option is present and visible")

        self.logger.info(
            "===== Product Import Logs Filter Test Passed ====="
        )
