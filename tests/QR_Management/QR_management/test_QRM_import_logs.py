import time
import pytest
from datetime import datetime, timedelta
from pages.QR_Management.QR_management_category import QR_Management_Category_Page
from pages.QR_Management.QR_management_products import QR_Management_products_Page
from pages.QR_Management.QR_management_QR_m import QR_Management_QR_m_Page
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# from pages.QR_Management.QR_management_products import (QR_Management_Import_Logs_Page)
from pages.common.base_page import BaseTest
from utilities.customlogger import LogGen
from utilities.screenshot_util import take_screenshot

@pytest.mark.order(5)
class Test_QRM_import_logs(BaseTest):

    logger = LogGen.loggen()

    def test_QRM_import_logs_filters(self, driver):

        self.logger.info(
            "===== QRM Import Logs filter Test Started ====="
        )
        wait = WebDriverWait(driver, 10)
        driver.refresh()
        qr_page = QR_Management_Category_Page(driver)
        qr_page.Click_Dashboard()
        self.logger.info("Clicked Dashboard")

        driver.refresh()
        self.logger.info("Page refreshed successfully")

        qr_page.Click_QR_management()
        self.logger.info("Opened QR Management module")

        qr_m_page = QR_Management_QR_m_Page(driver)
        qr_m_page.Click_Qr_management()
        # Open Import Logs
        qr_m_page.Click_import_logs_btn()

        # Fetch Imported By from first row
        imported_by = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//tbody/tr[1]/td[2]//span[@class='avatar-text copy-ellipsis-text']")
            )
        ).text.strip()

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
        qr_m_page.Enter_import_logs_search_value_field(imported_by)

        qr_m_page.Click_import_logs_calender()
        qr_m_page.select_date_range(start_date, end_date)

        # Select All status
        qr_m_page.Select_import_logs_status_drpdown("All")
        time.sleep(2)
        qr_m_page.Click_import_logs_action_icon()
        time.sleep(2)



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

        # Immediately check Failed File
        failed_file = wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//ul[@class='dropdown-menu dropdown-menu-end dd_action show']//a[@class='dropdown-item'][normalize-space()='Failed File']"
                )
            )
        )

        assert failed_file.is_displayed(), \
            "Failed File option is not present or visible"

        self.logger.info("Failed File option is present and visible")

        self.logger.info(
            "===== Uploaded and Failed File Options Test Passed ====="
        )
