import pytest
import time
from selenium.webdriver.common.by import By
from pages.common.AccessCodePage import AccessCodePage
from pages.QR_Management.login_page import Loginpage
from pages.QR_Management.QR_management_category import QR_Management_Category_Page
from utilities.read_excel import get_test_data  # your existing Excel utility
from utilities.readproperties import Readconfig
from utilities.customlogger import LogGen
from pages.common.base_page import BaseTest
from utilities.screenshot_util import take_screenshot

# Excel file containing category data
excel_path = r"C:\Users\Suresh V\Desktop\automation\mf_products_data.xlsx"
test_data = get_test_data(excel_path, "category")  # Sheet name: Category

@pytest.mark.order(2)
@pytest.mark.parametrize("data", test_data)
class Test_QRM_category(BaseTest):
    logger = LogGen.loggen()

    def test_QR_management_category_flow(self, driver, data):

        category = data["Category"]
        status = data["status"]

        # for one by one execution

        if data == test_data[0]:
            self.driver = driver
            self.login_and_access()
            self.logger.info("Login completed for first iteration")

            # # Check if login succeeded
            # if "dashboard" not in driver.current_url.lower():  # or use some element only visible on dashboard
            #     self.logger.error("Login failed! Check username/password")
            #     driver.save_screenshot(".\\screenshots\\test_login_failed.png")
            #     assert False, "Login failed Check username/password — cannot proceed to QR category"

        else:
            self.logger.info("Skipping login ")

        # Step 3: Category actions
        qr_page = QR_Management_Category_Page(driver)
        qr_page.Click_Dashboard()
        qr_page.Click_QR_management()
        qr_page.click_category()
        qr_page.click_create_category_button()
        qr_page.Enter_category_value(category)
        qr_page.click_category_status(status)
        qr_page.click_save_button()
        time.sleep(1)

        success_msg_category = driver.find_element(By.TAG_NAME, "body").text
        time.sleep(1)
        if "Category Created Successfully!" in success_msg_category:
            assert True
            self.logger.info("Category created successfully")

        else:
            take_screenshot(
                driver,
                test_name="test_create_category_failed",
                folder_name="Screenshots\\QRM_category"
            )
            self.logger.error("Create category failed,  please Enter category field correctly ")
            qr_page.Click_exit_option()
            assert False," please  Enter category field correctly"

        time.sleep(3)
