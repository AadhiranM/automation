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
            f"===== QR Management Products Edit Flow Started | Product: {data['edit_product_name']} ====="
        )

        product_name = data["search_value"]
        filter_status = data["filter_status"]
        start_date = data["start_date"]
        end_date = data["end_date"]
        filter_category = data["filter_category"]
        filter_created_by = data["filter_created_by"]

        self.logger.info(
            f"Filter Details | Product: {product_name} | "
            f"Status: {filter_status} | Category: {filter_category} | "
            f"Created By: {filter_created_by} | "
            f"Date Range: {start_date} to {end_date}"
        )

        wait = WebDriverWait(driver, 5)

        # LOGIN
        # if data == test_data[0]:
        #     self.driver = driver
        #     self.login_and_access()
        #     self.logger.info("Login successful (first iteration)")
        # else:
        #     self.logger.info("Skipping login — already logged in")

        # NAVIGATION
        self.logger.info("Starting navigation to Products module")

        qr_page = QR_Management_Category_Page(driver)

        qr_page.Click_Dashboard()
        self.logger.info("Clicked Dashboard")

        driver.refresh()
        self.logger.info("Page refreshed successfully")

        qr_page.Click_QR_management()
        self.logger.info("Opened QR Management module")

        qr_products_page = QR_Management_products_Page(driver)

        qr_products_page.Click_products()
        self.logger.info("Opened Products page")

        qr_products_page.click_filter_toggle_btn()
        self.logger.info("Opened Filter Toggle panel")

        qr_products_page.Enter_filter_product_name(product_name)
        self.logger.info(f"Entered Product Name filter: {product_name}")

        qr_products_page.select_filter_toggle_status(filter_status)
        self.logger.info(f"Selected Status filter: {filter_status}")

        qr_products_page.Enter_filter_category(filter_category)
        self.logger.info(f"Entered Category filter: {filter_category}")

        qr_products_page.Enter_filter_created_by(filter_created_by)
        self.logger.info(f"Entered Created By filter: {filter_created_by}")

        qr_products_page.click_filter_created_date()
        self.logger.info("Opened Created Date filter")

        qr_products_page.select_date_range(start_date, end_date)
        self.logger.info(
            f"Selected Date Range | Start Date: {start_date} | End Date: {end_date}"
        )

        qr_products_page.click_apply_btn()
        self.logger.info("Clicked Apply Filter button")

        status = qr_products_page.search_product(product_name)  # True if rows exist

        if not status:
            take_screenshot(
                driver,
                test_name="product_filter_failed",
                folder_name="Screenshots\\QRM_products\\product_filters"
            )

            self.logger.error(
                f"FILTER FAILED | Product: {product_name} | No matching records found"
            )

            assert status, "FILTER FAILED | No data found "

        self.logger.info(
            f"Filter applied successfully | Product: {product_name} | Records found"
        )

        qr_products_page.click_actions_icon()
        self.logger.info("Clicked Actions icon")

        time.sleep(1)

        qr_products_page.click_edit_opt()
        self.logger.info("Clicked Edit option")

        time.sleep(1)

        qr_products_page.Enter_product_name_or_Id(data["edit_product_name"])
        self.logger.info(
            f"Updated Product Name: {data['edit_product_name']}"
        )

        qr_products_page.Enter_brand_name(data["edit_brand_name"])
        self.logger.info(
            f"Updated Brand Name: {data['edit_brand_name']}"
        )

        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # IMAGE UPLOAD
        try:
            qr_products_page.Upload_Product_images(data["edit_upload_product_image"])

            self.logger.info(
                f"Product image uploaded successfully | "
                f"File: {data['edit_upload_product_image']}"
            )

        except Exception as e:
            self.logger.error(
                f"Image upload failed for {data['edit_product_name']} | Error: {e}"
            )
            return

        qr_products_page.Enter_Product_URL(data["edit_product_url"])
        self.logger.info(
            f"Entered Product URL: {data['edit_product_url']}"
        )

        qr_products_page.Enter_SKU_ID(data["edit_SKU_ID"])
        self.logger.info(
            f"Entered SKU ID: {data['edit_SKU_ID']}"
        )

        # PRODUCT DETAILS
        qr_products_page.select_category_opt()
        self.logger.info("Opened Category dropdown")

        qr_products_page.Enter_category_name(data["edit_select_category"])
        self.logger.info(
            f"Selected Category: {data['edit_select_category']}"
        )

        qr_products_page.select_status_drp(data["edit_status"])
        self.logger.info(
            f"Selected Status: {data['edit_status']}"
        )

        qr_products_page.Enter_description(data["edit_description"])
        self.logger.info("Entered Product Description")

        qr_products_page.Country_option()
        self.logger.info("Opened Country dropdown")

        qr_products_page.Country_of_origin(data["edit_country"])
        self.logger.info(
            f"Selected Country of Origin: {data['edit_country']}"
        )

        qr_products_page.Click_Proceed_to_child_SKU_button()
        self.logger.info("Clicked Proceed to Child SKU button")

        try:
            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located(
                    qr_products_page.continue_to_video_btn
                )
            )

            self.logger.info("Continue To Video button displayed")

            qr_products_page.ClicK_continue_video_btn()
            self.logger.info("Clicked Continue To Video button")

        except TimeoutException:
            print("please check and fill All the fields correctly")

            self.logger.error(
                "Continue To Video button not displayed. Mandatory fields may be missing."
            )

            take_screenshot(
                driver,
                test_name="test_edit_product",
                folder_name="Screenshots\\QRM_products\\product_edit_failed"
            )

            self.logger.error(
                "Screenshot captured for product edit failure"
            )

            assert False, "Please check and fill all the fields correctly"

        qr_products_page.Enter_video_title(data["edit_video_title"])
        self.logger.info(
            f"Entered Video Title: {data['edit_video_title']}"
        )

        qr_products_page.Choose_video_file(data["edit_video_file"])
        self.logger.info(
            f"Uploaded Video File: {data['edit_video_file']}"
        )

        qr_products_page.Click_create_product_submit_btn()
        self.logger.info("Clicked Submit button")

        # TOAST
        self.logger.info("Waiting for toast message")

        try:
            toast_msg = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".toastify"))
            ).text.strip()
            toast_msg = toast_msg.encode("ascii", errors="ignore").decode()

            self.logger.info(f"Toast received: {toast_msg}")

        except TimeoutException:
            toast_msg = ""
            self.logger.error("Toast message not displayed")

        # VALIDATION
        if "Product updated successfully!" in toast_msg:

            self.logger.info(
                f"Product updated successfully | "
                f"Product: {data['edit_product_name']} | "
                f"Toast: {toast_msg}"
            )

            assert True

        else:
            take_screenshot(
                driver,
                test_name="test_edit_product",
                folder_name="Screenshots\\QRM_products\\product_edit_failed"
            )

            self.logger.error(
                "Screenshot captured for failed product update"
            )

            self.logger.error(
                f"Product update FAILED | "
                f"Product: {data['edit_product_name']} | "
                f"Toast: {toast_msg}"
            )

            assert False, f"Product update failed | Toast: {toast_msg}"