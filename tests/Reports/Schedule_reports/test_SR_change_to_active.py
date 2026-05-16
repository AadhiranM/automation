import pytest
import time
from selenium.webdriver.common.by import By
from pages.common.AccessCodePage import AccessCodePage
from pages.QR_Management.login_page import Loginpage
from pages.QR_Management.QR_management_category import QR_Management_Category_Page
from pages.QR_monitering.QR_code_monitering import QR_code_monitering_page
from pages.reports.schedule_reports.schedule_report_filters import Generate_reports_page
from utilities.customlogger import LogGen
from utilities.readproperties import Readconfig
from utilities.read_excel import get_test_data
from pages.common.base_page import BaseTest
from utilities.screenshot_util import take_screenshot
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# ---------------------------
# LOAD EXCEL DATA
# ---------------------------
excel_path = r"C:\Users\Suresh V\Desktop\automation\mf_products_data.xlsx"
test_data = get_test_data(excel_path, "schedule_report_filters")

@pytest.mark.order(2)
@pytest.mark.parametrize("data", test_data)
class Test_SR_filters(BaseTest):

    logger = LogGen.loggen()

    def test_schedule_report_filters(self, driver, data):

        search_name = data["search_name"]
        select_status = data["select_status"]
        start_date = data["start_date"]
        end_date = data["end_date"]

        self.logger.info(
            f"===== schedule_report_filters |"
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
        driver.refresh()
        qr_page.Click_Dashboard()
        reports= Generate_reports_page(driver)
        reports.Click_reports_tab()
        reports.Click_schedule_report()
        reports.Click_search_field(search_name)
        reports.Click_filter_By_date()
        reports.select_date_range(start_date, end_date)
        reports.choose_select_status(select_status)

        # Wait properly here instead of sleep
        status = reports.search_product(search_name,"Inactive")  # True if rows exist

        if not status:
            take_screenshot(
                driver,
                test_name="schedule_report_filter_failed",
                folder_name="Screenshots\\reports\\schedule_reports"
            )
            self.logger.error("FILTER FAILED | No data found or status mismatch after applying filters")
            assert status, "FILTER FAILED | No data found or status mismatch after applying filters"
        self.logger.info("Filter applied successfully, table has records")

        reports.Click_actions_button()
        reports.Click_activate_icon()
        reports.Click_activate_btn()
        time.sleep(5)


