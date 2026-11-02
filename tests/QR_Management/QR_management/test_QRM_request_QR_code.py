

import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.QR_Management.QR_management_QR_m import QR_Management_QR_m_Page
from pages.QR_Management.QR_management_category import QR_Management_Category_Page
from pages.QR_Management.QR_management_products import QR_Management_products_Page

from utilities.customlogger import LogGen
from pages.common.base_page import BaseTest
from utilities.read_excel import get_test_data
from utilities.screenshot_util import take_screenshot
from selenium.common.exceptions import TimeoutException
import random
from datetime import datetime, timedelta


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

        # Fetch remaining fields from Excel
        variant_sku = data["variant_sku"]
        dimension = data["dimension"]
        delivery_location = data["delivery_location"]
        image_format = data["image_format"]

        # Generate dynamic test data
        batch_no = str(random.randint(1000, 9999))
        quantity = "1"
        today = datetime.today()

        manufacturing_date = today.strftime("%d-%m-%Y")
        expiry_date = (today + timedelta(days=1)).strftime("%d-%m-%Y")

        # NAVIGATION
        self.logger.info("Starting navigation to retrieve SKU from Products page")

        qr_page = QR_Management_Category_Page(driver)

        qr_page.Click_Dashboard()
        self.logger.info("Clicked Dashboard")

        driver.refresh()
        self.logger.info("Page refreshed successfully")

        qr_page.Click_QR_management()
        self.logger.info("Opened QR Management module")

        # Open Products page
        qr_products_page = QR_Management_products_Page(driver)
        qr_products_page.Click_products()
        self.logger.info("Opened Products page")

        # Get SKU ID from the first row, fourth column
        sku_locator = (By.XPATH, "//tbody/tr[1]/td[4]")

        sku_element = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located(sku_locator)
        )

        sku_id = sku_element.text.strip()

        if not sku_id:
            raise AssertionError("SKU ID is empty in the first row of Products table")

        self.logger.info(f"Retrieved first Product SKU ID: {sku_id}")

        qr_page = QR_Management_Category_Page(driver)

        qr_page.Click_Dashboard()
        self.logger.info("Clicked Dashboard")

        driver.refresh()
        self.logger.info("Page refreshed successfully")


        # Navigate to Request QR Code
        qr_QR_page = QR_Management_QR_m_Page(driver)

        qr_QR_page.Click_QR_management()
        self.logger.info("Opened QR Management menu")

        qr_QR_page.Click_Qr_management()
        self.logger.info("Opened QR Management page")

        qr_QR_page.Click_request_QR_button()
        self.logger.info("Clicked Request QR Code button")

        qr_QR_page.click_product_skuID_opt()
        self.logger.info("Opened Product SKU ID option")

        qr_QR_page.Enter_product_sku_field(sku_id)

        qr_QR_page.Enter_add_batch(batch_no)

        qr_QR_page.Click_product_name()
        self.logger.info("Selected Product Name")

        time.sleep(0.5)

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
        time.sleep(1)
        # QUANTITY
        qr_QR_page.Enter_Quantity(quantity)
        self.logger.info(
            f"Quantity to enter: {quantity}"
        )
        time.sleep(1)

        try:
            qr_QR_page.set_manufacturing_date(manufacturing_date)
            qr_QR_page.set_expiry_date(expiry_date)
            # DIMENSION
            qr_QR_page.select_dimension(
                dimension
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



            qr_QR_page.select_QR_Image_format(
                image_format
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