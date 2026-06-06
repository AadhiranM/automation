# import pytest
# import time
# from selenium.webdriver.common.by import By
#
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
# test_data = get_test_data(excel_path, "schedule_report_create")
#
# @pytest.mark.order(1)
# @pytest.mark.parametrize("data", test_data)
# class Test_SR_create(BaseTest):
#
#     logger = LogGen.loggen()
#
#     def test_schedule_report_create(self, driver, data):
#
#         select_report = data["select_report"]
#         select_format = data["select_format"]
#         select_duration = data["select_duration"]
#         mail_receiving_duration=data["mail_receiving_duration"]
#
#         self.logger.info(
#             f"===== schedule_report_create | select_report={select_report},====="
#         )
#
#         # ---------------------------
#         # LOGIN (ONLY ONCE)
#         # ---------------------------
#         if data == test_data[0]:
#             self.driver = driver
#             self.login_and_access()
#
#             self.logger.info("Login successful (first iteration)")
#         else:
#             self.logger.info("Skipping login — already logged in")
#
#         # ---------------------------
#         # NAVIGATION
#         # ---------------------------
#         qr_page = QR_Management_Category_Page(driver)
#         driver.refresh()
#         qr_page.Click_Dashboard()
#
#         reports= Generate_reports_page(driver)
#         reports.Click_reports_tab()
#         reports.Click_schedule_report()
#         reports.Click_create_btn()
#         time.sleep(2)
#         reports.choose_create_btn_select_report(select_report)
#         reports.choose_create_btn_select_format(select_format)
#         reports.choose_create_btn_select_duration(select_duration)
#         reports.choose_create_btn_mail_receiving_duration(mail_receiving_duration)
#         reports.Click_Create_btn_save_btn()
#
#
#         try:
#             toast_text = WebDriverWait(driver, 3).until(
#                 EC.visibility_of_element_located((By.CSS_SELECTOR, ".toastify"))
#             ).text
#             print("Toast:", toast_text)
#
#         except TimeoutException:
#             toast_text = "Toast message not displayed"
#             print("Toast:", toast_text)
#
#         # VALIDATION
#         if "Report schedule saved successfully" in toast_text:
#             self.logger.info(
#                 f"Schedule report saved successfully | "
#                 f"Report={select_report}, Format={select_format} | {toast_text}"
#             )
#         else:
#             take_screenshot(
#                 driver,
#                 test_name="schedule_report_create_fail",
#                 folder_name="Screenshots\\reports\\schedule_reports"
#             )
#             self.logger.error(
#                 f"Schedule report creation failed | "
#                 f"Report={select_report}, Format={select_format} | Toast: {toast_text}"
#             )
#             assert False, f"Schedule report creation failed | Toast: {toast_text}"
#
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
test_data = get_test_data(excel_path, "schedule_report_create")

@pytest.mark.order(1)
@pytest.mark.parametrize("data", test_data)
class Test_SR_create(BaseTest):

    logger = LogGen.loggen()

    def test_schedule_report_create(self, driver, data):

        select_report = data["select_report"]
        select_format = data["select_format"]
        select_duration = data["select_duration"]
        mail_receiving_duration = data["mail_receiving_duration"]

        # =========================
        # LOGGER START
        # =========================
        self.logger.info(
            f"===== Schedule Report Creation Test Started | Report: {select_report} ====="
        )

        self.logger.info(
            f"Schedule Report Details | "
            f"Report: {select_report} | "
            f"Format: {select_format} | "
            f"Duration: {select_duration} | "
            f"Mail Receiving Duration: {mail_receiving_duration}"
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

        # =========================
        # NAVIGATION LOGS
        # =========================
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

        reports.Click_create_btn()
        self.logger.info("Opened Create Schedule Report form")

        time.sleep(2)

        self.logger.info(
            f"Entering schedule report details | "
            f"Report: {select_report} | "
            f"Format: {select_format} | "
            f"Duration: {select_duration} | "
            f"Mail Receiving Duration: {mail_receiving_duration}"
        )

        reports.choose_create_btn_select_report(select_report)
        self.logger.info(f"Selected Report: {select_report}")

        reports.choose_create_btn_select_format(select_format)
        self.logger.info(f"Selected Format: {select_format}")

        reports.choose_create_btn_select_duration(select_duration)
        self.logger.info(f"Selected Duration: {select_duration}")

        reports.choose_create_btn_mail_receiving_duration(mail_receiving_duration)
        self.logger.info(
            f"Selected Mail Receiving Duration: {mail_receiving_duration}"
        )

        self.logger.info("Submitting schedule report creation request")

        reports.Click_Create_btn_save_btn()
        self.logger.info("Clicked Save button")

        # =========================
        # TOAST HANDLING
        # =========================
        self.logger.info("Waiting for toast message")

        try:
            toast_text = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".toastify"))
            ).text

            print("Toast:", toast_text)

            self.logger.info(f"Toast received: {toast_text}")

        except TimeoutException:
            toast_text = "Toast message not displayed"

            print("Toast:", toast_text)

            self.logger.error(
                "Toast message not displayed after schedule report creation"
            )

        # =========================
        # VALIDATION LOGS
        # =========================
        if "Report schedule saved successfully" in toast_text:

            self.logger.info(
                f"Schedule report created successfully | "
                f"Report: {select_report} | "
                f"Format: {select_format} | "
                f"Toast: {toast_text}"
            )

        else:

            self.logger.error(
                f"Schedule report creation FAILED | "
                f"Report: {select_report} | "
                f"Format: {select_format} | "
                f"Toast: {toast_text}"
            )

            take_screenshot(
                driver,
                test_name="schedule_report_create_fail",
                folder_name="Screenshots\\reports\\schedule_reports"
            )

            self.logger.error(
                "Screenshot captured for failed schedule report creation"
            )

            assert False, (
                f"Schedule report creation failed | Toast: {toast_text}"
            )