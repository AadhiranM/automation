# import pytest
# import time
# from selenium.webdriver.common.by import By
# from pages.common.AccessCodePage import AccessCodePage
# from pages.QR_Management.login_page import Loginpage
# from pages.QR_Management.QR_management_category import QR_Management_Category_Page
# from pages.QR_monitering.QR_code_monitering import QR_code_monitering_page
# from utilities.customlogger import LogGen
# from pages.reports.generate_reports.Generate_reports import Generate_reports_page
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
#
# from selenium.common.exceptions import TimeoutException
# from utilities.readproperties import Readconfig
# from utilities.read_excel import get_test_data
# from pages.common.base_page import BaseTest
# from utilities.screenshot_util import take_screenshot
#
#
# # ---------------------------
# # LOAD EXCEL DATA
# # ---------------------------
# excel_path = r"C:\Users\Suresh V\Desktop\automation\mf_products_data.xlsx"
# test_data = get_test_data(excel_path, "Reports")
#
# @pytest.mark.order(12)
# @pytest.mark.parametrize("data", test_data)
# class Test_R_product_analysis_report(BaseTest):
#     logger = LogGen.loggen()
#
#     def test_product_analysis_report(self, driver, data):
#
#         report_name = data["report_name"]
#         select_format = data["select_format"]
#         select_duration = data["select_duration"]
#
#         self.logger.info(
#             f"===== product_analysis_report | Report_name={report_name},====="
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
#         qr_page.Click_Dashboard()
#
#         report = Generate_reports_page(driver)
#         report.Click_reports_tab()
#         report.Click_generate_report()
#         report.Click_product_analytics_report()
#         time.sleep(1)
#         report.Enter_report_name(report_name)
#
#         report.choose_select_format(select_format)
#
#         report.choose_select_duration(select_duration)
#
#         report.Click_generate_btn()
#         time.sleep(1)
#
#
#         try:
#             toast_text = WebDriverWait(driver, 5).until(
#                 EC.visibility_of_element_located((By.CSS_SELECTOR, ".toastify"))
#             ).text
#             print("Toast:", toast_text)
#
#         except TimeoutException:
#             toast_text = "Toast message not displayed"
#             print("Toast:", toast_text)
#
#         # VALIDATION
#         if toast_text and "Report generation has been initiated successfully!" in toast_text:
#
#             self.logger.info(f"Product analysis report successful | {toast_text}")
#
#         else:
#
#             take_screenshot(
#                 driver,
#                 test_name="test_product_analysis_report_failed",
#                 folder_name="Screenshots\\reports\\Generate_reports\\Product_Analysis_Report"
#             )
#
#             self.logger.error(f"Product analysis report failed | Toast: {toast_text}")
#
#             assert False, f"Product analysis report generation failed | Toast: {toast_text}"
#         time.sleep(1)
#         report.click_report_download_btn(report_name)
#
#
import pytest
import time
from selenium.webdriver.common.by import By
from pages.common.AccessCodePage import AccessCodePage
from pages.QR_Management.login_page import Loginpage
from pages.QR_Management.QR_management_category import QR_Management_Category_Page
from pages.QR_monitering.QR_code_monitering import QR_code_monitering_page
from utilities.customlogger import LogGen
from pages.reports.generate_reports.Generate_reports import Generate_reports_page
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utilities.readproperties import Readconfig
from utilities.read_excel import get_test_data
from pages.common.base_page import BaseTest
from utilities.screenshot_util import take_screenshot


# ---------------------------
# LOAD EXCEL DATA
# ---------------------------
excel_path = r"C:\Users\Suresh V\Desktop\automation\mf_products_data.xlsx"
test_data = get_test_data(excel_path, "Reports")


@pytest.mark.order(12)
@pytest.mark.parametrize("data", test_data)
class Test_R_product_analysis_report(BaseTest):

    logger = LogGen.loggen()

    def test_product_analysis_report(self, driver, data):

        report_name = data["report_name"]
        select_format = data["select_format"]
        select_duration = data["select_duration"]

        self.logger.info(
            f"===== Product Analysis Report Flow Started | Report: {report_name} ====="
        )

        # ---------------------------
        # LOGIN (ONLY ONCE)
        # ---------------------------
        # if data == test_data[0]:
        #     self.driver = driver
        #     self.login_and_access()
        #     self.logger.info("Login successful (first iteration)")
        # else:
        #     self.logger.info("Skipping login — already logged in")

        # ---------------------------
        # NAVIGATION START
        # ---------------------------
        self.logger.info("Navigating to Reports module")

        qr_page = QR_Management_Category_Page(driver)
        qr_page.Click_Dashboard()
        self.logger.info("Clicked Dashboard")

        report = Generate_reports_page(driver)

        report.Click_reports_tab()
        self.logger.info("Clicked Reports tab")

        report.Click_generate_report()
        self.logger.info("Clicked Generate Report")

        report.Click_product_analytics_report()
        self.logger.info("Selected Product Analytics Report")

        time.sleep(1)

        self.logger.info(f"Filling report form | Report: {report_name}")

        report.Enter_report_name(report_name)

        report.choose_select_format(select_format)
        report.choose_select_duration(select_duration)

        self.logger.info("Clicked Generate Button")
        report.Click_generate_btn()

        time.sleep(1)

        # ---------------------------
        # TOAST HANDLING
        # ---------------------------
        try:
            toast_text = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".toastify"))
            ).text

            print("Toast:", toast_text)
            self.logger.info(f"Toast received: {toast_text}")

        except TimeoutException:
            toast_text = "Toast message not displayed"
            print("Toast:", toast_text)
            self.logger.error("Toast message not displayed after report generation")

        # ---------------------------
        # VALIDATION
        # ---------------------------
        if toast_text and "Report generation has been initiated successfully!" in toast_text:

            self.logger.info(
                f"Product analysis report generated successfully | {toast_text}"
            )

        else:

            take_screenshot(
                driver,
                test_name="test_product_analysis_report_failed",
                folder_name="Screenshots\\reports\\Generate_reports\\Product_Analysis_Report"
            )

            self.logger.error(
                f"Product analysis report failed | Toast: {toast_text}"
            )

            assert False, f"Product analysis report generation failed | Toast: {toast_text}"

        time.sleep(1)

        self.logger.info(f"Downloading report: {report_name}")
        report.click_report_download_btn(report_name)
