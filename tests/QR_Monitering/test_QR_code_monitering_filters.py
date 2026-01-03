
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

# ---------------------------
# LOAD EXCEL DATA
# ---------------------------
excel_path = r"C:\Users\Suresh V\Desktop\automation\mf_products_data.xlsx"
test_data = get_test_data(excel_path, "QR_Monitoring_Filters")

@pytest.mark.order(8)
@pytest.mark.parametrize("data", test_data)
class Test_QR_Code_Monitoring_Filters(BaseTest):

    logger = LogGen.loggen()

    def test_qr_code_monitoring_filters(self, driver, data):

        username = data["username"]
        usermobile = data["usermobile"]
        device_name = data["device_name"]
        start_date = data["start_date"]
        end_date = data["end_date"]

        self.logger.info(
            f"===== QR Monitoring Filter Test | User={username}, Mobile={usermobile} ====="
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

        qr_monitoring = QR_code_monitering_page(driver)
        qr_monitoring.Click_QR_monitering()
        qr_monitoring.Click_QR_code_monitering()

        # ---------------------------
        # FILTER ACTIONS
        # ---------------------------
        qr_monitoring.Click_filters_btn()
        time.sleep(1)

        qr_monitoring.Enter_filters_username(username)
        qr_monitoring.Enter_filters_usermobile(usermobile)
        qr_monitoring.Enter_device_name(device_name)

        # ---------------------------
        # DATE RANGE
        # ---------------------------
        qr_monitoring.Click_scanned_date()
        qr_monitoring.select_date_range(start_date, end_date)
        time.sleep(2)

        qr_monitoring.Click_filters_apply()
        time.sleep(5)

        status = qr_monitoring.search_product()  # True if rows exist, False if empty

        if status:
            self.logger.info("Filter applied successfully → table has records")
        else:
            self.logger.error("Filter applied but no records found in table")
            driver.save_screenshot(".\\Screenshots\\QR_Monitoring_No_Records.png")

        assert status is True, "No rows found after applying filters!"
