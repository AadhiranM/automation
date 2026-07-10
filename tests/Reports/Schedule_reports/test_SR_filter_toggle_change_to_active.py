# import pytest
# import time
# from selenium.webdriver.common.by import By
# from pages.common.AccessCodePage import AccessCodePage
# from pages.QR_Management.login_page import Loginpage
# from pages.QR_Management.QR_management_category import QR_Management_Category_Page
# from pages.QR_monitering.QR_code_monitering import QR_code_monitering_page
# from pages.reports.schedule_reports.schedule_report_filters import Generate_reports_page
# from utilities.customlogger import LogGen
# from utilities.readproperties import Readconfig
# from utilities.read_excel import get_test_data
# from pages.common.base_page import BaseTest
# from utilities.screenshot_util import take_screenshot
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
#
# # ---------------------------
# # LOAD EXCEL DATA
# # ---------------------------
# excel_path = r"C:\Users\Suresh V\Desktop\automation\mf_products_data.xlsx"
# test_data = get_test_data(excel_path, "schedule_report_filters")
#
# @pytest.mark.order(4)
# @pytest.mark.parametrize("data", test_data)
# class Test_SR_filter_toggle_change_to_active(BaseTest):
#
#     logger = LogGen.loggen()
#
#     def test_schedule_report_filters(self, driver, data):
#
#         report_name = data["report_name"]
#         select_format = data["select_format"]
#         select_status = data["select_status"]
#         date_string=data["date_string"]
#
#         self.logger.info(
#             f"===== schedule_report_filters |"
#         )
#
#         # ---------------------------
#         # LOGIN (ONLY ONCE)
#         # ---------------------------
#         # if data == test_data[0]:
#         #     self.driver = driver
#         #     self.login_and_access()
#         #
#         #     self.logger.info("Login successful (first iteration)")
#         # else:
#         #     self.logger.info("Skipping login — already logged in")
#
#         # ---------------------------
#         # NAVIGATION
#         # ---------------------------
#         qr_page = QR_Management_Category_Page(driver)
#         driver.refresh()
#         qr_page.Click_Dashboard()
#         reports= Generate_reports_page(driver)
#         reports.Click_reports_tab()
#         reports.Click_schedule_report()
#         reports.Click_filters_toggle()
#         reports.Click_filters_report_name(report_name)
#         time.sleep(1)
#         # reports.Choose_filters_format(select_format)
#         reports.Click_filters_nxt_schedule()
#         reports.set_filters_nxt_schedule(date_string)
#         # reports.Choose_filters_status(select_status)
#         reports.Click_filters_apply_btn()
#
#         # Wait properly here instead of sleep
#         status = reports.search_product(report_name,"Inactive")  # True if rows exist
#
#         if not status:
#             take_screenshot(
#                 driver,
#                 test_name="schedule_report_filter_failed",
#                 folder_name="Screenshots\\reports\\schedule_reports"
#             )
#             self.logger.error("FILTER FAILED | No data found or status mismatch after applying filters")
#             assert status, "FILTER FAILED | No data found or status mismatch after applying filters"
#         self.logger.info("Filter applied successfully, table has records")
#
#         reports.Click_actions_button()
#         reports.Click_activate_icon()
#         reports.Click_activate_btn()
#         time.sleep(2)
#
#         self.logger.info("Waiting for pop up  response")
#
#         expected_text = "Report status updated successfully."
#
#         try:
#             element = WebDriverWait(driver, 10).until(
#                 EC.visibility_of_element_located((By.XPATH, "//div[@id='swal2-html-container']"))
#             )
#
#             actual_text = element.text.strip()
#
#             if expected_text in actual_text:
#                 print("Report status updated successfully.")
#             else:
#                 print(f"Report status update failed .. Actual text: {actual_text}")
#                 self.logger.error(
#                     f" Report status update FAILED | popup: {actual_text}"
#                 )
#
#                 take_screenshot(
#                     driver,
#                     test_name="Schedule_report_update_fail",
#                     folder_name="screenshots\\reports\\schedule_reports\\change_to_active"
#                 )
#
#                 assert False, (
#                     f"Report status update failed | Toast: {actual_text}"
#                 )
#
#         except Exception as e:
#             print("Element is not present.")
#             print(f"Error: {e}")
#


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

@pytest.mark.order(4)
@pytest.mark.parametrize("data", test_data)
class Test_SR_filter_toggle_change_to_active(BaseTest):

    logger = LogGen.loggen()

    def test_schedule_report_filters(self, driver, data):

        report_name = data["report_name"]
        select_format = data["select_format"]
        select_status = data["select_status"]
        date_string = data["date_string"]

        self.logger.info(
            f"===== Schedule Report Filter Toggle Change To Active Flow Started | Report: {report_name} ====="
        )

        # ---------------------------
        # LOGIN (ONLY ONCE)
        # ---------------------------
        # if data == test_data[0]:
        #     self.driver = driver
        #     self.login_and_access()
        #
        #     self.logger.info("Login successful (first iteration)")
        # else:
        #     self.logger.info("Skipping login — already logged in")

        # ---------------------------
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

        reports.Click_filters_toggle()
        self.logger.info("Opened Filters panel")

        reports.Click_filters_report_name(report_name)
        self.logger.info(f"Entered Report Name filter: {report_name}")

        time.sleep(1)

        # reports.Choose_filters_format(select_format)

        reports.Click_filters_nxt_schedule()
        self.logger.info("Opened Next Schedule filter")

        reports.set_filters_nxt_schedule(date_string)
        self.logger.info(f"Selected Next Schedule date: {date_string}")


        # reports.Choose_filters_status(select_status)

        reports.Click_filters_apply_btn()
        self.logger.info("Clicked Apply Filters button")

        self.logger.info(
            f"Validating filtered results | Report Name: {report_name}"
        )

        # Wait properly here instead of sleep
        status = reports.search_product(report_name, "Inactive")  # True if rows exist

        if not status:
            take_screenshot(
                driver,
                test_name="schedule_report_filter_failed",
                folder_name="Screenshots\\reports\\schedule_reports"
            )

            self.logger.error(
                f"FILTER FAILED | Report Name: {report_name} | Status: Inactive | No matching records found"
            )

            assert status, "FILTER FAILED | No data found or status mismatch after applying filters"

        self.logger.info(
            f"Filter applied successfully | Report Name: {report_name} | Records found"
        )

        reports.Click_actions_button()
        self.logger.info("Clicked Actions button")

        reports.Click_activate_icon()
        self.logger.info("Clicked Activate icon")

        reports.Click_activate_btn()
        self.logger.info("Clicked Activate confirmation button")

        time.sleep(2)

        self.logger.info("Waiting for report status update popup")

        expected_text = "Report status updated successfully."

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
                print(f"Report status update failed .. Actual text: {actual_text}")

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
