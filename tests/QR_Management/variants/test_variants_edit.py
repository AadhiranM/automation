import pytest
import time
from selenium.webdriver.common.by import By
from pages.QR_Management.QR_management_category import QR_Management_Category_Page
from pages.QR_Management.QR_management_variants import QR_Management_variants_Page
from utilities.customlogger import LogGen
from pages.common.base_page import BaseTest
from utilities.read_excel import get_test_data
from utilities.screenshot_util import take_screenshot
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


excel_path = r"mf_products_data.xlsx"
test_data = get_test_data(excel_path, "variants")

@pytest.mark.order(2)
@pytest.mark.parametrize("data", test_data)
class Test_variants_edit(BaseTest):

    logger = LogGen.loggen()

    def test_QR_management_variants_flow(self, driver, data):

        self.logger.info("===== TEST STARTED: QR MANAGEMENT VARIANTS =====")

        wait = WebDriverWait(driver, 10)

        # ---------------- LOGIN ----------------

        # if data == test_data[0]:
        #     self.driver = driver
        #     self.login_and_access()
        #     self.logger.info("Login successful (first iteration)")
        # else:
        #     self.logger.info("Skipping login — already logged in")

        search_category_name = data["search_Category"]
        edit_variants_type = data["edit_variants_type"]
        edit_variants_value = data["edit_variants_value"]

        self.logger.info(f"Category: {search_category_name}")
        self.logger.info(f"Variant Type: {edit_variants_type}")
        self.logger.info(f"Variant Value: {edit_variants_value}")

        # ---------------- NAVIGATION ----------------
        self.logger.info("Navigating to QR Management module")

        qr_page = QR_Management_Category_Page(driver)
        driver.refresh()

        qr_page.Click_Dashboard()
        self.logger.info("Clicked Dashboard")

        qr_page.Click_QR_management()
        self.logger.info("Opened QR Management")

        # ---------------- VARIANTS FLOW ----------------
        qr_variants_page = QR_Management_variants_Page(driver)

        qr_variants_page.Click_variants()
        self.logger.info("Opened Variants section")

        qr_variants_page.Enter_search_category_name(search_category_name)
        self.logger.info(f"Searched for category: {search_category_name}")

        status = qr_variants_page.search_product(search_category_name)  # True if rows exist

        if not status:
            take_screenshot(
                driver,
                test_name="variant_filter_failed",
                folder_name="Screenshots\\QRM_variant\\variant_filters"
            )
            self.logger.error("FILTER FAILED | No data found ")
            assert status, "FILTER FAILED | No data found "
        self.logger.info("Filter applied successfully, table has records")

        qr_variants_page.click_actions_icon()
        self.logger.info("Clicked actions icon")
        qr_variants_page.click_edit_opt()
        self.logger.info("Clicked edit option")
        qr_variants_page.Enter_edit_variant_type(edit_variants_type)
        self.logger.info(f"Entered variant type: {edit_variants_type}")
        qr_variants_page.Enter_edit_variant_value(edit_variants_value)
        self.logger.info(f"Entered variant value: {edit_variants_value}")
        qr_variants_page.click_update_btn()
        self.logger.info("Clicked update button")

        try:
            toast_text = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".toastify"))
            ).text
            toast_text = toast_text.encode("ascii", errors="ignore").decode()
            print("Toast:", toast_text)

        except TimeoutException:
            toast_text = "Toast message not displayed"

            print("Toast:", toast_text)

            self.logger.error("Toast message not displayed after schedule report creation")

        if "Variants updated successfully" in toast_text:

            self.logger.info(
                f"variants Updated Successfully!"
            )

        else:

            self.logger.error(
                f"variants Updation FAILED | "
            )

            take_screenshot(
                driver,
                test_name="variants_update_fail",
                folder_name="Screenshots\\QRM_variant\\update_variants_fail"
            )

            assert False, (
                f"variants updation failed | Toast: {toast_text}"
            )





