
from pages.common.AccessCodePage import AccessCodePage
from pages.QR_Management.login_page import Loginpage
from utilities.readproperties import Readconfig

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

