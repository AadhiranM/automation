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

        report_name = data["report_name"]
        select_format = data["select_format"]
        select_status = data["select_status"]
        date_string=data["date_string"]

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
        reports.Click_filters_toggle()
        reports.Click_filters_report_name(report_name)
        # reports.Choose_filters_format(select_format)
        reports.Click_filters_nxt_schedule()
        reports.set_filters_nxt_schedule(date_string)
        reports.Choose_filters_status(select_status)
        reports.Click_filters_apply_btn()

        # Wait properly here instead of sleep
        status = reports.search_product(report_name)  # True if rows exist

        if not status:
            take_screenshot(
                driver,
                test_name="schedule_report_filter_failed",
                folder_name="Screenshots\\reports\\schedule_reports"
            )
            self.logger.error("Filter applied but no records found in table")

        assert status, "No rows found after applying filters!"
        self.logger.info("Filter applied successfully, table has records")

        reports.Click_actions_button()

        try:
            reports.Click_deactivate_icon()
            reports.Click_yes_deactivate_btn()
            reports.Click_submitted_ok_btn()

        except:
            reports.Click_activate_icon()
            reports.Click_yes_activate_btn()
            reports.Click_submitted_ok_btn()



