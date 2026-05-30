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
#
# # Excel path
# excel_path = os.path.join(os.getcwd(),r"C:\Users\Suresh V\Desktop\automation\mf_products_data.xlsx")
# test_data=get_test_data(excel_path,"products")
#
# @pytest.mark.order(4)
# @pytest.mark.parametrize("data", test_data)
# class Test_QRM_products(BaseTest):
#     logger = LogGen.loggen()
#
#     def test_QR_management_products_flow(self, driver,data):
#         self.logger.info(f"===== QR Management products Test Started for {data['product_name']} =====")
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
#         qr_page.Click_QR_management()
#
#         qr_products_page = QR_Management_products_Page(driver)
#         qr_products_page.Click_products()
#         qr_products_page.Click_create_product_button()
#         qr_products_page.Enter_product_name_or_Id(data["product_name"])
#         qr_products_page.Enter_brand_name(data["brand_name"])
#         time.sleep(3)
#
#         try:
#             qr_products_page.Upload_Product_images(data["upload_product_image"])
#         except Exception as e:
#             self.logger.warning(f"Unable to upload images for {data['product_name']}: {e}")
#             return  # Skip this product and continue
#
#         qr_products_page.Enter_Product_URL(data["product_url"])
#         qr_products_page.Enter_SKU_ID(data["SKU_ID"])
#         time.sleep(2)
#         qr_products_page.select_category_opt()
#         time.sleep(1)
#         qr_products_page.Enter_category_name(data["select_category"])
#         time.sleep(1)
#         qr_products_page.select_status_drp(data["status"])
#         time.sleep(1)
#         qr_products_page.Enter_description(data["description"])
#         time.sleep(2)
#         qr_products_page.Country_option()
#         time.sleep(1)
#         qr_products_page.Country_of_origin(data["country"])
#         qr_products_page.Click_Proceed_to_child_SKU_button()
#         time.sleep(1)
#
#         qr_products_page.ClicK_continue_video_btn()
#         time.sleep(1)
#         qr_products_page.Click_create_product_submit_btn()
#
#         try:
#             WebDriverWait(driver, 15).until(
#                 EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Product created successfully!")
#             )
#             self.logger.info(f"Product '{data['product_name']}' created successfully!")
#         except:
#
#             take_screenshot(
#                 driver,
#                 test_name="test_create_product.png",
#                 folder_name="Screenshots\\QRM_products"
#             )
#             self.logger.error(f"Create product failed for '{data['product_name']}'")
#             assert False,"please check all the fields entered correctly"
#             return
#
#
#
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
class Test_QRM_products(BaseTest):
    logger = LogGen.loggen()

    current_sku = "PRD2025X0012"

    def test_QR_management_products_flow(self, driver, data):

        self.logger.info(
            f"===== QR Management Products Flow Started for {data['product_name']} ====="
        )

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
        qr_products_page.Click_create_product_button()

        self.logger.info(f"Creating product: {data['product_name']}")
        qr_products_page.Enter_product_name_or_Id(data["product_name"])
        qr_products_page.Enter_brand_name(data["brand_name"])

        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # IMAGE UPLOAD
        try:
            qr_products_page.Upload_Product_images(data["upload_product_image"])
            self.logger.info("Product image uploaded successfully")

        except Exception as e:
            self.logger.error(
                f"Image upload failed for {data['product_name']} | Error: {e}"
            )
            return

        qr_products_page.Enter_Product_URL(data["product_url"])

        # SKU
        new_sku = generate_next_sku(self.current_sku)
        self.__class__.current_sku = new_sku

        self.logger.info(f"Generated SKU: {new_sku}")
        qr_products_page.Enter_SKU_ID(new_sku)

        # PRODUCT DETAILS
        qr_products_page.select_category_opt()
        qr_products_page.Enter_category_name(data["select_category"])
        qr_products_page.select_status_drp(data["status"])
        qr_products_page.Enter_description(data["description"])
        qr_products_page.Country_option()
        qr_products_page.Country_of_origin(data["country"])
        self.logger.info("Filled all product details")
        qr_products_page.Click_Proceed_to_child_SKU_button()
        qr_products_page.ClicK_continue_video_btn()

        qr_products_page.Enter_video_title(data["video_title"])
        qr_products_page.Choose_video_file(data["video_file"])

        qr_products_page.Click_create_product_submit_btn()

        # TOAST
        try:
            toast_msg = WebDriverWait(driver, 8).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".toastify"))
            ).text.strip()

            self.logger.info(f"Toast message: {toast_msg}")

        except TimeoutException:
            toast_msg = ""
            self.logger.error("Toast message not displayed")

        # VALIDATION
        if "Product created successfully!" in toast_msg:

            self.logger.info(
                f"Product created successfully | "
                f"Product: {data['product_name']} | SKU: {new_sku}"
            )
            assert True

        else:
            take_screenshot(
                driver,
                test_name="test_create_product",
                folder_name="Screenshots\\QRM_products"
            )

            self.logger.error(
                f"Product creation failed | "
                f"Product: {data['product_name']} | "
                f"Toast: {toast_msg}"
            )

            assert False, f"Product creation failed | Toast: {toast_msg}"
