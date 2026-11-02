
import pytest
import time
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.QR_Management.QR_management_category import QR_Management_Category_Page
from pages.QR_Management.QR_management_QR_m import QR_Management_QR_m_Page
from utilities.customlogger import LogGen
from pages.common.base_page import BaseTest
from utilities.screenshot_util import take_screenshot


@pytest.mark.order(3)
class Test_QRM_Filter(BaseTest):
    logger = LogGen.loggen()

    def test_QR_management_filter(self, driver):
        self.logger.info("===== QR Management Filters Test Started =====")

        wait = WebDriverWait(driver, 10)

        # STATUS VALUE - SET DIRECTLY
        filter_status = "All"

        # NAVIGATION
        qr_page = QR_Management_Category_Page(driver)
        driver.refresh()
        qr_page.Click_Dashboard()
        self.logger.info("Clicked Dashboard")

        driver.refresh()
        self.logger.info("Page refreshed successfully")

        qr_page.Click_QR_management()
        self.logger.info("Opened QR Management module")

        qr_m_page = QR_Management_QR_m_Page(driver)
        qr_m_page.Click_Qr_management()
        # Open QR Monitoring page
        # Replace this method name only if your actual navigation method differs.

        # self.logger.info("Opened QR Monitoring page")

        # GET BATCH NUMBER FROM FIRST ROW
        batch_no = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//tbody/tr[1]/td[3]")
            )
        ).text.strip()

        # GET MANUFACTURER DATE
        manufacturer_date_text = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//tbody/tr[1]/td[8]")
            )
        ).text.strip()

        # GET EXPIRY DATE
        expiry_date_text = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//tbody/tr[1]/td[9]")
            )
        ).text.strip()

        self.logger.info(f"Batch Number: {batch_no}")
        self.logger.info(f"Manufacturer Date: {manufacturer_date_text}")
        self.logger.info(f"Expiry Date: {expiry_date_text}")
        self.logger.info(f"Status Filter: {filter_status}")

        # CONVERT DATES
        manufacturer_date = datetime.strptime(
            manufacturer_date_text, "%d %b %Y"
        )

        expiry_date = datetime.strptime(
            expiry_date_text, "%d %b %Y"
        )

        start_date =manufacturer_date.strftime("%Y-%m-%d")

        end_date = expiry_date.strftime("%Y-%m-%d")

        self.logger.info(f"Start Date: {start_date}")
        self.logger.info(f"End Date: {end_date}")

        # APPLY SEARCH FILTER
        qr_m_page.Enter_search_value(batch_no)
        self.logger.info(f"Entered Batch Number: {batch_no}")

        # APPLY DATE FILTER
        qr_m_page.Click_calender_icon()
        self.logger.info("Clicked Calendar icon")

        qr_m_page.select_date_range(start_date, end_date)
        self.logger.info(
            f"Applied Date Range: {start_date} to {end_date}"
        )

        # APPLY STATUS FILTER
        qr_m_page.Enter_select_status(filter_status)
        self.logger.info(f"Selected Status: {filter_status}")

        # VERIFY FILTER RESULT
        filtered_batch_no = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//tbody/tr[1]/td[3]")
            )
        ).text.strip()

        assert filtered_batch_no == batch_no, (
            f"QR Monitoring filter failed. "
            f"Expected Batch Number: {batch_no}, "
            f"Actual Batch Number: {filtered_batch_no}"
        )

        self.logger.info(
            f"QR Monitoring filters applied successfully. "
            f"Batch Number: {filtered_batch_no}"
        )
        time.sleep(3)
        try:
            qr_m_page.Click_actions_icon()
            self.logger.info("Clicked Actions icon")
            qr_m_page.Click_view_icon()
            self.logger.info("Clicked View icon")
            time.sleep(1)

            wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//li[@class='breadcrumb-item active']")
                )
            )
            self.logger.info("View page loaded successfully")
        except TimeoutException:
            self.logger.error("No result found for the applied filters. Please check the filter criteria.")
            self.logger.info("===== QR Management Filter toggle Test Completed =====")
