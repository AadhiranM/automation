import time
import pytest
from pages.common.AccessCodePage import AccessCodePage
from pages.QR_Management.login_page import Loginpage
from utilities.customlogger import LogGen
from utilities.readproperties import Readconfig
from utilities.read_excel import get_test_data
from utilities.screenshot_util import take_screenshot
excel_path = r"C:\Users\Suresh V\Desktop\automation\mf_products_data.xlsx"
test_data = get_test_data(excel_path, "LoginData")

@pytest.mark.order(1)
@pytest.mark.parametrize("data", test_data)
class Test_QR_management_login_DDT:
    logger = LogGen.loggen()

    def test_homepageTitle(self, driver, data):
        self.logger.info("***** Verifying Homepage *****")

        username = data["username"]
        password = data["password"]

        expected_home_title = "Admin | DigiTathya"
        expected_login_title = "| DigiTathya - Admin Panel - Admin Panel"

        ac_page = AccessCodePage(driver)
        ac_present = ac_page.enter_access_code(Readconfig.getAccessCode())
        time.sleep(2)

        if ac_present:
            self.logger.info("Access code entered successfully")
        else:
            self.logger.info("Access code page not present, continuing")

        # Verify homepage title
        act_title = driver.title
        if act_title == expected_home_title:
            self.logger.info("Homepage title verified successfully")
            assert True
        else:
            driver.save_screenshot(".\\screenshots\\login\\test_homepageTitle.png")
            self.logger.error("Homepage title verification failed")
            assert False

        # Login
        lp = Loginpage(driver)
        lp.setUserName(username)
        lp.setPassword(password)
        lp.clickLogin()
        time.sleep(1)

        # Verify login success
        act_title = driver.title
        if act_title == expected_login_title:
            self.logger.info("Login successful")
            assert True
        else:
            driver.save_screenshot(".\\screenshots\\login\\test_login.png")
            self.logger.error("Login failed")
            assert False

        lp.clickLogout()