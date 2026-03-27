
from pages.common.AccessCodePage import AccessCodePage
from pages.QR_Management.login_page import Loginpage
from utilities.readproperties import Readconfig

import time
import pytest
from selenium.webdriver.support.wait import WebDriverWait

class BaseTest:
    def login_and_access(self):
        # Step 1: Access Code
        ac_page = AccessCodePage(self.driver)
        ac_present = ac_page.enter_access_code(Readconfig.getAccessCode())
        if ac_present:
            print("Access code entered successfully")
        else:
            print("Access code page not present, continuing")

        # Step 2: Login
        lp = Loginpage(self.driver)
        lp.setUserName(Readconfig.getUsername())
        lp.setPassword(Readconfig.getUserpassword())
        lp.clickLogin()

        current_url = self.driver.current_url

        if "dashboard" in current_url:
            self.logger.info("Login successful")
            assert True
        else:
            self.logger.error("Login failed! Check username/password")
            self.driver.save_screenshot(".\\screenshots\\test_login_failed.png")
            assert False, "Login failed Check username/password"
