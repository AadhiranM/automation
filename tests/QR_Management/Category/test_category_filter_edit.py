import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.QR_Management.QR_management_category import QR_Management_Category_Page
from utilities.read_excel import get_test_data
from utilities.customlogger import LogGen
from pages.common.base_page import BaseTest
from utilities.screenshot_util import take_screenshot
from selenium.common.exceptions import TimeoutException

# excel_path = r"/mf_products_data.xlsx"
excel_path = r"mf_products_data.xlsx"
test_data = get_test_data(excel_path, "category")

@pytest.mark.order(2)
@pytest.mark.parametrize("data", test_data)
class Test_category_filter_edit(BaseTest):

    logger = LogGen.loggen()
    def test_QR_management_category_flow(self, driver, data):

        category_name = data["category_name"]
        filter_status = data["filter_status"]
        start_date = data["start_date"]
        end_date = data["end_date"]

        edit_category_name = data["edit_category_name"]
        edit_status = data["edit_status"]

        self.logger.info("===== TEST STARTED: QR CATEGORY CREATION =====")
        self.logger.info(f"Category: {category_name} | Status: {filter_status}")

        wait = WebDriverWait(driver, 4)

        # self.driver = driver
        # self.login_and_access()

        # ---------------- LOGIN ----------------
        if data == test_data[0]:
            self.driver = driver
            self.login_and_access()
            self.logger.info("Login successful (first iteration)")
        else:
            self.logger.info("Skipping login — already logged in")

        # ---------------- NAVIGATION ----------------
        self.logger.info("Navigating to Category module")

        qr_page = QR_Management_Category_Page(driver)

        driver.refresh()

        qr_page.Click_Dashboard()
        self.logger.info("Clicked Dashboard")

        qr_page.Click_QR_management()
        self.logger.info("Opened QR Management")

        qr_page.click_category()
        self.logger.info("Opened Category section")

        qr_page.Enter_search_field(category_name)
        self.logger.info("Entered search field")
        time.sleep(2)

        qr_page.Click_calender_date_range()
        self.logger.info("Clicked calender date range")
        time.sleep(2)
        qr_page.select_date_range(start_date, end_date)
        qr_page.Enter_select_status(filter_status)
        self.logger.info("Selected status")


        status = qr_page.search_product(category_name)  # True if rows exist

        if not status:
            take_screenshot(
                driver,
                test_name="category_filter_failed",
                folder_name="Screenshots\\QRM_category\\category_filters"
            )
            self.logger.error("FILTER FAILED | No data found ")
            assert status, "FILTER FAILED | No data found "
        self.logger.info("Filter applied successfully, table has records")

        qr_page.click_actions_icon()
        time.sleep(1)
        qr_page.click_edit_opt()
        time.sleep(1)
        qr_page.enter_edit_category_name(edit_category_name)
        time.sleep(1)
        qr_page.select_edit_status(edit_status)
        time.sleep(1)
        qr_page.click_edit_update_btn()

        try:
            toast_text = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".toastify"))
            ).text

            print("Toast:", toast_text)

        except TimeoutException:
            toast_text = "Toast message not displayed"

            print("Toast:", toast_text)

            self.logger.error("Toast message not displayed after schedule report creation")

        if "Category Updated Successfully!" in toast_text:

            self.logger.info(
                f"Category Updated Successfully!"
            )

        else:

            self.logger.error(
                f"Category Updation FAILED | "
            )

            take_screenshot(
                driver,
                test_name="category_update_fail",
                folder_name="Screenshots\\QRM_category\\update_category_fail"
            )

            assert False, (
                f"category updation failed | Toast: {toast_text}"
            )