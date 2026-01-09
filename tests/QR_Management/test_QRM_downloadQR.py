import pytest
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.QR_Management.QR_management_category import QR_Management_Category_Page
from pages.QR_Management.QR_management_QR_m_filters import QR_Management_QR_m_filters
from utilities.customlogger import LogGen
from pages.common.base_page import BaseTest
from utilities.read_excel import get_test_data

# Excel path
excel_path = r"C:\Users\Suresh V\Desktop\automation\mf_products_data.xlsx"
test_data = get_test_data(excel_path, "Download_QR")

@pytest.mark.order(9)
@pytest.mark.parametrize("data", test_data)
class Test_QRM_downloadQR_DDT(BaseTest):
    logger = LogGen.loggen()

    def test_QR_management_download_QR(self, driver, data):

        search_value = data["search_value"]
        select_status = data["select_status"]

        self.logger.info(f"===== QR Download Test Started | Search={search_value}, Status={select_status} =====")

        # Login only once (same as products)
        if data == test_data[0]:
            self.driver = driver
            self.login_and_access()
            self.logger.info("Logged in successfully for first iteration")
        else:
            self.logger.info("Skipping login — already logged in")

        qr_page = QR_Management_Category_Page(driver)
        qr_page.Click_Dashboard()
        qr_page.Click_QR_management()
        qr_filters = QR_Management_QR_m_filters(driver)
        qr_filters.Click_Qr_management()
        qr_filters.Click_reset_btn()
        qr_filters.Enter_search_field(search_value)
        time.sleep(2)
        qr_filters.select_status_drp(select_status)
        time.sleep(2)
        status = qr_filters.search_product(search_value)
        if status:
            qr_filters.download_batch_QR()
            time.sleep(1)
            qr_filters.download_unit_QR()
            time.sleep(1)

            self.logger.info(f"QR downloaded successfully for '{search_value}'")
        else:
            driver.save_screenshot(f".\\Screenshots\\No_Data_{search_value}.png")
            self.logger.error(f"No matching data found for '{search_value}'")
            pytest.fail(f"No matching data found for '{search_value}'")
