import pytest
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.QR_Management.QR_management_category import QR_Management_Category_Page
from pages.QR_Management.QR_management_products import QR_Management_products_Page
from utilities.customlogger import LogGen
from pages.common.base_page import BaseTest
from utilities.read_excel import get_test_data
from utilities.screenshot_util import take_screenshot
from utilities.sku_utils import generate_next_sku

# Excel path
excel_path = r"mf_products_data.xlsx"
test_data = get_test_data(excel_path, "products")

@pytest.mark.order(2)
@pytest.mark.parametrize("data", test_data)
class Test_product_filter_toggle_edit(BaseTest):
    logger = LogGen.loggen()

    current_sku = "PRD2025X0012"

    def test_QR_management_products_flow(self, driver, data):

        self.logger.info(
            f"===== QR Management Products Flow ==="
        )
        product_name = data["search_value"]
        filter_status = data["filter_status"]
        start_date = data["start_date"]
        end_date = data["end_date"]
        filter_category = data["filter_category"]
        filter_created_by = data["filter_created_by"]

        wait = WebDriverWait(driver, 5)

        # LOGIN
        if data == test_data[0]:
            self.driver = driver
            self.login_and_access()
            self.logger.info("Login successful (first iteration)")
        else:
            self.logger.info("Skipping login — already logged in")

        # NAVIGATION
        self.logger.info("Navigating to Products module")
        qr_page = QR_Management_Category_Page(driver)

        qr_page.Click_Dashboard()
        driver.refresh()
        qr_page.Click_QR_management()

        qr_products_page = QR_Management_products_Page(driver)

        qr_products_page.Click_products()
        qr_products_page.click_filter_toggle_btn()
        qr_products_page.Enter_filter_product_name(product_name)
        # qr_products_page.selectfilter_status(filter_status)
        qr_products_page.Enter_filter_category(filter_category)
        qr_products_page.Enter_filter_created_by(filter_created_by)
        qr_products_page.click_filter_created_date()
        qr_products_page.select_date_range(start_date,end_date)
        qr_products_page.click_apply_btn()

        status = qr_products_page.search_product(product_name)  # True if rows exist

        if not status:
            take_screenshot(
                driver,
                test_name="product_filter_failed",
                folder_name="Screenshots\\QRM_products\\product_filters"
            )
            self.logger.error("FILTER FAILED | No data found ")
            assert status, "FILTER FAILED | No data found "
        self.logger.info("Filter applied successfully, table has records")

        qr_products_page.click_actions_icon()
        time.sleep(1)
        qr_products_page.click_edit_opt()
        time.sleep(1)

        qr_products_page.Enter_product_name_or_Id(data["edit_product_name"])
        qr_products_page.Enter_brand_name(data["edit_brand_name"])

        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # IMAGE UPLOAD
        try:
            qr_products_page.Upload_Product_images(data["edit_upload_product_image"])
            self.logger.info("Product image uploaded successfully")

        except Exception as e:
            self.logger.error(
                f"Image upload failed for {data['edit_product_name']} | Error: {e}"
            )
            return

        qr_products_page.Enter_Product_URL(data["edit_product_url"])

        qr_products_page.Enter_SKU_ID(data["edit_SKU_ID"])


        # PRODUCT DETAILS
        qr_products_page.select_category_opt()
        qr_products_page.Enter_category_name(data["edit_select_category"])
        qr_products_page.select_status_drp(data["edit_status"])
        qr_products_page.Enter_description(data["edit_description"])
        qr_products_page.Country_option()
        qr_products_page.Country_of_origin(data["edit_country"])

        qr_products_page.Click_Proceed_to_child_SKU_button()

        try:
            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located(
                    qr_products_page.continue_to_video_btn
                )
            )
            qr_products_page.ClicK_continue_video_btn()

        except TimeoutException:
            print("please check and fill All the fields correctly")
            take_screenshot(
                driver,
                test_name="test_edit_product",
                folder_name="Screenshots\\QRM_products\\product_edit_failed"

            )
            assert False, "Please check and fill all the fields correctly"


        qr_products_page.Enter_video_title(data["edit_video_title"])
        qr_products_page.Choose_video_file(data["edit_video_file"])

        qr_products_page.Click_create_product_submit_btn()

        # TOAST
        try:
            toast_msg = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".toastify"))
            ).text.strip()

            self.logger.info(f"Toast message: {toast_msg}")

        except TimeoutException:
            toast_msg = ""
            self.logger.error("Toast message not displayed")

        # VALIDATION
        if "Product updated successfully!" in toast_msg:

            self.logger.info(
                f"Product created successfully | "
                f"Product: {data['edit_product_name']}"
            )
            assert True

        else:
            take_screenshot(
                driver,
                test_name="test_edit_product",
                folder_name="Screenshots\\QRM_products\\product_edit_failed"
            )

            self.logger.error(
                f"Product update failed | "
                f"Product: {data['edit_product_name']} | "
                f"Toast: {toast_msg}"
            )

            assert False, f"Product update failed | Toast: {toast_msg}"



