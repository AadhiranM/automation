import pytest
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.QR_Management.QR_management_QR_m import QR_Management_QR_m_Page  # Your POM
from pages.QR_Management.QR_management_category import QR_Management_Category_Page
from pages.QR_Management.QR_management_QR_m_filters import QR_Management_QR_m_filters
from utilities.customlogger import LogGen
from pages.common.base_page import BaseTest
from utilities.read_excel import get_test_data
from utilities.screenshot_util import take_screenshot
@pytest.mark.order(8)
class Test_QRM_filter_option(BaseTest):
    logger = LogGen.loggen()

    product_name="iphone"
    manufacturing_date="10-05-2024"
    expiry_date="10-05-2027"

    def test_QR_management_filters(self, driver):
        self.logger.info(f"===== QR Management QR Test Started for QR management filters=====")
        # self.driver = driver
        # self.login_and_access()

        qr_page = QR_Management_Category_Page(driver)
        qr_page.Click_Dashboard()
        qr_page.Click_QR_management()

        qr_QRM_filters=QR_Management_QR_m_filters(driver)
        # Navigate to QR management
        qr_QRM_filters.Click_Qr_management()

        # Fill product details
        qr_QRM_filters.Click_reset_btn()
        qr_QRM_filters.Click_filter_button()
        qr_QRM_filters.Enter_filter_prd_name(self.product_name)
        time.sleep(2)
        # qr_QRM_filters.Click_manufacturer_date()
        # time.sleep(1)
        # qr_QRM_filters.set_manufacturing_date(self.manufacturing_date)
        # qr_QRM_filters.set_expiry_date(self.expiry_date)
        time.sleep(1)
        qr_QRM_filters.Click_filters_apply_btn()

        # qr_QRM_filters.select_status_drp(self.select_status)

        status=qr_QRM_filters.search_product(self.product_name)

        print(status)
        time.sleep(1)
        assert True==status
        time.sleep(1)


