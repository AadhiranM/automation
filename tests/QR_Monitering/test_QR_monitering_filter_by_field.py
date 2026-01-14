import pytest
import time
from selenium.webdriver.common.by import By

from pages.common.AccessCodePage import AccessCodePage
from pages.QR_Management.login_page import Loginpage
from pages.QR_Management.QR_management_category import QR_Management_Category_Page
from pages.QR_monitering.QR_code_monitering import QR_code_monitering_page
from utilities.customlogger import LogGen
from utilities.readproperties import Readconfig
from utilities.read_excel import get_test_data
from pages.common.base_page import BaseTest
from utilities.screenshot_util import take_screenshot


# ---------------------------
# LOAD EXCEL DATA
# ---------------------------
excel_path = r"C:\Users\Suresh V\Desktop\automation\mf_products_data.xlsx"
test_data = get_test_data(excel_path, "QR_Monitoring_Filter_By_field")

@pytest.mark.order(9)
@pytest.mark.parametrize("data", test_data)
class Test_QR_Monitoring_Filter_By_field(BaseTest):

    logger = LogGen.loggen()

    def test_qr_monitoring_filters_By_field(self, driver, data):

        search_value = data["search_value"]
        select_status = data["select_status"]
        start_date = data["start_date"]
        end_date = data["end_date"]

        self.logger.info(
            f"===== QR Monitoring Filter Test | search_value={search_value},====="
        )

        # ---------------------------
        # LOGIN (ONLY ONCE)
        # ---------------------------
        if data == test_data[0]:
            self.driver = driver
            self.login_and_access()

            self.logger.info("Login successful (first iteration)")
        else:
            self.logger.info("Skipping login — already logged in")

        # ---------------------------
        # NAVIGATION
        # ---------------------------
        qr_page = QR_Management_Category_Page(driver)
        qr_page.Click_Dashboard()

        qr_monitoring_filter= QR_code_monitering_page(driver)
        qr_monitoring_filter.Click_QR_monitering()
        qr_monitoring_filter.Click_QR_code_monitering()
        qr_monitoring_filter.Click_refresh_btn()
        # qr_monitoring_filter.Enter_search_field(search_value)
        # qr_monitoring_filter.Click_search_btn()
        time.sleep(5)
        # qr_monitoring_filter.Enter_select_status(select_status)

        qr_monitoring_filter.Click_date_range_field()
        qr_monitoring_filter.select_date_range(start_date,end_date)
        time.sleep(2)

        # status = qr_monitoring_filter.search_product(search_value)
        # time.sleep(5)
        # assert True == status

        status = qr_monitoring_filter.search_product()  # True if rows exist, False if empty

        if status:
            self.logger.info("Filter applied successfully ,table has records")
        else:
            self.logger.error("Filter applied but no records found in table")
            driver.save_screenshot(".\\Screenshots\\QR_monitering_filters\\QR_Monitoring_No_Records.png")

        assert status is True, "No rows found after applying filters!"
