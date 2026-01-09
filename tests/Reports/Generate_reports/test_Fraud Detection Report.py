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

# ---------------------------
# LOAD EXCEL DATA
# ---------------------------
excel_path = r"C:\Users\Suresh V\Desktop\automation\mf_products_data.xlsx"
test_data = get_test_data(excel_path, "Batch_status_report")

@pytest.mark.order(13)
@pytest.mark.parametrize("data", test_data)
class Test_R_fraud_detection_report(BaseTest):
    logger = LogGen.loggen()

    def test_fraud_detection_report(self, driver, data):

        report_name = data["report_name"]
        select_format = data["select_format"]
        select_duration = data["select_duration"]

        self.logger.info(
            f"===== fraud_detection_report | Report_name={report_name},====="
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
        report.Click_fraud_detection_report()
        time.sleep(1)
        report.Enter_report_name(report_name)
        time.sleep(1)
        report.choose_select_format(select_format)
        time.sleep(1)
        report.choose_select_duration(select_duration)
        time.sleep(1)
        report.Click_generate_btn()
        time.sleep(1)

        success_msg = driver.find_element(By.TAG_NAME, "body").text
        time.sleep(1)
        if "Report generation has been initiated successfully!" in success_msg:
            assert True
            self.logger.info("fraud detection report generated")

        else:
            driver.save_screenshot(".\\Screenshots\\test_Scan_analytics_report_scr.png")
            self.logger.error("fraud detection report failed")
            assert False
        time.sleep(2)

        report.click_report_download_btn(report_name)
        time.sleep(5)

