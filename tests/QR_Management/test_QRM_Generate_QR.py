#
# import pytest
# import time
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
#
# from pages.QR_Management.QR_management_QR_m import QR_Management_QR_m_Page
# from pages.QR_Management.QR_management_category import QR_Management_Category_Page
# from utilities.customlogger import LogGen
# from pages.common.base_page import BaseTest
# from utilities.read_excel import get_test_data
# from utilities.screenshot_util import take_screenshot
# # Load Excel test data
# excel_path = r"C:\Users\Suresh V\Desktop\automation\mf_products_data.xlsx"
# test_data = get_test_data(excel_path, "Generate_QR")  # Sheet name: Generate_QR
#
# @pytest.mark.order(5)
# @pytest.mark.parametrize("data", test_data)
# class Test_QRM_Generate_QR(BaseTest):
#     logger = LogGen.loggen()
#
#     def test_QR_management_generate(self, driver, data):
#
#         sku_id = data["sku_id"]
#         batch_no = data["batch_no"]
#         variant_sku = data["variant_sku"]
#         quantity = data["quantity"]
#         manufacturing_date = data["manufacturing_date"]
#         expiry_date = data["expiry_date"]
#         dimension = data["dimension"]
#         delivery_location = data["delivery_location"]
#         service=data["service"]
#
#         self.logger.info(f"===== Running QR Generation for SKU: {sku_id}, Batch: {batch_no} =====")
#
#         # Login only once
#         # if data == test_data[0]:
#         #     self.driver = driver
#         #     self.login_and_access()
#         #     self.logger.info("Logged in successfully for first iteration")
#         # else:
#         #     self.logger.info("Skipping login — already logged in")
#
#         # Navigate to QR Management
#         qr_page = QR_Management_Category_Page(driver)
#         qr_page.Click_Dashboard()
#         # qr_page.Click_QR_management()
#
#         qr_QR_page = QR_Management_QR_m_Page(driver)
#         qr_QR_page.Click_QR_management()
#         qr_QR_page.Click_Qr_management()
#         qr_QR_page.Click_generate_QR_button()
#         time.sleep(2)
#
#         # Fill Product Details
#         qr_QR_page.click_product_skuID_opt()
#         qr_QR_page.Enter_product_sku_field(sku_id)
#         qr_QR_page.Enter_add_batch(batch_no)
#         time.sleep(2)
#
#         qr_QR_page.Click_variant_skuID_opt()
#         time.sleep(2)
#
#         # Popup check
#         if qr_QR_page.is_popup_message_present("Batch number already exists for a different product."):
#             screenshot_path = f".\\Screenshots\\Generate_QR\\Batch_Id_exists_{batch_no}.png"
#             driver.save_screenshot(screenshot_path)
#
#             self.logger.error(f"Batch ID already exists! Skipping this row → Batch: {batch_no}")
#
#             # Mark this test case as failed but DO NOT stop the test run
#             assert False, f"Batch number already exists → {batch_no}"
#
#             return  # continue next data row
#
#         # Check if fields are disabled (= existing batch)
#         if not qr_QR_page.is_variant_field_editable():
#             self.logger.info(f"Existing Batch detected → Auto-fill mode for Batch: {batch_no}")
#             qr_QR_page.Enter_Quantity(quantity)
#             qr_QR_page.click_genarate_QR_button()
#
#             try:
#                 WebDriverWait(driver, 25).until(
#                     EC.text_to_be_present_in_element(
#                         (By.TAG_NAME, "body"),
#                         "QR Generation successfully initiated!"
#                     )
#                 )
#                 self.logger.info("QR Generated Successfully (Existing Batch Mode)")
#             except:
#                 driver.save_screenshot(f".\\Screenshots\\Generate_QR\\QR_fail_existing_batch_{batch_no}.png")
#                 self.logger.error("QR generation failed for existing batch")
#                 assert False
#
#             return  # Skip remaining steps for existing batch
#
#         # NEW Batch → All fields editable
#         qr_QR_page.Enter_varinat_sku_field(variant_sku)
#         time.sleep(1)
#         qr_QR_page.Enter_Quantity(quantity)
#         time.sleep(1)
#
#         # Manufacturing & Expiry Date
#         qr_QR_page.Click_manufacturer_date()
#         time.sleep(1)
#         qr_QR_page.set_manufacturing_date(manufacturing_date)
#         qr_QR_page.set_expiry_date(expiry_date)
#         time.sleep(1)
#
#         # Dimension + Delivery location
#         qr_QR_page.select_dimension(dimension)
#         time.sleep(1)
#         qr_QR_page.click_batch_delivery_opt()
#         qr_QR_page.Enter_batch_delivery_field(delivery_location)
#         time.sleep(1)
#         qr_QR_page.select_service_drpdwn(service)
#
#         # Generate QR
#         qr_QR_page.click_genarate_QR_button()
#
#         try:
#             WebDriverWait(driver, 25).until(
#                 EC.text_to_be_present_in_element(
#                     (By.TAG_NAME, "body"),
#                     "QR Generation successfully initiated!"
#                 )
#             )
#             self.logger.info(f"QR Generated Successfully for: SKU={sku_id}, Batch={batch_no}")
#         except:
#             driver.save_screenshot(f".\\Screenshots\\Generate_QR\\QR_fail_sku_{sku_id}.png")
#             self.logger.error(f"QR generation failed for SKU={sku_id}")
#             assert False
#
#         time.sleep(5)
#

import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.QR_Management.QR_management_QR_m import QR_Management_QR_m_Page
from pages.QR_Management.QR_management_category import QR_Management_Category_Page
from utilities.customlogger import LogGen
from pages.common.base_page import BaseTest
from utilities.read_excel import get_test_data
from utilities.screenshot_util import take_screenshot

# Load Excel test data
excel_path = r"C:\Users\Suresh V\Desktop\automation\mf_products_data.xlsx"
test_data = get_test_data(excel_path, "Generate_QR")  # Sheet name: Generate_QR

@pytest.mark.order(5)
@pytest.mark.parametrize("data", test_data)
class Test_QRM_Generate_QR(BaseTest):
    logger = LogGen.loggen()

    def test_QR_management_generate(self, driver, data):

        sku_id = data["sku_id"]
        batch_no = data["batch_no"]
        variant_sku = data["variant_sku"]
        quantity = data["quantity"]
        manufacturing_date = data["manufacturing_date"]
        expiry_date = data["expiry_date"]
        dimension = data["dimension"]
        delivery_location = data["delivery_location"]
        service = data["service"]

        self.logger.info(f"===== Running QR Generation for SKU: {sku_id}, Batch: {batch_no} =====")

        # # Login only once
        # if data == test_data[0]:
        #     self.driver = driver
        #     self.login_and_access()
        #     self.logger.info("Logged in successfully for first iteration")
        # else:
        #     self.logger.info("Skipping login — already logged in")

        # Navigate to QR Management
        qr_page = QR_Management_Category_Page(driver)
        qr_page.Click_Dashboard()

        qr_QR_page = QR_Management_QR_m_Page(driver)
        qr_QR_page.Click_QR_management()
        qr_QR_page.Click_Qr_management()
        qr_QR_page.Click_generate_QR_button()
        time.sleep(2)

        # Fill Product Details
        qr_QR_page.click_product_skuID_opt()
        qr_QR_page.Enter_product_sku_field(sku_id)
        qr_QR_page.Enter_add_batch(batch_no)
        time.sleep(2)

        qr_QR_page.Click_variant_skuID_opt()
        time.sleep(2)

        # Popup check
        if qr_QR_page.is_popup_message_present("Batch number already exists for a different product."):
            take_screenshot(
                driver,
                test_name=f"Batch_Id_exists",
                folder_name="Screenshots\\Generate_QR"
            )

            self.logger.error(f"Batch ID already exists! Skipping this row → Batch: {batch_no}")
            assert False, f"Batch number already exists → {batch_no}"
            return

        # Check if fields are disabled (= existing batch)
        if not qr_QR_page.is_variant_field_editable():
            self.logger.info(f"Existing Batch detected → Auto-fill mode for Batch: {batch_no}")
            qr_QR_page.Enter_Quantity(quantity)
            qr_QR_page.click_genarate_QR_button()

            try:
                WebDriverWait(driver, 25).until(
                    EC.text_to_be_present_in_element(
                        (By.TAG_NAME, "body"),
                        "QR Generation successfully initiated!"
                    )
                )
                self.logger.info("QR Generated Successfully (Existing Batch Mode)")
            except:
                take_screenshot(
                    driver,
                    test_name=f"QR_fail_existing_batch",
                    folder_name="Screenshots\\Generate_QR"
                )
                self.logger.error("QR generation failed for existing batch")
                assert False

            return

        # NEW Batch → All fields editable
        qr_QR_page.Enter_varinat_sku_field(variant_sku)
        time.sleep(1)
        qr_QR_page.Enter_Quantity(quantity)
        time.sleep(1)

        # Manufacturing & Expiry Date
        qr_QR_page.Click_manufacturer_date()
        time.sleep(1)
        qr_QR_page.set_manufacturing_date(manufacturing_date)
        qr_QR_page.set_expiry_date(expiry_date)
        time.sleep(1)

        # Dimension + Delivery location
        qr_QR_page.select_dimension(dimension)
        time.sleep(1)
        qr_QR_page.click_batch_delivery_opt()
        qr_QR_page.Enter_batch_delivery_field(delivery_location)
        time.sleep(1)
        qr_QR_page.select_service_drpdwn(service)

        # Generate QR
        qr_QR_page.click_genarate_QR_button()

        try:
            WebDriverWait(driver, 25).until(
                EC.text_to_be_present_in_element(
                    (By.TAG_NAME, "body"),
                    "QR Generation successfully initiated!"
                )
            )
            self.logger.info(f"QR Generated Successfully for: SKU={sku_id}, Batch={batch_no}")
        except:
            take_screenshot(
                driver,
                test_name=f"QR_fail_sku",
                folder_name="Screenshots\\Generate_QR"
            )
            self.logger.error(f"QR generation failed for SKU={sku_id}")
            assert False

        time.sleep(5)

