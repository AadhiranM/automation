import pytest
import time
from selenium.webdriver.common.by import By
from pages.common.AccessCodePage import AccessCodePage
from pages.QR_Management.login_page import Loginpage
from pages.QR_Management.QR_management_category import QR_Management_Category_Page
from pages.QR_monitering.QR_code_monitering import QR_code_monitering_page
from utilities.customlogger import LogGen
from pages.reports.generate_reports.Generate_reports import Generate_reports_page

from utilities.readproperties import Readconfig
from utilities.read_excel import get_test_data
from pages.common.base_page import BaseTest
from utilities.screenshot_util import take_screenshot


# ---------------------------
# LOAD EXCEL DATA
# ---------------------------
excel_path = r"C:\Users\Suresh V\Desktop\automation\mf_products_data.xlsx"
test_data = get_test_data(excel_path, "Reports")

@pytest.mark.order(11)
@pytest.mark.parametrize("data", test_data)
class Test_R_Scan_analytics_report(BaseTest):
    logger = LogGen.loggen()

    def test_Scan_analytics_report(self, driver, data):

        report_name = data["report_name"]
        select_format = data["select_format"]
        select_duration = data["select_duration"]

        self.logger.info(
            f"===== Scan_analytics_report | Report_name={report_name},====="
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
        qr_page = QR_Management_Category_Page(driver)
        qr_page.Click_Dashboard()

        report = Generate_reports_page(driver)
        report.Click_reports_tab()
        report.Click_generate_report()
        report.Click_scan_analytics_reports()
        report.Enter_report_name(report_name)
        report.choose_select_format(select_format)
        report.choose_select_duration(select_duration)
        report.Click_generate_btn()
        time.sleep(2)

        toast_text = driver.execute_script("""
            let toast = document.querySelector('.toastify');
            return toast ? toast.innerText : null;
        """)

        if toast_text:
            print("Toast:", toast_text)

        # validation
        if toast_text and "Report generation has been initiated successfully!" in toast_text:
            self.logger.info("Scan Analytics report successful")

        else:
            take_screenshot(
                driver,
                test_name="test_Scan_Analytics_report_failed",
                folder_name="Screenshots\\reports\\Generate_reports\\Scan Analytics_Report"
            )

            self.logger.error("Scan Analytics report failed")
            assert False, "Scan Analytics report generation failed"
        time.sleep(1)
        report.click_report_download_btn(report_name)


