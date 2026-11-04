
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

@pytest.mark.order(4)

class Test_QRM_Filter_toggle(BaseTest):
    logger = LogGen.loggen()

    def test_QR_management_filter_toggle(self, driver):
        self.logger.info("===== QR Management Filter toggle Test Started =====")

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
        product_name = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//tbody/tr[1]/td[2]")
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
                (By.XPATH, "//tbody/tr[1]/td[8]")
            )
        ).text.strip()

        created_by = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//tbody/tr[1]/td[11]//span[@class='avatar-text copy-ellipsis-text']")
            )
        ).text.strip()

        self.logger.info(f"product_name: {product_name}")
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

        start_date = manufacturer_date.strftime("%d-%m-%Y")
        end_date = expiry_date.strftime("%d-%m-%Y")

        self.logger.info(f"Manufacturing Date: {start_date}")
        self.logger.info(f"Expiry Date: {end_date}")

        qr_m_page.Click_filter_toggle_btn()
        self.logger.info("Clicked Filter Toggle button")

        qr_m_page.Enter_product_name(product_name)
        self.logger.info(f"Entered Product Name: {product_name}")
        time.sleep(1)
        qr_m_page.filter_toggle_manufacturing_date(start_date)
        self.logger.info(f"Selected Manufacturing Date: {start_date}")
        time.sleep(1)

        # qr_m_page.filter_toggle_expiry_date(end_date)
        # self.logger.info(f"Selected Expiry Date: {end_date}")

        qr_m_page.Click_created_by_field()
        qr_m_page.Enter_created_by_input_field(created_by)
        self.logger.info(f"Entered Created By: {created_by}")

        qr_m_page.Click_apply_btn()
        self.logger.info("Clicked Apply button")
        time.sleep(5)
        try:
            qr_m_page.Click_actions_icon()
            self.logger.info("Clicked Actions icon")
            time.sleep(1)
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


