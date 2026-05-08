
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.common.AccessCodePage import AccessCodePage
from pages.QR_Management.login_page import Loginpage
from pages.QR_Management.QR_management_category import QR_Management_Category_Page
from utilities.read_excel import get_test_data
from utilities.readproperties import Readconfig
from utilities.customlogger import LogGen
from pages.common.base_page import BaseTest
from utilities.screenshot_util import take_screenshot
from selenium.common.exceptions import TimeoutException


# Excel file containing category data
excel_path = r"C:\Users\Suresh V\Desktop\automation\mf_products_data.xlsx"
test_data = get_test_data(excel_path, "category")

@pytest.mark.order(2)
@pytest.mark.parametrize("data", test_data)
class Test_QRM_category(BaseTest):
    logger = LogGen.loggen()

    def test_QR_management_category_flow(self, driver, data):
        category = data["Category"]
        status = data["status"]

        wait = WebDriverWait(driver,4)

        if data == test_data[0]:
            self.driver = driver
            self.login_and_access()
            self.logger.info("Login completed for first iteration")
        else:
            self.logger.info("Skipping login ")

        qr_page = QR_Management_Category_Page(driver)
        driver.refresh()
        qr_page.Click_Dashboard()
        qr_page.Click_QR_management()
        qr_page.click_category()
        qr_page.click_create_category_button()
        qr_page.Enter_category_value(category)
        qr_page.click_category_status(status)
        qr_page.click_save_button()


        try:
            success_msg_category = WebDriverWait(driver,3).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, ".toastify")
                )
            ).text
            print("Success Message:", success_msg_category)
            assert "Category Created Successfully!" in success_msg_category
            self.logger.info("Category created successfully")

        except TimeoutException:
            take_screenshot(
                driver,
                test_name="test_create_category_failed",
                folder_name="Screenshots\\QRM_category"
            )

            self.logger.error("Category creation failed or success message not displayed")
            assert False, "Category creation failed - please  Enter category field correctly"