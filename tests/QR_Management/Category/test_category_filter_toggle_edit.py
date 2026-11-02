

import pytest
import time
import random
import string
from datetime import datetime, timedelta
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

@pytest.mark.order(3)
@pytest.mark.parametrize("data", test_data)
class Test_category_filter_toggle_edit(BaseTest):

    logger = LogGen.loggen()

    def test_QR_management_category_flow(self, driver, data):

        filter_status = data["filter_status"]
        edit_status = data["edit_status"]

        # Generate dynamic edit category name (5-10 letters)
        edit_category_name = random.choice(string.ascii_uppercase) + ''.join(
            random.choices(string.ascii_lowercase, k=random.randint(4, 9))
        )

        self.logger.info("===== TEST STARTED: QR CATEGORY FILTER TOGGLE EDIT =====")

        wait = WebDriverWait(driver, 4)

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

        # ---------------- GET CATEGORY NAME AND DATE ----------------
        wait = WebDriverWait(driver, 10)

        category_name = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//tbody/tr[1]/td[2]")
            )
        ).text.strip()

        date_value = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//tbody/tr[1]/td[5]")
            )
        ).text.strip()

        actual_date = datetime.strptime(
            date_value, "%d %b %Y %I:%M %p"
        )

        start_date = (
            actual_date - timedelta(days=1)
        ).strftime("%Y-%m-%d")

        end_date = actual_date.strftime("%Y-%m-%d")

        print("Category Name:", category_name)
        print("Start Date:", start_date)
        print("End Date:", end_date)
        print("Edit Category Name:", edit_category_name)

        self.logger.info(f"Category Name: {category_name}")
        self.logger.info(f"Start Date: {start_date}")
        self.logger.info(f"End Date: {end_date}")
        self.logger.info(f"Edit Category Name: {edit_category_name}")

        # ---------------- FILTER TOGGLE ----------------
        qr_page.Click_filter_toggle()

        qr_page.Enter_filter_toggle_category_field(category_name)
        self.logger.info("Entered category name in filter")

        qr_page.select_filter_toggle_status(filter_status)
        self.logger.info("Selected status")
        time.sleep(1)

        qr_page.Click_filter_toggle_date_range()
        self.logger.info("Clicked calender date range")
        time.sleep(1)

        qr_page.select_date_range(start_date, end_date)
        time.sleep(1)

        qr_page.Click_filter_toggle_apply_btn()
        self.logger.info("Clicked apply button")
        time.sleep(1)

        status = qr_page.search_product(category_name)  # True if rows exist

        if not status:
            take_screenshot(
                driver,
                test_name="category_filter_failed",
                folder_name="Screenshots\\QR_Management\\QRM_category\\category_filters"
            )
            self.logger.error("FILTER FAILED | No data found ")
            assert status, "FILTER FAILED | No data found "

        self.logger.info("Filter applied successfully, table has records")

        # ---------------- EDIT CATEGORY ----------------
        qr_page.click_actions_icon()
        time.sleep(1)

        qr_page.click_edit_opt()
        time.sleep(1)

        qr_page.enter_edit_category_name(edit_category_name)
        time.sleep(1)

        qr_page.select_edit_status(edit_status)
        time.sleep(1)

        qr_page.click_edit_update_btn()

        # ---------------- TOAST VALIDATION ----------------
        try:
            toast_text = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".toastify"))
            ).text

            toast_text = toast_text.encode("ascii", errors="ignore").decode()

            print("Toast:", toast_text)

        except TimeoutException:
            toast_text = "Toast message not displayed"

            print("Toast:", toast_text)

            self.logger.error("Toast message not displayed")

        # ---------------- FINAL VALIDATION ----------------
        if "Category Updated Successfully!" in toast_text:

            self.logger.info("Category Updated Successfully!")

        else:

            self.logger.error("Category Updation FAILED")

            take_screenshot(
                driver,
                test_name="category_update_fail",
                folder_name="Screenshots\\QR_Management\\QRM_category\\update_category_fail"
            )

            assert False, (
                f"category updation failed | Toast: {toast_text}"
            )