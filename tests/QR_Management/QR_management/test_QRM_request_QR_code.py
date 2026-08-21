# import pytest
# import time
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from pages.QR_Management.QR_management_QR_m import QR_Management_QR_m_Page
# from pages.QR_Management.QR_management_category import QR_Management_Category_Page
# from utilities.customlogger import LogGen
# from pages.common.base_page import BaseTest
# from utilities.read_excel import get_test_data
# from utilities.screenshot_util import take_screenshot
# from selenium.common.exceptions import TimeoutException
#
#
# # Load Excel test data
# excel_path = r"mf_products_data.xlsx"
# test_data = get_test_data(excel_path, "Request_QR_code")  # Sheet name: Request_QR_code
#
# @pytest.mark.order(2)
# @pytest.mark.parametrize("data", test_data)
# class Test_QRM_request_QR_code(BaseTest):
#     logger = LogGen.loggen()
#
#     def test_QRM_request_QR_code(self, driver, data):
#
#         sku_id = data["sku_id"]
#         batch_no = data["batch_no"]
#         variant_sku = data["variant_sku"]
#         quantity = data["quantity"]
#         manufacturing_date = data["manufacturing_date"]
#         expiry_date = data["expiry_date"]
#         dimension = data["dimension"]
#         delivery_location = data["delivery_location"]
#         image_format=data["image_format"]
#         QR_Type = data["QR_Type"]
#
#         self.logger.info(f"===== Running QR Generation for SKU: {sku_id}, Batch: {batch_no} =====")
#
#         # Login only once
#         # if data == test_data[0]:
#         #     self.driver = driver
#         #     self.login_and_access()
#         #     self.logger.info("Logged in successfully for first iteration")
#         #
#         # else:
#         #     self.logger.info("Skipping login — already logged in")
#
#
#         # Check if login succeeded
#         # if "dashboard" not in driver.current_url.lower():  # or use some element only visible on dashboard
#         #     self.logger.error("Login failed! Check username/password")
#         #     driver.save_screenshot(".\\screenshots\\test_login_failed.png")
#         #     assert False, "Login failed Check username/password — cannot proceed to QR generation"
#
#         # Navigate to QR Management
#         qr_page = QR_Management_Category_Page(driver)
#         driver.refresh()
#         qr_page.Click_Dashboard()
#         qr_QR_page = QR_Management_QR_m_Page(driver)
#         qr_QR_page.Click_QR_management()
#         qr_QR_page.Click_Qr_management()
#         qr_QR_page.Click_request_QR_button()
#         time.sleep(2)
#
#         # Fill Product Details
#         qr_QR_page.click_product_skuID_opt()
#         qr_QR_page.Enter_product_sku_field(sku_id)
#         qr_QR_page.Enter_add_batch(batch_no)
#         time.sleep(1)
#         qr_QR_page.Click_product_name()
#         time.sleep(1)
#
#         # qr_QR_page.Click_variant_skuID_opt()
#         # time.sleep(1)
#         # qr_QR_page.Enter_varinat_sku_field(variant_sku)
#
#         # Popup check
#         if qr_QR_page.is_popup_message_present("Batch number already exists for a different product."):
#             take_screenshot(
#                 driver,
#                 test_name=f"Batch_Id_exists",
#                 folder_name="Screenshots\\QR_Management\\QR_Management\\Request_QR_code"
#             )
#
#             self.logger.error(f"Batch ID already exists!  Batch: {batch_no}")
#             assert False, f"Batch ID already exists  {batch_no}"
#             return
#
#
#         qr_QR_page.Enter_Quantity(quantity)
#         time.sleep(1)
#
#         try:
#             # Manufacturing & Expiry Date
#             qr_QR_page.Click_manufacturer_date()
#             time.sleep(1)
#             qr_QR_page.set_manufacturing_date(manufacturing_date)
#             time.sleep(1)
#             qr_QR_page.set_expiry_date(expiry_date)
#             time.sleep(1)
#
#             # Dimension + Delivery location
#             qr_QR_page.select_dimension(dimension)
#
#             qr_QR_page.click_batch_delivery_opt()
#             qr_QR_page.Enter_batch_delivery_field(delivery_location)
#
#             # qr_QR_page.select_QR_Type_drpdwn(QR_Type)
#             qr_QR_page.select_QR_Image_format(image_format)
#
#             # Generate QR
#             qr_QR_page.click_request_QR_code_button()
#
#             try:
#                 WebDriverWait(driver, 10).until(
#                     EC.text_to_be_present_in_element(
#                         (By.TAG_NAME, "body"),
#                         "Batch created successfully"
#                     )
#                 )
#                 self.logger.info(f"QR Generated Successfully for: SKU={sku_id}, Batch={batch_no}")
#             except:
#                 take_screenshot(
#                     driver,
#                     test_name=f"QR_request_failed",
#                     folder_name="Screenshots\\QR_Management\\QR_Management\\Request_QR_code"
#                 )
#                 self.logger.error(f"QR generation failed for SKU={sku_id}")
#                 assert False
#
#         except:
#             qr_QR_page.click_request_QR_code_button()
#             time.sleep(1)
#
#             try:
#                 self.logger.info("Waiting for toast message")
#
#                 toast_msg = WebDriverWait(driver, 10).until(
#                     EC.visibility_of_element_located((By.CSS_SELECTOR, ".toastify"))
#                 ).text.strip()
#
#                 # Remove unsupported Unicode symbols before logging
#                 toast_msg = toast_msg.encode("ascii", errors="ignore").decode()
#
#                 self.logger.info(
#                     f"Toast received: {toast_msg}"
#                 )
#
#             except TimeoutException:
#                 toast_msg = ""
#                 self.logger.error("Toast message not displayed")
#
#             if "QR Generation successfully initiated!" in toast_msg:
#                 self.logger.info("QR Generated Successfully initiated for  (Existing Batch Mode)")
#
#
#             else:
#                 take_screenshot(
#                     driver,
#                     test_name=f"QR_fail_for_existing_batch",
#                     folder_name="Screenshots\\QR_Management\\QR_Management\\Request_QR_code"
#                 )
#                 self.logger.error("QR generation failed for existing batch")
#                 assert False
#
#             return
#
#
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
from selenium.common.exceptions import TimeoutException


# Load Excel test data
excel_path = r"mf_products_data.xlsx"
test_data = get_test_data(
    excel_path,
    "Request_QR_code"
)  # Sheet name: Request_QR_code


@pytest.mark.order(2)
@pytest.mark.parametrize("data", test_data)
class Test_QRM_request_QR_code(BaseTest):
    logger = LogGen.loggen()

    def test_QRM_request_QR_code(self, driver, data):

        sku_id = data["sku_id"]
        batch_no = data["batch_no"]
        variant_sku = data["variant_sku"]
        quantity = data["quantity"]
        manufacturing_date = data["manufacturing_date"]
        expiry_date = data["expiry_date"]
        dimension = data["dimension"]
        delivery_location = data["delivery_location"]
        image_format = data["image_format"]
        QR_Type = data["QR_Type"]

        # TEST START
        self.logger.info(
            f"===== QR Management Request QR Code Flow Started | "
            f"SKU: {sku_id} | Batch: {batch_no} ====="
        )

        self.logger.info(
            f"QR Request Details | "
            f"SKU: {sku_id} | "
            f"Batch: {batch_no} | "
            f"Variant SKU: {variant_sku} | "
            f"Quantity: {quantity} | "
            f"Manufacturing Date: {manufacturing_date} | "
            f"Expiry Date: {expiry_date} | "
            f"Dimension: {dimension} | "
            f"Delivery Location: {delivery_location} | "
            f"Image Format: {image_format} | "
            f"QR Type: {QR_Type}"
        )

        # Login only once
        # if data == test_data[0]:
        #     self.driver = driver
        #     self.login_and_access()
        #     self.logger.info("Logged in successfully for first iteration")
        #
        # else:
        #     self.logger.info("Skipping login — already logged in")

        # Check if login succeeded
        # if "dashboard" not in driver.current_url.lower():
        #     self.logger.error("Login failed! Check username/password")
        #     driver.save_screenshot(".\\screenshots\\test_login_failed.png")
        #     assert False, "Login failed Check username/password — cannot proceed to QR generation"

        # NAVIGATION
        self.logger.info("Starting navigation to Request QR Code")

        qr_page = QR_Management_Category_Page(driver)

        driver.refresh()
        self.logger.info("Page refreshed successfully")

        qr_page.Click_Dashboard()
        self.logger.info("Clicked Dashboard")

        qr_QR_page = QR_Management_QR_m_Page(driver)

        qr_QR_page.Click_QR_management()
        self.logger.info("Opened QR Management module")

        qr_QR_page.Click_Qr_management()
        self.logger.info("Opened QR Management page")

        qr_QR_page.Click_request_QR_button()
        self.logger.info("Clicked Request QR Code button")

        time.sleep(2)

        # PRODUCT DETAILS
        self.logger.info("Starting Product Details entry")

        qr_QR_page.click_product_skuID_opt()
        self.logger.info("Opened Product SKU ID option")

        qr_QR_page.Enter_product_sku_field(sku_id)
        self.logger.info(
            f"Entered Product SKU ID: {sku_id}"
        )

        qr_QR_page.Enter_add_batch(batch_no)
        self.logger.info(
            f"Entered Batch ID: {batch_no}"
        )

        time.sleep(0.5)

        qr_QR_page.Click_product_name()
        self.logger.info("Selected Product Name")

        time.sleep(0.5)

        # qr_QR_page.Click_variant_skuID_opt()
        # time.sleep(1)
        # qr_QR_page.Enter_varinat_sku_field(variant_sku)

        # POPUP CHECK
        self.logger.info("Checking for existing Batch ID popup")

        if qr_QR_page.is_popup_message_present(
            "Batch number already exists for a different product."
        ):
            take_screenshot(
                driver,
                test_name=f"Batch_Id_exists",
                folder_name="Screenshots\\QR_Management\\QR_Management\\Request_QR_code"
            )

            self.logger.error(
                f"Batch ID already exists for a different product | "
                f"SKU: {sku_id} | Batch: {batch_no}"
            )

            assert False, f"Batch ID already exists  {batch_no}"
            return

        self.logger.info(
            f"Batch ID validation completed successfully | "
            f"SKU: {sku_id} | Batch: {batch_no}"
        )

        # QUANTITY
        qr_QR_page.Enter_Quantity(quantity)
        self.logger.info(
            f"Entered Quantity: {quantity}"
        )

        time.sleep(0.5)

        try:

            # MANUFACTURING & EXPIRY DATE
            self.logger.info(
                "Starting Manufacturing and Expiry Date entry"
            )

            qr_QR_page.Click_manufacturer_date()
            self.logger.info(
                "Opened Manufacturing Date calendar"
            )

            time.sleep(1)

            qr_QR_page.set_manufacturing_date(
                manufacturing_date
            )
            self.logger.info(
                f"Selected Manufacturing Date: "
                f"{manufacturing_date}"
            )

            time.sleep(1)

            qr_QR_page.set_expiry_date(
                expiry_date
            )
            self.logger.info(
                f"Selected Expiry Date: "
                f"{expiry_date}"
            )

            time.sleep(1)

            # DIMENSION
            self.logger.info(
                f"Selecting Dimension: {dimension}"
            )

            qr_QR_page.select_dimension(
                dimension
            )

            self.logger.info(
                f"Selected Dimension: {dimension}"
            )

            # DELIVERY LOCATION
            self.logger.info(
                "Starting Delivery Location entry"
            )

            qr_QR_page.click_batch_delivery_opt()
            self.logger.info(
                "Opened Batch Delivery Location option"
            )

            qr_QR_page.Enter_batch_delivery_field(
                delivery_location
            )

            self.logger.info(
                f"Entered Delivery Location: "
                f"{delivery_location}"
            )

            # QR TYPE
            # qr_QR_page.select_QR_Type_drpdwn(QR_Type)

            # IMAGE FORMAT
            self.logger.info(
                f"Selecting QR Image Format: "
                f"{image_format}"
            )

            qr_QR_page.select_QR_Image_format(
                image_format
            )

            self.logger.info(
                f"Selected QR Image Format: "
                f"{image_format}"
            )

            # GENERATE QR
            self.logger.info(
                f"Submitting Request QR Code | "
                f"SKU: {sku_id} | Batch: {batch_no}"
            )

            qr_QR_page.click_request_QR_code_button()

            self.logger.info(
                "Clicked Request QR Code button"
            )

            try:

                self.logger.info(
                    "Waiting for QR generation response toast"
                )

                toast_msg = WebDriverWait(
                    driver,
                    10
                ).until(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, ".toastify")
                    )
                ).text.strip()

                # Remove unsupported Unicode symbols before logging
                toast_msg = toast_msg.encode(
                    "ascii",
                    errors="ignore"
                ).decode()

                self.logger.info(
                    f"Toast received | "
                    f"SKU: {sku_id} | "
                    f"Batch: {batch_no} | "
                    f"Toast: {toast_msg}"
                )

                if "Batch created successfully" in toast_msg:

                    self.logger.info(
                        f"QR Generated Successfully | "
                        f"SKU: {sku_id} | "
                        f"Batch: {batch_no} | "
                        f"Quantity: {quantity} | "
                        f"Toast: {toast_msg}"
                    )

                else:

                    take_screenshot(
                        driver,
                        test_name=f"QR_request_failed",
                        folder_name="Screenshots\\QR_Management\\QR_Management\\Request_QR_code"
                    )

                    self.logger.error(
                        f"QR generation failed | "
                        f"SKU: {sku_id} | "
                        f"Batch: {batch_no} | "
                        f"Dimension: {dimension} | "
                        f"Image Format: {image_format} | "
                        f"Toast: {toast_msg}"
                    )

                    assert False, (
                        f"QR generation failed | "
                        f"Toast: {toast_msg}"
                    )

            except TimeoutException:

                take_screenshot(
                    driver,
                    test_name=f"QR_request_failed",
                    folder_name="Screenshots\\QR_Management\\QR_Management\\Request_QR_code"
                )

                self.logger.error(
                    f"QR generation response toast not displayed | "
                    f"SKU: {sku_id} | "
                    f"Batch: {batch_no}"
                )

                assert False, (
                    "QR generation response toast not displayed"
                )

        except:

            self.logger.warning(
                f"Exception occurred during new batch QR generation | "
                f"SKU: {sku_id} | Batch: {batch_no}"
            )

            self.logger.info(
                "Attempting Request QR Code again for existing batch mode"
            )

            qr_QR_page.click_request_QR_code_button()

            self.logger.info(
                "Clicked Request QR Code button for existing batch mode"
            )

            time.sleep(1)

            try:

                self.logger.info(
                    "Waiting for toast message"
                )

                toast_msg = WebDriverWait(
                    driver,
                    10
                ).until(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, ".toastify")
                    )
                ).text.strip()

                # Remove unsupported Unicode symbols before logging
                toast_msg = toast_msg.encode(
                    "ascii",
                    errors="ignore"
                ).decode()

                self.logger.info(
                    f"Toast received: {toast_msg}"
                )

            except TimeoutException:

                toast_msg = ""

                self.logger.error(
                    f"Toast message not displayed | "
                    f"SKU: {sku_id} | Batch: {batch_no}"
                )

            if "QR Generation successfully initiated!" in toast_msg:

                self.logger.info(
                    f"QR Generation successfully initiated | "
                    f"Existing Batch Mode | "
                    f"SKU: {sku_id} | "
                    f"Batch: {batch_no} | "
                    f"Quantity: {quantity} | "
                    f"Toast: {toast_msg}"
                )

            else:

                take_screenshot(
                    driver,
                    test_name=f"QR_fail_for_existing_batch",
                    folder_name="Screenshots\\QR_Management\\QR_Management\\Request_QR_code"
                )

                self.logger.error(
                    f"QR generation failed for existing batch | "
                    f"SKU: {sku_id} | "
                    f"Batch: {batch_no} | "
                    f"Toast: {toast_msg}"
                )

                assert False

            return