
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
test_data = get_test_data(excel_path, "QR_Monitoring_export_ID_based")

@pytest.mark.order(9)
@pytest.mark.parametrize("data", test_data)
class Test_QR_Code_Monitoring_export(BaseTest):

    logger = LogGen.loggen()

    def test_qr_code_monitoring_export(self, driver, data):

        Report_start_Id= data["Report_start_Id"]
        Report_end_Id= data["Report_end_Id"]
        select_user = data["select_user"]


        self.logger.info(
            f"===== QR Monitoring export Test | select_user={select_user} ====="
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

        qr_monitoring_export_id = QR_code_monitering_page(driver)
        qr_monitoring_export_id.Click_QR_monitering()
        qr_monitoring_export_id.Click_QR_code_monitering()
        qr_monitoring_export_id.click_Export_btn()
        time.sleep(1)

        qr_monitoring_export_id.Enter_report_start_id(Report_start_Id)
        time.sleep(1)
        qr_monitoring_export_id.Enter_report_end_id(Report_end_Id)
        time.sleep(1)

        qr_monitoring_export_id.Select_user_opt()
        time.sleep(3)
        # qr_monitoring_export_id.select_id_select_user(select_user)
        qr_monitoring_export_id.Enter_id_select_user_input(select_user)
        time.sleep(3)
        qr_monitoring_export_id.click_submit_btn()

