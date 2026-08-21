
# import pytest
# import time
# import os
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from pages.QR_Management.QR_management_category import QR_Management_Category_Page
# from pages.QR_Management.QR_management_products import QR_Management_products_Page
# from utilities.customlogger import LogGen
# from pages.common.base_page import BaseTest
# from utilities.read_excel import get_test_data
# from utilities.screenshot_util import take_screenshot
# from utilities.sku_utils import generate_next_sku
# from selenium.common.exceptions import TimeoutException
#
#
# # Excel path
# excel_path = os.path.join(os.getcwd(), r"C:\Users\Suresh V\Desktop\automation\mf_products_data.xlsx")
# test_data = get_test_data(excel_path, "products")
#
# @pytest.mark.order(4)
# @pytest.mark.parametrize("data", test_data)
# class Test_QRM_products(BaseTest):
#     logger = LogGen.loggen()
#
#     def test_QR_management_products_flow(self, driver, data):
#         self.logger.info(f"===== QR Management products Test Started for {data['product_name']} =====")
#
#         wait = WebDriverWait(driver,4)
#
#         # Login only once
#         if data == test_data[0]:
#             self.driver = driver
#             self.login_and_access()
#             self.logger.info("Logged in successfully for first iteration")
#         else:
#             self.logger.info("Skipping login ")
#
#         qr_page = QR_Management_Category_Page(driver)
#         qr_page.Click_Dashboard()
#         driver.refresh()
#         qr_page.Click_QR_management()
#
#         qr_products_page = QR_Management_products_Page(driver)
#         qr_products_page.Click_products()
#         qr_products_page.Click_create_product_button()
#         qr_products_page.Enter_product_name_or_Id(data["product_name"])
#         qr_products_page.Enter_brand_name(data["brand_name"])
#
#         wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
#
#         try:
#             qr_products_page.Upload_Product_images(data["upload_product_image"])
#         except Exception as e:
#             self.logger.warning(f"Unable to upload images for {data['product_name']}: {e}")
#             return
#
#         qr_products_page.Enter_Product_URL(data["product_url"])
#
#
#         old_sku = data["SKU_ID"]
#         new_sku = generate_next_sku(old_sku)
#
#         qr_products_page.Enter_SKU_ID(new_sku)
#
#
#         # qr_products_page.Enter_SKU_ID(data["SKU_ID"])
#
#         qr_products_page.select_category_opt()
#
#         qr_products_page.Enter_category_name(data["select_category"])
#
#         qr_products_page.select_status_drp(data["status"])
#
#         qr_products_page.Enter_description(data["description"])
#
#         qr_products_page.Country_option()
#
#         qr_products_page.Country_of_origin(data["country"])
#         qr_products_page.Click_Proceed_to_child_SKU_button()
#
#         qr_products_page.ClicK_continue_video_btn()
#
#         qr_products_page.Enter_video_title(data["video_title"])
#         # time.sleep(2)
#
#         qr_products_page.Choose_video_file(data["video_file"])
#
#         qr_products_page.Click_create_product_submit_btn()
#
#
#         try:
#             toast_msg = WebDriverWait(driver, 5).until(
#                 EC.visibility_of_element_located(
#                     (By.CSS_SELECTOR, ".toastify")
#                 )
#             ).text
#             print("toast :", toast_msg)
#
#         except TimeoutException:
#             toast_msg = "Toast message not displayed"
#
#         # VALIDATION
#         if "Product created successfully!" in toast_msg:
#             print("Product created successfully")
#
#             self.logger.info(
#                 f"Product created successfully '{data['product_name']}' | {toast_msg}"
#             )
#
#         else:
#
#             take_screenshot(
#                 driver,
#                 test_name="test_create_product",
#                 folder_name="Screenshots\\QRM_products"
#             )
#
#             self.logger.error(
#                 f"Create product failed for '{data['product_name']}' | Toast: {toast_msg}"
#             )
#
#             assert False, f"Product creation failed | Toast: {toast_msg}"



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


@pytest.mark.order(1)
@pytest.mark.parametrize("data", test_data)
class Test_product_create(BaseTest):
    logger = LogGen.loggen()

    current_sku = "PRD2025X0015"

    def test_QR_management_products_flow(self, driver, data):

        self.logger.info(
            f"===== QR Management Product Creation Flow Started | Product: {data['product_name']} ====="
        )

        self.logger.info(
            f"Product Details | "
            f"Product: {data['product_name']} | "
            f"Brand: {data['brand_name']} | "
            f"Category: {data['select_category']} | "
            f"Status: {data['status']} | "
            f"Country: {data['country']}"
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

        qr_products_page.Click_create_product_button()
        self.logger.info("Clicked Create Product button")

        self.logger.info(
            f"Entering Product Details | Product Name: {data['product_name']}"
        )

        qr_products_page.Enter_product_name_or_Id(data["product_name"])
        self.logger.info(
            f"Entered Product Name: {data['product_name']}"
        )

        qr_products_page.Enter_brand_name(data["brand_name"])
        self.logger.info(
            f"Entered Brand Name: {data['brand_name']}"
        )

        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # IMAGE UPLOAD
        try:
            qr_products_page.Upload_Product_images(
                data["upload_product_image"]
            )

            self.logger.info(
                f"Product image uploaded successfully | "
                f"File: {data['upload_product_image']}"
            )

        except Exception as e:
            self.logger.error(
                f"Image upload failed for "
                f"{data['product_name']} | Error: {e}"
            )
            return

        qr_products_page.Enter_Product_URL(data["product_url"])
        self.logger.info(
            f"Entered Product URL: {data['product_url']}"
        )

        # SKU
        # new_sku = generate_next_sku(self.current_sku)
        # self.__class__.current_sku = new_sku
        #
        # self.logger.info(f"Generated SKU: {new_sku}")

        qr_products_page.Enter_SKU_ID(data["SKU_ID"])
        self.logger.info(f"Entered SKU ID: {data['SKU_ID']}")

        # PRODUCT DETAILS
        qr_products_page.select_category_opt()
        self.logger.info("Opened Category dropdown")

        qr_products_page.Enter_category_name(data["select_category"])
        self.logger.info(
            f"Selected Category: {data['select_category']}"
        )

        qr_products_page.select_status_drp(data["status"])
        self.logger.info(
            f"Selected Status: {data['status']}"
        )

        qr_products_page.Enter_description(data["description"])
        self.logger.info("Entered Product Description")

        qr_products_page.Country_option()
        self.logger.info("Opened Country dropdown")

        qr_products_page.Country_of_origin(data["country"])
        self.logger.info(
            f"Selected Country of Origin: {data['country']}"
        )

        self.logger.info("Filled all product details successfully")

        qr_products_page.Click_Proceed_to_child_SKU_button()
        self.logger.info("Clicked Proceed to Child SKU button")

        qr_products_page.ClicK_continue_video_btn()
        self.logger.info("Clicked Continue To Video button")

        qr_products_page.Enter_video_title(data["video_title"])
        self.logger.info(
            f"Entered Video Title: {data['video_title']}"
        )

        qr_products_page.Choose_video_file(data["video_file"])
        self.logger.info(
            f"Uploaded Video File: {data['video_file']}"
        )

        qr_products_page.Click_create_product_submit_btn()
        self.logger.info("Clicked Submit button")

        # TOAST
        try:
            self.logger.info("Waiting for toast message")

            toast_msg = WebDriverWait(driver,10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".toastify"))
            ).text.strip()

            # Remove unsupported Unicode symbols before logging
            toast_msg = toast_msg.encode("ascii", errors="ignore").decode()

            self.logger.info(
                f"Toast received: {toast_msg}"
            )

        except TimeoutException:
            toast_msg = ""
            self.logger.error("Toast message not displayed")

        # VALIDATION
        if "Product created successfully!" in toast_msg:

            self.logger.info(
                f"Product created successfully | "
                f"Product: {data['product_name']} | "
                f"SKU: {data['SKU_ID']} | "
                f"Toast: {toast_msg}"
            )

            assert True

        else:
            take_screenshot(
                driver,
                test_name="test_create_product",
                folder_name="Screenshots\\QR_Management\\QRM_products\\product_create"
            )

            self.logger.error(
                f"Product creation failed | "
                f"Product: {data['product_name']} | "
                f"SKU: {data['SKU_ID']} | "
                f"Toast: {toast_msg}"
            )

            assert False, f"Product creation failed | Toast: {toast_msg}"
