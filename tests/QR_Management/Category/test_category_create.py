import pytest
import time
import random
import string
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

@pytest.mark.order(1)
@pytest.mark.parametrize("data", test_data)
class Test_category_create(BaseTest):

    logger = LogGen.loggen()

    def test_QR_management_category_flow(self, driver, data):

        # Generate a dynamic category name with 5–10 uppercase letters
        category = random.choice(string.ascii_uppercase) + ''.join(
            random.choices(string.ascii_lowercase, k=random.randint(4, 9))
        )

        status = data["status"]

        self.logger.info("===== TEST STARTED: QR CATEGORY CREATION =====")
        self.logger.info(f"Category: {category} | Status: {status}")

        wait = WebDriverWait(driver, 10)

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

        qr_page.click_create_category_button()
        self.logger.info("Clicked Create Category button")

        # ---------------- ACTION ----------------
        qr_page.Enter_category_value(category)
        self.logger.info(f"Entered category: {category}")

        qr_page.click_category_status(status)
        self.logger.info(f"Selected status: {status}")

        qr_page.click_save_button()
        self.logger.info("Clicked Save button")

        # ---------------- TOAST VALIDATION ----------------
        try:
            toast_element = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, ".toastify")
                )
            )

            toast = toast_element.text.strip()
            toast = toast.encode("ascii", errors="ignore").decode()

            self.logger.info(f"Toast received: {toast}")
            print("Toast Message:", toast)

        except TimeoutException:
            toast = "Toast message not displayed"
            self.logger.error("Toast not displayed within time")

        # ---------------- FINAL VALIDATION ----------------
        if "Category Created Successfully!" in toast:

            self.logger.info(
                f"Category created successfully | {category}"
            )
            self.logger.info("===== TEST PASSED =====")

        else:
            self.logger.error(
                f"Category creation failed | Toast: {toast}"
            )

            take_screenshot(
                driver,
                test_name="test_create_category_failed",
                folder_name="Screenshots\\QR_Management\\QRM_category\\create_category"
            )

            self.logger.error("===== TEST FAILED =====")

            assert False, f"Category creation failed | Toast: {toast}"