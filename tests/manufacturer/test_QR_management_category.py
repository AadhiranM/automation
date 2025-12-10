import pytest
import time
from selenium.webdriver.common.by import By
from pages.common.AccessCodePage import AccessCodePage
from pages.QR_Management.login_page import Loginpage
from pages.QR_Management.QR_management_category import QR_Management_Category_Page
from utilities.readproperties import Readconfig
from utilities.customlogger import LogGen


@pytest.mark.order(2)
class Test_002_QR_management:
    logger = LogGen.loggen()
    category = "lenss"
    status = "Active"

    def test_QR_management_category_flow(self, driver):
        self.logger.info("===== QR Management Category Test Started =====")

        # Step 1: Access code
        ac_page = AccessCodePage(driver)
        ac_page.enter_access_code(Readconfig.getAccessCode())

        # Step 2: Login
        lp = Loginpage(driver)
        lp.setUserName(Readconfig.getUsername())
        lp.setPassword(Readconfig.getUserpassword())
        lp.clickLogin()
        self.logger.info("Login completed for Category test")

        # Step 3: Category actions
        qr_page = QR_Management_Category_Page(driver)
        qr_page.Click_QR_management()
        qr_page.click_category()
        qr_page.click_create_category_button()
        qr_page.Enter_category_value(self.category)
        qr_page.click_category_status(self.status)
        qr_page.click_save_button()
        time.sleep(1)

        success_msg_category =driver.find_element(By.TAG_NAME, "body").text
        time.sleep(1)
        if "Category Created Successfully!" in success_msg_category:
            assert True
            self.logger.info("Category created successfully")

        else:
            driver.save_screenshot(".\\Screenshots\\test_create_category_scr.png")
            self.logger.error("Create category failed")
            qr_page.Click_exit_option()
            assert False
        time.sleep(3)


