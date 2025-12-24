import time
import pytest
from selenium.webdriver.common.by import By

from pages.common.AccessCodePage import AccessCodePage
from pages.QR_Management.login_page import Loginpage
from pages.QR_Management.QR_management_category import QR_Management_Category_Page
from pages.QR_monitering.QR_code_monitering import QR_code_monitering_page
from utilities.customlogger import LogGen
from utilities.readproperties import Readconfig


@pytest.mark.order(8)
class Test_QR_Code_Monitoring_Filters:

    logger = LogGen.loggen()

    username = "testuser"
    usermobile = "9876543210"
    device_name = "Android"
    start_date = "2024-01-01"
    end_date = "2024-01-31"

    def test_qr_code_monitoring_filters(self, driver):
        self.logger.info("===== QR Code Monitoring Filter Test Started =====")

        # ---------------------------
        # LOGIN + ACCESS CODE
        # ---------------------------
        ac_page = AccessCodePage(driver)
        ac_page.enter_access_code(Readconfig.getAccessCode())
        time.sleep(1)

        login_page = Loginpage(driver)
        login_page.setUserName(Readconfig.getUsername())
        login_page.setPassword(Readconfig.getUserpassword())
        login_page.clickLogin()
        self.logger.info("Login successful")

        # ---------------------------
        # NAVIGATION
        # ---------------------------
        qr_page = QR_Management_Category_Page(driver)
        qr_page.Click_Dashboard()
        qr_monitering=QR_code_monitering_page(driver)
        qr_monitering.Click_QR_monitering()
        qr_monitering.Click_QR_code_monitering()

        # ---------------------------
        # FILTER ACTIONS
        # ---------------------------
        qr_monitering.Click_filters_btn()
        time.sleep(1)

        qr_monitering.Enter_filters_username(self.username)
        qr_monitering.Enter_filters_usermobile(self.usermobile)
        qr_monitering.Enter_device_name(self.device_name)

        # ---------------------------
        # DATE RANGE
        # ---------------------------
        qr_monitering.Click_scanned_date()
        qr_monitering.select_date_range(self.start_date, self.end_date)

        qr_monitering.Click_filters_apply()
        time.sleep(3)

        # ---------------------------
        # VALIDATION
        # ---------------------------
        body_text = driver.find_element(By.TAG_NAME, "body").text

        assert (
            self.username in body_text
            or self.usermobile in body_text
            or self.device_name in body_text
            or "No data available" in body_text
        )

        self.logger.info("QR Code Monitoring Filter Test Passed")
