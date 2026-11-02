import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.QR_Management.QR_management_category import QR_Management_Category_Page
from pages.reports.generate_reports.Generate_reports import Generate_reports_page
from pages.reports.generate_reports.Generate_report_download import Generate_reports_download_page
from utilities.customlogger import LogGen
from utilities.read_excel import get_test_data
from pages.common.base_page import BaseTest
from utilities.screenshot_util import take_screenshot
from datetime import datetime
import string
from datetime import datetime, timedelta


# LOAD EXCEL DATA
excel_path = r"C:\Users\Suresh V\Desktop\automation\mf_products_data.xlsx"
test_data = get_test_data(excel_path, "Reports")

@pytest.mark.order(1)
@pytest.mark.parametrize("data", test_data)
class Test_generate_report_filters(BaseTest):
    logger = LogGen.loggen()
    def test_generate_report_filters(self, driver, data):

        wait = WebDriverWait(driver, 15)

        self.logger.info(
            f"===== generate_report_filters Flow Started "
        )

        # NAVIGATION START
        # ---------------------------
        self.logger.info("Starting navigation to Reports module")

        qr_page = QR_Management_Category_Page(driver)
        qr_page.Click_Dashboard()
        self.logger.info("Clicked Dashboard")

        report = Generate_reports_page(driver)

        report.Click_reports_tab()
        self.logger.info("Clicked Reports tab")

        report.Click_generate_report()
        self.logger.info("Clicked Generate Report")

        reports_download = Generate_reports_download_page(driver)
        reports_download.Click_download_tab()
        self.logger.info("Opened Downloads page")

        # TABLE FIRST ROW VALUES
        report_name = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//tbody/tr[1]/td[2]")
            )
        ).text.strip()

        report_type = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//tbody/tr[1]/td[3]")
            )
        ).text.strip()

        start_date = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//tbody/tr[1]/td[5]")
            )
        ).text.strip()

        end_date = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//tbody/tr[1]/td[6]")
            )
        ).text.strip()

        created_at = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//tbody/tr[1]/td[8]")
            )
        ).text.strip()

        actual_date = datetime.strptime(
            created_at, "%d %b %Y %I:%M %p"
        )

        start_date = (
                actual_date - timedelta(days=1)
        ).strftime("%Y-%m-%d")

        end_date = actual_date.strftime("%Y-%m-%d")

        self.logger.info(f"Report Name: {report_name}")
        self.logger.info(f"Report Type: {report_type}")
        self.logger.info(f"Start Date: {start_date}")
        self.logger.info(f"End Date: {end_date}")
        self.logger.info(f"Created At: {created_at}")

        # SEARCH REPORT NAME
        reports_download.Enter_search_report_name(report_name)
        self.logger.info(f"Entered Report Name: {report_name}")
        time.sleep(1)
        # APPLY CREATED AT DATE FILTER
        reports_download.Click_created_at()
        self.logger.info("Clicked Created At date field")
        time.sleep(1)
        reports_download.select_date_range(start_date, end_date)
        self.logger.info(
            f"Applied date range: {start_date} to {end_date}"
        )

        time.sleep(2)
        report.click_report_download_btn(report_name)
        time.sleep(3)
        self.logger.info("===== Generate Report download Test Completed =====")
