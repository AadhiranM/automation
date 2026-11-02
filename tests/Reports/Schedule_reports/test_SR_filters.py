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
from datetime import datetime, timedelta

# ---------------------------
# LOAD EXCEL DATA
# ---------------------------
excel_path = r"C:\Users\Suresh V\Desktop\automation\mf_products_data.xlsx"
test_data = get_test_data(excel_path, "schedule_report_filters")

@pytest.mark.order(2)
@pytest.mark.parametrize("data", test_data)
class Test_SR_filters(BaseTest):

    logger = LogGen.loggen()

    def test_SR_filters_change_status(self, driver, data):

        wait = WebDriverWait(driver, 15)

        self.logger.info("===== Schedule Report Filter Flow Started =====")

        # NAVIGATION
        # ---------------------------
        self.logger.info("Starting navigation to Schedule Reports module")

        qr_page = QR_Management_Category_Page(driver)

        driver.refresh()
        self.logger.info("Page refreshed successfully")

        qr_page.Click_Dashboard()
        self.logger.info("Clicked Dashboard")

        reports = Generate_reports_page(driver)

        reports.Click_reports_tab()
        self.logger.info("Clicked Reports tab")

        reports.Click_schedule_report()
        self.logger.info("Opened Schedule Report page")

        # GET FIRST ROW VALUES FROM TABLE
        # ---------------------------
        search_name = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//tbody/tr[1]/td[2]")
            )
        ).text.strip()

        date_value = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//tbody/tr[1]/td[6]")
            )
        ).text.strip()

        select_status = "All"

        self.logger.info(f"Search Name: {search_name}")
        self.logger.info(f"Date Value: {date_value}")
        self.logger.info(f"Selected Status: {select_status}")

        # CONVERT TABLE DATE
        # ---------------------------
        actual_date = datetime.strptime(
            date_value, "%d %b %Y"
        )

        start_date = (
            actual_date - timedelta(days=1)
        ).strftime("%Y-%m-%d")

        end_date = actual_date.strftime("%Y-%m-%d")

        self.logger.info(f"Start Date: {start_date}")
        self.logger.info(f"End Date: {end_date}")

        # APPLY FILTERS
        # ---------------------------
        reports.Click_search_field(search_name)
        self.logger.info(f"Entered Search Name: {search_name}")

        reports.Click_filter_By_date()
        self.logger.info("Clicked Filter By Date")

        reports.select_date_range(start_date, end_date)
        self.logger.info(
            f"Applied Date Range: {start_date} to {end_date}"
        )

        reports.choose_select_status(select_status)
        self.logger.info(f"Selected Status: {select_status}")

        self.logger.info(
            f"Filters Applied | Search: {search_name} | "
            f"Start Date: {start_date} | End Date: {end_date} | "
            f"Status: {select_status}"
        )
        time.sleep(5)
        # CHANGE REPORT STATUS
        # ---------------------------
        reports.Click_actions_button()
        self.logger.info("Clicked Actions button")

        try:
            reports.Click_activate_icon()
            self.logger.info("Clicked Activate icon")

            reports.Click_activate_btn()
            self.logger.info("Clicked Activate confirmation button")

            time.sleep(2)

            self.logger.info("Waiting for report status update popup")

            expected_text = "Report status updated successfully."

        except Exception:
            reports.Click_deactivate_icon()
            self.logger.info("Clicked Deactivate icon")

            reports.Click_deactivate_btn()
            self.logger.info("Clicked Deactivate confirmation button")

            time.sleep(2)

            self.logger.info("Waiting for report status update popup")

            expected_text = "Report status updated successfully."

        # VALIDATE STATUS UPDATE POPUP
        # ---------------------------
        try:
            element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div[@id='swal2-html-container']")
                )
            )

            actual_text = element.text.strip()

            self.logger.info(f"Popup received: {actual_text}")

            if expected_text in actual_text:
                print("Report status updated successfully.")

                self.logger.info(
                    f"Report status updated successfully | Popup: {actual_text}"
                )

            else:
                print(
                    f"Report status update failed. Actual text: {actual_text}"
                )

                self.logger.error(
                    f"Report status update FAILED | Popup: {actual_text}"
                )

                take_screenshot(
                    driver,
                    test_name="Schedule_report_update_fail",
                    folder_name="screenshots\\reports\\schedule_reports\\change_to_active"
                )

                assert False, (
                    f"Report status update failed | Toast: {actual_text}"
                )

        except Exception as e:
            print("Element is not present.")
            print(f"Error: {e}")

            self.logger.error(
                f"Status update popup not displayed or validation failed | Error: {e}"
            )

            take_screenshot(
                driver,
                test_name="Schedule_report_update_fail",
                folder_name="screenshots\\reports\\schedule_reports\\change_to_active"
            )
            raise
        self.logger.info("Schedule Reports filters  module test completed successfully")