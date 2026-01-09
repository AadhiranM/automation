
import time
import pytest
from pages.common.AccessCodePage import AccessCodePage
from pages.QR_Management.login_page import Loginpage
from utilities.customlogger import LogGen
from utilities.readproperties import Readconfig
@pytest.mark.order(1)
class Test_001_QR_management_login:
    logger = LogGen.loggen()

    def test_homepageTitle(self, driver):
        self.logger.info("***** Verifying Homepage *****")
        ac_page = AccessCodePage(driver)
        ac_present = ac_page.enter_access_code(Readconfig.getAccessCode())
        time.sleep(2)
        if ac_present:
            self.logger.info("Access code entered successfully")
        else:
            self.logger.info("Access code page not present, continuing")

        act_title = driver.title
        if act_title == "Admin | DigiTathya":
            assert True
            self.logger.info("Homepage title verified successfully")
        else:
            driver.save_screenshot(".\\screenshots\\test_homepageTitle.png")
            self.logger.error("Homepage title verification failed")
            assert False

        lp = Loginpage(driver)
        lp.setUserName(Readconfig.getUsername())
        lp.setPassword(Readconfig.getUserpassword())
        lp.clickLogin()

        act_title = driver.title
        if act_title == "| DigiTathya - Admin Panel":
            assert True
            self.logger.info("Login successful")
        else:
            driver.save_screenshot(".\\screenshots\\test_login.png")
            self.logger.error("Login failed")
            assert False

