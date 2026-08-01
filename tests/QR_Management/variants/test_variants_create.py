# import pytest
# import time
# from selenium.webdriver.common.by import By
# from pages.QR_Management.QR_management_category import QR_Management_Category_Page
# from pages.QR_Management.QR_management_variants import QR_Management_variants_Page
# from utilities.customlogger import LogGen
# from pages.common.base_page import BaseTest
# from utilities.read_excel import get_test_data  # your Excel utility
# from utilities.screenshot_util import take_screenshot
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
#
#
# # Excel file containing variants data
# excel_path = r"C:\Users\Suresh V\Desktop\automation\mf_products_data.xlsx"
# test_data = get_test_data(excel_path,"variants")  # Sheet name: Variants
#
# @pytest.mark.order(3)
# @pytest.mark.parametrize("data", test_data)
# class Test_QRM_variants(BaseTest):
#     logger = LogGen.loggen()
#
#     def test_QR_management_variants_flow(self, driver, data):
#         self.logger.info("===== QR Management Variants Test Started =====")
#         wait = WebDriverWait(driver, 10)
#
#         # this need to enable if want to run this specific module
#         if data == test_data[0]:
#             self.driver = driver
#             self.login_and_access()
#             self.logger.info("Login completed for first iteration")
#         else:
#             self.logger.info("Skipping login")
#
#         category_name = data["Category"]        # Match Excel header
#         variants_type = data["variants_type"]
#         variants_value = data["variants_value"]
#
#         # Navigate to QR Management (already logged in)
#         qr_page = QR_Management_Category_Page(driver)
#         driver.refresh()
#         qr_page.Click_Dashboard()
#         qr_page.Click_QR_management()
#
#         # Variants Page
#         qr_variants_page = QR_Management_variants_Page(driver)
#
#         qr_variants_page.Click_variants()
#         qr_variants_page.click_create_button()
#         qr_variants_page.click_category_option()
#         qr_variants_page.Enter_category_field(category_name)
#         try:
#             qr_variants_page.Click_Category_Entered_name()
#         except:
#             self.logger.warning(f"No category found with name '{category_name}'. Variant '{variants_value}' cannot be created.")
#             assert False,"No category found in that name"
#             return
#
#         # qr_variants_page.Click_Category_Entered_name()
#         qr_variants_page.Enter_variants_type_field(variants_type)
#         qr_variants_page.Enter_variants_value_field(variants_value)
#
#         qr_variants_page.click_save_variants_button()
#         time.sleep(1)
#
#         try:
#             toast_text = WebDriverWait(driver, 5).until(
#                 EC.visibility_of_element_located((By.CSS_SELECTOR, ".toastify"))
#             ).text
#             print("Toast:", toast_text)
#         except TimeoutException:
#             toast_text = "Toast not displayed"
#
#         # VALIDATION
#         if toast_text and "Variants saved successfully" in toast_text:
#             self.logger.info(f"Variant created successfully | {toast_text}")
#         else:
#             take_screenshot(
#                 driver,
#                 test_name="test_create_variant_failed",
#                 folder_name="Screenshots\\QRM_Variants"
#             )
#             self.logger.error(
#                 f"Create variant failed for '{variants_value}' | Toast: {toast_text}"
#             )
#             assert False, f"Variant creation failed | Toast: {toast_text}"

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

@pytest.mark.order(1)
@pytest.mark.parametrize("data", test_data)
class Test_variants_create(BaseTest):

    logger = LogGen.loggen()

    def test_QR_management_variants_flow(self, driver, data):

        self.logger.info("===== TEST STARTED: QR MANAGEMENT VARIANTS =====")

        wait = WebDriverWait(driver, 10)

        ---------------- LOGIN ----------------
        if data == test_data[0]:
            self.driver = driver
            self.login_and_access()
            self.logger.info("Login successful (first iteration)")
        else:
            self.logger.info("Skipping login — already logged in")

        category_name = data["Category"]
        variants_type = data["variants_type"]
        variants_value = data["variants_value"]

        self.logger.info(f"Category: {category_name}")
        self.logger.info(f"Variant Type: {variants_type}")
        self.logger.info(f"Variant Value: {variants_value}")

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

        qr_variants_page.click_create_button()
        self.logger.info("Clicked Create Variant button")

        qr_variants_page.click_category_option()
        self.logger.info("Opened Category dropdown")

        qr_variants_page.Enter_category_field(category_name)
        self.logger.info(f"Entered category: {category_name}")

        try:
            qr_variants_page.Click_Category_Entered_name()
            self.logger.info("Category selected successfully")

        except:
            self.logger.warning(
                f"No category found: {category_name} | Cannot proceed with variant creation"
            )
            self.logger.error("TEST FAILED - Category not found")
            assert False, "No category found in that name"

        qr_variants_page.Enter_variants_type_field(variants_type)
        self.logger.info(f"Entered variant type: {variants_type}")

        qr_variants_page.Enter_variants_value_field(variants_value)
        self.logger.info(f"Entered variant value: {variants_value}")

        qr_variants_page.click_save_variants_button()
        self.logger.info("Clicked Save Variant button")

        time.sleep(1)

        # ---------------- TOAST VALIDATION ----------------
        try:
            toast_text = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".toastify"))
            ).text
            toast_text = toast_text.encode("ascii", errors="ignore").decode()
            print("Toast:", toast_text)
            self.logger.info(f"Toast received: {toast_text}")

        except TimeoutException:
            toast_text = "Toast not displayed"
            self.logger.error("Toast not displayed within time")

        # ---------------- FINAL VALIDATION ----------------
        if toast_text and "Variants saved successfully" in toast_text:
            self.logger.info(f"Variant created successfully | {variants_value}")
            self.logger.info("===== TEST PASSED =====")

        else:
            take_screenshot(
                driver,
                test_name="test_create_variant_failed",
                folder_name="Screenshots\\QRM_variant\\create_variant_failed"
            )
            self.logger.error(
                f"Variant creation failed | Value: {variants_value} | Toast: {toast_text}"
            )

            self.logger.error("===== TEST FAILED =====")

            assert False, f"Variant creation failed | Toast: {toast_text}"


