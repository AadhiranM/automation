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
class Test_QR_Monitoring_Filter_toggle(BaseTest):
    logger = LogGen.loggen()

    def test_qr_code_monitoring_filter_toggle(self, driver):

        self.logger.info("===== QR Code Monitoring Filter toggle Test Started =====")
        wait = WebDriverWait(driver, 10)

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

        # GET DATE FROM FIRST ROW
        date_value = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//tbody/tr[1]/td[6]")
            )
        ).text.strip()

        self.logger.info(f"Date value: {date_value}")

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


        # Scroll search field to the center of the viewport
        filter_toggle_element = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//button[@id='filterToggleBtn']")
            )
        )

        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
            filter_toggle_element
        )

        self.logger.info("Scrolled filter toggle botton to the center")
        time.sleep(2)
        qr_monitoring.Click_filter_toggle_btn()
        self.logger.info("Clicked Filter Toggle button")

        time.sleep(3)
        qr_monitoring.Click_scanned_at_field()
        self.logger.info("Clicked Scanned At field")

        time.sleep(4)
        qr_monitoring.select_date_range(start_date, end_date)
        self.logger.info(
            f"Applied Date Range: {start_date} to {end_date}"
        )

        qr_monitoring.Click_apply_btn()
        self.logger.info("Clicked Apply button")
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

        self.logger.info("===== QR Code Monitoring Filter toggle  Test Completed =====")
