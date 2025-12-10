
import pytest
import time
from selenium.webdriver.common.by import By
from pages.QR_Management.QR_management_category import QR_Management_Category_Page
from pages.QR_Management.QR_management_variants import QR_Management_variants_Page
from utilities.customlogger import LogGen
from pages.common.base_page import BaseTest


@pytest.mark.order(3)
class Test_003_QR_management_variants(BaseTest):
    logger = LogGen.loggen()
    category_name = "lenss"
    variants_type = "001"
    variants_value = "black"

    def test_QR_management_variants_flow(self, driver):
        self.logger.info("===== QR Management Variants Test Started =====")

        # this need to enable if want to run this specific module
        # self.driver = driver
        # self.login_and_access()

        # Navigate to QR Management (already logged in from Category test)
        qr_page = QR_Management_Category_Page(driver)
        qr_page.Click_Dashboard()
        qr_page.Click_QR_management()

        # Variants Page
        qr_variants_page = QR_Management_variants_Page(driver)

        qr_variants_page.Click_variants()
        qr_variants_page.click_create_button()
        qr_variants_page.click_category_option()
        qr_variants_page.Enter_category_field(self.category_name)
        time.sleep(2)
        qr_variants_page.Click_Category_Entered_name()
        qr_variants_page.Enter_variants_type_field(self.variants_type)
        qr_variants_page.Enter_variants_value_field(self.variants_value)
        time.sleep(2)
        qr_variants_page.click_save_variants_button()
        time.sleep(1)
        success_msg_variant=driver.find_element(By.TAG_NAME,"body").text
        time.sleep(1)
        if "Variants saved successfully" in success_msg_variant:
            assert True
            self.logger.info("Variants saved successfully")
        else:
            driver.save_screenshot(".\\Screenshots\\test_create_variant_scr.png")
            self.logger.error("Create variant failed")
            assert False
        time.sleep(3)
