import time
import pytest
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.QR_Management.QR_management_category import QR_Management_Category_Page
from pages.QR_monitering.QR_code_monitering import QR_code_monitering_page
from utilities.customlogger import LogGen
from pages.common.base_page import BaseTest
from selenium.common.exceptions import TimeoutException

@pytest.mark.order(1)
class Test_QR_Monitoring_Filters(BaseTest):
    logger = LogGen.loggen()

    def test_qr_code_monitoring_filters(self, driver):

        self.logger.info("===== QR Code Monitoring Filter Test Started =====")

        wait = WebDriverWait(driver, 10)

        # STATUS VALUE - SET DIRECTLY
        filter_status = "All"

        # NAVIGATION
        qr_page = QR_Management_Category_Page(driver)
        driver.refresh()
        qr_page.Click_Dashboard()
        self.logger.info("Clicked Dashboard")

        qr_page.Click_QR_management()
        self.logger.info("Opened QR Management module")

        # OPEN QR CODE MONITORING
        qr_monitoring = QR_code_monitering_page(driver)
        qr_monitoring.Click_QR_monitering()
        qr_monitoring.Click_QR_code_monitering()
        self.logger.info("Opened QR Code Monitoring page")

        # GET SCAN ID FROM FIRST ROW
        scan_id = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//tbody/tr[1]/td[1]")
            )
        ).text.strip()

        # GET DATE FROM FIRST ROW
        date_value = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//tbody/tr[1]/td[6]")
            )
        ).text.strip()

        self.logger.info(f"Scan ID: {scan_id}")
        self.logger.info(f"Date value: {date_value}")
        self.logger.info(f"Status Filter: {filter_status}")

        # CONVERT DATE
        actual_date = datetime.strptime(
            date_value, "%d %b %Y %I:%M:%S %p"
        )

        start_date = (
                actual_date - timedelta(days=1)
        ).strftime("%Y-%m-%d")

        end_date = actual_date.strftime("%Y-%m-%d")

        self.logger.info(f"Start Date: {start_date}")
        self.logger.info(f"End Date: {end_date}")
        time.sleep(2)

        # Scroll search field to the center of the viewport
        search_element = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//input[@id='search-vale']")
            )
        )

        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
            search_element
        )

        self.logger.info("Scrolled search field to the center")

        # APPLY SEARCH FILTER
        qr_monitoring.Enter_search_field(scan_id)
        self.logger.info(f"Entered Scan ID: {scan_id}")

        qr_monitoring.Click_search_btn()
        self.logger.info("Clicked Search button")

        # APPLY DATE FILTER
        qr_monitoring.Click_date_range_field()
        self.logger.info("Clicked Date Range field")

        time.sleep(3)
        qr_monitoring.select_date_range(start_date, end_date)
        self.logger.info(
            f"Applied Date Range: {start_date} to {end_date}"
        )

        # APPLY STATUS FILTER
        qr_monitoring.Enter_select_status(filter_status)
        self.logger.info(f"Selected Status: {filter_status}")


        # VERIFY FILTER RESULT
        filtered_scan_id = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//tbody/tr[1]/td[1]")
            )
        ).text.strip()

        assert filtered_scan_id == scan_id, (
            f"QR Code Monitoring filter failed. "
            f"Expected Scan ID: {scan_id}, "
            f"Actual Scan ID: {filtered_scan_id}"
        )

        self.logger.info(
            f"QR Code Monitoring filters applied successfully. "
            f"Scan ID: {filtered_scan_id}"
        )
        time.sleep(3)

        try:

            qr_monitoring.Click_actions_icon()
            self.logger.info("Clicked Actions icon")
            qr_monitoring.Click_view_icon()
            self.logger.info("Clicked View icon")
            time.sleep(1)

            wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//li[@class='breadcrumb-item d-flex align-items-center active']")
                )
            )
            self.logger.info("View page loaded successfully")
        except TimeoutException:
            self.logger.error("No result found for the applied filters. Please check the filter criteria.")
            self.logger.info("===== QR Management Filter toggle Test Completed =====")

        self.logger.info("===== QR Code Monitoring Filter Test Completed =====")
