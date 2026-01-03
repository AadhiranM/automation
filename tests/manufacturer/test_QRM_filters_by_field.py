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

@pytest.mark.order(7)
class Test_QRM_filters(BaseTest):
    logger = LogGen.loggen()

    search_value="iphone"
    select_status="Completed"

    def test_QR_management_filters(self, driver):
        self.logger.info(f"===== QR Management QR Test Started for QR management filters=====")

        self.driver = driver
        self.login_and_access()

        qr_page = QR_Management_Category_Page(driver)
        qr_page.Click_Dashboard()
        qr_page.Click_QR_management()

        qr_QRM_filters=QR_Management_QR_m_filters(driver)
        # Navigate to QR management
        qr_QRM_filters.Click_Qr_management()

        # Fill product details
        qr_QRM_filters.Click_reset_btn()
        qr_QRM_filters.Enter_search_field(self.search_value)
        # qr_QRM_filters.Click_search_btn()
        time.sleep(1)

        qr_QRM_filters.select_status_drp(self.select_status)

        status=qr_QRM_filters.search_product(self.search_value)
        time.sleep(1)
        assert True==status
        time.sleep(1)



